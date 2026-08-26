#!/usr/bin/env python3
"""One-shot migration for low-confidence illustration records before strict gate activation."""
from __future__ import annotations
import argparse,json
from pathlib import Path


def migrate_file(path:Path,dry_run:bool=False)->tuple[int,int]:
    data=json.loads(path.read_text(encoding="utf-8"));items=data if isinstance(data,list) else [data]
    changed=0;demoted=0
    for item in items:
        review=item.get("vision_review") or {}
        if review.get("confidence")!="low":continue
        depiction=item.setdefault("depiction",{})
        if depiction.get("evidence_status")!="interpretive":
            depiction["evidence_status"]="interpretive";changed+=1
        if not item.get("tag_review"):
            item["tag_review"]={"status":"pending","trigger":"auto_low_confidence","notes":"Migration: explicit human tag review required before vision_validated promotion."};changed+=1
        if item.get("status") in {"vision_validated","reader_eligible"} and item["tag_review"].get("status")!="approved":
            item["status"]="candidate";demoted+=1;changed+=1
            render=item.setdefault("render",{});render["required_in_reader"]=False
    if changed and not dry_run:
        path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return changed,demoted


def main()->int:
    parser=argparse.ArgumentParser();parser.add_argument("project");parser.add_argument("--dry-run",action="store_true");args=parser.parse_args()
    root=Path(args.project)/"09_output"/"illustrations";changed=demoted=0
    for path in sorted(root.glob("*.json")):
        c,d=migrate_file(path,args.dry_run);changed+=c;demoted+=d
    mode="DRY RUN" if args.dry_run else "MIGRATED"
    print(f"CONFIDENCE GATE {mode}: {changed} changes, {demoted} low-confidence assets demoted pending human tag review")
    return 0

if __name__=="__main__":raise SystemExit(main())
