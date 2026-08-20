#!/usr/bin/env python3
"""Audit context as orchestrator + actually routed skills, never one file in isolation."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path

def latest_manifest(repo:Path)->Path:
    found=[]
    for p in (repo/"docs").glob("RUN*_MANIFEST.json"):
        m=re.match(r"RUN(\d+)",p.name)
        if m:found.append((int(m.group(1)),p.name,p))
    if not found:raise FileNotFoundError("no RUN*_MANIFEST.json")
    return max(found)[2]
def main():
    repo=Path(__file__).resolve().parents[1];p=argparse.ArgumentParser();p.add_argument("manifest",nargs="?",default="--latest");p.add_argument("--budget",type=int,default=12000);a=p.parse_args()
    path=latest_manifest(repo) if a.manifest=="--latest" else repo/a.manifest;data=json.loads(path.read_text(encoding="utf-8"));names=[x["skill"] for x in data.get("dispatched_skills",[])]
    files=[repo/"SKILL.md"]+[repo/"skills"/n/"SKILL.md" for n in names];words=sum(len(f.read_text(encoding="utf-8").split()) for f in files if f.exists())
    if words>a.budget:print(f"ERROR: routed context {words} words exceeds budget {a.budget}");return 1
    print(f"CONTEXT BUDGET OK: {words}/{a.budget} words across orchestrator + {len(names)} dispatched skills");return 0
if __name__=="__main__":raise SystemExit(main())
