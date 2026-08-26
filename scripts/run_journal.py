#!/usr/bin/env python3
"""Append-only run journal helper used by deterministic transition scripts."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path


def journal_path(repo: Path, run: int) -> Path:
    return repo / "docs" / f"RUN{run}_JOURNAL.md"


def append_entry(
    repo: Path,
    run: int,
    step: str,
    artifacts: list[str],
    trigger: str,
    consistency: str,
    timestamp: str | None = None,
    details: list[str] | None = None,
) -> Path:
    """Append one immutable journal entry; never rewrite previous entries."""
    path = journal_path(repo, run)
    path.parent.mkdir(parents=True, exist_ok=True)
    if not path.exists():
        path.write_text(f"# Run {run} — journal\n\n", encoding="utf-8")
    stamp = timestamp or datetime.now(timezone.utc).astimezone().isoformat(timespec="minutes")
    lines = [
        f"## {step} — {stamp}",
        f"- artefacts touchés : {', '.join(artifacts) if artifacts else 'aucun'}",
        f"- déclencheur : {trigger}",
        f"- cohérence croisée : {consistency}",
    ]
    for detail in details or []:
        lines.append(f"- {detail}")
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n".join(lines) + "\n\n")
    return path


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run", type=int, required=True)
    parser.add_argument("--step", required=True)
    parser.add_argument("--artifact", action="append", default=[])
    parser.add_argument("--trigger", required=True)
    parser.add_argument("--consistency", required=True)
    parser.add_argument("--detail", action="append", default=[])
    args = parser.parse_args()
    repo = Path(__file__).resolve().parents[1]
    path = append_entry(repo, args.run, args.step, args.artifact, args.trigger, args.consistency, details=args.detail)
    print(path.relative_to(repo))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
