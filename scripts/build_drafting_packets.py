#!/usr/bin/env python3
"""Shared drafting packet entry point.

For now this wraps the existing from-scratch packet builder and applies the bounded
legacy-fragment migration overlay. The same overlay is intended for iterative and
from-scratch composition so legacy debt is handled once, not by each writer.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path

from build_from_scratch_packets import (
    REPO,
    ReadLedger,
    build_packets as build_from_scratch_packets,
    fragment_index,
    fragment_refs,
    load_records,
)
from legacy_fragment_bypass import virtual_legacy_statements


def _all_claims(project: Path, ledger: ReadLedger) -> list[dict]:
    return load_records(ledger, project.glob("01_arcs/*/claims/*.json"))


def apply_legacy_overlay(project: Path, output: Path, manifest: dict) -> dict:
    ledger = ReadLedger(project)
    fragments = fragment_index(project, ledger)
    claims = _all_claims(project, ledger)
    claim_ids = {str(c.get("id")) for c in claims if c.get("id")}
    claimed_fragment_ids: set[str] = set()
    for claim in claims:
        claimed_fragment_ids |= fragment_refs(claim)

    virtuals = virtual_legacy_statements(project, fragments, claimed_fragment_ids, claim_ids)
    by_arc: dict[str, list[dict]] = defaultdict(list)
    for item in virtuals:
        by_arc[str(item["arc"])].append(item)

    arc_summaries = {str(row.get("arc")): row for row in manifest.get("arc_summaries") or []}
    for packet_name in manifest.get("packet_paths") or []:
        path = output / packet_name
        packet = json.loads(path.read_text(encoding="utf-8"))
        arc = str(packet.get("arc") or "")
        items = by_arc.get(arc, [])
        if not items:
            packet.setdefault("counts", {})["legacy_virtual_claims"] = 0
            packet.setdefault("drafting_contract", {})["legacy_fragment_bypass"] = {
                "enabled": True,
                "virtual_only": True,
                "may_establish_new_fact_without_source": False,
            }
            path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            continue

        counts = packet.setdefault("counts", {})
        counts["persisted_claims"] = counts.get("claims", len(packet.get("claims") or []))
        packet.setdefault("claims", []).extend(items)
        counts["legacy_virtual_claims"] = len(items)
        counts["claims"] = len(packet["claims"])
        packet["legacy_fragments"] = items
        packet.setdefault("drafting_contract", {})["legacy_fragment_bypass"] = {
            "enabled": True,
            "virtual_only": True,
            "statement_type": "legacy_fragment",
            "may_preserve_existing_narrative": True,
            "may_establish_new_fact_without_source": False,
            "may_satisfy_sourcing_gate": False,
            "render_type_in_reader": False,
        }

        present_fragment_ids = {
            str(x.get("id")) for x in packet.get("fragments") or [] if isinstance(x, dict) and x.get("id")
        }
        for item in items:
            fid = str((item.get("origin_fragment_ids") or [""])[0])
            if fid and fid in fragments and fid not in present_fragment_ids:
                clean = {k: v for k, v in fragments[fid].items() if k != "_capture_path"}
                packet.setdefault("fragments", []).append(clean)
                present_fragment_ids.add(fid)
        counts["fragments"] = len(packet.get("fragments") or [])
        path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

        summary = arc_summaries.get(arc)
        if summary is not None:
            summary["persisted_claims"] = summary.get("claims", 0)
            summary["legacy_virtual_claims"] = len(items)
            summary["claims"] = summary.get("claims", 0) + len(items)

    manifest["class"] = "drafting_packet_manifest"
    manifest["legacy_fragment_bypass"] = {
        "enabled": True,
        "virtual_claim_count": len(virtuals),
        "virtual_claim_ids": [x["id"] for x in virtuals],
        "policy": "allowlisted unsourced legacy debt only; no evidentiary upgrade",
    }
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def build_packets(project: Path, output: Path) -> dict:
    project = project.resolve()
    manifest = build_from_scratch_packets(project, output)
    return apply_legacy_overlay(project, output, manifest)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    project = Path(args.project)
    project = project if project.is_absolute() else REPO / project
    output = Path(args.output) if args.output else project / "09_output" / "drafting_packets"
    output = output if output.is_absolute() else REPO / output
    manifest = build_packets(project, output)
    print(json.dumps({
        "project": manifest["project"],
        "arcs": len(manifest.get("packet_paths") or []),
        "legacy_virtual_claims": manifest["legacy_fragment_bypass"]["virtual_claim_count"],
        "reader_prose_loaded": manifest["contamination_check"]["reader_prose_loaded"],
        "output": str(output.relative_to(REPO)),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
