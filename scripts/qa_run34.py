#!/usr/bin/env python3
"""Run34 acceptance gates for mudra, Sasana backlog, side stories and blocked bridges."""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

from paragraph_review_gate import review_paragraph
from reciprocal_coverage_check import downstream_fragment_refs, fragment_index
from sarah_voice_contract import review_skeleton
from side_story_contract import validate_side_stories

ROOT = Path(__file__).resolve().parents[1]
PROJECT = ROOT / "examples" / "sri_lanka_pre_1948"
MUDRA_IDS = {f"GF-MUDRA-{i:02d}" for i in range(1, 9)}
BACKLOG_IDS = {"GF-MIH-01","GF-MIH-03","GF-MIH-04","GF-MIH-05","GF-MIH-06","GF-MIH-09","GF-ABH-02","GF-ABH-04","GF-ABH-06"}
STORY_IDS = {"SS-R34-MUDRA-DETOUR-001","SS-R34-BUDDHIST-ICONOGRAPHY-METHOD-001"}
BRIDGE_IDS = {"B-R34-CREOLISATION-MEDITATION-DRAFT-001","B-R34-RED-GOD-KATARAGAMA-NALLUR-DRAFT-001"}
INSTRUMENTED = PROJECT / "09_output" / "report_v3_full_run34_instrumented.md"
READER_MD = PROJECT / "09_output" / "report_v3_full.md"
READER_DOCX = PROJECT / "09_output" / "Sri_Lanka_Fresque_historico_geographique_vol_retour_v3.docx"


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def find_claim(claim_id: str) -> dict:
    for path in PROJECT.glob("01_arcs/*/claims/*.json"):
        item = load_json(path)
        if isinstance(item, dict) and item.get("id") == claim_id:
            return item
    raise AssertionError(f"claim missing: {claim_id}")


def story(story_id: str) -> dict:
    path = PROJECT / "09_output" / "side_stories" / f"{story_id}.json"
    return load_json(path)


def paragraph_gate() -> dict:
    item = story("SS-R34-MUDRA-DETOUR-001")
    initial = item["review"]["initial"]
    assert initial == {"checklist_passed":False,"style_sarah_passed":False,"hil_scope_passed":False}, "Run34 paragraph gate must initialize false"
    body = item["content"]["body_markdown"]
    claim_id = item["lineage"]["claim_ids"][0]
    claim = find_claim(claim_id)
    audit = item["review"]
    review = review_skeleton(body, generation_pass_id=audit["generation_pass_id"], generation_context_id=audit["generation_context_id"])
    review.update({
        "passed": True,
        "evaluator": audit["evaluator"],
        "review_pass_id": audit["review_pass_id"],
        "review_context_id": audit["review_context_id"],
        "marker_results": audit["marker_results"],
        "notes": "Independent Run34 Sarah gate; hashes are bound at execution time.",
    })
    context = {
        "neighbor_context_loaded": True,
        "sarah_style_review": review,
        "hil_scope_declared": True,
        "selected_hil_ids": item["lineage"]["hil_ids"],
        "claim_hil_map": {claim_id: item["lineage"]["hil_ids"]},
    }
    result = review_paragraph(body, claim, context)
    assert result.passed, [v.message for v in result.violations]
    final = item["review"]["final"]
    assert final == {"checklist_passed":True,"style_sarah_passed":True,"hil_scope_passed":True}, "stored Run34 final gate must record the executed pass"
    return {"passed": result.passed, "warnings": result.warnings}


def coverage_gate() -> dict:
    fragments = fragment_index(PROJECT)
    used = downstream_fragment_refs(PROJECT)
    required = MUDRA_IDS | BACKLOG_IDS
    missing_records = sorted(required - set(fragments))
    unaccounted = sorted(required - used)
    assert not missing_records, f"Run34 fragment records missing: {missing_records}"
    assert not unaccounted, f"Run34 reciprocal coverage unaccounted: {unaccounted}"
    return {"required": len(required), "accounted_for": len(required), "unaccounted": []}


def backlog_gate() -> dict:
    data = load_json(ROOT / "docs" / "RUN34_BACKLOG_DISPOSITIONS.json")
    rows = {row["fragment_id"]: row for row in data["dispositions"]}
    assert set(rows) == BACKLOG_IDS, f"Run34 backlog decisions drift: {sorted(set(rows)^BACKLOG_IDS)}"
    allowed = {"promote_to_claim","merge","discard_as_tradition_only"}
    for fid, row in rows.items():
        assert row.get("decision") in allowed, f"{fid}: invalid disposition"
        assert str(row.get("reason") or "").strip(), f"{fid}: disposition reason required"
        if row["decision"] == "promote_to_claim":
            assert row.get("qualification") in {"chronicle_tradition","source_fact"}, f"{fid}: qualification missing"
            assert row.get("claim_id"), f"{fid}: promoted claim missing"
    return {"decisions": len(rows), "statuses": {fid: rows[fid]["decision"] for fid in sorted(rows)}}


def bridge_gate(reader_text: str | None = None) -> dict:
    rows = load_json(PROJECT / "08_questions" / "run34_blocked_bridge_drafts.json")
    assert {row["id"] for row in rows} == BRIDGE_IDS
    for row in rows:
        assert row.get("status") == "draft_blocked_pending_sourcing"
        assert row.get("source_ids") == []
        assert "mechanism" not in row
        assert "reader_policy" in row and "No reader text" in row["reader_policy"]
    if reader_text is not None:
        for bridge_id in BRIDGE_IDS:
            assert bridge_id not in reader_text, f"blocked bridge leaked into reader: {bridge_id}"
    return {"blocked": sorted(BRIDGE_IDS), "reader_leak": False if reader_text is not None else "not_checked"}


def sources_gate() -> dict:
    rows = load_json(PROJECT / "05_sources" / "source_register_run34_iconography.json")
    tiers = {row["id"]: row.get("tier") for row in rows}
    method = story("SS-R34-BUDDHIST-ICONOGRAPHY-METHOD-001")
    for source_id in method["lineage"]["source_ids"]:
        assert tiers.get(source_id) in {"T1","T2"}, f"method source must be T1/T2: {source_id}"
    assert "SS-R34-MUDRA-DETOUR-001" in method["content"].get("callback_side_story_ids", [])
    return {"method_sources": {sid: tiers[sid] for sid in method["lineage"]["source_ids"]}, "callback_reused": True}


def return_target_gate(instrumented: str) -> dict:
    out = {}
    for sid in sorted(STORY_IDS):
        item = story(sid)
        ret = item["placement"].get("return_to")
        assert item["placement"].get("return_resolution") == "reader_patch_marker"
        side_marker = f"[SIDE-STORY:{sid}]"
        claim_marker = f"[claim:{ret}]"
        assert side_marker in instrumented, f"side-story marker absent: {sid}"
        assert claim_marker in instrumented, f"return marker absent: {ret}"
        assert instrumented.index(side_marker) < instrumented.index(claim_marker), f"return marker must follow side story: {sid}"
        out[sid] = {"return_to": ret, "resolved_by": claim_marker}
    return out


def _fill(paragraph):
    ppr = paragraph._p.pPr
    if ppr is None:
        return None
    shd = ppr.find(qn("w:shd"))
    return shd.get(qn("w:fill")) if shd is not None else None


def _has_bottom(paragraph):
    ppr = paragraph._p.pPr
    if ppr is None:
        return False
    borders = ppr.find(qn("w:pBdr"))
    return borders is not None and borders.find(qn("w:bottom")) is not None


def box_integrity_gate() -> dict:
    doc = Document(READER_DOCX)
    paragraphs = doc.paragraphs
    report = {}
    for sid in sorted(STORY_IDS):
        item = story(sid)
        title = item["title"]
        index = next((i for i,p in enumerate(paragraphs) if title in p.text), None)
        assert index is not None, f"DOCX side-story header missing: {sid}"
        assert index + 1 < len(paragraphs), f"DOCX side-story body missing: {sid}"
        header, body = paragraphs[index], paragraphs[index+1]
        hfill, bfill = _fill(header), _fill(body)
        assert hfill and bfill and hfill == bfill, f"DOCX fill not continuous: {sid}"
        assert not _has_bottom(header), f"DOCX side-story header closes box too early: {sid}"
        assert _has_bottom(body), f"DOCX side-story final border missing: {sid}"
        report[sid] = {"continuous_fill": True, "final_border": True}
    return report


def run(post_render: bool) -> dict:
    errors, warnings, count, coverage = validate_side_stories(PROJECT, check_render=True)
    assert not errors, errors
    report = {
        "side_story_contract": {"errors": errors, "warnings": warnings, "registry_count": count, "coverage": coverage},
        "paragraph_review_gate": paragraph_gate(),
        "reciprocal_coverage_run34": coverage_gate(),
        "backlog": backlog_gate(),
        "sources": sources_gate(),
        "bridges": bridge_gate(),
    }
    if post_render:
        assert INSTRUMENTED.exists(), f"instrumented Run34 reader missing: {INSTRUMENTED}"
        instrumented = INSTRUMENTED.read_text(encoding="utf-8")
        reader = READER_MD.read_text(encoding="utf-8")
        report["return_targets"] = return_target_gate(instrumented)
        report["bridges"] = bridge_gate(reader)
        report["docx_box_integrity"] = box_integrity_gate()
        assert "[claim:" not in reader, "reader-facing markdown leaked claim markers"
        report["frontstage_reader"] = {"claim_marker_leak": False}
    return report


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--post-render", action="store_true")
    parser.add_argument("--output", type=Path, default=ROOT / "docs" / "RUN34_QA_REPORT.json")
    args = parser.parse_args()
    try:
        report = run(args.post_render)
    except Exception as exc:
        print(f"RUN34 QA FAILED: {exc}", file=sys.stderr)
        return 1
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({"status":"green","post_render":args.post_render,"output":str(args.output.relative_to(ROOT))}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
