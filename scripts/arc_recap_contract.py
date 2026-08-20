#!/usr/bin/env python3
"""Validate causal end-of-arc recap artefacts."""
from __future__ import annotations
import json
from pathlib import Path
from output_state import load_output_state

SCHEMA_VERSION="1.0"; CLASS="arc_recap"; STATUSES={"candidate","validated","promoted","retired"}

def load_arc_recaps(project:Path):
    root=project/"09_output"/"arc_recaps"; out=[]
    if not root.exists(): return out
    for p in sorted(root.glob("*.json")):
        data=json.loads(p.read_text(encoding="utf-8")); items=data if isinstance(data,list) else [data]
        out.extend((p,x) for x in items)
    return out

def _load(project:Path,pattern:str)->set[str]:
    out=set()
    for p in project.glob(pattern):
        try:d=json.loads(p.read_text(encoding="utf-8"))
        except Exception:continue
        if isinstance(d,dict) and d.get("id"): out.add(d["id"])
    return out

def validate_arc_recaps(project:Path)->tuple[list[str],list[str],int]:
    errors=[]; warnings=[]; recaps=load_arc_recaps(project)
    arcs={p.name for p in (project/"01_arcs").iterdir() if p.is_dir() and (p/"ARC.md").exists()} if (project/"01_arcs").exists() else set()
    claims=_load(project,"01_arcs/*/claims/*.json"); bridges=_load(project,"06_bridges/*.json")
    by_arc={}; seen=set()
    for p,item in recaps:
        rid=item.get("id"); arc=item.get("arc"); status=item.get("status")
        if item.get("schema_version")!=SCHEMA_VERSION or item.get("class")!=CLASS: errors.append(f"arc recap {rid or p.name}: invalid class/schema")
        if not rid or rid in seen: errors.append(f"arc recap {rid or p.name}: missing/duplicate id")
        else: seen.add(rid)
        if status not in STATUSES: errors.append(f"arc recap {rid}: invalid status")
        if status in {"validated","promoted"} and arc not in arcs: errors.append(f"arc recap {rid}: unknown materialized arc {arc!r}")
        by_arc.setdefault(arc,[]).append(item)
        causal=item.get("causal_schema") or {}
        for key in ("drivers","amplifiers","constraints","consequences"):
            vals=causal.get(key)
            if not isinstance(vals,list): errors.append(f"arc recap {rid}: causal_schema.{key} must be list")
            else:
                for row in vals:
                    cid=row.get("claim_id") if isinstance(row,dict) else None
                    if cid and cid not in claims: errors.append(f"arc recap {rid}: unknown claim {cid}")
        protagonists=item.get("protagonists") or []
        if status in {"validated","promoted"} and not protagonists: errors.append(f"arc recap {rid}: protagonists required")
        for actor in protagonists:
            for cid in actor.get("claim_ids") or []:
                if cid not in claims: errors.append(f"arc recap {rid}: protagonist unknown claim {cid}")
        teasers=item.get("prepares_next") or []
        if status in {"validated","promoted"} and not teasers: errors.append(f"arc recap {rid}: prepares_next required")
        for row in teasers:
            if not row.get("bullet"): errors.append(f"arc recap {rid}: empty teaser bullet")
            for bid in row.get("bridge_ids") or []:
                if bid not in bridges: errors.append(f"arc recap {rid}: unknown teaser bridge {bid}")
        marker=(item.get("render") or {}).get("marker")
        if marker!=f"[ARC-RECAP:{rid}]": errors.append(f"arc recap {rid}: invalid marker")
    try: required=bool(load_output_state(project).get("composition",{}).get("require_arc_recaps"))
    except Exception: required=False
    if required:
        missing=sorted(a for a in arcs if not any(x.get("status") in {"validated","promoted"} for x in by_arc.get(a,[])))
        if missing: errors.append("missing validated arc recaps: "+", ".join(missing))
    return errors,warnings,len(recaps)
