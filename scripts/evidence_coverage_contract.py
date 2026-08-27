#!/usr/bin/env python3
"""Exhaustive reader coverage contract: every eligible claim and promoted field fragment gets a disposition."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from typing import Any
from from_scratch_review_contract import load_claim_index,manuscript_paragraphs,visible_text
from paragraph_repair_loop import FINAL_STATUSES

WORD_RE=re.compile(r"\b[\wÀ-ÖØ-öø-ÿĀ-ž'’.-]+\b",re.UNICODE)
def word_count(text:str)->int:return len(WORD_RE.findall(visible_text(text)))

def load_promoted_fragments(project:Path)->dict[str,dict[str,Any]]:
    out={}
    for path in sorted(project.glob("00_method/capture/*field_fragments.json")):
        data=json.loads(path.read_text(encoding="utf-8"));items=data if isinstance(data,list) else [data]
        for item in items:
            if not isinstance(item,dict) or not item.get("id"):continue
            target=str(item.get("promotes_to") or "").strip()
            if target:out[str(item["id"])]=dict(item,source_path=str(path.relative_to(project)),promotes_to=target)
    return out

def build_claim_manifest(project:Path,markdown:str)->dict[str,dict[str,Any]]:
    claims=load_claim_index(project);manifest={cid:{"claim_id":cid,"paragraph_ids":[],"paragraph_count":0,"gross_word_count":0,"apportioned_word_count":0.0} for cid in sorted(claims)}
    for paragraph in manuscript_paragraphs(markdown):
        ids=[cid for cid in paragraph["claim_ids"] if cid in manifest]
        if not ids:continue
        words=word_count(paragraph["text"]);share=words/len(ids)
        for cid in ids:
            row=manifest[cid];row["paragraph_ids"].append(paragraph["id"]);row["paragraph_count"]+=1;row["gross_word_count"]+=words;row["apportioned_word_count"]+=share
    for row in manifest.values():row["apportioned_word_count"]=round(row["apportioned_word_count"],1)
    return manifest

def normalize_dispositions(project:Path,run_report:dict[str,Any],claim_manifest:dict[str,dict[str,Any]])->dict[str,dict[str,Any]]:
    claims=load_claim_index(project);fragments=load_promoted_fragments(project);raw=run_report.get("dispositions") or {};out={}
    for cid in claims:
        row=raw.get(cid)
        if row is None and claim_manifest[cid]["paragraph_count"]>0:
            row={"status":"included","rationale":"Present in reviewed manuscript.","paragraph_ids":claim_manifest[cid]["paragraph_ids"]}
        if row is not None:
            row=dict(row);row.setdefault("unit_id",cid);out[f"claim:{cid}"]=row
    for fid,fragment in fragments.items():
        target=fragment["promotes_to"];claim_row=out.get(f"claim:{target}")
        if claim_row:out[f"fragment:{fid}"]={"unit_id":fid,"status":claim_row["status"],"rationale":f"Disposed through promoted claim {target}.","via_claim":target}
        elif raw.get(fid):
            row=dict(raw[fid]);row.setdefault("unit_id",fid);out[f"fragment:{fid}"]=row
    return out

def coverage_completeness(project:Path,markdown:str,run_report:dict[str,Any])->dict[str,Any]:
    claims=load_claim_index(project);fragments=load_promoted_fragments(project);manifest=build_claim_manifest(project,markdown);dispositions=normalize_dispositions(project,run_report,manifest)
    eligible={f"claim:{cid}" for cid in claims}|{f"fragment:{fid}" for fid in fragments};accounted=set(dispositions);unaccounted=sorted(eligible-accounted);errors=[]
    for key,row in dispositions.items():
        status=row.get("status")
        if status not in FINAL_STATUSES:errors.append(f"{key}: invalid status {status!r}")
        if status=="not_selected_for_reader" and not str(row.get("rationale") or "").strip():errors.append(f"{key}: not_selected_for_reader requires rationale")
        if status=="included_as_side_story" and not str(row.get("side_story_id") or "").strip():errors.append(f"{key}: included_as_side_story requires side_story_id")
    if unaccounted:errors.append(f"unaccounted eligible units: {unaccounted}")
    thin=[cid for cid,row in manifest.items() if row["paragraph_count"]>0 and row["apportioned_word_count"]<25]
    return {"eligible_total":len(eligible),"eligible_claims":len(claims),"eligible_promoted_fragments":len(fragments),"accounted_for":len(accounted),"unaccounted":unaccounted,"errors":errors,"status_counts":{status:sum(1 for row in dispositions.values() if row.get("status")==status) for status in sorted(FINAL_STATUSES)},"thin_claim_coverage_signal":thin,"claim_manifest":manifest,"dispositions":dispositions}

def main()->int:
    p=argparse.ArgumentParser();p.add_argument("--project",required=True,type=Path);p.add_argument("--manuscript",required=True,type=Path);p.add_argument("--run-report",required=True,type=Path);p.add_argument("--output",required=True,type=Path);a=p.parse_args()
    report=coverage_completeness(a.project,a.manuscript.read_text(encoding="utf-8"),json.loads(a.run_report.read_text(encoding="utf-8")));a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");print(json.dumps({k:v for k,v in report.items() if k not in {"claim_manifest","dispositions"}},ensure_ascii=False,indent=2));return 1 if report["errors"] else 0
if __name__=="__main__":raise SystemExit(main())
