#!/usr/bin/env python3
from __future__ import annotations
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'examples/sri_lanka_pre_1948'; POST=ROOT/'examples/sri_lanka_post_1948'

def load_json(p): return json.loads(p.read_text(encoding='utf-8'))
def fail(msgs):
    for m in msgs: print('ERROR:',m,file=sys.stderr)
    return 1 if msgs else 0

def main():
    errors=[]
    pre_src=load_json(PRE/'05_sources/source_register_run16_field.json')
    post_src=load_json(POST/'05_sources/source_register_run16_field.json')
    src=pre_src+post_src
    tiers={s.get('tier') for s in src}
    for tier in {'T0','T2','T4','T5'}:
        if tier not in tiers: errors.append(f'Run16 missing required source tier {tier}')
    afp=[s for s in src if 'AFP' in (s.get('id') or '') or 'AFP' in (s.get('author_or_institution') or '')]
    if len(afp)!=1: errors.append(f'AFP source family must be registered once, got {len(afp)}')
    if afp and afp[0].get('id')!='AFP-ABHAYAGIRI-BRONZES-2026-08': errors.append('unexpected AFP source id')
    field=next((s for s in pre_src if s.get('id')=='FIELD-MIHINTALE-STELE-2024'),None)
    if not field or field.get('tier')!='T0': errors.append('Mihintale field stele missing T0 source record')
    claims=list((PRE/'01_arcs/A02c_anuradhapura_and_the_mahavihara/claims').glob('C-R16-*.json'))
    for p in claims:
        c=load_json(p)
        if c.get('type')=='tradition' and c.get('confidence') in {'A','B'}: errors.append(f'{c.get("id")}: ancient tradition above C ceiling')
        if c.get('id')=='C-R16-ABH-DATE-001':
            if c.get('confidence')!='C' or not c.get('bounded_by'): errors.append('Abhayagiri dating must remain C and bounded')
    contradictions=load_json(POST/'00_method/capture/run16_contradictions.json')
    if len(contradictions)<2: errors.append('Run16 requires two contradiction records')
    bridge=load_json(POST/'06_bridges/B-R16-MIL-INTERNAL-COMPARATOR-001.json')
    if bridge.get('transportability')!='mechanism': errors.append('internal military comparator transportability must be mechanism')
    if len(bridge.get('confounders') or [])<5: errors.append('internal military comparator requires populated confounders')
    if not bridge.get('bounded_by'): errors.append('internal military comparator requires bounded_by')
    kinds=set()
    for p in (PRE/'09_output/side_stories').glob('SS-R16-*.json'):
        kinds.add(load_json(p).get('kind'))
    for kind in {'method','object_focus','portrait'}:
        if kind not in kinds: errors.append(f'Run16 missing side-story kind {kind}')
    qcount=0
    for p in [PRE/'08_questions/run16_field_open_questions.md',POST/'08_questions/run16_field_open_questions.md']:
        text=p.read_text(encoding='utf-8') if p.exists() else ''
        qcount+=len(re.findall(r'^\d+\.',text,re.M))
    claimcount=len(list(PRE.rglob('C-R16-*.json')))+len(list(POST.rglob('C-R16-*.json')))
    if qcount<=claimcount: errors.append(f'Run16 should remain question-heavy: questions={qcount}, claims={claimcount}')
    if not (POST/'01_arcs/A17_highland_conservation/ARC.md').exists(): errors.append('A17 highland conservation arc missing')
    if errors: return fail(errors)
    print(f'RUN16 FIELD AUDIT OK: tiers={sorted(tiers)}; questions={qcount} > claims={claimcount}; contradictions={len(contradictions)}; comparator bounded; ancient ceiling enforced')
    return 0
if __name__=='__main__': raise SystemExit(main())
