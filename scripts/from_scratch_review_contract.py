#!/usr/bin/env python3
"""Review-ledger contract for Run26 from-scratch manuscripts."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Iterable

from sarah_voice_contract import review_skeleton, validate_style_review

CLAIM_MARKER=re.compile(r"\[claim:([^\]]+)\]",re.I)
SIDE_BEGIN=re.compile(r"^<!--\s*\[SIDE-STORY:([^\]]+)\]\s+BEGIN\s+kind=([a-z_]+)\s*-->$")
SIDE_END=re.compile(r"^<!--\s*\[SIDE-STORY:([^\]]+)\]\s+END\s*-->$")


def visible_text(text:str)->str:
    return re.sub(r"\s+"," ",CLAIM_MARKER.sub("",text)).strip()


def paragraph_id(text:str)->str:
    payload=visible_text(text).encode("utf-8")
    return "P-"+hashlib.sha256(payload).hexdigest()[:16]


def _is_structural(line:str)->bool:
    s=line.strip()
    return (not s or s.startswith("#") or s=="---" or SIDE_BEGIN.match(s) is not None or SIDE_END.match(s) is not None)


def manuscript_paragraphs(markdown:str)->list[dict]:
    """Return reader-prose units; headings and side-story fences are not paragraphs."""
    out=[];buffer=[]
    def flush():
        nonlocal buffer
        if not buffer:return
        raw=" ".join(x.strip() for x in buffer if x.strip()).strip();buffer=[]
        if not raw:return
        out.append({"id":paragraph_id(raw),"text":raw,"claim_ids":sorted(set(CLAIM_MARKER.findall(raw)))})
    for raw in markdown.splitlines():
        s=raw.strip()
        if SIDE_BEGIN.match(s) or SIDE_END.match(s) or s.startswith("#") or s=="---":flush();continue
        if not s:flush();continue
        if re.match(r"^(?:[-*]|\d+\.)\s+",s):flush();out.append({"id":paragraph_id(s),"text":s,"claim_ids":sorted(set(CLAIM_MARKER.findall(s)))})
        else:buffer.append(raw)
    flush();return out


def claim_hils(claim:dict)->set[str]:
    out=set();value=claim.get("hil")
    if isinstance(value,str) and value:out.add(value)
    out|={str(x) for x in claim.get("hil_ids") or [] if x};return out


def load_claim_index(project:Path)->dict[str,dict]:
    out={}
    for path in sorted(project.glob("01_arcs/*/claims/*.json")):
        data=json.loads(path.read_text(encoding="utf-8"));items=data if isinstance(data,list) else [data]
        for item in items:
            if isinstance(item,dict) and item.get("id"):out[str(item["id"])]=item
    return out


def relevant_hils(claim_ids:Iterable[str],claims:dict[str,dict])->set[str]:
    out=set()
    for cid in claim_ids:
        if cid in claims:out|=claim_hils(claims[cid])
    return out


def initialize_ledger(markdown:str,*,generation_pass_id:str|None=None,generation_context_id:str|None=None)->list[dict]:
    """Create an all-false ledger; Sarah records are hash-bound but non-passing."""
    records=[]
    for paragraph in manuscript_paragraphs(markdown):
        records.append({
            "paragraph_id":paragraph["id"],
            "claim_ids":paragraph["claim_ids"],
            "selected_hil_ids":[],
            "initial_state":{"checklist_reviewed":False,"sarah_style_reviewed":False,"hil_scope_reviewed":False},
            "review_state":{"checklist_reviewed":False,"sarah_style_reviewed":False,"hil_scope_reviewed":False},
            "sarah_style_review":review_skeleton(
                paragraph["text"],
                generation_pass_id=generation_pass_id,
                generation_context_id=generation_context_id,
            ),
            "review_notes":"",
        })
    return records


def load_ledger(path:Path)->list[dict]:
    if path.suffix==".jsonl":
        return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    data=json.loads(path.read_text(encoding="utf-8"));return data if isinstance(data,list) else data.get("paragraphs",[])


def validate_review_ledger(project:Path,markdown:str,records:list[dict])->list[str]:
    errors=[];paragraphs=manuscript_paragraphs(markdown);by_id={str(r.get("paragraph_id")):r for r in records};claims=load_claim_index(project)
    if len(by_id)!=len(records):errors.append("duplicate paragraph_id in review ledger")
    expected={p["id"] for p in paragraphs};extra=set(by_id)-expected;missing=expected-set(by_id)
    if missing:errors.append(f"review ledger missing paragraphs: {sorted(missing)}")
    if extra:errors.append(f"review ledger contains stale paragraphs: {sorted(extra)}")
    for paragraph in paragraphs:
        pid=paragraph["id"];record=by_id.get(pid)
        if not record:continue
        initial=record.get("initial_state") or {};state=record.get("review_state") or {}
        for key in ("checklist_reviewed","sarah_style_reviewed","hil_scope_reviewed"):
            if initial.get(key) is not False:errors.append(f"{pid}: initial_state.{key} must be false")
            if state.get(key) is not True:errors.append(f"{pid}: review_state.{key} must be true before final render")
        declared_claims={str(x) for x in record.get("claim_ids") or []};actual_claims=set(paragraph["claim_ids"])
        if declared_claims!=actual_claims:errors.append(f"{pid}: claim_ids drift: ledger={sorted(declared_claims)} manuscript={sorted(actual_claims)}")
        unknown=actual_claims-set(claims)
        if unknown:errors.append(f"{pid}: unknown claim ids {sorted(unknown)}")
        relevant=relevant_hils(actual_claims,claims);selected={str(x) for x in record.get("selected_hil_ids") or []};extraneous=selected-relevant
        if extraneous:errors.append(f"{pid}: irrelevant HIL selection {sorted(extraneous)}")

        style_errors,_=validate_style_review(paragraph["text"],record.get("sarah_style_review") or {})
        errors.extend(f"{pid}: {message}" for message in style_errors)
        if state.get("sarah_style_reviewed") is True and style_errors:
            errors.append(f"{pid}: review_state.sarah_style_reviewed cannot be true while Sarah review contract fails")
    return errors


def assert_review_complete(project:Path,manuscript:Path,ledger:Path)->int:
    markdown=manuscript.read_text(encoding="utf-8");records=load_ledger(ledger);errors=validate_review_ledger(project,markdown,records)
    if errors:raise RuntimeError("from-scratch review gate failed:\n- "+"\n- ".join(errors))
    return len(records)
