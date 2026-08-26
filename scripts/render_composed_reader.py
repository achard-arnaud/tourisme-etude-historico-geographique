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
import render_full_reader_v3 as base

def build(key:str)->dict:
    spec=base.SPECS[key];project=spec["project"];delta_path=project/"09_output"/spec["delta"];original=delta_path.read_bytes();recap_count=0;story_inserted=0
    try:
        composed,story_inserted=materialize_side_stories(project,original.decode("utf-8"));composed,recap_count=materialize_arc_recaps(project,composed);delta_path.write_text(composed,encoding="utf-8");metric=base.build(key);metric.update(finalize_reader(project,spec))
    finally:delta_path.write_bytes(original)
    reader=(project/"09_output"/spec["markdown_output"]).read_text(encoding="utf-8");required=assert_rendered_arc_recaps(project,reader);plan=build_plan(project);illustration_count=assert_rendered_illustrations(reader,plan["selected_illustration_ids"])
    if required!=recap_count:raise RuntimeError(f"arc recap render count mismatch for {key}: materialized={recap_count}, required={required}")
    metric["arc_recaps"]=recap_count;metric["side_stories_materialized"]=story_inserted;metric["illustrations_verified"]=illustration_count;return metric
def main():
    p=argparse.ArgumentParser();p.add_argument("--project",choices=["pre","post","all"],default="all");a=p.parse_args();keys=list(base.SPECS) if a.project=="all" else [a.project];metrics=[build(k) for k in keys];path=base.REPO/"docs"/"RUN12_COMPOSITION_RENDER_METRICS.json";path.write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(json.dumps(metrics,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
