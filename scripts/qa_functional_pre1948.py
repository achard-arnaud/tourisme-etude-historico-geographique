#!/usr/bin/env python3
"""End-to-end mechanical regression baseline for the Sri Lanka pre-1948 fixture."""
from __future__ import annotations
import json,subprocess,sys
from pathlib import Path
from side_story_contract import validate_side_stories
from arc_recap_contract import assert_rendered_arc_recaps,validate_arc_recaps,load_arc_recaps,RENDERABLE
from graph_link_audit import validate_graph_links
REPO=Path(__file__).resolve().parents[1];PROJECT=REPO/'examples/sri_lanka_pre_1948'
BASELINE={'claims':9,'sources':44,'bridges':3,'wiki':3,'edges':4,'hils':8,'recaps':3}
def run(cmd):
    r=subprocess.run(cmd,cwd=REPO,text=True,capture_output=True)
    if r.returncode:
        if r.stdout:print(r.stdout,end='',file=sys.stderr)
        if r.stderr:print(r.stderr,end='',file=sys.stderr)
        raise RuntimeError('command failed: '+' '.join(cmd))
    return r
def main():
    errors=[]
    for rel in ['project.json','00_method/output_state.json','00_method/reader_profile.json','01_arcs','02_hil','03_wiki','04_graph/nodes.jsonl','04_graph/edges.jsonl','05_sources','06_bridges','07_drifts','08_questions/baseline_questions.md','09_output/report_v3_full.md','09_output/side_stories','09_output/arc_recaps']:
        if not (PROJECT/rel).exists():errors.append(f'missing {rel}')
    claims=list(PROJECT.glob('01_arcs/*/claims/*.json'));sources=[]
    for p in (PROJECT/'05_sources').glob('source_register*.json'):sources+=json.loads(p.read_text(encoding='utf-8'))
    bridges=list((PROJECT/'06_bridges').glob('*.json'));wiki=[p for p in (PROJECT/'03_wiki').rglob('*.md') if p.name.lower()!='readme.md'];edges=sum(1 for p in (PROJECT/'04_graph').glob('edges*.jsonl') for line in p.read_text(encoding='utf-8').splitlines() if line.strip())
    actual={'claims':len(claims),'sources':len(sources),'bridges':len(bridges),'wiki':len(wiki),'edges':edges}
    for key,value in actual.items():
        if value<BASELINE[key]:errors.append(f'{key} count regressed: {value} < baseline {BASELINE[key]}')
    hils=list((PROJECT/'02_hil').glob('HIL-*/baseline.json'))
    if len(hils)!=BASELINE['hils']:errors.append(f'HIL baseline count {len(hils)} != {BASELINE["hils"]}')
    se,sw,side_count,coverage=validate_side_stories(PROJECT);errors+=se+[f'unexpected side-story warning: {w}' for w in sw]
    if side_count<26:errors.append(f'side-story inventory too small: {side_count}')
    if coverage['untracked']!=0:errors.append(f"untracked side stories: {coverage['untracked']}")
    re,rw,recaps=validate_arc_recaps(PROJECT);errors+=re+[f'unexpected recap warning: {w}' for w in rw]
    if recaps<BASELINE['recaps']:errors.append(f'arc recap count regressed: {recaps} < baseline {BASELINE["recaps"]}')
    required_recaps=sum(1 for _,item in load_arc_recaps(PROJECT) if item.get('status') in RENDERABLE and (item.get('render') or {}).get('required_in_reader'))
    ge,gw,nodes,gedges=validate_graph_links(PROJECT);errors+=ge+[f'unexpected graph warning: {w}' for w in gw]
    if errors:
        for e in errors:print('ERROR:',e,file=sys.stderr)
        return 1
    try:
        run([sys.executable,'scripts/audit_skill.py','.']);run([sys.executable,'scripts/audit_workflow.py','--latest']);run([sys.executable,'scripts/qa_project.py',str(PROJECT)]);run([sys.executable,'scripts/qa_composition_pipeline.py',str(PROJECT)])
        rendered=run([sys.executable,'scripts/render_composed_reader.py','--project','pre']);metric=json.loads(rendered.stdout)[0];ret=float(metric['retention_vs_baseline_percent']);reader=(PROJECT/'09_output/report_v3_full.md').read_text(encoding='utf-8');rendered_recaps=assert_rendered_arc_recaps(PROJECT,reader)
        if ret<100:raise RuntimeError(f'retention {ret}%')
        if metric.get('arc_recaps')!=required_recaps or rendered_recaps!=required_recaps:raise RuntimeError(f'arc recap render mismatch: metric={metric.get("arc_recaps")}, rendered={rendered_recaps}, required={required_recaps}, registered={recaps}')
    except Exception as exc:print(f'ERROR: {exc}',file=sys.stderr);return 1
    print(f"PRE1948 FUNCTIONAL QA OK: {len(claims)} claims, {len(sources)} sources, {len(bridges)} bridges, {len(wiki)} wiki pages, {edges} graph edges/{nodes} nodes, {len(hils)} HIL baselines, {side_count} side stories ({coverage['tracked']}/{coverage['discovered']} tracked), {required_recaps}/{recaps} reader-required/registered arc recaps rendered, retention {ret}%");return 0
if __name__=='__main__':raise SystemExit(main())
