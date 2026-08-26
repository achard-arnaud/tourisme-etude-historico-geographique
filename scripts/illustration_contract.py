#!/usr/bin/env python3
"""Validate reader-facing illustrations linked to evidence inputs."""
from __future__ import annotations
import json,os,re
from pathlib import Path
import sys

SCHEMA_VERSION = "1.0"
CLASS = "illustration"
STATUSES = {"candidate", "vision_validated", "reader_eligible", "retired"}
INPUT_TYPES = {"intake", "field_fragment", "claim", "bridge", "side_story", "arc"}
EVIDENCE_STATUSES = {"observed_caption", "canonical_text", "chronicle_tradition", "interpretive"}
TEXTUAL_LAYERS = {"early_discourse", "canonical_vinaya", "later_biography", "chronicle", "local_temple", "unresolved"}
BINARY_STATUSES = {"external_only", "repository"}
SHA_STATUSES = {"verified_at_intake", "repository_verified", "supplied_unverified"}
TAG_REVIEW_STATUSES = {"pending", "approved", "rejected"}
TAG_REVIEW_TRIGGERS = {"auto_low_confidence", "manual"}
FORBIDDEN_CAPTION_PATTERNS = [r"\bprouve\b", r"\bconfirme historiquement\b", r"\battest[ée] formellement\b", r"\bdémontre que\b"]
STRICT_CONFIDENCE_GATE = os.environ.get("ILLUSTRATION_CONFIDENCE_GATE", "0") == "1"


def illustration_marker(iid: str) -> str:
    return f"[ILLUSTRATION:{iid}]"


def load_illustrations(project: Path):
    root = project / "09_output" / "illustrations"
    out = []
    if not root.exists():
        return out
    for p in sorted(root.glob("*.json")):
        data = json.loads(p.read_text(encoding="utf-8"))
        items = data if isinstance(data, list) else [data]
        out.extend((p, x) for x in items)
    return out


def _json_ids(path: Path) -> set[str]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return set()
    items = data if isinstance(data, list) else [data]
    return {str(x["id"]) for x in items if isinstance(x, dict) and x.get("id")}


def _ref_resolves(project: Path, ref: dict) -> bool:
    rel = ref.get("path")
    rid = str(ref.get("id") or "")
    if rel:
        path = project / str(rel)
        return path.exists() and (not rid or rid in _json_ids(path))
    if ref.get("type") == "arc" and rid:
        return (project / "01_arcs" / rid / "ARC.md").exists()
    patterns = {
        "claim": "01_arcs/*/claims/*.json",
        "bridge": "06_bridges/*.json",
        "side_story": "09_output/side_stories/*.json",
    }
    return bool(rid and any(rid in _json_ids(p) for p in project.glob(patterns.get(ref.get("type"), "__none__"))))


def lint_caption_language(item: dict) -> list[str]:
    """L1 regex linter over short illustration fragments only; never hydrates the manuscript."""
    iid = item.get("id", "<unknown>")
    fragment = item.get("fragment") or {}
    errors = []
    for field in ("caption", "what_it_shows", "why_here"):
        text = str(fragment.get(field) or "")
        for pattern in FORBIDDEN_CAPTION_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                errors.append(f"illustration {iid}: fragment.{field} uses overclaiming language matching {pattern}")
    return errors


def check_illustration_density(markdown: str, selected_ids: list[str], max_per_n_pages: int = 2, words_per_page: int = 500) -> list[str]:
    """L0 deterministic density gate using word windows and already-selected marker IDs."""
    if max_per_n_pages < 1 or words_per_page < 1:
        return ["illustration density policy must use positive max_per_n_pages and words_per_page"]
    selected = set(selected_ids)
    if not selected:
        return []
    tokens = re.findall(r"\[ILLUSTRATION:[^\]]+\]|\S+", markdown)
    window_words = max_per_n_pages * words_per_page
    errors = []
    word_index = 0
    buckets: dict[int, list[str]] = {}
    for token in tokens:
        marker = re.fullmatch(r"\[ILLUSTRATION:([^\]]+)\]", token)
        if marker:
            iid = marker.group(1)
            if iid in selected:
                bucket = word_index // window_words
                buckets.setdefault(bucket, []).append(iid)
        else:
            word_index += 1
    for bucket, ids in sorted(buckets.items()):
        if len(ids) > 1:
            start = bucket * window_words + 1
            end = (bucket + 1) * window_words
            errors.append(f"illustration density exceeded in words {start}-{end}: {', '.join(ids)}")
    return errors


def validate_illustrations(project: Path) -> tuple[list[str], list[str], int]:
    errors: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()
    seen_assets: set[tuple[str, str]] = set()
    assets = load_illustrations(project)
    for p, item in assets:
        iid = item.get("id")
        status = item.get("status")
        if item.get("schema_version") != SCHEMA_VERSION or item.get("class") != CLASS:
            errors.append(f"illustration {iid or p.name}: invalid class/schema")
        if not iid or iid in seen:
            errors.append(f"illustration {iid or p.name}: missing/duplicate id")
        else:
            seen.add(iid)
        if status not in STATUSES:
            errors.append(f"illustration {iid}: invalid status")
        src = item.get("source") or {}
        if not src.get("asset_ref") or not src.get("sha256"):
            errors.append(f"illustration {iid}: source asset_ref and sha256 required")
        elif not re.fullmatch(r"[0-9a-f]{64}", str(src.get("sha256"))):
            errors.append(f"illustration {iid}: invalid sha256")
        asset_key = (str(src.get("asset_ref") or ""), str(src.get("sha256") or ""))
        if all(asset_key) and asset_key in seen_assets:
            errors.append(f"illustration {iid}: duplicate source asset/hash")
        elif all(asset_key):
            seen_assets.add(asset_key)
        if src.get("binary_status") not in BINARY_STATUSES:
            errors.append(f"illustration {iid}: invalid binary_status")
        if src.get("sha256_status") not in SHA_STATUSES:
            errors.append(f"illustration {iid}: source.sha256_status required")
        if src.get("binary_status") == "repository" and src.get("sha256_status") != "repository_verified":
            errors.append(f"illustration {iid}: repository binary requires repository_verified hash")
        refs = item.get("input_refs") or []
        if not refs:
            errors.append(f"illustration {iid}: at least one input_ref required")
        for ref in refs:
            if ref.get("type") not in INPUT_TYPES or not (ref.get("id") or ref.get("path")):
                errors.append(f"illustration {iid}: invalid input_ref")
            elif not _ref_resolves(project, ref):
                errors.append(f"illustration {iid}: unresolved input_ref {ref}")
        depiction = item.get("depiction") or {}
        if depiction.get("evidence_status") not in EVIDENCE_STATUSES:
            errors.append(f"illustration {iid}: invalid depiction.evidence_status")
        if depiction.get("textual_layer") not in TEXTUAL_LAYERS:
            errors.append(f"illustration {iid}: depiction.textual_layer required")
        review = item.get("vision_review") or {}
        frag = item.get("fragment") or {}
        if status in {"vision_validated", "reader_eligible"}:
            if review.get("status") != "reviewed" or review.get("confidence") not in {"low", "medium", "high"}:
                errors.append(f"illustration {iid}: reviewed vision metadata required")
            for key in ("caption", "what_it_shows", "why_here", "limits"):
                if not frag.get(key):
                    errors.append(f"illustration {iid}: fragment.{key} required")
        if review.get("confidence") == "low":
            if depiction.get("evidence_status") != "interpretive":
                errors.append(f"illustration {iid}: low-confidence vision_review requires depiction.evidence_status=interpretive")
            tag_review = item.get("tag_review") or {}
            if tag_review:
                if tag_review.get("status") not in TAG_REVIEW_STATUSES or tag_review.get("trigger") not in TAG_REVIEW_TRIGGERS:
                    errors.append(f"illustration {iid}: invalid tag_review metadata")
                if status in {"vision_validated", "reader_eligible"} and tag_review.get("status") != "approved":
                    errors.append(f"illustration {iid}: low-confidence tagging requires explicit tag_review approval")
            elif status in {"vision_validated", "reader_eligible"}:
                message=f"illustration {iid}: legacy low-confidence asset lacks tag_review; run migrate_confidence_gate.py before strict activation"
                if STRICT_CONFIDENCE_GATE: errors.append(message)
                else: warnings.append(message)
        errors.extend(lint_caption_language(item))
        if status == "reader_eligible":
            human = item.get("human_review") or {}
            if human.get("status") != "approved":
                errors.append(f"illustration {iid}: reader_eligible requires human approval")
        if status != "reader_eligible" and (item.get("render") or {}).get("required_in_reader"):
            errors.append(f"illustration {iid}: non-eligible asset cannot be required_in_reader")
        if (item.get("render") or {}).get("marker") != illustration_marker(str(iid)):
            errors.append(f"illustration {iid}: invalid render marker")
        placement = item.get("placement") or {}
        if not placement.get("arc_ref"):
            errors.append(f"illustration {iid}: placement.arc_ref required")
        elif not (project / "01_arcs" / str(placement["arc_ref"]) / "ARC.md").exists():
            errors.append(f"illustration {iid}: placement.arc_ref does not resolve")
        if placement.get("target_status") not in {"resolved", "proposed_missing"}:
            errors.append(f"illustration {iid}: placement.target_status required")
        if placement.get("target_status") == "resolved" and not placement.get("section_anchor"):
            errors.append(f"illustration {iid}: resolved placement requires section_anchor")
        if status == "reader_eligible" and placement.get("target_status") != "resolved":
            errors.append(f"illustration {iid}: reader_eligible requires resolved placement")
        if src.get("binary_status") == "external_only":
            warnings.append(f"illustration {iid}: binary external to repository; placement may render as caption-only")
    return errors, warnings, len(assets)


def assert_rendered_illustrations(markdown: str, selected_ids: list[str]) -> int:
    missing = [iid for iid in selected_ids if markdown.count(illustration_marker(iid)) != 1]
    if missing:
        raise RuntimeError("selected illustrations must appear exactly once: " + ", ".join(sorted(missing)))
    return len(selected_ids)


def main() -> int:
    project = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    errors, warnings, count = validate_illustrations(project)
    for value in warnings:
        print("WARN:", value, file=sys.stderr)
    for value in errors:
        print("ERROR:", value, file=sys.stderr)
    if errors:
        return 1
    print(f"ILLUSTRATION CONTRACT OK: {count} assets")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
