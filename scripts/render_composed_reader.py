#!/usr/bin/env python3
"""Render the reviewed core first, then perform post-review side-story stitching."""
from __future__ import annotations
import argparse,json
from arc_recap_contract import assert_rendered_arc_recaps
from materialize_arc_recaps import materialize_arc_recaps
from illustration_contract import assert_rendered_illustrations
from resolve_reader_plan import build_plan
from frontstage_reader_contract import finalize_reader
from run34_reader_patch import apply_run34_reader_patch
from post_review_side_story_placement import place_reader
import render_full_reader_v3 as base


def build(key:str)->dict:
    spec=base.SPECS[key];project=spec["project"];delta_path=project/"09_output"/spec["delta"]
    original=delta_path.read_bytes();recap_count=0
    try:
        # Core composition/review substrate first. Arc recaps belong to the causal trunk;
        # new side stories deliberately do not participate in this pass.
        core,recap_count=materialize_arc_recaps(project,original.decode("utf-8"))
        delta_path.write_text(core,encoding="utf-8")
        metric=base.build(key)
    finally:
        delta_path.write_bytes(original)

    # Legacy Run34 reader material is hydrated before the generic placement pass so
    # density scoring sees it and avoids stacking a new box beside it.
    if key=="pre":metric.update(apply_run34_reader_patch(project,spec))

    markdown_path=project/"09_output"/spec["markdown_output"]
    docx_path=project/"09_output"/spec["output"]
    metric.update(place_reader(project,markdown_path,docx_path))

    # Frontstage cleanup and presentation are intentionally last: the local stitch is
    # now part of the reader and receives the same leakage/palette checks as the core.
    metric.update(finalize_reader(project,spec))

    reader=markdown_path.read_text(encoding="utf-8")
    required=assert_rendered_arc_recaps(project,reader);plan=build_plan(project)
    illustration_count=assert_rendered_illustrations(reader,plan["selected_illustration_ids"])
    if required!=recap_count:raise RuntimeError(f"arc recap render count mismatch for {key}: materialized={recap_count}, required={required}")
    metric["arc_recaps"]=recap_count
    metric["side_stories_materialized_pre_core"]=0
    metric["book_end_storytelling_appendix"]=0
    metric["illustrations_verified"]=illustration_count
    return metric


def main():
    p=argparse.ArgumentParser();p.add_argument("--project",choices=["pre","post","all"],default="all");a=p.parse_args()
    keys=list(base.SPECS) if a.project=="all" else [a.project]
    metrics=[build(k) for k in keys]
    path=base.REPO/"docs"/"RUN12_COMPOSITION_RENDER_METRICS.json"
    path.write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(metrics,ensure_ascii=False,indent=2))
if __name__=="__main__":main()
