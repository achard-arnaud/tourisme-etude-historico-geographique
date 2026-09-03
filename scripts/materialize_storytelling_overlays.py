#!/usr/bin/env python3
"""Materialize reviewed storytelling overlays onto the current pre-1948 reader Markdown.

Proof and composition stay separate. The script consumes the already-rendered V3
Markdown plus reviewed RUN47/RUN50/RUN51/RUN52/RUN53 narrative material and
produces a candidate full Markdown reader. It does not alter claims, confidence,
source registers, or the archived V1 baseline.
"""
from __future__ import annotations

import argparse
import json
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
RUN52_CH5 = OUTPUT / "run52_storytelling_ch5_fall_polonnaruwa.md"
RUN52_CH6 = OUTPUT / "run52_storytelling_ch6_mobile_capitals.md"
RUN53_OVERLAY = OUTPUT / "run53_transversal_reader_overlay.md"
DEFAULT_OUT = OUTPUT / "report_v4_full.md"

CH4 = "**Chapitre 4 — Polonnaruwa à l’apogée : eau, Saṅgha, souveraineté et projection régionale**"
CH5 = "**Chapitre 5 — La chute de Polonnaruwa : violence, fragmentation et changement d’optimum**"
CH6 = "**Chapitre 6 — Dambadeniya, Yapahuwa, Kurunegala, Gampola et Kotte : déplacer la souveraineté**"
CH7 = "**Chapitre 7 — Le royaume de Jaffna : un autre modèle sri-lankais**"
CH8 = "**Chapitre 8 — Kandy face aux Portugais : la côte ne suffit pas à conquérir l’île**"
CH9 = "**Chapitre 9 — Kandy face à la VOC : de l’alliance à l’encerclement**"
CH10 = "**Chapitre 10 — Ceylan britannique : conquérir l’intérieur et reconnecter l’île au marché mondial**"
EPILOGUE = "# **Épilogue — ce que la longue durée fait apparaître**"
A02_INSERT_BEFORE = "## **VI. VIIe–Xe siècles — Islam, Tamilakam et militarisation des réseaux**"
A03_INSERT_BEFORE = "### **3. Rohana/Mahagama : le « hedge » territorial de la monarchie**"
TRACE_APPENDIX = "# **Annexe technique — récaps causaux de traçabilité**"
STORY_DISPOSITIONS = OUTPUT / "story_dispositions.json"

SPECIAL_BLOCK = re.compile(
    r"(?ms)<!-- \[(?P<kind>SIDE-STORY|ARC-RECAP):(?P<id>[^\]]+)\].*?(?:<!-- \[/ARC-RECAP:[^\]]+\] -->|<!-- \[SIDE-STORY:[^\]]+\] END -->|(?=\n## |\n\*\*Chapitre |\Z))"
)
ARC_RECAP_BLOCK = re.compile(
    r"(?ms)<!-- \[ARC-RECAP:(?P<id>[^\]]+)\] -->.*?<!-- \[/ARC-RECAP:(?P=id)\] -->"
)

VALID_LEGACY_DISPOSITIONS = {
    "absorbed_into_core",
    "retained_in_replacement",
    "moved_to_traceability_appendix",
}


def load_story_dispositions(path: Path = STORY_DISPOSITIONS) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = data.get("decisions") if isinstance(data, dict) else None
    if not isinstance(rows, list):
        raise ValueError(f"invalid story disposition ledger: {path}")
    seen: set[tuple[str, str]] = set()
    for row in rows:
        key = (str(row.get("object_type") or ""), str(row.get("id") or ""))
        if not all(key) or key in seen:
            raise ValueError(f"invalid or duplicate story disposition: {key}")
        seen.add(key)
        if row.get("disposition") not in VALID_LEGACY_DISPOSITIONS:
            raise ValueError(f"invalid disposition for {key}: {row.get('disposition')}")
        if not row.get("source_chapter") or not str(row.get("reason") or "").strip():
            raise ValueError(f"incomplete story disposition: {key}")
    return rows


def legacy_skip_keys(chapter: str, rows: list[dict] | None = None) -> set[str]:
    records = load_story_dispositions() if rows is None else rows
    prefixes = {"side_story": "SIDE-STORY", "arc_recap": "ARC-RECAP"}
    return {
        f"{prefixes[row['object_type']]}:{row['id']}"
        for row in records
        if row.get("source_chapter") == chapter
    }


# RUN53 decisions are now machine-readable rather than duplicated as Python-only
# knowledge. The materializer still preserves every object according to its
# explicit destination; these sets only suppress stale copies from old chapters.
CH8_ABSORBED = legacy_skip_keys("ch8")
CH9_ABSORBED = legacy_skip_keys("ch9")


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


def arc_recap_blocks(text: str) -> dict[str, str]:
    return {
        match.group("id"): match.group(0).strip()
        for match in ARC_RECAP_BLOCK.finditer(text)
    }


def preserve_missing_specials(
    old: str,
    replacement: str,
    *,
    skip_keys: set[str] | None = None,
) -> str:
    old_blocks = special_blocks(old)
    if not old_blocks:
        return replacement.rstrip()
    skipped = skip_keys or set()
    missing = [
        block
        for key, block in old_blocks.items()
        if key not in replacement and key not in skipped
    ]
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


def replace_reviewed_chapter(
    text: str,
    start: str,
    end: str,
    draft: str,
    *,
    skip_keys: set[str] | None = None,
) -> str:
    old = section(text, start, end)
    body = preserve_missing_specials(old, strip_first_heading(draft), skip_keys=skip_keys)
    return replace_range(text, start, end, start + "\n\n" + body)


def append_traceability_recaps(text: str, recaps: dict[str, str]) -> str:
    wanted = ["RECAP-A06", "RECAP-A07", "RECAP-A08"]
    missing = [rid for rid in wanted if rid not in recaps]
    if missing:
        raise RuntimeError(f"missing legacy recaps for traceability appendix: {missing}")
    body = "\n\n".join(recaps[rid] for rid in wanted)
    return text.rstrip() + "\n\n" + TRACE_APPENDIX + "\n\n" + body + "\n"


def materialize(
    baseline: str,
    run47: str,
    overlay: str,
    run51_ch4: str,
    run51_ch8: str,
    run52_ch5: str,
    run52_ch6: str,
    run53_overlay: str,
) -> str:
    # RUN47: reviewed rewrites for the VOC and British chapters. RUN53 prevents
    # malformed legacy side-story tails from being blindly appended after the new
    # VOC conclusion; their disposition is explicit in RUN53_TRANSVERSAL_READER_AUDIT.md.
    a06, a07b = extract_run47(run47)
    old_ch9 = section(baseline, CH9, CH10)
    old_ch10 = section(baseline, CH10, EPILOGUE)
    legacy_recaps = arc_recap_blocks(old_ch9)
    chapter9 = CH9 + "\n\n" + preserve_missing_specials(
        old_ch9, a06, skip_keys=CH9_ABSORBED
    )
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
    out = replace_reviewed_chapter(out, CH8, CH9, run51_ch8, skip_keys=CH8_ABSORBED)

    # RUN52: only chapters that failed the form-global audit are replaced.
    # Chapters 1-3 and 7 are deliberately preserved from the baseline because their
    # chronology already serves a coherent causal question rather than a topic list.
    out = replace_reviewed_chapter(out, CH5, CH6, run52_ch5)
    out = replace_reviewed_chapter(out, CH6, CH7, run52_ch6)

    # RUN53/RUN54: transversal handoffs. They are anchored to the real chapter
    # headings, not to PARTIE labels, because the latter also occur in the table of
    # contents. This keeps narrative prose out of the sommaire.
    trans34 = extract_overlay(run53_overlay, "TRANSITION_CH3_CH4")
    trans78 = extract_overlay(run53_overlay, "TRANSITION_CH7_CH8")
    out = insert_once(out, CH4, trans34, "RUN53:TRANSITION-CH3-CH4")
    out = insert_once(out, CH8, trans78, "RUN53:TRANSITION-CH7-CH8")

    # Arc recaps remain available for audit/traceability, but no longer interrupt
    # the narrative conclusion of the VOC chapter.
    out = append_traceability_recaps(out, legacy_recaps)

    # Hard guards against accidental content loss, duplicate materialization,
    # silent side-story loss, and fallback to former dossier-style openings.
    for anchor in (CH4, CH5, CH6, CH7, CH8, CH9, CH10, EPILOGUE):
        if out.count(anchor) != 1:
            raise RuntimeError(f"chapter-boundary integrity check failed: {anchor}")
    if out.count("[RUN50:A02-A03-MARITIME] BEGIN") != 1:
        raise RuntimeError("A02 overlay count failed")
    if out.count("[RUN50:GOKANNA-POLONNARUWA] BEGIN") != 1:
        raise RuntimeError("A03 overlay count failed")
    if out.count("[RUN53:TRANSITION-CH3-CH4] BEGIN") != 1:
        raise RuntimeError("RUN53 chapter 3->4 transition missing or duplicated")
    if out.count("[RUN53:TRANSITION-CH7-CH8] BEGIN") != 1:
        raise RuntimeError("RUN53 chapter 7->8 transition missing or duplicated")
    toc_start = out.find("# **Sommaire**")
    body_start = out.find("**Chapitre 1 — Rāmāyaṇa, origines et protohistoire**")
    if toc_start < 0 or body_start < 0 or body_start <= toc_start:
        raise RuntimeError("cannot resolve reader table-of-contents boundary")
    toc = out[toc_start:body_start]
    if "RUN53:TRANSITION-" in toc:
        raise RuntimeError("transversal narrative handoff leaked into table of contents")
    if out.count("Comment une monarchie restaurée transforme-t-elle eau, fiscalité, Saṅgha") != 1:
        raise RuntimeError("RUN51 Polonnaruwa signature missing or duplicated")
    if out.count("Comment le Portugal convertit-il supériorité navale, ports, alliances dynastiques") != 1:
        raise RuntimeError("RUN51 Portugal signature missing or duplicated")
    if out.count("Pourquoi un système aussi intégré et productif que Polonnaruwa devient-il") != 1:
        raise RuntimeError("RUN52 chapter 5 signature missing or duplicated")
    if out.count("Comment la disparition de l’optimum de Rajarata transforme-t-elle la souveraineté sri-lankaise") != 1:
        raise RuntimeError("RUN52 chapter 6 signature missing or duplicated")
    if "## **Apogée : eau, Saṅgha, légitimité, savoir et projection**" in section(out, CH4, CH5):
        raise RuntimeError("legacy Polonnaruwa thematic opening survived chapter replacement")
    if "## **Pourquoi le système Polonnaruwa cesse d’être optimal**" in section(out, CH5, CH6):
        raise RuntimeError("legacy chapter 5 dossier opening survived chapter replacement")
    if "## **Des capitales fortifiées aux économies portuaires, puis à Kandy**" in section(out, CH6, CH7):
        raise RuntimeError("legacy chapter 6 dossier opening survived chapter replacement")

    ch8 = section(out, CH8, CH9)
    ch9 = section(out, CH9, CH10)
    if "SIDE-STORY:SS-PRE-004" in ch8:
        raise RuntimeError("absorbed Mannar legacy side story still rendered after RUN51 core")
    for legacy_id in ("SS-PRE-003", "SS-PRE-001", "SS-PRE-002"):
        if legacy_id in ch9:
            raise RuntimeError(f"absorbed legacy side story still rendered in chapter 9: {legacy_id}")
    if ch9.count("[SIDE-STORY:SS-R23-KDY-SIAM-DEZOOM-001] BEGIN") != 1:
        raise RuntimeError("Siam dezoom must render exactly once in chapter 9")
    if "ARC-RECAP:" in ch9:
        raise RuntimeError("technical arc recaps must not interrupt chapter 9 narrative")
    appendix = section(out, TRACE_APPENDIX)
    for recap_id in ("RECAP-A06", "RECAP-A07", "RECAP-A08"):
        if appendix.count(f"[ARC-RECAP:{recap_id}]") != 1:
            raise RuntimeError(f"traceability recap missing or duplicated: {recap_id}")
    if len(out) < len(baseline) * 0.75:
        raise RuntimeError("retention guard failed: candidate unexpectedly short")
    return out.rstrip() + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--baseline", type=Path, default=BASELINE)
    parser.add_argument("--run47", type=Path, default=RUN47)
    parser.add_argument("--overlay", type=Path, default=RUN50_OVERLAY)
    parser.add_argument("--run51-ch4", type=Path, default=RUN51_CH4)
    parser.add_argument("--run51-ch8", type=Path, default=RUN51_CH8)
    parser.add_argument("--run52-ch5", type=Path, default=RUN52_CH5)
    parser.add_argument("--run52-ch6", type=Path, default=RUN52_CH6)
    parser.add_argument("--run53-overlay", type=Path, default=RUN53_OVERLAY)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUT)
    parser.add_argument("--check", action="store_true", help="validate an existing output instead of writing it")
    args = parser.parse_args()

    expected = materialize(
        args.baseline.read_text(encoding="utf-8"),
        args.run47.read_text(encoding="utf-8"),
        args.overlay.read_text(encoding="utf-8"),
        args.run51_ch4.read_text(encoding="utf-8"),
        args.run51_ch8.read_text(encoding="utf-8"),
        args.run52_ch5.read_text(encoding="utf-8"),
        args.run52_ch6.read_text(encoding="utf-8"),
        args.run53_overlay.read_text(encoding="utf-8"),
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
