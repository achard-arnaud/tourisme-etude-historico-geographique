#!/usr/bin/env python3
"""Pre-edit graph-light endpoint and tagged-reference resolution gate."""
from __future__ import annotations
import argparse, json, re, sys
from collections import Counter, defaultdict
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

def graph_diagnostics(project:Path)->dict:
    """Return report-only claim/bridge density signals grouped by evidence arc."""
    claims=_json_items(project,"01_arcs/*/claims/*.json")
    bridges=_json_items(project,"06_bridges/*.json")
    edges=[]
    for p in (project/"04_graph").glob("edges*.jsonl"):
        for line in p.read_text(encoding="utf-8").splitlines():
            if line.strip():
                edges.append(json.loads(line))
    refs=Counter(); incoming=Counter(); outgoing=Counter(); bridge_refs=Counter()
    for edge in edges:
        source=str(edge.get("from") or ""); target=str(edge.get("to") or "")
        if source in claims:outgoing[source]+=1;refs[source]+=1
        if target in claims:incoming[target]+=1;refs[target]+=1
        for claim_id in edge.get("claim_ids",[]):
            if claim_id in claims:refs[claim_id]+=1
        for bridge_id in edge.get("bridge_ids",[]):
            if bridge_id in bridges:bridge_refs[bridge_id]+=1
    by_arc=defaultdict(list)
    for claim_id,claim in claims.items():
        by_arc[str(claim.get("arc") or "unassigned")].append(claim_id)
    arcs=[]
    for arc,ids in sorted(by_arc.items()):
        linked=[claim_id for claim_id in ids if refs[claim_id]]
        arcs.append({
            "arc":arc,"claims":len(ids),"linked_claims":len(linked),
            "unlinked_claims":sorted(set(ids)-set(linked)),
            "mean_graph_references":round(sum(refs[x] for x in ids)/max(1,len(ids)),2),
        })
    return {
        "schema_version":1,"project":str(project),"claims":len(claims),"bridges":len(bridges),
        "edges":len(edges),"arcs":arcs,
        "orphan_claims":sorted(claim_id for claim_id in claims if not refs[claim_id]),
        "unreferenced_bridges":sorted(bridge_id for bridge_id in bridges if not bridge_refs[bridge_id]),
        "claim_degrees":{
            claim_id:{"incoming":incoming[claim_id],"outgoing":outgoing[claim_id],"references":refs[claim_id]}
            for claim_id in sorted(claims)
        },
    }

def main():
    parser=argparse.ArgumentParser();parser.add_argument("project",nargs="?",type=Path,default=Path("."));parser.add_argument("--diagnostics",type=Path)
    args=parser.parse_args();project=args.project; errors,warnings,nodes,edges=validate_graph_links(project)
    for x in warnings:print("WARN:",x,file=sys.stderr)
    for x in errors:print("ERROR:",x,file=sys.stderr)
    if errors:return 1
    if args.diagnostics:
        args.diagnostics.parent.mkdir(parents=True,exist_ok=True)
        args.diagnostics.write_text(json.dumps(graph_diagnostics(project),ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(f"GRAPH LINK AUDIT OK: {nodes} explicit nodes, {edges} edges, 0 unresolved endpoints/tags")
    return 0
if __name__=="__main__":raise SystemExit(main())
