#!/usr/bin/env python3
"""Deterministically materialize structured arc recaps at declared arc-end anchors."""
from __future__ import annotations
import argparse
import re
from pathlib import Path
from arc_recap_contract import RENDERABLE, load_arc_recaps, render_arc_recap_markdown
from output_state import canonical_markdown_path


def _norm(text: str) -> str:
    return re.sub(r"[*_`]", "", text).strip().casefold()


def _remove_existing(text: str, recap_id: str) -> str:
    pattern = re.compile(rf"\n?<!-- \[ARC-RECAP:{re.escape(recap_id)}\] -->.*?<!-- \[/ARC-RECAP:{re.escape(recap_id)}\] -->\n?", re.S)
    return pattern.sub("\n", text)


def materialize_arc_recaps(project: Path, markdown: str) -> tuple[str, int]:
    """Return Markdown with each validated/promoted required recap inserted exactly once."""
    items = [item for _, item in load_arc_recaps(project) if item.get("status") in RENDERABLE and (item.get("render") or {}).get("required_in_reader")]
    for item in items:
        markdown = _remove_existing(markdown, item["id"])
    grouped: dict[str, list[dict]] = {}
    for item in items:
        anchor = (item.get("placement") or {}).get("before_anchor")
        if not anchor:
            raise RuntimeError(f"arc recap {item.get('id')}: missing placement.before_anchor")
        grouped.setdefault(anchor, []).append(item)
    for anchor, recaps in grouped.items():
        lines = markdown.splitlines()
        needle = _norm(anchor)
        index = next((i for i, line in enumerate(lines) if needle in _norm(line).lstrip("# ")), None)
        if index is None:
            raise RuntimeError(f"arc recap placement anchor not found: {anchor}")
        block = "\n\n".join(render_arc_recap_markdown(item) for item in sorted(recaps, key=lambda row: row.get("id", "")))
        lines[index:index] = [block, ""]
        markdown = "\n".join(lines)
    return markdown.rstrip() + "\n", len(items)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--source")
    parser.add_argument("--output")
    parser.add_argument("--check", action="store_true", help="dry-run: resolve all placements without writing")
    args = parser.parse_args()
    project = Path(args.project)
    source = Path(args.source) if args.source else canonical_markdown_path(project)
    text = source.read_text(encoding="utf-8")
    rendered, count = materialize_arc_recaps(project, text)
    if not args.check:
        output = Path(args.output) if args.output else source
        output.write_text(rendered, encoding="utf-8")
    print(f"ARC RECAP MATERIALIZATION OK: {count} recaps, source={source.name}, mode={'check' if args.check else 'write'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
