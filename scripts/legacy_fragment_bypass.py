#!/usr/bin/env python3
"""Bound legacy capture debt without promoting it to evidence.

The bypass converts explicitly allowlisted, unsourced, unclaimed capture fragments
into virtual `legacy_fragment` statements at drafting time. Nothing is persisted
under `01_arcs/*/claims/`, and the wrapper never upgrades evidence.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

LEGACY_TYPE = "legacy_fragment"
CONFIG_PATH = Path("00_method/legacy_fragment_bypass.json")


def load_policy(project: Path) -> dict:
    path = project / CONFIG_PATH
    if not path.exists():
        return {"enabled": False, "capture_paths": []}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"invalid legacy fragment bypass config: {path}")
    paths = data.get("capture_paths") or []
    if not isinstance(paths, list) or not all(isinstance(x, str) for x in paths):
        raise ValueError(f"legacy capture_paths must be a string list: {path}")
    return {**data, "enabled": bool(data.get("enabled", True)), "capture_paths": paths}


def fragment_source_ids(fragment: dict) -> list[str]:
    out: list[str] = []
    sid = fragment.get("source_id")
    if isinstance(sid, str) and sid:
        out.append(sid)
    for value in fragment.get("source_ids") or []:
        if isinstance(value, str) and value and value not in out:
            out.append(value)
    return out


def fragment_text(fragment: dict) -> str:
    for key in ("assertion_summary", "summary", "verbatim", "text", "title"):
        value = fragment.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def fragment_arc(fragment: dict) -> str:
    for key in ("candidate_arc", "arc"):
        value = fragment.get(key)
        if isinstance(value, str) and value:
            return value
    return ""


def promoted_claim_ids(fragment: dict) -> set[str]:
    value = fragment.get("promotes_to")
    if isinstance(value, str):
        return {value} if value else set()
    if isinstance(value, list):
        return {str(x) for x in value if x}
    return set()


def virtual_legacy_statements(
    project: Path,
    fragments: dict[str, dict],
    claimed_fragment_ids: Iterable[str],
    known_claim_ids: Iterable[str],
) -> list[dict]:
    policy = load_policy(project)
    if not policy.get("enabled"):
        return []
    allowed_paths = set(policy.get("capture_paths") or [])
    claimed = {str(x) for x in claimed_fragment_ids}
    known_claims = {str(x) for x in known_claim_ids}
    out: list[dict] = []
    for fid, fragment in sorted(fragments.items()):
        capture_path = str(fragment.get("_capture_path") or "")
        if capture_path not in allowed_paths:
            continue
        if fid in claimed:
            continue
        if promoted_claim_ids(fragment) & known_claims:
            continue
        # The bypass exists for the original unsourced debt only. If a source has
        # since been attached, the fragment should flow through normal evidence paths.
        if fragment_source_ids(fragment):
            continue
        arc = fragment_arc(fragment)
        text = fragment_text(fragment)
        if not arc or not text:
            continue
        out.append({
            "id": f"LEGACY::{fid}",
            "type": LEGACY_TYPE,
            "claim": text,
            "confidence": "U",
            "zoom": fragment.get("zoom") if fragment.get("zoom") in {f"Z{i}" for i in range(5)} else "Z0",
            "causal_role": "context",
            "arc": arc,
            "source_ids": [],
            "origin_fragment_ids": [fid],
            "legacy_unsourced": True,
            "virtual": True,
            "drafting_policy": {
                "may_preserve_existing_narrative": True,
                "may_seed_research_question": True,
                "may_establish_new_fact_without_source": False,
                "may_satisfy_sourcing_gate": False,
                "render_type_in_reader": False,
            },
        })
    return out


def validate_persisted_legacy_claim(claim: dict) -> list[str]:
    """Allow the type in contracts, but keep persisted use deliberately narrow."""
    if claim.get("type") != LEGACY_TYPE:
        return []
    errors: list[str] = []
    if not claim.get("legacy_unsourced"):
        errors.append("legacy_fragment requires legacy_unsourced=true")
    if claim.get("source_ids"):
        errors.append("legacy_fragment must not masquerade as sourced evidence")
    refs = claim.get("origin_fragment_ids") or []
    if not isinstance(refs, list) or not refs:
        errors.append("legacy_fragment requires origin_fragment_ids")
    if claim.get("confidence") not in {"D", "U"}:
        errors.append("legacy_fragment confidence must be D or U")
    if claim.get("causal_role") not in {"context", "none"}:
        errors.append("legacy_fragment causal_role must be context or none")
    return errors
