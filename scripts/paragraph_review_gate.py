#!/usr/bin/env python3
"""Bounded paragraph review state machine for storytelling-historical-travel.

Every paragraph begins with all review flags false. A flag can become true only
after its own gate has actually run and passed:
- deterministic checklist;
- independent Sarah-style review bound to paragraph + frozen voice contract;
- HIL scope review limited to dimensions supported by claims used in the paragraph.
"""
from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass, field
import json
from pathlib import Path
import re
import unicodedata
from typing import Any

from sarah_voice_contract import validate_style_review


@dataclass(frozen=True)
class Violation:
    category: str
    rule: str
    message: str


@dataclass
class ReviewState:
    checklist_reviewed: bool = False
    sarah_style_reviewed: bool = False
    hil_scope_reviewed: bool = False

    @property
    def complete(self) -> bool:
        return self.checklist_reviewed and self.sarah_style_reviewed and self.hil_scope_reviewed


@dataclass
class ReviewResult:
    passed: bool
    review_state: ReviewState = field(default_factory=ReviewState)
    violations: list[Violation] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)


METHOD_LEAKAGE = (
    (r"\bTL;DR\b", "tldr_reader_leak"),
    (r"\bstatut canonique\b", "statut_canonique_reader_leak"),
    (r"\bce qu['’]on ne doit pas en déduire\b", "method_heading_reader_leak"),
    (r"\bpourquoi l['’]insérer directement dans notre arc\b", "method_heading_reader_leak"),
    (r"\bHIL[- _]?\d*\b", "hil_reader_leak"),
    (r"\brun\s*\d+\b", "run_reader_leak"),
    (r"\bversion\s+[vV]?\d+\b", "version_reader_leak"),
    (r"\bpolitique éditoriale de la\s+[vV]\d+\b", "production_policy_reader_leak"),
    (r"\bcomplément\s+[vV]\d+\b", "production_version_reader_leak"),
    (r"\breport\.md\b", "production_artifact_reader_leak"),
    (r"\bbaseline\b", "production_artifact_reader_leak"),
    (r"\blineage\b", "production_artifact_reader_leak"),
)

FOREIGN_TERMS = {
    "clearing house": ("chambre de compensation", "centre de compensation", "plateforme de compensation"),
    "trade-off": ("arbitrage", "compromis"),
    "path dependency": ("dépendance au sentier", "dépendance de trajectoire"),
}

STOPWORDS = {
    "avec", "dans", "pour", "mais", "donc", "ainsi", "apres", "avant", "cette", "cela",
    "comme", "plus", "moins", "entre", "sous", "vers", "leur", "leurs", "dont", "avait",
    "avoir", "etre", "fait", "faire", "site", "roi", "royal", "reine", "puis", "parce",
    "tradition", "texte", "claim", "source", "point", "durant", "depuis", "elle",
}

CLAIM_MARKER = re.compile(r"\[claim:([^\]]+)\]", re.I)


def initialize_review_state() -> ReviewState:
    """Explicitly return the only legal initial state for a paragraph review."""
    return ReviewState(False, False, False)


def _norm(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", value.lower()).strip()


def _tokens(value: str) -> set[str]:
    return {
        token for token in re.findall(r"[a-z0-9]+", _norm(value))
        if len(token) >= 4 and token not in STOPWORDS
    }


def _canonical_points(claim: dict[str, Any]) -> list[str]:
    explicit = claim.get("canonical_points") or claim.get("canonical_summary_points")
    if not isinstance(explicit, list):
        return []
    out: list[str] = []
    for item in explicit:
        if isinstance(item, str) and item.strip():
            out.append(item.strip())
        elif isinstance(item, dict):
            text = item.get("text") or item.get("summary")
            if text:
                out.append(str(text).strip())
    return out


def _point_is_covered(point: str, paragraph: str) -> bool:
    required = _tokens(point)
    if not required:
        return _norm(point) in _norm(paragraph)
    observed = _tokens(paragraph)
    threshold = 1 if len(required) == 1 else min(2, len(required))
    return len(required & observed) >= threshold


def _has_foreign_gloss(text: str, term: str, glosses: tuple[str, ...]) -> bool:
    lowered = _norm(text)
    if _norm(term) not in lowered:
        return True
    if any(_norm(gloss) in lowered for gloss in glosses):
        return True
    return bool(re.search(re.escape(term) + r"\s*\([^)]{4,100}\)", text, flags=re.I))


def _unexplained_acronyms(text: str, arc_context: dict[str, Any]) -> list[str]:
    explained = {str(x).upper() for x in arc_context.get("explained_acronyms", [])}
    hidden = re.sub(r"\[(?:claim|ILLUSTRATION|SIDE-STORY|ARC-RECAP):[^\]]+\]", "", text, flags=re.I)
    candidates = sorted(set(re.findall(r"\b[A-ZÀ-ÖØ-Þ]{2,6}\b", hidden)))
    out: list[str] = []
    for acronym in candidates:
        if acronym in explained:
            continue
        if re.search(rf"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ '\-]{{5,80}}\({re.escape(acronym)}\)", hidden):
            continue
        out.append(acronym)
    return out


def _deterministic_checklist(text: str, claim: dict[str, Any], arc_context: dict[str, Any]) -> tuple[list[Violation], list[str]]:
    violations: list[Violation] = []
    warnings: list[str] = []

    for pattern, rule in METHOD_LEAKAGE:
        if re.search(pattern, text, flags=re.I):
            violations.append(Violation("Don't", rule, "Backstage methodological language leaked into reader-facing prose."))
            break

    for term, glosses in FOREIGN_TERMS.items():
        if not _has_foreign_gloss(text, term, glosses):
            violations.append(Violation("forme", "terme_technique_non_glose", f"Foreign technical term '{term}' is not glossed or francised."))
            break

    acronyms = _unexplained_acronyms(text, arc_context)
    if acronyms:
        violations.append(Violation("forme", "sigle_non_explicite", "Unexplained acronym(s): " + ", ".join(acronyms)))

    points = _canonical_points(claim)
    if points:
        missing = [point for point in points if not _point_is_covered(point, text)]
        if missing:
            violations.append(Violation("fond", "couverture_canonique_incomplete", f"Missing {len(missing)}/{len(points)} canonical point(s)."))
    else:
        warnings.append("canonical_points_missing: targeted semantic review required; deterministic gate does not invent canonical points")

    normalized = _norm(text)
    if re.search(r"(?:consequence|par consequent|donc|ainsi|renforc\w*)[^.;]{0,220}(?:apres que|apres avoir)", normalized):
        violations.append(Violation("fond", "ordre_fait_avant_consequence", "Consequence/perspective precedes the source-attested action."))

    claim_id = str(claim.get("id") or "")
    marker = f"[claim:{claim_id}]" if claim_id else ""
    mention_count = (arc_context.get("mention_count") or {}).get(claim_id, 0)
    active_callbacks = set(arc_context.get("active_callbacks") or [])
    if marker and marker in text and mention_count >= 2 and claim_id in active_callbacks:
        violations.append(Violation("fond", "citation_evidentielle_au_dela_du_callback_disponible", "A third direct evidentiary citation is used while an active callback is available."))
    elif marker and marker in text and mention_count >= 2:
        warnings.append("over_mentioned_claim: more than two direct citations; review whether a callback should replace this citation")

    if arc_context.get("false_lead"):
        if int(arc_context.get("false_lead_count_in_subsection", 0)) >= 2:
            violations.append(Violation("forme", "false_lead_rerank_limit", "Subsection already contains the maximum two false leads."))
        if "?" not in text:
            violations.append(Violation("forme", "false_lead_socratic_format", "False lead must contain a naïve or semi-rhetorical question."))

    if not arc_context.get("neighbor_context_loaded", False):
        warnings.append("tone_context_missing: previous/next paragraph not loaded for bounded continuity review")

    return violations, warnings


def _review_sarah_style(text: str, arc_context: dict[str, Any]) -> tuple[bool, list[Violation], list[str]]:
    record = arc_context.get("sarah_style_review")
    if not record:
        return False, [Violation(
            "style",
            "sarah_style_review_required",
            "Sarah-style review starts false and requires an independent review record bound to the paragraph and frozen voice contract.",
        )], []
    errors, warnings = validate_style_review(text, record)
    if errors:
        return False, [Violation("style", "sarah_style_review_invalid", message) for message in errors], warnings
    return True, [], warnings


def _claim_hils_from_context(claim: dict[str, Any], text: str, arc_context: dict[str, Any]) -> tuple[set[str], set[str]]:
    used_claim_ids = {match.group(1) for match in CLAIM_MARKER.finditer(text)}
    current_id = str(claim.get("id") or "")
    if not used_claim_ids and current_id:
        used_claim_ids.add(current_id)

    mapping = arc_context.get("claim_hil_map") or {}
    relevant: set[str] = set()
    for cid in used_claim_ids:
        value = mapping.get(cid) or []
        if isinstance(value, str):
            relevant.add(value)
        else:
            relevant |= {str(x) for x in value if x}

    if current_id in used_claim_ids:
        direct = claim.get("hil")
        if isinstance(direct, str) and direct:
            relevant.add(direct)
        relevant |= {str(x) for x in claim.get("hil_ids") or [] if x}

    return used_claim_ids, relevant


def _review_hil_scope(claim: dict[str, Any], text: str, arc_context: dict[str, Any]) -> tuple[bool, list[Violation], list[str]]:
    if arc_context.get("hil_scope_declared") is not True:
        return False, [Violation("HIL", "hil_scope_review_required", "HIL review starts false; the paragraph must explicitly declare the dimensions considered.")], []

    _, relevant = _claim_hils_from_context(claim, text, arc_context)
    selected = {str(x) for x in arc_context.get("selected_hil_ids") or [] if x}
    extraneous = selected - relevant
    if extraneous:
        return False, [Violation("HIL", "hil_dimension_not_relevant_to_paragraph", f"HIL dimension(s) selected without a supporting claim in this paragraph: {sorted(extraneous)}")], []

    warnings: list[str] = []
    omitted = relevant - selected
    if omitted:
        warnings.append(f"hil_relevant_but_not_selected: {sorted(omitted)}; allowed because HIL is relevance-driven, not a coverage quota")
    return True, [], warnings


def review_paragraph(text: str, claim: dict[str, Any], arc_context: dict[str, Any] | None = None) -> ReviewResult:
    """Review one paragraph. No review flag is ever true by default."""
    arc_context = arc_context or {}
    state = initialize_review_state()

    violations, warnings = _deterministic_checklist(text, claim, arc_context)
    if not violations:
        state.checklist_reviewed = True

    sarah_ok, sarah_violations, sarah_warnings = _review_sarah_style(text, arc_context)
    violations.extend(sarah_violations)
    warnings.extend(sarah_warnings)
    if sarah_ok:
        state.sarah_style_reviewed = True

    hil_ok, hil_violations, hil_warnings = _review_hil_scope(claim, text, arc_context)
    violations.extend(hil_violations)
    warnings.extend(hil_warnings)
    if hil_ok:
        state.hil_scope_reviewed = True

    passed = state.complete and not violations
    return ReviewResult(passed=passed, review_state=state, violations=violations, warnings=warnings)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--paragraph", required=True)
    parser.add_argument("--claim-json", required=True)
    parser.add_argument("--arc-context-json", required=True)
    args = parser.parse_args()

    text = Path(args.paragraph).read_text(encoding="utf-8")
    claim = json.loads(Path(args.claim_json).read_text(encoding="utf-8"))
    context = json.loads(Path(args.arc_context_json).read_text(encoding="utf-8"))
    result = review_paragraph(text, claim, context)
    print(json.dumps({
        "passed": result.passed,
        "review_state": asdict(result.review_state),
        "violations": [asdict(x) for x in result.violations],
        "warnings": result.warnings,
    }, ensure_ascii=False, indent=2))
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
