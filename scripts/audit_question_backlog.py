#!/usr/bin/env python3
"""Report intermediate questions that need bounded remediation.

The audit is report-only by default. It never promotes, closes or rewrites a
question. ``--fail-stale`` is available for a future human-approved hard gate.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
INTERMEDIATE_STATUSES = {"open", "bounded", "blocked", "pending_external"}
RUN_ID_RE = re.compile(r"(?:^|-)R(\d+)(?:-|$)")


def latest_run(repo: Path = REPO) -> int:
    runs = []
    for path in (repo / "docs").glob("RUN*"):
        match = re.match(r"RUN(\d+)", path.name)
        if match:
            runs.append(int(match.group(1)))
    if not runs:
        raise FileNotFoundError("no RUN artefact found")
    return max(runs)


def inferred_opened_run(question: dict) -> int | None:
    explicit = question.get("opened_run")
    if isinstance(explicit, int):
        return explicit
    match = RUN_ID_RE.search(str(question.get("id") or ""))
    return int(match.group(1)) if match else None


def audit_project(project: Path, current_run: int, max_age: int) -> list[dict]:
    rows: list[dict] = []
    for path in sorted((project / "08_questions").glob("question_register*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(data, list):
            continue
        for item in data:
            if not isinstance(item, dict) or item.get("status") not in INTERMEDIATE_STATUSES:
                continue
            opened = inferred_opened_run(item)
            explicit_review = item.get("review_after_run")
            review_after = explicit_review if isinstance(explicit_review, int) else None
            if review_after is None and opened is not None:
                review_after = opened + max_age
            if review_after is None:
                state = "unscheduled"
            elif current_run >= review_after:
                state = "stale"
            else:
                state = "scheduled"
            try:
                register = str(path.relative_to(REPO))
            except ValueError:
                register = str(path)
            rows.append(
                {
                    "project": project.name,
                    "register": register,
                    "id": item.get("id"),
                    "status": item.get("status"),
                    "priority": item.get("priority"),
                    "opened_run": opened,
                    "review_after_run": review_after,
                    "age_runs": current_run - opened if opened is not None else None,
                    "state": state,
                    "next_action": "human_triage_for_research_plan" if state in {"stale", "unscheduled"} else "none",
                }
            )
    return rows


def build_report(projects: list[Path], current_run: int, max_age: int) -> dict:
    rows = [row for project in projects for row in audit_project(project, current_run, max_age)]
    return {
        "schema_version": 1,
        "class": "question_backlog_audit",
        "current_run": current_run,
        "default_max_age_runs": max_age,
        "policy": "report_only_no_automatic_research_or_status_change",
        "counts": {
            state: sum(row["state"] == state for row in rows)
            for state in ("stale", "unscheduled", "scheduled")
        },
        "questions": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", action="append", type=Path)
    parser.add_argument("--current-run", type=int)
    parser.add_argument("--max-age", type=int, default=5)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--fail-stale", action="store_true")
    args = parser.parse_args()
    projects = args.project or [
        REPO / "examples" / "sri_lanka_pre_1948",
        REPO / "examples" / "sri_lanka_post_1948",
    ]
    current = args.current_run if args.current_run is not None else latest_run()
    report = build_report(projects, current, args.max_age)
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(payload, encoding="utf-8")
    print(json.dumps({"current_run": current, **report["counts"]}, ensure_ascii=False))
    if args.fail_stale and (report["counts"]["stale"] or report["counts"]["unscheduled"]):
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
