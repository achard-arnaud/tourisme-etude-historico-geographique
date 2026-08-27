#!/usr/bin/env python3
"""Strict final closure gate for Run27 after semantic drafting/review is complete."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from from_scratch_review_contract import assert_review_complete
from return_target_resolution import apply_project_research_resolutions,validate_required_return_targets
from run27_coverage_contract import coverage_completeness
from render_from_scratch_reader import build as render_fresh

REPO=Path(__file__).resolve().parents[1]
SPECS={
 "pre":{"project":REPO/"examples/sri_lanka_pre_1948","manuscript":"Sri_Lanka_pre_1948_run27_from_scratch.md","ledger":"review_ledger_run27_pre.json","run_report":"run27_report_pre.json","coverage":"run27_coverage_pre.json"},
 "post":{"project":REPO/"examples/sri_lanka_post_1948","manuscript":"Sri_Lanka_post_1948_run27_from_scratch.md","ledger":"review_ledger_run27_post.json","run_report":"run27_report_post.json","coverage":"run27_coverage_post.json"},
}

def close_one(key:str,render:bool=True)->dict:
    spec=SPECS[key];project=spec["project"];root=project/"09_output"/"from_scratch"
    paths={name:root/spec[name] for name in ("manuscript","ledger","run_report","coverage")}
    missing=[name for name in ("manuscript","ledger","run_report") if not paths[name].exists()]
    if missing:raise RuntimeError(f"{key}: final semantic artefacts missing: {missing}")
    reviewed=assert_review_complete(project,paths["manuscript"],paths["ledger"])
    markdown=paths["manuscript"].read_text(encoding="utf-8")
    augmented,research=apply_project_research_resolutions(project,markdown)
    if research["errors"]:raise RuntimeError(f"{key}: return research errors: {research['errors']}")
    return_errors,return_report=validate_required_return_targets(project,augmented)
    if return_errors:raise RuntimeError(f"{key}: unresolved required returns: {return_errors}")
    run_report=json.loads(paths["run_report"].read_text(encoding="utf-8"));coverage=coverage_completeness(project,markdown,run_report)
    paths["coverage"].write_text(json.dumps(coverage,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    if coverage["errors"]:raise RuntimeError(f"{key}: coverage closure failed: {coverage['errors']}")
    render_metrics=render_fresh(key,27) if render else None
    return {"project":key,"reviewed_paragraphs":reviewed,"eligible_claims":coverage["eligible_claims"],"eligible_promoted_fragments":coverage["eligible_promoted_fragments"],"unaccounted":coverage["unaccounted"],"thin_claims":coverage["thin_claim_coverage_signal"],"required_returns":len(return_report),"research_markers_materialized":len(research["applied"]),"render":render_metrics}

def main()->int:
    p=argparse.ArgumentParser();p.add_argument("--project",choices=["pre","post","all"],default="all");p.add_argument("--no-render",action="store_true");a=p.parse_args();keys=list(SPECS) if a.project=="all" else [a.project];results=[close_one(k,not a.no_render) for k in keys];out=REPO/"docs"/"RUN27_FINAL_CLOSURE.json";out.write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(json.dumps(results,ensure_ascii=False,indent=2));return 0
if __name__=="__main__":raise SystemExit(main())
