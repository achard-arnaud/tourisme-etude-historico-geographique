#!/usr/bin/env python3
"""Materialize the post-1948 V4 reader without altering its evidence state.

The V3 corpus is retained.  This pass only normalizes reader-facing labels and
moves each already-approved causal question and synopsis to the start of its
chapter so that the manuscript follows the problem-first contract.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
OUTPUT = REPO / "examples" / "sri_lanka_post_1948" / "09_output"
DEFAULT_SOURCE = OUTPUT / "report_v3_full.md"
DEFAULT_OUTPUT = OUTPUT / "report_v4_full.md"
ARC_HEADING = re.compile(r"^# ARC A(\d{2}) — (.+)$", re.MULTILINE)


def _trim_separators(lines: list[str]) -> list[str]:
    while lines and (not lines[0].strip() or lines[0].strip() == "---"):
        lines.pop(0)
    while lines and (not lines[-1].strip() or lines[-1].strip() == "---"):
        lines.pop()
    return lines


def _normalize_reader_labels(text: str) -> str:
    text = re.sub(r"^## Complément V3 — Run 5 — ", "## ", text, flags=re.MULTILINE)
    text = re.sub(r"^## Complément V3 — ", "## ", text, flags=re.MULTILINE)
    text = re.sub(r"^### HIL-[0-9/]+ — ", "### ", text, flags=re.MULTILINE)
    text = re.sub(r"^### Z[0-9]+(?:/Z?[0-9]+)* — ", "### ", text, flags=re.MULTILINE)
    text = text.replace("### Axe Run 5 — conversion territoriale", "### Axe de conversion territoriale")
    text = text.replace("## Appareil de sources des compléments V3", "## Appareil de sources")
    text = text.replace("Mais Run 5 ajoute une correction centrale", "La comparaison ajoute une correction centrale")
    text = text.replace("Mais Cette passe ajoute une correction centrale", "La comparaison ajoute une correction centrale")
    text = text.replace("Run 5 ferme précisément ces raccourcis", "La comparaison ferme précisément ces raccourcis")
    text = re.sub(
        r"\*\*Bridge vers A(\d{2}) :\*\*",
        lambda match: f"**Passage vers le chapitre {int(match.group(1))} :**",
        text,
    )
    return text


def _normalize_preamble(text: str) -> str:
    text = re.sub(
        r"\A\*\*SRI LANKA\*\*.*?(?=^# Méthode de lecture$)",
        "",
        text,
        flags=re.MULTILINE | re.DOTALL,
    )
    text = text.replace("## Politique éditoriale de la V3 intégrale", "## Promesse de lecture")
    text = re.sub(
        r"Cette édition conserve la totalité de la V1 moderne.*?ses limites\.\n",
        "Cette édition V4 conserve la matière historique et les limites de preuve de l’édition intégrale. "
        "Elle réordonne chaque chapitre autour de sa question causale, sans plafond de mots ni compression automatique.\n",
        text,
        flags=re.DOTALL,
    )
    text = re.sub(
        r"^- \*\*A(\d{2}) · ([^—]+)—\*\* ",
        lambda match: f"- **Chapitre {int(match.group(1))} · {match.group(2).strip()} —** ",
        text,
        flags=re.MULTILINE,
    )
    return _normalize_reader_labels(text)


def _summary_span(lines: list[str], start: int) -> tuple[int, list[str]]:
    index = start
    while index < len(lines) and not lines[index].strip():
        index += 1
    summary: list[str] = []
    while index < len(lines):
        value = lines[index]
        if value.startswith("#") or value.strip() == "---":
            break
        if not value.strip() and summary:
            break
        if value.strip():
            summary.append(value)
        index += 1
    if not summary:
        raise ValueError("empty TL;DR summary")
    return index, summary


def normalize_chapter(number: int, title: str, body: str) -> str:
    lines = body.splitlines()
    question_indexes = [i for i, line in enumerate(lines) if line.startswith("**Question causale :")]
    if len(question_indexes) != 1:
        raise ValueError(f"chapter {number}: expected one causal question, found {len(question_indexes)}")
    question_index = question_indexes[0]
    try:
        summary_heading = lines.index("## TL;DR", question_index + 1)
    except ValueError as exc:
        raise ValueError(f"chapter {number}: missing TL;DR after causal question") from exc
    summary_end, summary = _summary_span(lines, summary_heading + 1)
    before = _trim_separators(lines[:question_index])
    after = _trim_separators(lines[summary_end:])
    assembled = [
        f"# Chapitre {number} — {title}",
        "",
        lines[question_index],
        "",
        *summary,
        "",
        *before,
        "",
        *after,
    ]
    return _normalize_reader_labels("\n".join(assembled).strip())


def materialize(source_text: str) -> str:
    matches = list(ARC_HEADING.finditer(source_text))
    if len(matches) != 8:
        raise ValueError(f"expected eight arcs, found {len(matches)}")
    preamble = _normalize_preamble(source_text[: matches[0].start()].rstrip())
    chapters: list[str] = []
    for index, match in enumerate(matches):
        end = matches[index + 1].start() if index + 1 < len(matches) else len(source_text)
        tail_marker = source_text.find("\n# Synthèse", match.end(), end)
        chapter_end = tail_marker if tail_marker >= 0 else end
        number = int(match.group(1))
        if number != index + 1:
            raise ValueError(f"unexpected arc order: A{number:02d}")
        chapters.append(normalize_chapter(number, match.group(2), source_text[match.end():chapter_end]))
        if tail_marker >= 0:
            tail = source_text[tail_marker + 1 :]
            break
    else:
        tail = ""
    if not tail.startswith("# Synthèse"):
        raise ValueError("missing synthesis after A08")
    tail = _normalize_reader_labels(tail)
    return "\n\n".join([preamble, *chapters, tail]).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rendered = materialize(args.source.read_text(encoding="utf-8"))
    if args.check:
        if not args.output.exists() or args.output.read_text(encoding="utf-8") != rendered:
            raise SystemExit(f"post-1948 V4 is stale: {args.output}")
        print(f"POST-1948 V4 IDEMPOTENCE OK: {args.output}")
        return 0
    args.output.write_text(rendered, encoding="utf-8")
    print(f"POST-1948 V4 MATERIALIZED: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
