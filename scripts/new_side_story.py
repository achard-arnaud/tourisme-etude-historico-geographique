#!/usr/bin/env python3
"""Create a versioned candidate side-story composition artifact."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from side_story_contract import KINDS, RENDER_LABELS, SCHEMA_VERSION, canonical_marker, side_story_dir


def csv_items(value: str | None) -> list[str]:
    return [item.strip() for item in (value or "").split(",") if item.strip()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--id", required=True)
    parser.add_argument("--kind", required=True, choices=sorted(KINDS))
    parser.add_argument("--arc", required=True)
    parser.add_argument("--title", required=True)
    parser.add_argument("--section-anchor", required=True)
    parser.add_argument("--return-to", required=True)
    parser.add_argument("--purpose", required=True)
    parser.add_argument("--claim-ids")
    parser.add_argument("--source-ids")
    parser.add_argument("--bridge-ids")
    parser.add_argument("--hil-ids")
    parser.add_argument("--drift-paths")
    parser.add_argument("--origin-paths")
    parser.add_argument("--related-arcs")
    parser.add_argument("--reader-presets", default="advanced")
    parser.add_argument("--reason-off-trunk", default="Candidate pending editorial validation.")
    parser.add_argument("--payoff", default="Pending editorial payoff.")
    parser.add_argument("--takeaway", default="Pending narrative takeaway.")
    parser.add_argument("--required-in-reader", action="store_true")
    parser.add_argument("--zoom-from")
    parser.add_argument("--zoom-to")
    parser.add_argument("--zoom-return-to")
    parser.add_argument("--zoom-mechanism")
    parser.add_argument("--zoom-local-payoff")
    args = parser.parse_args()

    if args.kind == "dezoom":
        required = {
            "--zoom-from": args.zoom_from,
            "--zoom-to": args.zoom_to,
            "--zoom-return-to": args.zoom_return_to,
            "--zoom-mechanism": args.zoom_mechanism,
            "--zoom-local-payoff": args.zoom_local_payoff,
        }
        missing = [name for name, value in required.items() if not value]
        if missing:
            parser.error(f"dezoom requires {', '.join(missing)}")

    project = Path(args.project)
    output_dir = side_story_dir(project)
    output_dir.mkdir(parents=True, exist_ok=True)
    output = output_dir / f"{args.id}.json"
    if output.exists():
        parser.error(f"side story already exists: {output}")

    item = {
        "schema_version": SCHEMA_VERSION,
        "class": "side_story",
        "id": args.id,
        "kind": args.kind,
        "status": "candidate",
        "title": args.title,
        "arc": args.arc,
        "related_arcs": csv_items(args.related_arcs),
        "purpose": args.purpose,
        "reason_off_trunk": args.reason_off_trunk,
        "payoff": args.payoff,
        "reader_presets": csv_items(args.reader_presets),
        "lineage": {
            "claim_ids": csv_items(args.claim_ids),
            "source_ids": csv_items(args.source_ids),
            "bridge_ids": csv_items(args.bridge_ids),
            "hil_ids": csv_items(args.hil_ids),
            "drift_paths": csv_items(args.drift_paths),
            "origin_paths": csv_items(args.origin_paths),
        },
        "placement": {
            "section_anchor": args.section_anchor,
            "return_to": args.return_to,
        },
        "zoom_excursion": (
            {
                "from": args.zoom_from,
                "to": args.zoom_to,
                "return_to": args.zoom_return_to,
                "mechanism": args.zoom_mechanism,
                "local_payoff": args.zoom_local_payoff,
            }
            if args.kind == "dezoom"
            else None
        ),
        "content": {"takeaway": args.takeaway},
        "render": {
            "label": RENDER_LABELS[args.kind],
            "marker": canonical_marker(args.id),
            "required_in_reader": bool(args.required_in_reader),
        },
    }
    output.write_text(json.dumps(item, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
