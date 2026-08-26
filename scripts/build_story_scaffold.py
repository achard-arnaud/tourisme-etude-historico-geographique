#!/usr/bin/env python3
"""Build a compact, deterministic narrative topology before reader drafting."""
from __future__ import annotations
import argparse,json,re
from collections import Counter,defaultdict,deque
from pathlib import Path
from arc_recap_contract import load_arc_recaps
from illustration_contract import load_illustrations
from map_asset_contract import load_map_assets
from side_story_contract import load_side_stories

SCHEMA_VERSION="1.0"
CONFIDENCE_ORDER={"A":0,"B":1,"C":2,"D":3,"U":4}
ROLE_ORDER={"driver":0,"mechanism":1,"amplifier":2,"constraint":3,"outcome":4,"context":5,"none":6}

def _records(project:Path,pattern:str):
    out=[]
    for path in sorted(project.glob(pattern)):
        try:data=json.loads(path.read_text(encoding="utf-8"))
        except Exception:continue
        for item in (data if isinstance(data,list) else [data]):
            if isinstance(item,dict) and item.get("id"):out.append(item)
    return out

def _arc_status(path:Path)->str:
    text=path.read_text(encoding="utf-8")
    match=re.search(r"(?mi)^\s*-?\s*evidence_status\s*:\s*([a-z0-9_-]+)",text)
    return match.group(1) if match else "researched"

def _components(edges:list[dict])->list[list[str]]:
    graph=defaultdict(set)
    for edge in edges:
        left,right=edge.get("from"),edge.get("to")
        if left and right:graph[left].add(right);graph[right].add(left)
    seen=set();components=[]
    for node in sorted(graph):
        if node in seen:continue
        queue=deque([node]);seen.add(node);component=[]
        while queue:
            current=queue.popleft();component.append(current)
            for nxt in sorted(graph[current]-seen):seen.add(nxt);queue.append(nxt)
        components.append(sorted(component))
    return sorted(components,key=lambda x:(-len(x),x))

def build_scaffold(project:Path)->dict:
    claims=_records(project,"01_arcs/*/claims/*.json");claim_by_id={x["id"]:x for x in claims}
    bridges=_records(project,"06_bridges/*.json");edges=_records(project,"04_graph/edges*.jsonl")
    if not edges:
        for path in sorted((project/"04_graph").glob("edges*.jsonl")):
            edges.extend(json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    stories=[x for _,x in load_side_stories(project)];recaps=[x for _,x in load_arc_recaps(project)]
    maps=[x for _,x in load_map_assets(project)];illustrations=[x for _,x in load_illustrations(project)]
    questions=_records(project,"08_questions/question_register.json")
    by_arc_claims=defaultdict(list);by_arc_questions=defaultdict(list);by_arc_stories=defaultdict(list);by_arc_recaps=defaultdict(list);by_arc_illustrations=defaultdict(list)
    for claim in claims:by_arc_claims[claim.get("arc","")].append(claim)
    for question in questions:by_arc_questions[question.get("arc","")].append(question)
    for story in stories:by_arc_stories[story.get("arc","")].append(story)
    for recap in recaps:by_arc_recaps[recap.get("arc","")].append(recap)
    for item in illustrations:by_arc_illustrations[(item.get("placement") or {}).get("arc_ref","")].append(item)
    bridge_by_arc=defaultdict(list)
    for bridge in bridges:
        for endpoint in (bridge.get("from_claim"),bridge.get("to_claim")):
            arc=(claim_by_id.get(endpoint) or {}).get("arc")
            if arc:bridge_by_arc[arc].append(bridge["id"])
    arcs=[]
    for arc_md in sorted((project/"01_arcs").glob("*/ARC.md")):
        arc=arc_md.parent.name;arc_claims=by_arc_claims[arc]
        spine=sorted((c for c in arc_claims if c.get("type") not in {"question","discarded_lead"}),key=lambda c:(ROLE_ORDER.get(c.get("causal_role"),9),CONFIDENCE_ORDER.get(c.get("confidence"),9),c["id"]))
        arcs.append({"arc":arc,"evidence_status":_arc_status(arc_md),"spine_claim_ids":[c["id"] for c in spine],"claim_count":len(arc_claims),"causal_roles":dict(sorted(Counter(c.get("causal_role","none") for c in arc_claims).items())),"bridge_ids":sorted(set(bridge_by_arc[arc])),"side_story_ids":[s["id"] for s in by_arc_stories[arc] if s.get("status") in {"validated","promoted"}],"candidate_side_story_ids":[s["id"] for s in by_arc_stories[arc] if s.get("status")=="candidate"],"arc_recap_ids":[r["id"] for r in by_arc_recaps[arc] if r.get("status") in {"validated","promoted"}],"illustration_ids":[x["id"] for x in by_arc_illustrations[arc] if x.get("status")=="reader_eligible"],"illustration_review_queue_ids":[x["id"] for x in by_arc_illustrations[arc] if x.get("status") in {"candidate","vision_validated"}],"open_question_ids":[q["id"] for q in by_arc_questions[arc] if q.get("status") in {"open","bounded","pending_external"}]})
    all_linked=set()
    for edge in edges:all_linked|={str(edge.get("from")),str(edge.get("to"))}
    unresolved_illustrations=[x["id"] for x in illustrations if (x.get("placement") or {}).get("target_status")!="resolved"]
    return {"schema_version":SCHEMA_VERSION,"class":"story_scaffold","project":project.name,"strategy":"global topology -> arc-local retrieval packs -> cross-arc stitch -> illustration pass -> coverage reconciliation","token_policy":{"global_pass":"IDs, counts and topology only","draft_pass":"hydrate only one arc plus adjacent bridges","final_pass":"hydrate unresolved coverage items, not the full corpus"},"coverage":{"claims":len(claims),"bridges":len(bridges),"graph_edges":len(edges),"side_stories":len(stories),"arc_recaps":len(recaps),"maps":len(maps),"illustrations":len(illustrations),"open_questions":sum(1 for q in questions if q.get("status") in {"open","bounded","pending_external"})},"diagnostics":{"graph_components":_components(edges),"graph_orphan_claim_ids":sorted(c["id"] for c in claims if c["id"] not in all_linked),"illustration_missing_target_ids":sorted(unresolved_illustrations)},"arcs":arcs}

def render_mermaid(data:dict,project:Path)->str:
    edges=[]
    for path in sorted((project/"04_graph").glob("edges*.jsonl")):
        edges.extend(json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    endpoints=sorted({str(e.get(key)) for e in edges for key in ("from","to") if e.get(key)})
    aliases={value:f"n{index}" for index,value in enumerate(endpoints)}
    lines=["flowchart TD",f"%% {data['coverage']['claims']} claims; {len(data['diagnostics']['graph_orphan_claim_ids'])} graph-orphan claims; {data['coverage']['illustrations']} illustrations"]
    for value in endpoints:
        label=value.replace('"',"'");lines.append(f'  {aliases[value]}["{label}"]')
    for edge in edges:
        relation=str(edge.get("relation") or "LINK").replace('"',"'")
        lines.append(f'  {aliases[str(edge["from"])]} -->|"{relation}"| {aliases[str(edge["to"])]}')
    return "\n".join(lines)+"\n"

def write_scaffold(project:Path)->dict:
    data=build_scaffold(project);root=project/"09_output";(root/"story_scaffold.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8");(root/"story_scaffold.mmd").write_text(render_mermaid(data,project),encoding="utf-8");return data

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--project",required=True);args=parser.parse_args();data=write_scaffold(Path(args.project));print(f"STORY SCAFFOLD OK: {len(data['arcs'])} arcs, {data['coverage']['claims']} claims, {data['coverage']['illustrations']} illustrations")
if __name__=="__main__":main()
