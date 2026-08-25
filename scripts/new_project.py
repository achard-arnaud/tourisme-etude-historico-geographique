#!/usr/bin/env python3
import argparse,json
from pathlib import Path
HILS=["HIL-01_institutions-chronology","HIL-02_geography-environment","HIL-03_economy-infrastructure","HIL-04_society-demography","HIL-05_religion-culture-legitimacy","HIL-06_security-coercion","HIL-07_regional-global-system","HIL-08_historiography-bias"]
DIRS=["00_method","01_arcs","02_hil","03_wiki/people","03_wiki/places","03_wiki/institutions","03_wiki/concepts","03_wiki/commodities","03_wiki/artifacts","04_graph","05_sources","06_bridges","07_drifts","08_questions","09_output/side_stories","09_output/arc_recaps","09_output/map_assets"]
def main():
    p=argparse.ArgumentParser();p.add_argument('--name',required=True);p.add_argument('--output',required=True);a=p.parse_args();root=Path(a.output);root.mkdir(parents=True,exist_ok=True)
    for rel in DIRS:
        d=root/rel;d.mkdir(parents=True,exist_ok=True);(d/'.gitkeep').touch()
    for hil in HILS:
        d=root/'02_hil'/hil;d.mkdir(parents=True,exist_ok=True);(d/'.gitkeep').touch()
    (root/'README.md').write_text(f"# {a.name}\n\nHistorico-geographic study project.\n",encoding='utf-8')
    (root/'project.json').write_text(json.dumps({'name':a.name,'method':'tourisme-etude-historico-geographique','version':3},indent=2)+'\n',encoding='utf-8')
    (root/'09_output'/'report.md').write_text(f"# {a.name}\n",encoding='utf-8')
    profile=json.loads((Path(__file__).resolve().parents[1]/'reader_profiles'/'educated_generalist.json').read_text(encoding='utf-8'))
    (root/'00_method'/'reader_profile.json').write_text(json.dumps(profile,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (root/'00_method'/'reader_contract.json').write_text(json.dumps({'audience':'intermediate','language':'fr','tone':'analytical guide','register':'educated generalist','length_budget':'standard','reading_context':'long-form travel reader'},indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    state={'schema_version':1,'baseline_markdown':'09_output/report.md','delta_markdown':'09_output/report.md','canonical_markdown':'09_output/report.md','reader_markdown':'09_output/report.md','composition':{'side_story_coverage_required':False,'require_arc_recaps':False,'graph_preflight_required':True}}
    (root/'00_method'/'output_state.json').write_text(json.dumps(state,indent=2)+'\n',encoding='utf-8')
    manifest=json.loads((Path(__file__).resolve().parents[1]/'templates'/'run-manifest.json').read_text(encoding='utf-8'));manifest['project_roots']=[str(root)]
    (root/'00_method'/'run_manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (root/'05_sources'/'source_register.json').write_text('[]\n',encoding='utf-8');(root/'04_graph'/'nodes.jsonl').write_text('',encoding='utf-8');(root/'04_graph'/'edges.jsonl').write_text('',encoding='utf-8');print(root)
if __name__=='__main__':main()
