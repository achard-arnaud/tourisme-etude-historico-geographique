#!/usr/bin/env python3
"""Materialize reviewed storytelling overlays onto the current pre-1948 reader Markdown.

RUN50 deliberately keeps proof and composition separate. The script consumes the
already-rendered V3 Markdown plus reviewed RUN47/RUN49 narrative overlays and
produces a candidate full Markdown reader. It does not alter claim confidence,
source registers, or the archived V1 baseline.
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
DEFAULT_OUT = OUTPUT / "report_v4_full.md"

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


def materialize(baseline: str, run47: str, overlay: str) -> str:
    a06, a07b = extract_run47(run47)

    old_ch9 = section(baseline, CH9, CH10)
    old_ch10 = section(baseline, CH10, EPILOGUE)

    new_ch9_body = preserve_missing_specials(old_ch9, a06)
    new_ch10_body = preserve_missing_specials(old_ch10, a07b)

    chapter9 = CH9 + "\n\n" + new_ch9_body
    chapter10 = CH10 + "\n\n" + new_ch10_body

    out = replace_range(baseline, CH9, CH10, chapter9)
    out = replace_range(out, CH10, EPILOGUE, chapter10)

    a02 = extract_overlay(overlay, "OVERLAY_A02")
    a03 = extract_overlay(overlay, "OVERLAY_A03")
    out = insert_once(out, A02_INSERT_BEFORE, a02, "RUN50:A02-A03-MARITIME")
    out = insert_once(out, A03_INSERT_BEFORE, a03, "RUN50:GOKANNA-POLONNARUWA")

    # Hard guards against accidental content loss / duplicate materialization.
    if out.count(CH9) != 1 or out.count(CH10) != 1 or out.count(EPILOGUE) != 1:
        raise RuntimeError("chapter-boundary integrity check failed")
    if out.count("[RUN50:A02-A03-MARITIME] BEGIN") != 1:
        raise RuntimeError("A02 overlay count failed")
    if out.count("[RUN50:GOKANNA-POLONNARUWA] BEGIN") != 1:
        raise RuntimeError("A03 overlay count failed")
    if len(out) < len(baseline) * 0.80:
        raise RuntimeError("retention guard failed: candidate unexpectedly short")
    return out.rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, default=BASELINE)
    parser.add_argument("--run47", type=Path, default=RUN47)
    parser.add_argument("--overlay", type=Path, default=RUN50_OVERLAY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--check", action="store_true", help="validate an existing output instead of writing it")
    args = parser.parse_args()

    expected = materialize(
        args.baseline.read_text(encoding="utf-8"),
        args.run47.read_text(encoding="utf-8"),
        args.overlay.read_text(encoding="utf-8"),
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
