#!/usr/bin/env python3
"""Run16 hard gates for Mihintale, Abhayagiri, militarisation and Horton field intakes."""
from __future__ import annotations
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'examples/sri_lanka_pre_1948'
POST=ROOT/'examples/sri_lanka_post_1948'

def load(path):return json.loads(path.read_text(encoding='utf-8'))
def claims(project):
    out=[]
    for p in project.glob('01_arcs/*/claims/C-R16-*.json'):
        try:out.append((p,load(p)))
        except Exception:pass
    return out

def main():
    errors=[]
    pre_sources=load(PRE/'05_sources/source_register_run16_field.json')
    post_sources=load(POST/'05_sources/source_register_run16_field.json')
    sources=pre_sources+post_sources
    tiers={s.get('tier') for s in sources}
    for tier in {'T0','T2','T4','T5'}:
        if tier not in tiers:errors.append(f'missing required Run16 source tier {tier}')
    afp=[s for s in sources if 'AFP' in str(s.get('id','')) or 'AFP' in str(s.get('author_or_institution',''))]
    if len(afp)!=1:errors.append(f'AFP source-family count={len(afp)}; expected exactly one registration')
    field=next((s for s in pre_sources if s.get('id')=='FIELD-MIHINTALE-STELE-2024'),{})
    if field.get('tier')!='T0' or '2024' not in str(field.get('scope','')) or 'third-century' not in str(field.get('limitations','')):
        errors.append('Mihintale stele must be T0 for 2024 and explicitly bounded for antiquity')
    positioned={'HRW-MILITARY-LAND-2018','UKHO-JAFFNA-CHECKPOINTS-2025','SL-ARMY-JAFFNA-LAND-2025','TAMIL-GUARDIAN-VALIKAMAM-2026'}
    for s in post_sources:
        if s.get('id') in positioned and not s.get('limitations'):errors.append(f"{s.get('id')}: source position/limitation missing")
    contradictions=load(POST/'00_method/capture/run16_contradictions.json')
    topics={c.get('topic') for c in contradictions}
    if len(contradictions)!=2 or not {'worlds_end_drop','protected_area_share'}.issubset(topics):errors.append('Run16 requires exactly the two field contradiction records')
    bridge=load(POST/'06_bridges/B-R16-MIL-INTERNAL-COMPARATOR-001.json')
    if bridge.get('transportability')!='mechanism':errors.append('internal comparator transportability must be mechanism at most')
    if len(bridge.get('confounders') or [])<5 or not bridge.get('bounded_by'):errors.append('internal comparator requires populated confounders and bounded_by')
    all_claims=claims(PRE)+claims(POST)
    for p,c in claims(PRE):
        if c.get('arc')=='A02c_anuradhapura_and_the_mahavihara' and c.get('type')=='tradition' and c.get('confidence') in {'A','B'}:
            errors.append(f'{p.name}: ancient tradition exceeds confidence C')
    abh=next((c for _,c in claims(PRE) if c.get('id')=='C-R16-ABH-DATE-001'),{})
    if abh.get('confidence')!='C' or not abh.get('bounded_by'):errors.append('Abhayagiri provisional dating must remain C with bounded_by')
    checkpoint=next((c for _,c in claims(POST) if c.get('id')=='C-R16-MIL-CHECKPOINT-001'),{})
    if checkpoint.get('confidence')!='C' or not checkpoint.get('bounded_by'):errors.append('checkpoint reinstatement must remain C and family-bounded')
    for p,c in claims(POST):
        if 'BLOG-UPEC-HORTON-2026' in (c.get('source_ids') or []):errors.append(f'{p.name}: T5 visitor blog cannot close a claim')
    for arc_path in [PRE/'01_arcs/A02c_anuradhapura_and_the_mahavihara/ARC.md',POST/'01_arcs/A17_highland_conservation/ARC.md']:
        if 'evidence_status: partial' not in arc_path.read_text(encoding='utf-8'):errors.append(f'{arc_path}: must remain partial')
    side=PRE/'09_output/side_stories'
    kinds={load(p).get('kind') for p in side.glob('SS-R16-MIH-*.json')}
    if not {'method','object_focus','portrait'}.issubset(kinds):errors.append('Mihintale method/object_focus/portrait side stories missing')
    if not (POST/'07_drifts/run16_militarisation_source_positioning.md').exists():errors.append('drift-first militarisation audit missing')
    qcount=0
    for qpath in [PRE/'08_questions/run16_field_open_questions.md',POST/'08_questions/run16_field_open_questions.md']:
        text=qpath.read_text(encoding='utf-8');qcount+=len(re.findall(r'^\d+\.\s',text,re.M))
    if qcount<=len(all_claims):errors.append(f'Run16 expected more questions than claims: {qcount} questions <= {len(all_claims)} claims')
    if '2026-09-19' not in (PRE/'08_questions/run16_field_open_questions.md').read_text(encoding='utf-8'):errors.append('Abhayagiri one-month review date missing')
    for err in errors:print('ERROR:',err,file=sys.stderr)
    if errors:return 1
    print(f'RUN16 INTAKE AUDIT OK: {qcount} questions > {len(all_claims)} claims; tiers {sorted(tiers)}; 2 contradictions; AFP single-family; comparator bounded')
    return 0
if __name__=='__main__':raise SystemExit(main())
