#!/usr/bin/env python3
"""Pre-edit graph-light endpoint and tagged-reference resolution gate."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

def _frontmatter_slug(path:Path):
    text=path.read_text(encoding="utf-8"); m=re.match(r"^---\n(.*?)\n---",text,re.S)
    if not m:return None
    for line in m.group(1).splitlines():
        if line.startswith("slug:"): return line.split(":",1)[1].strip().strip("\"'")
    return None

def _json_items(project:Path,pattern:str):
    out={}
    for p in project.glob(pattern):
        try:d=json.loads(p.read_text(encoding="utf-8"))
        except Exception:continue
        items=d if isinstance(d,list) else [d]
        for x in items:
            if isinstance(x,dict) and x.get("id"):out[str(x["id"])]=x
    return out

def validate_illustration_graph_consistency(project:Path,edges:list[dict],illustrations:dict,claims:dict)->list[str]:
    """L0: compare only scalar IDs/arc refs for ILLUSTRATED_BY edges."""
    errors=[]
    for edge in edges:
        if edge.get("relation")!="ILLUSTRATED_BY":continue
        illustration=illustrations.get(str(edge.get("to")))
        claim=claims.get(str(edge.get("from")))
        if not illustration or not claim:continue
        placed=(illustration.get("placement") or {}).get("arc_ref")
        owned=claim.get("arc")
        if placed!=owned:
            errors.append(f"illustration {edge.get('to')} placed in {placed} but illustrates claim {edge.get('from')} owned by {owned}")
    return errors

def validate_graph_links(project:Path):
    errors=[]; warnings=[]; graph=project/"04_graph"; nodes=set(); node_count=0; edges=[]; seen_edges=set()
    claims=_json_items(project,"01_arcs/*/claims/*.json")
    bridges=_json_items(project,"06_bridges/*.json")
    sources=_json_items(project,"05_sources/source_register*.json")
    illustrations=_json_items(project,"09_output/illustrations/*.json")
    for p in graph.glob("nodes*.jsonl"):
        for n,line in enumerate(p.read_text(encoding="utf-8").splitlines(),1):
            if not line.strip():continue
            node_count+=1
            try:d=json.loads(line)
            except Exception as exc: errors.append(f"invalid graph node {p}:{n}: {exc}");continue
            nid=d.get("id")
            if not nid: errors.append(f"graph node missing id {p}:{n}")
            elif nid in nodes: errors.append(f"duplicate graph node id {nid}")
            else:nodes.add(nid)
    known=set(nodes)|set(claims)|set(bridges)
    for p in (project/"03_wiki").rglob("*.md"):
        slug=_frontmatter_slug(p)
        if slug:known.add(slug)
    known|=set(_json_items(project,"09_output/side_stories/*.json"))|set(_json_items(project,"09_output/arc_recaps/*.json"))|set(illustrations)
    for p in graph.glob("edges*.jsonl"):
        for n,line in enumerate(p.read_text(encoding="utf-8").splitlines(),1):
            if not line.strip():continue
            try:e=json.loads(line)
            except Exception as exc: errors.append(f"invalid graph edge {p}:{n}: {exc}");continue
            edges.append(e); key=(e.get("from"),e.get("relation"),e.get("to"))
            if key in seen_edges:errors.append(f"duplicate graph edge {key!r} at {p.name}:{n}")
            seen_edges.add(key)
            for endpoint in ("from","to"):
                if e.get(endpoint) not in known: errors.append(f"unresolved graph fragment {e.get(endpoint)!r} at {p.name}:{n}")
            for field,valid in (("claim_ids",claims),("bridge_ids",bridges),("source_ids",sources)):
                values=e.get(field,[])
                if not isinstance(values,list):errors.append(f"graph edge {field} must be list at {p.name}:{n}");continue
                for value in values:
                    if value not in valid:errors.append(f"unresolved graph {field[:-1]} {value!r} at {p.name}:{n}")
            for bridge_id in e.get("bridge_ids",[]):
                bridge=bridges.get(bridge_id,{})
                if bridge and (e.get("from")!=bridge.get("from_claim") or e.get("to")!=bridge.get("to_claim")):
                    errors.append(f"graph edge endpoints do not match tagged bridge {bridge_id} at {p.name}:{n}")
    errors+=validate_illustration_graph_consistency(project,edges,illustrations,claims)
    return errors,warnings,node_count,len(edges)

def main():
    project=Path(sys.argv[1] if len(sys.argv)>1 else "."); errors,warnings,nodes,edges=validate_graph_links(project)
    for x in warnings:print("WARN:",x,file=sys.stderr)
    for x in errors:print("ERROR:",x,file=sys.stderr)
    if errors:return 1
    print(f"GRAPH LINK AUDIT OK: {nodes} explicit nodes, {edges} edges, 0 unresolved endpoints/tags")
    return 0
if __name__=="__main__":raise SystemExit(main())
