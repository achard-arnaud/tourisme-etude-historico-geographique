#!/usr/bin/env python3
"""Chapter-local conservation and frontstage QA for the post-1948 V4."""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
PROJECT = REPO / "examples" / "sri_lanka_post_1948"
BASELINE = PROJECT / "09_output" / "report_v3_full.md"
CANDIDATE = PROJECT / "09_output" / "report_v4_full.md"
DEFAULT_OUTPUT = REPO / "docs" / "RUN56_POST1948_CHAPTER_REVIEW.json"
BASELINE_HEADING = re.compile(r"^# ARC A(\d{2}) — .+$", re.MULTILINE)
CANDIDATE_HEADING = re.compile(r"^# Chapitre (\d+) — .+$", re.MULTILINE)
SOURCE_ID = re.compile(r"\b[A-Z][A-Z0-9]*(?:-[A-Z0-9]+)+\b")
PROHIBITED = (
    re.compile(r"^# ARC A\d{2}", re.MULTILINE),
    re.compile(r"^## TL;DR$", re.MULTILINE),
    re.compile(r"^## Complément V3", re.MULTILINE),
    re.compile(r"^### HIL-[0-9/]", re.MULTILINE),
    re.compile(r"^### Z[0-9]+(?:/Z?[0-9]+)*\s+[—–-]", re.MULTILINE),
    re.compile(r"\bRun 5\b"),
)


def _split(text: str, heading: re.Pattern[str]) -> dict[int, str]:
    matches = list(heading.finditer(text))
    out: dict[int, str] = {}
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
        if index + 1 == len(matches):
            synthesis = text.find("\n# Synthèse", match.end(), end)
            if synthesis >= 0:
                end = synthesis
        out[int(match.group(1))] = text[match.start():end].strip()
    return out


def _source_counter(text: str) -> Counter[str]:
    ids: list[str] = []
    for bracket in re.findall(r"\[([^\]]+)\]", text):
        ids.extend(SOURCE_ID.findall(bracket))
    return Counter(ids)


def _paragraphs(text: str) -> list[str]:
    cleaned = re.sub(r"<[^>]+>", " ", text)
    return [re.sub(r"\s+", " ", part).strip() for part in re.split(r"\n\s*\n", cleaned)]


def build_report(baseline: Path = BASELINE, candidate: Path = CANDIDATE) -> dict:
    base_text = baseline.read_text(encoding="utf-8")
    candidate_text = candidate.read_text(encoding="utf-8")
    base_chapters = _split(base_text, BASELINE_HEADING)
    candidate_chapters = _split(candidate_text, CANDIDATE_HEADING)
    errors: list[str] = []
    chapters: list[dict] = []
    if sorted(base_chapters) != list(range(1, 9)):
        errors.append("baseline does not contain A01-A08 exactly once")
    if sorted(candidate_chapters) != list(range(1, 9)):
        errors.append("candidate does not contain chapters 1-8 exactly once")
    for number in range(1, 9):
        base = base_chapters.get(number, "")
        current = candidate_chapters.get(number, "")
        chapter_errors: list[str] = []
        nonempty = [line.strip() for line in current.splitlines() if line.strip()]
        if len(nonempty) < 2 or not nonempty[1].startswith("**Question causale :"):
            chapter_errors.append("causal question is not the first substantive line")
        if current.count("**Question causale :") != 1:
            chapter_errors.append("causal question count is not one")
        if _source_counter(base) != _source_counter(current):
            chapter_errors.append("source citation inventory changed")
        base_callouts = base.count("<table>")
        current_callouts = current.count("<table>")
        if base_callouts != current_callouts:
            chapter_errors.append("HTML callout inventory changed")
        retention = len(current) / max(1, len(base))
        if retention < 0.90:
            chapter_errors.append(f"character retention below 90% ({retention:.3f})")
        for pattern in PROHIBITED:
            if pattern.search(current):
                chapter_errors.append(f"backstage/production label remains: {pattern.pattern}")
        chapters.append(
            {
                "chapter": number,
                "status": "pass" if not chapter_errors else "fail",
                "sha256": hashlib.sha256(current.encode("utf-8")).hexdigest(),
                "character_retention": round(retention, 4),
                "source_citations": sum(_source_counter(current).values()),
                "html_callouts": current_callouts,
                "errors": chapter_errors,
            }
        )
        errors.extend(f"chapter {number}: {error}" for error in chapter_errors)
    occurrences: dict[str, list[str]] = defaultdict(list)
    for number, chapter in candidate_chapters.items():
        for paragraph in _paragraphs(chapter):
            if len(paragraph) >= 180 and not paragraph.startswith(("#", "|")):
                occurrences[paragraph.casefold()].append(f"chapter {number}")
    duplicates = [locations for locations in occurrences.values() if len(locations) > 1]
    if duplicates:
        errors.append(f"exact long-paragraph duplicates remain: {duplicates}")
    for pattern in PROHIBITED:
        if pattern.search(candidate_text):
            errors.append(f"frontstage production label remains outside chapter QA: {pattern.pattern}")
    report = {
        "schema_version": 1,
        "run_id": "RUN56",
        "mode": "proofread",
        "baseline": str(baseline.relative_to(REPO)),
        "candidate": str(candidate.relative_to(REPO)),
        "status": "pass" if not errors else "fail",
        "chapters": chapters,
        "exact_long_paragraph_duplicates": duplicates,
        "errors": errors,
        "next": "Render the two V4 DOCX files, lint their visible frontstage, then complete page-by-page visual QA.",
    }
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, default=BASELINE)
    parser.add_argument("--candidate", type=Path, default=CANDIDATE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    report = build_report(args.baseline, args.candidate)
    payload = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != payload:
            print(f"POST-1948 V4 QA REPORT STALE: {args.output}")
            return 1
    else:
        args.output.write_text(payload, encoding="utf-8")
    if report["errors"]:
        for error in report["errors"]:
            print("ERROR:", error)
        return 1
    print("POST-1948 V4 CHAPTER QA OK: 8/8 chapters")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
