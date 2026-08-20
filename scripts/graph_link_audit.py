#!/usr/bin/env python3
"""Pre-edit graph-light fragment resolution gate."""
from __future__ import annotations
import json, re, sys
from pathlib import Path

def _frontmatter_slug(path:Path):
    text=path.read_text(encoding="utf-8"); m=re.match(r"^---\n(.*?)\n---",text,re.S)
    if not m:return None
    for line in m.group(1).splitlines():
        if line.startswith("slug:"): return line.split(":",1)[1].strip().strip("\"'")
    return None
def _json_ids(project:Path,pattern:str):
    out=set()
    for p in project.glob(pattern):
        try:d=json.loads(p.read_text(encoding="utf-8"))
        except Exception:continue
        items=d if isinstance(d,list) else [d]
        out|={str(x["id"]) for x in items if isinstance(x,dict) and x.get("id")}
    return out
def validate_graph_links(project:Path):
    errors=[]; warnings=[]; graph=project/"04_graph"; nodes=set(); node_count=0; edges=[]
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
    known=set(nodes)
    for p in (project/"03_wiki").rglob("*.md"):
        slug=_frontmatter_slug(p)
        if slug:known.add(slug)
    known|=_json_ids(project,"01_arcs/*/claims/*.json")|_json_ids(project,"06_bridges/*.json")|_json_ids(project,"09_output/side_stories/*.json")|_json_ids(project,"09_output/arc_recaps/*.json")
    for p in graph.glob("edges*.jsonl"):
        for n,line in enumerate(p.read_text(encoding="utf-8").splitlines(),1):
            if not line.strip():continue
            try:e=json.loads(line)
            except Exception as exc: errors.append(f"invalid graph edge {p}:{n}: {exc}");continue
            edges.append(e)
            for endpoint in ("from","to"):
                if e.get(endpoint) not in known: errors.append(f"unresolved graph fragment {e.get(endpoint)!r} at {p.name}:{n}")
    return errors,warnings,node_count,len(edges)
def main():
    project=Path(sys.argv[1] if len(sys.argv)>1 else "."); errors,warnings,nodes,edges=validate_graph_links(project)
    for x in warnings:print("WARN:",x,file=sys.stderr)
    for x in errors:print("ERROR:",x,file=sys.stderr)
    if errors:return 1
    print(f"GRAPH LINK AUDIT OK: {nodes} explicit nodes, {edges} edges, 0 unresolved")
    return 0
if __name__=="__main__":raise SystemExit(main())
