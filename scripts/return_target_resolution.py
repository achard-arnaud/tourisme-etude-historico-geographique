#!/usr/bin/env python3
"""Marker-first side-story return resolution with persisted research fallback."""
from __future__ import annotations
from dataclasses import dataclass
import json,re
from pathlib import Path
from typing import Any
from side_story_contract import APPARATUS_CLASS,SIDE_STORY_CLASS,load_side_stories

TARGET_MARKER=re.compile(r"\[(claim|bridge|arc):([^\]]+)\]",re.I)
ID_LIKE=re.compile(r"^[A-Z][A-Z0-9]*-[A-Z0-9-]+$",re.I)
VALID_VERDICTS={"supported","challenged","redirected"}
QUALIFIED_ROLES={"primary","official_archive","peer_reviewed","academic_monograph","specialist_institution"}
DIRECT_AUTHORITY_ROLES={"primary","official_archive","specialist_institution"}
FINAL_STORY_STATUSES={"validated","promoted"}

@dataclass(frozen=True)
class ReturnResolution:
    status:str
    return_to:str
    target_id:str|None=None
    paragraph_anchor:str|None=None
    reason:str|None=None

def marker_for(target_id:str)->str:
    if target_id.startswith("C-"):return f"[claim:{target_id}]"
    if target_id.startswith("B-"):return f"[bridge:{target_id}]"
    return f"[arc:{target_id}]"

def _lexical_anchor(value:str)->str:
    value=TARGET_MARKER.sub("",value or "")
    value=re.sub(r"<!--.*?-->"," ",value,flags=re.S)
    value=re.sub(r"[*_`]","",value)
    value=re.sub(r"\[([^\]]+)\]\([^\)]+\)",r"\1",value)
    return re.sub(r"\s+"," ",value).strip().casefold()

def resolve_return_to(return_to:str|None,canonical_markdown:str)->ReturnResolution:
    if not return_to:return ReturnResolution("none","")
    if return_to.startswith("anchor:"):
        anchor=return_to.split(":",1)[1].strip()
        return ReturnResolution("resolved_anchor",return_to,paragraph_anchor=anchor) if anchor and _lexical_anchor(anchor) in _lexical_anchor(canonical_markdown) else ReturnResolution("needs_research",return_to,reason="literal anchor absent from canonical manuscript")
    if not ID_LIKE.match(return_to):
        return ReturnResolution("resolved_anchor",return_to,paragraph_anchor=return_to) if _lexical_anchor(return_to) in _lexical_anchor(canonical_markdown) else ReturnResolution("needs_research",return_to,reason="unresolved non-ID return target")
    marker=marker_for(return_to)
    return ReturnResolution("resolved_marker",return_to,target_id=return_to) if marker in canonical_markdown else ReturnResolution("needs_research",return_to,target_id=return_to,reason=f"missing canonical marker {marker}")

def _independent_source_families(record:dict[str,Any])->set[str]:
    families=set()
    for source in record.get("sources") or []:
        if not isinstance(source,dict):continue
        family=source.get("independence_family") or source.get("domain") or source.get("publisher")
        if family:families.add(str(family).casefold())
    return families

def _authoritative_direct_proof(sources:list[dict[str,Any]])->bool:
    return any(s.get("role") in DIRECT_AUTHORITY_ROLES and s.get("directly_closes_proposition") is True and s.get("scope_fit")=="direct" for s in sources)

def validate_research_resolution(record:dict[str,Any])->list[str]:
    errors=[];verdict=record.get("verdict")
    if verdict not in VALID_VERDICTS:errors.append("verdict must be supported|challenged|redirected")
    sources=[s for s in (record.get("sources") or []) if isinstance(s,dict)]
    qualified=[s for s in sources if s.get("role") in QUALIFIED_ROLES]
    if not ((len(qualified)>=2 and len(_independent_source_families({"sources":qualified}))>=2) or _authoritative_direct_proof(qualified)):
        errors.append("research closure requires either two independent qualified source families or one authoritative direct proof")
    if not str(record.get("target_id") or "").strip():errors.append("target_id required")
    if not str(record.get("proposition") or "").strip():errors.append("proposition required")
    if verdict=="supported" and not str(record.get("paragraph_anchor") or "").strip():errors.append("supported resolution requires paragraph_anchor for marker materialisation")
    if verdict in {"challenged","redirected"} and not (record.get("replacement_return_to") or record.get("action")=="retire_side_story"):
        errors.append("challenged/redirected resolution requires replacement_return_to or retire_side_story")
    return errors

def materialize_supported_marker(markdown:str,record:dict[str,Any])->str:
    errors=validate_research_resolution(record)
    if errors:raise ValueError("invalid research resolution: "+"; ".join(errors))
    if record.get("verdict")!="supported":raise ValueError("marker materialisation is only valid for supported research resolution")
    target_id=str(record["target_id"]);marker=marker_for(target_id)
    if marker in markdown:return markdown
    anchor=str(record["paragraph_anchor"]).strip();needle=_lexical_anchor(anchor)
    blocks=re.split(r"(\n\s*\n)",markdown)
    for i in range(0,len(blocks),2):
        if needle and needle in _lexical_anchor(blocks[i]):
            blocks[i]=blocks[i].rstrip()+f" {marker}";return "".join(blocks)
    raise ValueError(f"paragraph_anchor not found for {target_id}: {anchor}")

def load_research_records(path:Path)->list[dict[str,Any]]:
    data=json.loads(path.read_text(encoding="utf-8"));return data if isinstance(data,list) else data.get("resolutions",[])

def load_project_research_records(project:Path)->list[dict[str,Any]]:
    records=[];root=project/"08_questions";seen=set()
    if not root.exists():return records
    for path in sorted(root.glob("return_target_research*.json")):
        for record in load_research_records(path):
            target_id=str(record.get("target_id") or "")
            if target_id and target_id in seen:raise ValueError(f"duplicate return-target research record: {target_id}")
            if target_id:seen.add(target_id)
            records.append(record)
    return records

def apply_project_research_resolutions(project:Path,markdown:str)->tuple[str,dict[str,Any]]:
    applied=[];challenged=[];errors=[]
    for record in load_project_research_records(project):
        target_id=str(record.get("target_id") or "<unknown>");validation=validate_research_resolution(record)
        if validation:errors.extend(f"{target_id}: {m}" for m in validation);continue
        if record.get("verdict")=="supported":
            try:
                before=markdown;markdown=materialize_supported_marker(markdown,record)
                if markdown!=before:applied.append(target_id)
            except ValueError as exc:errors.append(str(exc))
        else:challenged.append(target_id)
    return markdown,{"applied":sorted(applied),"challenged_or_redirected":sorted(challenged),"errors":errors}

def validate_required_return_targets(project:Path,canonical_markdown:str)->tuple[list[str],list[dict[str,str]]]:
    errors=[];report=[]
    for _,item in load_side_stories(project):
        if item.get("class") not in {SIDE_STORY_CLASS,APPARATUS_CLASS}:continue
        if item.get("status") not in FINAL_STORY_STATUSES:continue
        if not (item.get("render") or {}).get("required_in_reader"):continue
        return_to=(item.get("placement") or {}).get("return_to")
        if not return_to:continue
        result=resolve_return_to(str(return_to),canonical_markdown)
        report.append({"side_story_id":str(item.get("id")),"return_to":str(return_to),"status":result.status})
        if result.status not in {"resolved_marker","resolved_anchor"}:errors.append(f"{item.get('id')}: required return_to {return_to!r} remains {result.status}")
    return errors,report
