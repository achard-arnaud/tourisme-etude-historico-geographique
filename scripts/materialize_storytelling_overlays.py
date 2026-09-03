#!/usr/bin/env python3
"""Materialize reviewed storytelling overlays onto the current pre-1948 reader Markdown.

Proof and composition stay separate. The script consumes the already-rendered V3
Markdown plus reviewed RUN47/RUN50/RUN51 narrative material and produces a
candidate full Markdown reader. It does not alter claims, confidence, source
registers, or the archived V1 baseline.
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PROJECT = REPO / "examples" / "sri_lanka_pre_1948"
OUTPUT = PROJECT / "09_output"

BASELINE = OUTPUT / "report_v3_full.md"
RUN47 = OUTPUT / "run47_storytelling_iterative_two_arcs.md"
RUN50_OVERLAY = OUTPUT / "run50_A02_A03_canonical_overlay.md"
RUN51_CH4 = OUTPUT / "run51_storytelling_ch4_polonnaruwa.md"
RUN51_CH8 = OUTPUT / "run51_storytelling_ch8_portugal_kandy.md"
DEFAULT_OUT = OUTPUT / "report_v4_full.md"

CH4 = "**Chapitre 4 — Polonnaruwa à l’apogée : eau, Saṅgha, souveraineté et projection régionale**"
CH5 = "**Chapitre 5 — La chute de Polonnaruwa : violence, fragmentation et changement d’optimum**"
CH8 = "**Chapitre 8 — Kandy face aux Portugais : la côte ne suffit pas à conquérir l’île**"
CH9 = "**Chapitre 9 — Kandy face à la VOC : de l’alliance à l’encerclement**"
CH10 = "**Chapitre 10 — Ceylan britannique : conquérir l’intérieur et reconnecter l’île au marché mondial**"
EPILOGUE = "# **Épilogue — ce que la longue durée fait apparaître**"
A02_INSERT_BEFORE = "## **VI. VIIe–Xe siècles — Islam, Tamilakam et militarisation des réseaux**"
A03_INSERT_BEFORE = "### **3. Rohana/Mahagama : le « hedge » territorial de la monarchie**"

SPECIAL_BLOCK = re.compile(
    r"(?ms)<!-- \[(?P<kind>SIDE-STORY|ARC-RECAP):(?P<id>[^\]]+)\].*?(?:<!-- \[/ARC-RECAP:[^\]]+\] -->|<!-- \[SIDE-STORY:[^\]]+\] END -->|(?=\n## |\n\*\*Chapitre |\Z))"
)


def section(text: str, start: str, end: str | None = None) -> str:
    s = text.find(start)
    if s < 0:
        raise ValueError(f"missing start anchor: {start}")
    e = len(text) if end is None else text.find(end, s + len(start))
    if e < 0:
        raise ValueError(f"missing end anchor: {end}")
    return text[s:e]


def strip_first_heading(text: str) -> str:
    return re.sub(r"(?m)^#\s+[^\n]+\n+", "", text.strip(), count=1).strip()


def extract_run47(run47: str) -> tuple[str, str]:
    a06 = section(run47, "# A06 —", "# A07b —")
    a07b = section(run47, "# A07b —")
    return strip_first_heading(a06), strip_first_heading(a07b)


def extract_overlay(text: str, name: str) -> str:
    begin = f"## {name}_BEGIN"
    end = f"## {name}_END"
    return section(text, begin, end).replace(begin, "", 1).strip()


def special_blocks(text: str) -> dict[str, str]:
    blocks: dict[str, str] = {}
    for match in SPECIAL_BLOCK.finditer(text):
        blocks[f"{match.group('kind')}:{match.group('id')}"] = match.group(0).strip()
    return blocks


def preserve_missing_specials(old: str, replacement: str) -> str:
    old_blocks = special_blocks(old)
    if not old_blocks:
        return replacement.rstrip()
    missing = [block for key, block in old_blocks.items() if key not in replacement]
    if not missing:
        return replacement.rstrip()
    return replacement.rstrip() + "\n\n" + "\n\n".join(missing)


def replace_range(text: str, start: str, end: str, replacement: str) -> str:
    s = text.find(start)
    e = text.find(end, s + len(start))
    if s < 0 or e < 0:
        raise ValueError(f"cannot replace range {start!r} -> {end!r}")
    return text[:s] + replacement.rstrip() + "\n\n" + text[e:]


def insert_once(text: str, anchor: str, block: str, marker: str) -> str:
    if marker in text:
        return text
    pos = text.find(anchor)
    if pos < 0:
        raise ValueError(f"missing insertion anchor: {anchor}")
    wrapped = f"<!-- [{marker}] BEGIN -->\n{block.strip()}\n<!-- [{marker}] END -->\n\n"
    return text[:pos] + wrapped + text[pos:]


def replace_reviewed_chapter(text: str, start: str, end: str, draft: str) -> str:
    old = section(text, start, end)
    body = preserve_missing_specials(old, strip_first_heading(draft))
    return replace_range(text, start, end, start + "\n\n" + body)


def materialize(baseline: str, run47: str, overlay: str, run51_ch4: str, run51_ch8: str) -> str:
    # RUN47: reviewed rewrites for the VOC and British chapters.
    a06, a07b = extract_run47(run47)
    old_ch9 = section(baseline, CH9, CH10)
    old_ch10 = section(baseline, CH10, EPILOGUE)
    chapter9 = CH9 + "\n\n" + preserve_missing_specials(old_ch9, a06)
    chapter10 = CH10 + "\n\n" + preserve_missing_specials(old_ch10, a07b)
    out = replace_range(baseline, CH9, CH10, chapter9)
    out = replace_range(out, CH10, EPILOGUE, chapter10)

    # RUN50: bounded A02/A03 insertions.
    a02 = extract_overlay(overlay, "OVERLAY_A02")
    a03 = extract_overlay(overlay, "OVERLAY_A03")
    out = insert_once(out, A02_INSERT_BEFORE, a02, "RUN50:A02-A03-MARITIME")
    out = insert_once(out, A03_INSERT_BEFORE, a03, "RUN50:GOKANNA-POLONNARUWA")

    # RUN51: problem-first rewrites for Polonnaruwa's apogee and Portugal/Kandy.
    out = replace_reviewed_chapter(out, CH4, CH5, run51_ch4)
    out = replace_reviewed_chapter(out, CH8, CH9, run51_ch8)

    # Hard guards against accidental content loss, duplicate chapter materialization,
    # and fallback to the former thematic-list openings.
    for anchor in (CH4, CH5, CH8, CH9, CH10, EPILOGUE):
        if out.count(anchor) != 1:
            raise RuntimeError(f"chapter-boundary integrity check failed: {anchor}")
    if out.count("[RUN50:A02-A03-MARITIME] BEGIN") != 1:
        raise RuntimeError("A02 overlay count failed")
    if out.count("[RUN50:GOKANNA-POLONNARUWA] BEGIN") != 1:
        raise RuntimeError("A03 overlay count failed")
    if out.count("Comment une monarchie restaurée transforme-t-elle eau, fiscalité, Saṅgha") != 1:
        raise RuntimeError("RUN51 Polonnaruwa signature missing or duplicated")
    if out.count("Comment le Portugal convertit-il supériorité navale, ports, alliances dynastiques") != 1:
        raise RuntimeError("RUN51 Portugal signature missing or duplicated")
    if "## **Apogée : eau, Saṅgha, légitimité, savoir et projection**" in section(out, CH4, CH5):
        raise RuntimeError("legacy Polonnaruwa thematic opening survived chapter replacement")
    if len(out) < len(baseline) * 0.80:
        raise RuntimeError("retention guard failed: candidate unexpectedly short")
    return out.rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, default=BASELINE)
    parser.add_argument("--run47", type=Path, default=RUN47)
    parser.add_argument("--overlay", type=Path, default=RUN50_OVERLAY)
    parser.add_argument("--run51-ch4", type=Path, default=RUN51_CH4)
    parser.add_argument("--run51-ch8", type=Path, default=RUN51_CH8)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--check", action="store_true", help="validate an existing output instead of writing it")
    args = parser.parse_args()

    expected = materialize(
        args.baseline.read_text(encoding="utf-8"),
        args.run47.read_text(encoding="utf-8"),
        args.overlay.read_text(encoding="utf-8"),
        args.run51_ch4.read_text(encoding="utf-8"),
        args.run51_ch8.read_text(encoding="utf-8"),
    )
    if args.check:
        if not args.output.exists():
            raise SystemExit(f"missing materialized output: {args.output}")
        actual = args.output.read_text(encoding="utf-8")
        if actual != expected:
            raise SystemExit(f"stale materialized output: {args.output}")
        print(f"OK {args.output}")
        return
    args.output.write_text(expected, encoding="utf-8")
    print(f"wrote {args.output} ({len(expected)} chars)")


if __name__ == "__main__":
    main()
