#!/usr/bin/env python3
"""Validate YouTube evidence and its lead-only proposition register."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

EVIDENCE_SCHEMA = "video-evidence/v1"
REGISTER_SCHEMA = "video-proposition-register/v1"
LEAD_CLASSES = {"reported_claim", "interpretation", "tradition", "question", "metric_lead", "causal_lead", "discarded_lead"}
STATUSES = {"lead_only", "researching", "rejected", "promoted"}


def load(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_evidence(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != EVIDENCE_SCHEMA: errors.append("invalid evidence schema_version")
    for key in ("id", "url", "video_id", "status", "acquired_at", "segments", "transcript_sha256"):
        if key not in data: errors.append(f"evidence missing {key}")
    if data.get("status") == "success":
        if not data.get("segments"): errors.append("successful evidence has no timestamped segments")
        if not data.get("transcript_text"): errors.append("successful evidence has no transcript_text")
        if not data.get("transcript_sha256"): errors.append("successful evidence has no transcript_sha256")
    previous = -1.0
    for index, segment in enumerate(data.get("segments") or []):
        if not isinstance(segment, dict) or not segment.get("text"): errors.append(f"invalid segment {index}"); continue
        start = segment.get("start_s")
        if not isinstance(start, (int, float)) or start < previous: errors.append(f"non-monotonic segment {index}")
        elif isinstance(start, (int, float)): previous = float(start)
    return errors


def validate_register(data: dict[str, Any], evidence_ids: set[str]) -> list[str]:
    errors: list[str] = []
    if data.get("schema_version") != REGISTER_SCHEMA: errors.append("invalid proposition register schema_version")
    seen: set[str] = set()
    for index, item in enumerate(data.get("propositions") or []):
        prefix = f"proposition[{index}]"
        if not isinstance(item, dict): errors.append(f"{prefix} must be an object"); continue
        pid = item.get("id")
        if not pid: errors.append(f"{prefix} missing id")
        elif pid in seen: errors.append(f"duplicate proposition id {pid}")
        else: seen.add(pid)
        for key in ("statement", "claim_class", "status", "video_evidence_id", "timestamp_start_s", "timestamp_end_s", "transcript_excerpt", "research_queries"):
            if key not in item: errors.append(f"{prefix} missing {key}")
        if item.get("claim_class") not in LEAD_CLASSES: errors.append(f"{prefix} invalid claim_class")
        if item.get("status") not in STATUSES: errors.append(f"{prefix} invalid status")
        if item.get("video_evidence_id") not in evidence_ids: errors.append(f"{prefix} unresolved video_evidence_id")
        start, end = item.get("timestamp_start_s"), item.get("timestamp_end_s")
        if not isinstance(start, (int, float)) or not isinstance(end, (int, float)) or end < start:
            errors.append(f"{prefix} invalid timestamp range")
        if not isinstance(item.get("research_queries"), list) or not item.get("research_queries"):
            errors.append(f"{prefix} requires at least one falsifiable research query")
        if item.get("status") == "promoted" and not item.get("promoted_claim_ids"):
            errors.append(f"{prefix} promoted without promoted_claim_ids")
        if item.get("status") != "promoted" and item.get("promoted_claim_ids"):
            errors.append(f"{prefix} has promoted_claim_ids before promotion")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--evidence", type=Path, nargs="+", required=True)
    parser.add_argument("--register", type=Path, required=True)
    args = parser.parse_args()
    errors: list[str] = []
    evidence_ids: set[str] = set()
    for path in args.evidence:
        try: data = load(path)
        except (OSError, json.JSONDecodeError) as exc: errors.append(f"{path}: {exc}"); continue
        errors.extend(f"{path}: {error}" for error in validate_evidence(data))
        if data.get("id"): evidence_ids.add(str(data["id"]))
    try: register = load(args.register)
    except (OSError, json.JSONDecodeError) as exc: errors.append(f"{args.register}: {exc}"); register = {}
    errors.extend(f"{args.register}: {error}" for error in validate_register(register, evidence_ids))
    for error in errors: print(f"ERROR: {error}")
    if errors: return 1
    print(f"VIDEO CLAIM CONTRACT OK: {len(evidence_ids)} evidence ledger(s), {len(register.get('propositions', []))} proposition(s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
