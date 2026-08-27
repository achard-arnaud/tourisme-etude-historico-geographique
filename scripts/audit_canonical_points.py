#!/usr/bin/env python3
"""Audit canonical-point population without pretending the gate is active."""
from __future__ import annotations
import argparse,json
from pathlib import Path
REPO=Path(__file__).resolve().parents[1]
PROJECTS=(REPO/"examples/sri_lanka_pre_1948",REPO/"examples/sri_lanka_post_1948")
def load_claims(project:Path):
    for path in sorted(project.glob("01_arcs/*/claims/*.json")):
        data=json.loads(path.read_text(encoding="utf-8"));items=data if isinstance(data,list) else [data]
        for item in items:
            if isinstance(item,dict) and item.get("id"):yield path,item
def audit(projects=PROJECTS)->dict:
    total=0;populated=[];missing=[]
    for project in projects:
        for path,claim in load_claims(project):
            total+=1;points=claim.get("canonical_points") or claim.get("canonical_summary_points");row={"id":str(claim["id"]),"path":str(path.relative_to(REPO))}
            if isinstance(points,list) and any((isinstance(x,str) and x.strip()) or (isinstance(x,dict) and (x.get("text") or x.get("summary"))) for x in points):populated.append(row)
            else:missing.append(row)
    return {"mode":"warning_only_until_populated","claims_total":total,"claims_with_canonical_points":len(populated),"claims_missing_canonical_points":len(missing),"coverage_percent":round((len(populated)/total*100),1) if total else 100.0,"missing":missing}
def main()->int:
    p=argparse.ArgumentParser();p.add_argument("--strict",action="store_true");p.add_argument("--output");a=p.parse_args();report=audit();text=json.dumps(report,ensure_ascii=False,indent=2)+"\n"
    if a.output:Path(a.output).write_text(text,encoding="utf-8")
    print(text,end="");return 1 if a.strict and report["claims_missing_canonical_points"] else 0
if __name__=="__main__":raise SystemExit(main())
