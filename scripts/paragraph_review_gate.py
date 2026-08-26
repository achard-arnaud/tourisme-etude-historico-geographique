#!/usr/bin/env python3
"""Deterministic L1 paragraph gate for storytelling-historical-travel.

The gate intentionally handles only rules that can be checked without semantic
hallucination. Tone, deep factual completeness for legacy claims and nuanced
texture remain targeted-review warnings rather than fake deterministic passes.
"""
from __future__ import annotations

from dataclasses import dataclass, field
import re
import unicodedata
from typing import Any


@dataclass(frozen=True)
class Violation:
    category: str
    rule: str
    message: str


@dataclass
class ReviewResult:
    passed: bool
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
    "tradition", "texte", "claim", "source", "point", "durant", "depuis", "elle", "il",
}


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
    if isinstance(explicit, list):
        points = []
        for item in explicit:
            if isinstance(item, str) and item.strip():
                points.append(item.strip())
            elif isinstance(item, dict):
                text = item.get("text") or item.get("summary")
                if text:
                    points.append(str(text).strip())
        return points
    return []


def _point_is_covered(point: str, paragraph: str) -> bool:
    required = _tokens(point)
    if not required:
        return _norm(point) in _norm(paragraph)
    observed = _tokens(paragraph)
    threshold = 1 if len(required) == 1 else min(2, len(required))
    return len(required & observed) >= threshold


def _has_foreign_gloss(text: str, term: str, french_glosses: tuple[str, ...]) -> bool:
    lowered = _norm(text)
    if _norm(term) not in lowered:
        return True
    if any(_norm(gloss) in lowered for gloss in french_glosses):
        return True
    # A directly attached explanatory parenthesis is also acceptable.
    return bool(re.search(re.escape(term) + r"\s*\([^)]{4,100}\)", text, flags=re.I))


def _unexplained_acronyms(text: str, arc_context: dict[str, Any]) -> list[str]:
    explained = {str(x).upper() for x in arc_context.get("explained_acronyms", [])}
    hidden = re.sub(r"\[(?:claim|ILLUSTRATION|SIDE-STORY|ARC-RECAP):[^\]]+\]", "", text, flags=re.I)
    candidates = sorted(set(re.findall(r"\b[A-ZÀ-ÖØ-Þ]{2,6}\b", hidden)))
    out = []
    for acronym in candidates:
        if acronym in explained:
            continue
        # Accept an inline expansion of the form "long expression (ABC)".
        if re.search(rf"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ '\-]{{5,80}}\({re.escape(acronym)}\)", hidden):
            continue
        out.append(acronym)
    return out


def review_paragraph(text: str, claim: dict[str, Any], arc_context: dict[str, Any] | None = None) -> ReviewResult:
    """Review one paragraph without loading the manuscript.

    `arc_context` may provide:
      - mention_count: {claim_id: int}
      - active_callbacks: [claim_id, ...]
      - explained_acronyms: ["VOC", ...]
      - false_lead: bool
      - false_lead_count_in_subsection: int
    """
    arc_context = arc_context or {}
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
        warnings.append("canonical_points_missing: legacy claim requires targeted semantic review; deterministic gate does not invent canonical points")

    normalized = _norm(text)
    if re.search(r"(?:consequence|par consequent|donc|ainsi|renforc\w*)[^.;]{0,220}(?:apres que|apres avoir)", normalized):
        violations.append(Violation("fond", "ordre_fait_avant_consequence", "Consequence/perspective precedes the source-attested action."))

    claim_id = str(claim.get("id") or "")
    marker = f"[claim:{claim_id}]" if claim_id else ""
    mention_count = (arc_context.get("mention_count") or {}).get(claim_id, 0)
    active_callbacks = set(arc_context.get("active_callbacks") or [])
    if marker and marker in text and mention_count >= 2 and claim_id in active_callbacks:
        violations.append(Violation(
            "fond",
            "citation_evidentielle_au_dela_du_callback_disponible",
            "A third direct evidentiary citation is used while an active callback is available.",
        ))
    elif marker and marker in text and mention_count >= 2:
        warnings.append("over_mentioned_claim: more than two direct citations; review whether a callback should replace this citation")

    if arc_context.get("false_lead"):
        count = int(arc_context.get("false_lead_count_in_subsection", 0))
        if count >= 2:
            violations.append(Violation("forme", "false_lead_rerank_limit", "Subsection already contains the maximum two false leads."))
        if "?" not in text:
            violations.append(Violation("forme", "false_lead_socratic_format", "False lead must contain a naïve or semi-rhetorical question."))

    if not arc_context.get("neighbor_context_loaded", False):
        warnings.append("tone_not_checked: load only previous/next paragraph for bounded L2 continuity review")

    return ReviewResult(passed=not violations, violations=violations, warnings=warnings)
