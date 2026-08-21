#!/usr/bin/env python3
"""Resolve side stories, recaps and approved maps deterministically for a reader profile."""
from __future__ import annotations
import argparse,json
from pathlib import Path
from side_story_contract import load_side_stories
from arc_recap_contract import load_arc_recaps
from map_asset_contract import load_map_assets
from reader_profile_contract import load_reader_profile

def build_plan(project:Path)->dict:
    profile=load_reader_profile(project); policy=profile["side_story_policy"]; priority={k:i for i,k in enumerate(policy["priority_order"])}
    age=profile.get("min_age"); stories=[]
    for _,s in load_side_stories(project):
        if s.get("status") not in {"validated","promoted"}:continue
        rp=s.get("reader_policy") or {}; min_age=rp.get("min_age")
        if age is not None and min_age is not None and age<min_age:continue
        if policy["coverage_mode"]=="selective" and s.get("kind") not in set(policy.get("include_kinds") or []):continue
        stories.append(s)
    stories.sort(key=lambda s:(priority.get(s.get("kind"),99),s.get("id","")))
    recaps=[r for _,r in load_arc_recaps(project) if r.get("status") in {"validated","promoted"}]
    approved=[m for _,m in load_map_assets(project) if m.get("status")=="human_approved"]
    selected_maps=[]; used=set()
    for m in sorted(approved,key=lambda x:((x.get("placement") or {}).get("relevance_rank",99),x.get("id",""))):
        slot=(m.get("placement") or {}).get("subsection_ref")
        if slot and slot not in used: selected_maps.append(m);used.add(slot)
    return {"profile_id":profile["id"],"content_temperature":profile["content_temperature"],"story_template":profile["story_template"],"eligible_side_story_ids":[s["id"] for s in stories],"arc_recap_ids":[r["id"] for r in recaps] if profile.get("arc_recap_policy",{}).get("enabled",True) else [],"selected_map_ids":[m["id"] for m in selected_maps],"map_rule":"max one human-approved map per subsection/side-story slot"}
def main():
    p=argparse.ArgumentParser();p.add_argument("--project",required=True);p.add_argument("--output");a=p.parse_args();project=Path(a.project);plan=build_plan(project);text=json.dumps(plan,ensure_ascii=False,indent=2)+"\n"
    if a.output:Path(a.output).write_text(text,encoding="utf-8")
    print(text,end="")
if __name__=="__main__":main()
