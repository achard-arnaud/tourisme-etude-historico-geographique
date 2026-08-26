#!/usr/bin/env python3
"""L0 reciprocal claim/fragment/side-story coverage diagnostics."""
from __future__ import annotations
import argparse,json,re
from pathlib import Path
from output_state import canonical_markdown_path
from run_journal import append_entry

MARKER=re.compile(r"\[claim:([^\]]+)\]",re.I);WORD=re.compile(r"\b[\wÀ-ÖØ-öø-ÿĀ-ž'’.-]+\b",re.UNICODE)

def records(project:Path,pattern:str)->list[dict]:
    out=[]
    for p in sorted(project.glob(pattern)):
        try:data=json.loads(p.read_text(encoding="utf-8"))
        except Exception:continue
        for item in data if isinstance(data,list) else [data]:
            if isinstance(item,dict):out.append(item)
    return out

def walk(v):
    if isinstance(v,dict):
        yield v
        for child in v.values():yield from walk(child)
    elif isinstance(v,list):
        for child in v:yield from walk(child)

def fragment_index(project:Path)->dict[str,dict]:
    out={};root=project/"00_method"/"capture"
    if not root.exists():return out
    for p in root.rglob("*.json"):
        try:data=json.loads(p.read_text(encoding="utf-8"))
        except Exception:continue
        for item in walk(data):
            iid=str(item.get("id") or "")
            if iid.startswith(("GF-","FRAG-","FIELD-")) or item.get("class") in {"fragment","field_fragment"}:out[iid]=item
    return out

def fragment_refs(item:dict)->set[str]:
    refs=set()
    for node in walk(item):
        for ref in node.get("input_refs") or []:
            if isinstance(ref,dict) and ref.get("id"):refs.add(str(ref["id"]))
            elif isinstance(ref,str):refs.add(ref)
        for key in ("fragment_ids","origin_fragment_ids","input_fragment_ids"):
            refs|={str(x) for x in node.get(key) or []}
    return refs

def downstream_fragment_refs(project:Path)->set[str]:
    patterns=("01_arcs/*/claims/*.json","06_bridges/*.json","09_output/side_stories/*.json","09_output/illustrations/*.json","09_output/arc_recaps/*.json")
    refs=set()
    for pattern in patterns:
        for item in records(project,pattern):refs|=fragment_refs(item)
    return refs

def text_payload(item:dict)->str:
    out=[]
    for key in ("claim","bounded_by","notes","text","raw_text","caption","summary"):
        value=item.get(key)
        if isinstance(value,str):out.append(value)
        elif isinstance(value,dict):out.extend(str(v) for v in value.values() if isinstance(v,str))
    return " ".join(out)

def density_signals(claims:list[dict],fragments:dict[str,dict],markdown:str)->list[dict]:
    blocks=re.split(r"\n\s*\n",markdown);out=[]
    for claim in claims:
        cid=str(claim.get("id") or "");marker=f"[claim:{cid}]";block=next((b for b in blocks if marker.lower() in b.lower()),"")
        if not block:continue
        source=text_payload(claim)+" "+" ".join(text_payload(fragments[f]) for f in fragment_refs(claim) if f in fragments);sw=len(WORD.findall(source));rw=len(WORD.findall(MARKER.sub("",block)))
        if not sw:continue
        ratio=rw/sw;warning="compression_risk" if ratio<0.45 else "stylistic_padding_risk" if ratio>3 else None;out.append({"claim_id":cid,"source_words":sw,"rendered_words":rw,"ratio":round(ratio,3),"warning":warning})
    return out

def side_story_overlap(project:Path,scaffold:dict)->list[dict]:
    spine={str(cid) for arc in scaffold.get("arcs",[]) for cid in arc.get("spine_claim_ids",[])};out=[]
    for story in records(project,"09_output/side_stories/*.json"):
        claims={str(x) for x in (story.get("lineage") or {}).get("claim_ids",[])};overlap=sorted(claims&spine)
        if overlap:
            place=story.get("placement") or {};out.append({"side_story_id":story.get("id"),"section_anchor":place.get("section_anchor") or place.get("subsection_ref"),"spine_overlap":overlap,"overlap_ratio":round(len(overlap)/len(claims),3) if claims else 0,"review":"distinct_angle_required" if claims==set(overlap) else "partial_overlap"})
    return out

def reciprocal_coverage_check(project:Path,scaffold:dict,markdown:str,instrumentation_complete:bool=False)->dict:
    claims=records(project,"01_arcs/*/claims/*.json");ids={str(c["id"]) for c in claims if c.get("id")};seen=[m.group(1) for m in MARKER.finditer(markdown)];counts={cid:seen.count(cid) for cid in ids};covered=sorted(cid for cid,n in counts.items() if n);absent=sorted(ids-set(covered));fragments=fragment_index(project);used=downstream_fragment_refs(project);unref=sorted(set(fragments)-used);density=density_signals(claims,fragments,markdown)
    return {"project":project.name,"instrumentation_complete":instrumentation_complete,"explicitly_covered_claims":covered,"unused_claims":absent if instrumentation_complete else [],"coverage_unknown_legacy":[] if instrumentation_complete else absent,"over_mentioned":sorted(cid for cid,n in counts.items() if n>2),"mention_count":{cid:n for cid,n in sorted(counts.items()) if n},"referenced_fragments":sorted(set(fragments)&used),"unreferenced_fragments":unref,"unused_fragments":unref if instrumentation_complete else [],"coverage_unknown_legacy_fragments":[] if instrumentation_complete else unref,"side_story_claim_overlap":side_story_overlap(project,scaffold),"density_signals":density,"density_warnings":[x for x in density if x["warning"]],"notes":["Legacy prose without claim markers is unknown coverage, not automatically unused.","Fragments are considered referenced by claims, bridges, side stories, illustrations or arc recaps.","Unreferenced legacy fragments are unknown coverage until instrumentation is declared complete.","More than two direct citations is a callback-review signal.","Density warnings are advisory only and never block narrative output."]}

def main()->int:
    ap=argparse.ArgumentParser();ap.add_argument("--project",required=True);ap.add_argument("--run",type=int,required=True);ap.add_argument("--canonical");ap.add_argument("--instrumentation-complete",action="store_true");ap.add_argument("--output");a=ap.parse_args();repo=Path(__file__).resolve().parents[1];project=Path(a.project);project=project if project.is_absolute() else repo/project
    scaffold=json.loads((project/"09_output/story_scaffold.json").read_text(encoding="utf-8"));canonical=Path(a.canonical) if a.canonical else canonical_markdown_path(project);canonical=canonical if canonical.is_absolute() else repo/canonical;data=reciprocal_coverage_check(project,scaffold,canonical.read_text(encoding="utf-8"),a.instrumentation_complete);output=Path(a.output) if a.output else project/"08_questions"/f"coverage_gaps_run{a.run}.json";output=output if output.is_absolute() else repo/output;output.parent.mkdir(parents=True,exist_ok=True);output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    append_entry(repo,a.run,"Contrôle réciproque scaffold",[str(output.relative_to(repo))],"scaffold + manuscrit canonique",f"OK — explicit={len(data['explicitly_covered_claims'])}, legacy_unknown={len(data['coverage_unknown_legacy'])}, over_mentioned={len(data['over_mentioned'])}",details=[f"fragments référencés : {len(data['referenced_fragments'])}",f"fragments legacy non référencés : {len(data['coverage_unknown_legacy_fragments'])}",f"warnings densité : {len(data['density_warnings'])}"]);print(output.relative_to(repo));return 0
if __name__=="__main__":raise SystemExit(main())
