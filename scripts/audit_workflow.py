#!/usr/bin/env python3
import json
import os
import sys
from pathlib import Path


ALLOWED_EXECUTION_STATUS = {"executed", "verified"}
DEBUG = bool(os.environ.get("SKILL_DEBUG"))


def main():
    repo = Path(__file__).resolve().parents[1]
    manifest_path = Path(sys.argv[1] if len(sys.argv) > 1 else "docs/RUN6_WORKFLOW_MANIFEST.json")
    if not manifest_path.is_absolute():
        manifest_path = repo / manifest_path
    errors = []
    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        if DEBUG:
            raise
        print(f"ERROR: invalid workflow manifest: {manifest_path}: {exc}", file=sys.stderr)
        return 1

    known = {p.parent.name for p in (repo / "skills").glob("*/SKILL.md")}
    dispatched = data.get("dispatched_skills") or []
    skipped = data.get("skipped_skills") or []
    seen = set()

    for entry in dispatched:
        name = entry.get("skill")
        if name not in known:
            errors.append(f"unknown dispatched skill: {name}")
        if name in seen:
            errors.append(f"duplicate skill routing: {name}")
        seen.add(name)
        if entry.get("status") not in ALLOWED_EXECUTION_STATUS:
            errors.append(f"invalid execution status for {name}")
        if not entry.get("reason"):
            errors.append(f"missing dispatch reason for {name}")
        outputs = entry.get("outputs") or []
        if not outputs:
            errors.append(f"missing output evidence for {name}")
        for rel in outputs:
            if not (repo / rel).exists():
                errors.append(f"missing workflow evidence path for {name}: {rel}")

    for entry in skipped:
        name = entry.get("skill")
        if name not in known:
            errors.append(f"unknown skipped skill: {name}")
        if name in seen:
            errors.append(f"duplicate skill routing: {name}")
        seen.add(name)
        if not entry.get("reason"):
            errors.append(f"missing skip reason for {name}")

    if data.get("status") == "reviewed" and seen != known:
        missing = sorted(known - seen)
        extra = sorted(seen - known)
        if missing:
            errors.append(f"unrouted skills: {', '.join(missing)}")
        if extra:
            errors.append(f"unrecognized routed skills: {', '.join(extra)}")

    for key in ("run_id", "mode", "state_before", "state_after", "promotion_decision"):
        if not data.get(key):
            errors.append(f"missing manifest field: {key}")

    for error in errors:
        print("ERROR:", error, file=sys.stderr)
    if errors:
        return 1
    print(f"WORKFLOW AUDIT OK: {len(dispatched)} dispatched, {len(skipped)} skipped, {len(known)} known skills")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
