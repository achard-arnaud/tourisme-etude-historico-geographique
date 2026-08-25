#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'examples/sri_lanka_pre_1948'
POST=ROOT/'examples/sri_lanka_post_1948'

def load(p): return json.loads(p.read_text(encoding='utf-8'))

def main():
    errors=[]
    pre_sources=load(PRE/'05_sources/source_register_run16_field.json')
    post_sources=load(POST/'05_sources/source_register_run16_field.json')+load(POST/'05_sources/source_register_run16_comparator.json')
    tiers={s.get('tier') for s in pre_sources+post_sources}
    for tier in {'T0','T2','T4','T5'}:
        if tier not in tiers: errors.append(f'missing required Run16 tier {tier}')
    afp=[s for s in pre_sources if (s.get('id') or '').startswith('AFP-ABHAYAGIRI')]
    if len(afp)!=1: errors.append(f'Abhayagiri AFP source-family count={len(afp)}; expected exactly 1')
    field=next((s for s in pre_sources if s.get('id')=='FIELD-MIHINTALE-STELE-2024'),None)
    limitations=(field or {}).get('limitations','').lower();scope=(field or {}).get('scope','')
    if not field or field.get('tier')!='T0' or '2024' not in scope or 'antiquity' not in limitations or ('only' not in limitations and 'not primary' not in limitations):
        errors.append('Mihintale field source must be T0 for 2024 and explicitly bounded for antiquity')
    trad=load(PRE/'01_arcs/A02c_anuradhapura_and_mahavihara/claims/C-R16-MIH-TRAD-002.json')
    if trad.get('confidence') not in {'C','D','U'} or trad.get('type')!='tradition':
        errors.append('third-century BCE Mihintale sequence must remain tradition at confidence C or lower')
    abh=load(PRE/'01_arcs/A02c_anuradhapura_and_mahavihara/claims/C-R16-ABH-002.json')
    if abh.get('confidence')!='C' or not abh.get('bounded_by'):
        errors.append('Abhayagiri stylistic dating must remain C and bounded')
    contradictions=load(POST/'07_drifts/run16_contradictions.json')
    ids={r.get('id') for r in contradictions}
    for cid in {'CON-R16-HOR-WORLDS-END-001','CON-R16-PROTECTED-AREA-SHARE-002'}:
        if cid not in ids: errors.append(f'missing contradiction {cid}')
    bridge=load(POST/'06_bridges/B-R16-MIL-INTERNAL-COMPARATOR-001.json')
    if bridge.get('transportability')!='mechanism' or not bridge.get('bounded_by') or len(bridge.get('confounders') or [])<5:
        errors.append('internal military comparator must be mechanism-only with bounded_by and populated confounders')
    for path,kind in [
      (PRE/'09_output/side_stories/SS-R16-MIH-OBJECT-001.json','object_focus'),
      (PRE/'09_output/side_stories/SS-R16-MIH-PORTRAIT-001.json','portrait'),
      (PRE/'09_output/side_stories/SS-R16-MIH-METHOD-001.json','method')]:
        if not path.exists() or load(path).get('kind')!=kind: errors.append(f'missing Run16 side-story kind {kind}')
    pre_q=(PRE/'08_questions/run16_field_open_questions.md').read_text(encoding='utf-8')
    post_q=(POST/'08_questions/run16_field_open_questions.md').read_text(encoding='utf-8')
    qcount=len(re.findall(r'^\d+\.',pre_q,flags=re.M))+len(re.findall(r'^\d+\.',post_q,flags=re.M))
    claim_count=sum(1 for p in list(PRE.rglob('C-R16-*.json'))+list(POST.rglob('C-R16-*.json')) if '/claims/' in p.as_posix())
    if qcount<=claim_count: errors.append(f'Run16 expected more questions than claims; questions={qcount} claims={claim_count}')
    if qcount<3: errors.append('Run16 requires at least three open questions')
    for arc in [PRE/'01_arcs/A02c_anuradhapura_and_mahavihara/ARC.md',POST/'01_arcs/A17_highland_conservation/ARC.md']:
        if not re.search(r'(?mi)^\s*evidence_status\s*:\s*partial\s*$',arc.read_text(encoding='utf-8')): errors.append(f'{arc}: must remain partial')
    checkpoint=load(POST/'01_arcs/A09_electoral_realignment_2024_2026/claims/C-R16-MIL-CHECKPOINT-004.json')
    if checkpoint.get('confidence')!='C' or 'no corroborating' not in (checkpoint.get('bounded_by') or '').lower():
        errors.append('checkpoint report must remain C with explicit non-corroboration bound')
    for err in errors: print('ERROR:',err,file=sys.stderr)
    if errors:return 1
    print(f'RUN16 FIELD AUDIT OK: tiers={sorted(tiers)} questions={qcount} claims={claim_count}; AFP family=1; contradictions=2; internal comparator bounded')
    return 0
if __name__=='__main__': raise SystemExit(main())
