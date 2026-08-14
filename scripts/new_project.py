#!/usr/bin/env python3
import argparse, json
from pathlib import Path

DIRS=["00_method","01_arcs","02_hil","03_wiki/people","03_wiki/places","03_wiki/institutions","03_wiki/concepts","03_wiki/commodities","03_wiki/artifacts","04_graph","05_sources","06_bridges","07_drifts","08_questions","09_output"]

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--name',required=True)
    p.add_argument('--output',required=True)
    a=p.parse_args()
    root=Path(a.output)
    root.mkdir(parents=True,exist_ok=True)
    for rel in DIRS: (root/rel).mkdir(parents=True,exist_ok=True)
    (root/'README.md').write_text(f"# {a.name}\n\nHistorico-geographic study project.\n",encoding='utf-8')
    (root/'project.json').write_text(json.dumps({'name':a.name,'method':'tourisme-etude-historico-geographique','version':1},indent=2),encoding='utf-8')
    (root/'05_sources'/'source_register.json').write_text('[]\n',encoding='utf-8')
    (root/'04_graph'/'nodes.jsonl').write_text('',encoding='utf-8')
    (root/'04_graph'/'edges.jsonl').write_text('',encoding='utf-8')
    print(root)

if __name__=='__main__': main()
