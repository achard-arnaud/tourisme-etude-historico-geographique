#!/usr/bin/env python3
"""Render the lossless V3 reader with deterministic composition injected first."""
from __future__ import annotations
import argparse,json
from arc_recap_contract import assert_rendered_arc_recaps
from materialize_arc_recaps import materialize_arc_recaps
from materialize_side_stories import materialize_text as materialize_side_stories
from illustration_contract import assert_rendered_illustrations
from resolve_reader_plan import build_plan
from frontstage_reader_contract import finalize_reader
from run34_reader_patch import apply_run34_reader_patch
import render_full_reader_v3 as base

RUN40_APPENDIX="run40_storytelling_appendix.md"

def _append_book_end_apparatus(project,composed:str)->tuple[str,int]:
    path=project/"09_output"/RUN40_APPENDIX
    if not path.exists():return composed,0
    appendix=path.read_text(encoding="utf-8").strip()
    if not appendix:return composed,0
    # Explicit user-requested end apparatus. It is intentionally separate from
    # inline promoted-side-story materialization while its typed records remain
    # candidates; this prevents composition from laundering unresolved claims.
    return composed.rstrip()+"\n\n---\n\n"+appendix+"\n",1

def build(key:str)->dict:
    spec=base.SPECS[key];project=spec["project"];delta_path=project/"09_output"/spec["delta"];original=delta_path.read_bytes();recap_count=0;story_inserted=0;appendix_count=0
    try:
        composed,story_inserted=materialize_side_stories(project,original.decode("utf-8"));composed,recap_count=materialize_arc_recaps(project,composed)
        if key=="pre":composed,appendix_count=_append_book_end_apparatus(project,composed)
        delta_path.write_text(composed,encoding="utf-8");metric=base.build(key);metric.update(finalize_reader(project,spec))
        if key=="pre":metric.update(apply_run34_reader_patch(project,spec))
    finally:delta_path.write_bytes(original)
    reader=(project/"09_output"/spec["markdown_output"]).read_text(encoding="utf-8");required=assert_rendered_arc_recaps(project,reader);plan=build_plan(project);illustration_count=assert_rendered_illustrations(reader,plan["selected_illustration_ids"])
    if required!=recap_count:raise RuntimeError(f"arc recap render count mismatch for {key}: materialized={recap_count}, required={required}")
    metric["arc_recaps"]=recap_count;metric["side_stories_materialized"]=story_inserted;metric["book_end_storytelling_appendix"]=appendix_count;metric["illustrations_verified"]=illustration_count;return metric

def main():
    p=argparse.ArgumentParser();p.add_argument("--project",choices=["pre","post","all"],default="all");a=p.parse_args();keys=list(base.SPECS) if a.project=="all" else [a.project];metrics=[build(k) for k in keys];path=base.REPO/"docs"/"RUN12_COMPOSITION_RENDER_METRICS.json";path.write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(json.dumps(metrics,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
