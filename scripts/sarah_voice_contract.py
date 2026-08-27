#!/usr/bin/env python3
"""Auditable Sarah voice contract and independent-review validation.

The voice definition is static and versioned in
skills/storytelling-historical-travel/references/sarah_voice_markers.md.
Runtime never researches or mutates Sarah's voice.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import re
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CONTRACT_PATH = ROOT / "skills/storytelling-historical-travel/references/sarah_voice_markers.md"
CONTRACT_RE = re.compile(
    r"<!--\s*SARAH_VOICE_CONTRACT_BEGIN\s*-->\s*```json\s*(.*?)\s*```\s*<!--\s*SARAH_VOICE_CONTRACT_END\s*-->",
    re.S,
)
CLAIM_MARKER = re.compile(r"\[claim:[^\]]+\]", re.I)
VALID_STATUSES = {"pass", "fail", "not_applicable"}


def _norm_visible_text(text: str) -> str:
    return re.sub(r"\s+", " ", CLAIM_MARKER.sub("", text or "")).strip()


def paragraph_sha256(text: str) -> str:
    return hashlib.sha256(_norm_visible_text(text).encode("utf-8")).hexdigest()


def contract_sha256(path: Path = DEFAULT_CONTRACT_PATH) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_voice_contract(path: Path = DEFAULT_CONTRACT_PATH) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    match = CONTRACT_RE.search(text)
    if not match:
        raise RuntimeError(f"Sarah voice contract block missing in {path}")
    data = json.loads(match.group(1))
    markers = data.get("markers") or []
    ids = [str(item.get("id")) for item in markers if isinstance(item, dict) and item.get("id")]
    if len(ids) != len(markers) or len(ids) != len(set(ids)):
        raise RuntimeError("Sarah voice contract contains missing or duplicate marker ids")
    mandatory = {str(x) for x in data.get("mandatory_markers") or []}
    if not mandatory.issubset(set(ids)):
        raise RuntimeError("Sarah voice contract mandatory_markers reference unknown markers")
    return data


def marker_index(contract: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(item["id"]): item for item in contract.get("markers") or []}


def review_skeleton(text: str, *, generation_pass_id: str | None = None, generation_context_id: str | None = None) -> dict[str, Any]:
    """Create a non-passing review record bound to the current paragraph/contract."""
    contract = load_voice_contract()
    return {
        "passed": False,
        "reviewer_role": "independent_style_gate",
        "evaluator": None,
        "generation_pass_id": generation_pass_id,
        "review_pass_id": None,
        "generation_context_id": generation_context_id,
        "review_context_id": None,
        "paragraph_sha256": paragraph_sha256(text),
        "voice_contract_id": contract["contract_id"],
        "voice_contract_sha256": contract_sha256(),
        "marker_results": {},
        "notes": "",
    }


def validate_style_review(text: str, record: dict[str, Any] | None, *, contract_path: Path = DEFAULT_CONTRACT_PATH) -> tuple[list[str], list[str]]:
    """Validate auditability and bounded semantic verdict structure.

    This cannot mechanically decide whether prose 'sounds like Sarah'. It prevents
    self-certification, stale reviews and marker-name box ticking, and requires an
    independent reviewer to leave paragraph-specific verdicts against the frozen
    contract.
    """
    errors: list[str] = []
    warnings: list[str] = []
    record = record or {}
    contract = load_voice_contract(contract_path)
    markers = marker_index(contract)

    if record.get("passed") is not True:
        errors.append("Sarah style review not explicitly passed")
    if record.get("reviewer_role") != "independent_style_gate":
        errors.append("Sarah review must use reviewer_role=independent_style_gate")
    if not str(record.get("evaluator") or "").strip():
        errors.append("Sarah review evaluator missing")

    generation_pass_id = str(record.get("generation_pass_id") or "").strip()
    review_pass_id = str(record.get("review_pass_id") or "").strip()
    if not generation_pass_id or not review_pass_id:
        errors.append("Sarah review must record generation_pass_id and review_pass_id")
    elif generation_pass_id == review_pass_id:
        errors.append("Sarah review pass must be distinct from generation pass")

    generation_context_id = str(record.get("generation_context_id") or "").strip()
    review_context_id = str(record.get("review_context_id") or "").strip()
    if not generation_context_id or not review_context_id:
        errors.append("Sarah review must record generation_context_id and review_context_id")
    elif generation_context_id == review_context_id:
        errors.append("Sarah review context must be independent from generation context")

    expected_paragraph_hash = paragraph_sha256(text)
    if record.get("paragraph_sha256") != expected_paragraph_hash:
        errors.append("Sarah review paragraph hash is stale or does not match reviewed prose")
    if record.get("voice_contract_id") != contract.get("contract_id"):
        errors.append("Sarah review references the wrong voice contract id")
    expected_contract_hash = contract_sha256(contract_path)
    if record.get("voice_contract_sha256") != expected_contract_hash:
        errors.append("Sarah review voice contract hash is stale")

    results = record.get("marker_results") or {}
    if not isinstance(results, dict):
        errors.append("Sarah review marker_results must be an object")
        results = {}
    unknown = set(results) - set(markers)
    if unknown:
        errors.append(f"Sarah review contains unknown marker ids: {sorted(unknown)}")

    applicable_signature_passes = 0
    supporting_passes = 0
    signature_applicable = False
    for marker_id, marker in markers.items():
        result = results.get(marker_id)
        if result is None:
            if marker_id in set(contract.get("mandatory_markers") or []):
                errors.append(f"Sarah mandatory marker missing: {marker_id}")
            continue
        if not isinstance(result, dict):
            errors.append(f"Sarah marker result must be an object: {marker_id}")
            continue
        status = str(result.get("status") or "")
        rationale = str(result.get("rationale") or "").strip()
        if status not in VALID_STATUSES:
            errors.append(f"Sarah marker {marker_id} has invalid status {status!r}")
            continue
        if not rationale:
            errors.append(f"Sarah marker {marker_id} requires paragraph-specific rationale")
        if marker.get("applicability") == "always" and status == "not_applicable":
            errors.append(f"Sarah always-applicable marker cannot be not_applicable: {marker_id}")
        if status == "fail":
            errors.append(f"Sarah applicable marker failed: {marker_id}")
        if marker.get("kind") == "signature" and status != "not_applicable":
            signature_applicable = True
        if marker.get("kind") == "signature" and status == "pass":
            applicable_signature_passes += 1
        if marker.get("kind") == "supporting" and status == "pass":
            supporting_passes += 1

    for marker_id in contract.get("mandatory_markers") or []:
        result = results.get(str(marker_id)) or {}
        if result.get("status") != "pass":
            errors.append(f"Sarah mandatory marker must pass: {marker_id}")

    minimum = int(contract.get("minimum_signature_passes") or 1)
    if signature_applicable:
        if applicable_signature_passes < minimum:
            errors.append(f"Sarah review needs at least {minimum} applicable signature marker pass(es)")
    elif supporting_passes < 1:
        errors.append("Sarah review needs one supporting marker pass when no signature marker is applicable")

    if contract.get("primary_source_status") != "imported":
        warnings.append("Sarah primary external-memory source is not imported; review uses the frozen user-provided Run25 contract only")

    return errors, warnings
