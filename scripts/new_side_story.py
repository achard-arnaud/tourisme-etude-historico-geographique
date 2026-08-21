#!/usr/bin/env python3
"""Create a versioned candidate side-story composition artifact."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from side_story_contract import ANALYTICAL_FOCUS_KIND,KINDS,RENDER_LABELS,SCHEMA_VERSION,canonical_marker,side_story_dir

def csv_items(value):return [item.strip() for item in (value or "").split(",") if item.strip()]
def main()->int:
    p=argparse.ArgumentParser();p.add_argument("--project",required=True);p.add_argument("--id",required=True);p.add_argument("--kind",required=True,choices=sorted(KINDS));p.add_argument("--arc",required=True);p.add_argument("--title",required=True);p.add_argument("--section-anchor",required=True);p.add_argument("--return-to",required=True);p.add_argument("--purpose",required=True)
    for arg in ("claim-ids","source-ids","bridge-ids","hil-ids","drift-paths","origin-paths","related-arcs"):p.add_argument("--"+arg)
    p.add_argument("--reason-off-trunk",default="Candidate pending editorial validation.");p.add_argument("--payoff",default="Pending editorial payoff.");p.add_argument("--takeaway",default="Pending narrative takeaway.");p.add_argument("--required-in-reader",action="store_true");p.add_argument("--map-eligible",action="store_true");p.add_argument("--min-age",type=int,default=10)
    for arg in ("zoom-from","zoom-to","zoom-return-to","zoom-mechanism","zoom-local-payoff"):p.add_argument("--"+arg)
    a=p.parse_args()
    if a.kind==ANALYTICAL_FOCUS_KIND:p.error("analytical_focus requires the structured templates/side-stories/analytical-focus.json contract")
    if a.kind=="dezoom":
        req={"--zoom-from":a.zoom_from,"--zoom-to":a.zoom_to,"--zoom-return-to":a.zoom_return_to,"--zoom-mechanism":a.zoom_mechanism,"--zoom-local-payoff":a.zoom_local_payoff};missing=[k for k,v in req.items() if not v]
        if missing:p.error("dezoom requires "+", ".join(missing))
    project=Path(a.project);outdir=side_story_dir(project);outdir.mkdir(parents=True,exist_ok=True);out=outdir/f"{a.id}.json"
    if out.exists():p.error(f"side story already exists: {out}")
    item={"schema_version":SCHEMA_VERSION,"class":"side_story","id":a.id,"kind":a.kind,"status":"candidate","lineage_quality":"full","title":a.title,"arc":a.arc,"related_arcs":csv_items(a.related_arcs),"purpose":a.purpose,"reason_off_trunk":a.reason_off_trunk,"payoff":a.payoff,"map_eligible":bool(a.map_eligible),"reader_policy":{"min_age":a.min_age},"lineage":{"claim_ids":csv_items(a.claim_ids),"source_ids":csv_items(a.source_ids),"bridge_ids":csv_items(a.bridge_ids),"hil_ids":csv_items(a.hil_ids),"drift_paths":csv_items(a.drift_paths),"origin_paths":csv_items(a.origin_paths)},"placement":{"section_anchor":a.section_anchor,"return_to":a.return_to},"zoom_excursion":{"from":a.zoom_from,"to":a.zoom_to,"return_to":a.zoom_return_to,"mechanism":a.zoom_mechanism,"local_payoff":a.zoom_local_payoff} if a.kind=="dezoom" else None,"analysis":None,"visual":None,"content":{"takeaway":a.takeaway,"body_markdown":"","legacy_titles":[]},"render":{"label":RENDER_LABELS[a.kind],"marker":canonical_marker(a.id),"required_in_reader":bool(a.required_in_reader)}}
    out.write_text(json.dumps(item,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(out);return 0
if __name__=="__main__":raise SystemExit(main())
