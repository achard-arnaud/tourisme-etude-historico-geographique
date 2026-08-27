#!/usr/bin/env python3
"""Paragraph repair loop: gate failure triggers targeted rewrite, never silent omission.

The module is orchestration infrastructure. The caller supplies `draft_fn` and
`review_fn`; therefore the semantic writer/reviewer may be an LLM, a human tool or a
test fixture while the retry/disposition semantics remain deterministic.
"""
from __future__ import annotations

from dataclasses import asdict,dataclass
from typing import Any,Callable

MAX_ATTEMPTS=3
FINAL_STATUSES={"included","included_as_side_story","not_selected_for_reader"}


@dataclass(frozen=True)
class AttemptRecord:
    attempt:int
    text:str
    passed:bool
    violations:list[dict[str,Any]]


@dataclass(frozen=True)
class RepairDisposition:
    status:str
    unit_id:str
    attempts:int
    text:str|None
    rationale:str
    attempt_records:list[AttemptRecord]
    side_story_id:str|None=None

    def to_dict(self)->dict[str,Any]:
        row=asdict(self);row["attempt_records"]=[asdict(x) for x in self.attempt_records];return row


def _violations(result:Any)->list[dict[str,Any]]:
    out=[]
    for value in getattr(result,"violations",[]) or []:
        if hasattr(value,"rule"):
            out.append({"category":getattr(value,"category",""),"rule":getattr(value,"rule",""),"message":getattr(value,"message",str(value))})
        elif isinstance(value,dict):out.append({"category":str(value.get("category","")),"rule":str(value.get("rule","")),"message":str(value.get("message",value))})
        else:out.append({"category":"","rule":"","message":str(value)})
    return out


def repair_paragraph(
    unit_id:str,
    draft_fn:Callable[[int,list[dict[str,Any]]],str],
    review_fn:Callable[[str],Any],
    *,
    route_to_side_story:Callable[[str],str|None]|None=None,
    max_attempts:int=MAX_ATTEMPTS,
)->RepairDisposition:
    """Draft/rewrite until review passes or return an explicit final disposition.

    `draft_fn(attempt, prior_violations)` receives only the previous typed violations
    as repair instruction. A failing draft is never silently discarded. Review-state
    reset is the reviewer's responsibility and is asserted indirectly by the review
    contract used by `review_fn`.
    """
    if max_attempts<1:raise ValueError("max_attempts must be >=1")
    records=[];prior=[];last_text=""
    for attempt in range(1,max_attempts+1):
        text=draft_fn(attempt,prior)
        if not isinstance(text,str) or not text.strip():raise RuntimeError(f"{unit_id}: attempt {attempt} produced empty text")
        last_text=text;result=review_fn(text);passed=bool(getattr(result,"passed",False));violations=_violations(result)
        records.append(AttemptRecord(attempt,text,passed,violations))
        if passed:
            side_story_id=route_to_side_story(text) if route_to_side_story else None
            if side_story_id:
                return RepairDisposition("included_as_side_story",unit_id,attempt,text,"Passed all review gates and was deliberately routed to a side story.",records,side_story_id)
            return RepairDisposition("included",unit_id,attempt,text,"Passed all review gates.",records)
        prior=violations
    rationale="; ".join(v.get("message") or v.get("rule") or "review failure" for v in prior) or "review failed after maximum attempts"
    return RepairDisposition("not_selected_for_reader",unit_id,max_attempts,None,rationale,records)


def validate_disposition(row:dict[str,Any])->list[str]:
    errors=[];status=row.get("status")
    if status not in FINAL_STATUSES:errors.append(f"invalid disposition status: {status!r}")
    attempts=int(row.get("attempts") or 0)
    if attempts<1 or attempts>MAX_ATTEMPTS:errors.append(f"attempt count must be 1..{MAX_ATTEMPTS}")
    if status=="not_selected_for_reader" and not str(row.get("rationale") or "").strip():errors.append("not_selected_for_reader requires rationale")
    if status=="included_as_side_story" and not str(row.get("side_story_id") or "").strip():errors.append("included_as_side_story requires side_story_id")
    if status in {"included","included_as_side_story"} and not str(row.get("text") or "").strip():errors.append(f"{status} requires text")
    return errors
