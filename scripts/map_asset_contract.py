#!/usr/bin/env python3
"""Validate optional historical-map candidates through vision and human approval."""
from __future__ import annotations
import json
from pathlib import Path
from side_story_contract import load_side_stories

SCHEMA_VERSION="1.0"; CLASS="map_asset"; STATUSES={"candidate","vision_validated","human_approved","retired"}

def load_map_assets(project:Path):
    root=project/"09_output"/"map_assets"; out=[]
    if not root.exists(): return out
    for p in sorted(root.glob("*.json")):
        data=json.loads(p.read_text(encoding="utf-8")); items=data if isinstance(data,list) else [data]
        out.extend((p,x) for x in items)
    return out

def validate_map_assets(project:Path)->tuple[list[str],list[str],int]:
    errors=[]; warnings=[]; assets=load_map_assets(project); seen=set()
    stories={x.get("id"):x for _,x in load_side_stories(project)}
    arcs={p.name for p in (project/"01_arcs").iterdir() if p.is_dir()} if (project/"01_arcs").exists() else set()
    profile_path=project/"00_method"/"reader_profile.json"; doc_lang="fr"
    if profile_path.exists(): doc_lang=json.loads(profile_path.read_text(encoding="utf-8")).get("language","fr")
    for p,item in assets:
        mid=item.get("id"); status=item.get("status")
        if item.get("schema_version")!=SCHEMA_VERSION or item.get("class")!=CLASS: errors.append(f"map {mid or p.name}: invalid class/schema")
        if not mid or mid in seen: errors.append(f"map {mid or p.name}: missing/duplicate id")
        else: seen.add(mid)
        if status not in STATUSES: errors.append(f"map {mid}: invalid status")
        target=item.get("story_ref") or {}; ttype=target.get("type"); tid=target.get("id")
        if ttype=="side_story":
            if tid not in stories: errors.append(f"map {mid}: unknown side_story {tid}")
            elif not stories[tid].get("map_eligible"): errors.append(f"map {mid}: target side_story is not map_eligible")
        elif ttype=="arc":
            if tid not in arcs: errors.append(f"map {mid}: unknown arc {tid}")
        else: errors.append(f"map {mid}: story_ref.type must be arc or side_story")
        source=item.get("source") or {}; hist=item.get("historical_context") or {}; vision=item.get("vision_review") or {}; human=item.get("human_review") or {}; fragment=item.get("fragment") or {}
        if status in {"vision_validated","human_approved"}:
            if not source.get("url") or not source.get("image_path"): errors.append(f"map {mid}: validated map needs source URL and image_path")
            checks=vision.get("checks") or {}
            for key in ("geography_matches","historical_scope_matches","labels_legible","no_obvious_anachronism"):
                if checks.get(key) is not True: errors.append(f"map {mid}: vision check {key} not passed")
            if not hist.get("map_date"): errors.append(f"map {mid}: historical map_date required after vision validation")
        if status=="human_approved":
            if human.get("status")!="approved" or not human.get("reviewed_at"): errors.append(f"map {mid}: human approval evidence required")
            if source.get("language") not in {doc_lang,"en"}: errors.append(f"map {mid}: map language must be document language ({doc_lang}) or English")
            for key in ("caption","what_it_shows","why_here","limits"):
                if not fragment.get(key): errors.append(f"map {mid}: fragment.{key} required")
        if status=="retired" and human.get("status")=="approved": warnings.append(f"map {mid}: retired after prior human approval")
    return errors,warnings,len(assets)
