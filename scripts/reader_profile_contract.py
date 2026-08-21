#!/usr/bin/env python3
"""Deterministic reader-profile and content-temperature contract."""
from __future__ import annotations
import json
from pathlib import Path
SCHEMA_VERSION="1.0";CLASS="reader_profile";KINDS={"detour","dezoom","also","method","false_lead","portrait","object_focus","comparator","callback","analytical_focus"}
def load_reader_profile(project:Path)->dict:
    p=project/"00_method"/"reader_profile.json"
    if not p.exists():raise FileNotFoundError(f"missing reader profile: {p}")
    return json.loads(p.read_text(encoding="utf-8"))
def validate_reader_profile(project:Path)->tuple[list[str],list[str],int]:
    errors=[];warnings=[]
    try:p=load_reader_profile(project)
    except Exception as exc:return [str(exc)],[],0
    if p.get("schema_version")!=SCHEMA_VERSION or p.get("class")!=CLASS:errors.append("reader profile invalid class/schema")
    temp=p.get("content_temperature")
    if not isinstance(temp,int) or not 1<=temp<=5:errors.append("reader profile content_temperature must be integer 1..5")
    policy=p.get("side_story_policy") or {};priority=policy.get("priority_order") or []
    if set(priority)!=KINDS or len(priority)!=len(KINDS):errors.append("reader profile priority_order must enumerate every side-story kind exactly once")
    if policy.get("coverage_mode") not in {"all","selective"}:errors.append("reader profile coverage_mode must be all/selective")
    tpl=p.get("story_template")
    if not tpl or not (Path(__file__).resolve().parents[1]/tpl).exists():errors.append("reader profile story_template missing")
    if p.get("audience")=="child_10_plus" and p.get("min_age")!=10:errors.append("child_10_plus profile must set min_age=10")
    return errors,warnings,1
