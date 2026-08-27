#!/usr/bin/env python3
"""Prepare the final Run27 from-scratch generation request for both Sri Lanka corpora.

This script deliberately does not generate prose. It rebuilds contamination-safe packets,
checks the two evidence universes, and emits the exact contract a semantic writer/reviewer
must satisfy before the Run27 outputs can be rendered or proposed as canon.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from build_from_scratch_packets import build_packets
from audit_canonical_points import audit as audit_canonical_points

REPO=Path(__file__).resolve().parents[1]
PROJECTS={
    "pre":REPO/"examples/sri_lanka_pre_1948",
    "post":REPO/"examples/sri_lanka_post_1948",
}
OUTPUT_NAMES={
    "pre":{"manuscript":"Sri_Lanka_pre_1948_run27_from_scratch.md","ledger":"review_ledger_run27_pre.json","run_report":"run27_report_pre.json","coverage":"run27_coverage_pre.json","docx":"Sri_Lanka_pre_1948_run27_from_scratch.docx"},
    "post":{"manuscript":"Sri_Lanka_post_1948_run27_from_scratch.md","ledger":"review_ledger_run27_post.json","run_report":"run27_report_post.json","coverage":"run27_coverage_post.json","docx":"Sri_Lanka_post_1948_run27_from_scratch.docx"},
}

def claim_total(manifest:dict)->int:return sum(int(row.get("claims",0)) for row in manifest.get("arc_summaries") or [])

def prepare()->dict:
    corpora={}
    for key,project in PROJECTS.items():
        packet_dir=project/"09_output"/"from_scratch"/"run27_packets";manifest=build_packets(project,packet_dir)
        if manifest.get("contamination_check",{}).get("reader_prose_loaded") is not False:raise RuntimeError(f"{key}: reader prose contamination detected")
        total=claim_total(manifest)
        if total<=0:raise RuntimeError(f"{key}: empty claim universe")
        corpora[key]={"project":str(project.relative_to(REPO)),"packet_dir":str(packet_dir.relative_to(REPO)),"arc_packets":len(manifest.get("packet_paths") or []),"eligible_claims":total,"reader_prose_loaded":False,"outputs":OUTPUT_NAMES[key]}
    canonical=audit_canonical_points()
    request={
        "schema_version":"1.0","run_id":"run27-final-from-scratch","status":"ready_for_semantic_generation","mode":"from_scratch","corpora":corpora,
        "generation_contract":{
            "allowed_drafting_input":"one run27 arc packet at a time plus adjacent structured bridge endpoints; never a prior reader manuscript",
            "previous_reader_prose_forbidden":True,
            "paragraph_initial_review_state":{"checklist_reviewed":False,"sarah_style_reviewed":False,"hil_scope_reviewed":False},
            "paragraph_repair":"up to 3 attempts; then explicit not_selected_for_reader rationale",
            "hil":"only dimensions actually mobilised by the paragraph; normal 1, exceptional 2, >=3 review signal",
            "return_targets":"explicit marker first; if absent, researched proposition must be supported/challenged from >=2 independent qualified source families before marker/reroute",
            "coverage":"every eligible claim and promoted fragment gets included|included_as_side_story|not_selected_for_reader; coverage_completeness.unaccounted must be []",
            "comparison":"Run25 iterative vs Run27 from-scratch: claim-level depth manifest plus residual word gap explained entirely by dispositions",
            "illustrations":"never fake human_review; only reader_eligible assets render"},
        "canonical_points":{"mode":canonical.get("mode"),"claims_total":canonical.get("claims_total"),"claims_with_canonical_points":canonical.get("claims_with_canonical_points"),"claims_missing_canonical_points":canonical.get("claims_missing_canonical_points"),"coverage_percent":canonical.get("coverage_percent"),"gate":"warning-only until a genuine editorial migration populates the field"},
        "closure_conditions":["both review ledgers complete and independently Sarah-reviewed","required return targets all resolved_marker or resolved_anchor after persisted research fallback","coverage_completeness.unaccounted == [] for both corpora","no silent evidence-status upgrade","Run25-vs-Run27 residual content gap fully explained","DOCX visual side-story boundary QA green"]}
    path=REPO/"docs"/"RUN27_FINAL_RUN_REQUEST.json";path.write_text(json.dumps(request,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");return request

def main()->int:
    p=argparse.ArgumentParser();p.parse_args();request=prepare();print(json.dumps({"run_id":request["run_id"],"status":request["status"],"corpora":{k:{"claims":v["eligible_claims"],"arc_packets":v["arc_packets"]} for k,v in request["corpora"].items()}},ensure_ascii=False,indent=2));return 0
if __name__=="__main__":raise SystemExit(main())
