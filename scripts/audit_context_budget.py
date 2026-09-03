#!/usr/bin/env python3
"""Audit the context that a routed run can actually load.

The former audit counted only ``SKILL.md`` files from the latest JSON manifest.
That produced two false-green modes: a newer run could exist without a manifest,
and mandatory companion Markdown referenced by a routed skill was invisible.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


RUN_RE = re.compile(r"^RUN(\d+)")
MARKDOWN_REF_RE = re.compile(
    r"`(?P<code>[^`\n]+\.md)`|\((?P<link>[^)\s]+\.md)(?:#[^)]*)?\)"
)


def run_number(path: Path) -> int | None:
    match = RUN_RE.match(path.name)
    return int(match.group(1)) if match else None


def latest_manifest(repo: Path) -> Path:
    manifests = [
        (run_number(path), path.name, path)
        for path in (repo / "docs").glob("RUN*_MANIFEST.json")
        if run_number(path) is not None
    ]
    if not manifests:
        raise FileNotFoundError("no RUN*_MANIFEST.json")
    latest = max(manifests)
    run_artifacts = [
        run_number(path)
        for path in (repo / "docs").glob("RUN*")
        if run_number(path) is not None
    ]
    latest_artifact_run = max(run_artifacts, default=latest[0])
    if latest[0] < latest_artifact_run:
        raise RuntimeError(
            f"latest run is RUN{latest_artifact_run} but latest workflow manifest "
            f"is RUN{latest[0]}; add a manifest before auditing context"
        )
    return latest[2]


def _resolve_markdown_ref(repo: Path, source: Path, raw: str) -> Path | None:
    ref = raw.split("#", 1)[0]
    candidates = [repo / ref, source.parent / ref]
    for candidate in candidates:
        try:
            resolved = candidate.resolve()
            resolved.relative_to(repo.resolve())
        except (OSError, ValueError):
            continue
        if resolved.is_file():
            return resolved
    return None


def _companion_files(repo: Path, routed_skill_files: list[Path]) -> set[Path]:
    """Follow Markdown references from routed skills, not all root capabilities."""
    found: set[Path] = set()
    queue = list(routed_skill_files)
    visited: set[Path] = set()
    while queue:
        source = queue.pop()
        if source in visited:
            continue
        visited.add(source)
        text = source.read_text(encoding="utf-8")
        for match in MARKDOWN_REF_RE.finditer(text):
            raw = match.group("code") or match.group("link")
            target = _resolve_markdown_ref(repo, source, raw)
            if target and target not in found:
                found.add(target)
                queue.append(target)
    return found


def context_files(repo: Path, manifest: dict) -> list[Path]:
    names = [entry.get("skill") for entry in manifest.get("dispatched_skills", [])]
    names = [name for name in names if name]
    routed = [repo / "skills" / name / "SKILL.md" for name in names]
    missing = [str(path.relative_to(repo)) for path in routed if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing routed skill context: " + ", ".join(missing))

    explicit: list[Path] = []
    for raw in manifest.get("runtime_context_files", []) or []:
        path = (repo / raw).resolve()
        try:
            path.relative_to(repo.resolve())
        except ValueError as exc:
            raise ValueError(f"runtime context escapes repository: {raw}") from exc
        if not path.is_file():
            raise FileNotFoundError(f"missing runtime context file: {raw}")
        explicit.append(path)

    files = {repo / "SKILL.md", *routed, *explicit}
    files |= _companion_files(repo, routed)
    return sorted(files, key=lambda path: str(path.relative_to(repo)))


def audit(repo: Path, manifest_path: Path, budget: int) -> dict:
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    files = context_files(repo, data)
    counts = {
        str(path.relative_to(repo)): len(path.read_text(encoding="utf-8").split())
        for path in files
    }
    words = sum(counts.values())
    return {
        "manifest": manifest_path.name,
        "budget": budget,
        "words": words,
        "files": counts,
        "dispatched_skills": len(data.get("dispatched_skills", []) or []),
        "ok": words <= budget,
    }


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser()
    parser.add_argument("manifest", nargs="?")
    parser.add_argument("--latest", action="store_true")
    parser.add_argument("--budget", type=int, default=12000)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        path = (
            latest_manifest(repo)
            if args.latest or not args.manifest
            else (repo / args.manifest).resolve()
        )
        report = audit(repo, path, args.budget)
    except Exception as exc:
        print(f"ERROR: context budget audit failed: {exc}")
        return 1
    if args.json:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    elif report["ok"]:
        print(
            f"CONTEXT BUDGET OK: {report['words']}/{report['budget']} words "
            f"across {len(report['files'])} runtime files and "
            f"{report['dispatched_skills']} dispatched skills from {report['manifest']}"
        )
    else:
        print(
            f"ERROR: routed context {report['words']} words exceeds budget "
            f"{report['budget']} across {len(report['files'])} files"
        )
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
