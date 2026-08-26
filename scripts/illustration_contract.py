#!/usr/bin/env python3
"""Validate reader-facing illustrations linked to evidence inputs."""
from __future__ import annotations
import json
from pathlib import Path

SCHEMA_VERSION = "1.0"
CLASS = "illustration"
STATUSES = {"candidate", "vision_validated", "reader_eligible", "retired"}
INPUT_TYPES = {"intake", "field_fragment", "claim", "bridge", "side_story", "arc"}


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


def validate_illustrations(project: Path) -> tuple[list[str], list[str], int]:
    errors: list[str] = []
    warnings: list[str] = []
    seen: set[str] = set()
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
        refs = item.get("input_refs") or []
        if not refs:
            errors.append(f"illustration {iid}: at least one input_ref required")
        for ref in refs:
            if ref.get("type") not in INPUT_TYPES or not (ref.get("id") or ref.get("path")):
                errors.append(f"illustration {iid}: invalid input_ref")
        review = item.get("vision_review") or {}
        frag = item.get("fragment") or {}
        if status in {"vision_validated", "reader_eligible"}:
            if review.get("status") != "reviewed" or review.get("confidence") not in {"low", "medium", "high"}:
                errors.append(f"illustration {iid}: reviewed vision metadata required")
            for key in ("caption", "what_it_shows", "why_here", "limits"):
                if not frag.get(key):
                    errors.append(f"illustration {iid}: fragment.{key} required")
        if status == "reader_eligible":
            human = item.get("human_review") or {}
            if human.get("status") != "approved":
                errors.append(f"illustration {iid}: reader_eligible requires human approval")
        if src.get("binary_status") == "external_only":
            warnings.append(f"illustration {iid}: binary external to repository; placement may render as caption-only")
    return errors, warnings, len(assets)
