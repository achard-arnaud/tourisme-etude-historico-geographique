#!/usr/bin/env python3
"""Run17 hard gates: measure before explaining Kandy."""
from __future__ import annotations
import json,re,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'examples/sri_lanka_pre_1948'
POST=ROOT/'examples/sri_lanka_post_1948'

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def claim(project, cid):
    hits=list(project.glob(f'01_arcs/*/claims/{cid}.json'))
    return load(hits[0]) if hits else None

def main():
    errors=[]
    mpath=POST/'00_method/capture/run17_kandy_measurements.json'
    m=load(mpath)
    metrics=m.get('metrics') or []
    if len(metrics)<8: errors.append(f'measurement gate requires >=8 metric records, got {len(metrics)}')
    required={'M-R17-KDY-POP-MC','M-R17-KDY-POP-AGG','M-R17-KDY-POP-DIST','M-R17-KDY-GROWTH','M-R17-KDY-PGDP','M-R17-KDY-LAND','M-R17-KDY-MIGRATION','M-R17-KDY-EMPLOY','M-R17-KDY-TOURISM'}
    ids={x.get('id') for x in metrics}
    missing=sorted(required-ids)
    if missing: errors.append('missing measurement records: '+', '.join(missing))
    for row in metrics:
        for field in ('denominator','geography','period','source_definition','status'):
            if not row.get(field): errors.append(f"{row.get('id')}: missing metric field {field}")
    if m.get('hypothesis_status')!='D': errors.append('unqualified economic-success hypothesis must materialize as D')
    false_claim=claim(POST,'C-R17-KDY-ECON-FALSE-001')
    if not false_claim or false_claim.get('type')!='discarded_lead' or false_claim.get('confidence')!='D':
        errors.append('economic-success false lead claim missing or not D')
    func=claim(POST,'C-R17-KDY-FUNC-001')
    if not func or func.get('confidence') not in {'C','U'} or not func.get('bounded_by'):
        errors.append('narrow functional-node replacement hypothesis must remain bounded C/U')
    arc=(POST/'01_arcs/A19_kandy_second_city_paradox/ARC.md').read_text(encoding='utf-8')
    if 'measurement_gate: completed before explanatory claims' not in arc: errors.append('A19 measurement gate not explicit')
    if 'Never use “second city” without a denominator or function.' not in arc: errors.append('second-city denominator rule missing')
    pre_arc=(PRE/'01_arcs/A07b_kandyan_kingdom_and_defensive_interior/ARC.md').read_text(encoding='utf-8')
    if 'cross_reference: plantation sequence' not in pre_arc or 'do not narrate road/rail twice' not in pre_arc:
        errors.append('Kandy/plantation cross-reference missing or duplicate-narration gate absent')
    land=claim(PRE,'C-R17-KDY-LAND-001'); labour=claim(PRE,'C-R17-KDY-LABOUR-001')
    if not land or not labour: errors.append('two dispossession mechanisms must be materialized separately')
    elif set(land.get('source_ids',[]))==set(labour.get('source_ids',[])):
        errors.append('land alienation and labour-import mechanisms cannot collapse to identical evidence lineage')
    terrain=claim(PRE,'C-R17-KDY-TERRAIN-001')
    if not terrain or terrain.get('confidence') not in {'B','C','D','U'} or not terrain.get('bounded_by'):
        errors.append('terrain-defense claim missing or above B/unbounded')
    for p in PRE.glob('01_arcs/*/claims/C-R17-*.json'):
        c=load(p); text=(c.get('claim','')+' '+c.get('notes','')+' '+c.get('bounded_by','')).lower()
        if any(k in text for k in ('deliberate non-development','passes unroaded','no bridges')) and c.get('confidence')=='A':
            errors.append(f'{p.name}: deliberate non-development cannot be A without documentary anchor')
    b=load(POST/'06_bridges/B-R17-KDY-SACRED-CITY-COMPARATOR-001.json')
    if b.get('transportability')!='mechanism': errors.append('sacred-city comparator transportability must be mechanism')
    conf=[str(x).lower() for x in (b.get('confounders') or [])]
    if not any('colombo' in x for x in conf): errors.append('sacred-city comparator must include proximity to Colombo confounder')
    if not b.get('bounded_by') or b.get('result') not in {'U','D','C','B'}: errors.append('sacred-city comparator must be bounded and non-A')
    side=POST/'09_output/side_stories'
    needed=['SS-R17-KDY-METHOD-SECOND-CITY-001.json','SS-R17-KDY-FALSE-ECON-001.json','SS-R17-KDY-COMPARATOR-SACRED-001.json']
    for name in needed:
        if not (side/name).exists(): errors.append(f'missing Run17 side story {name}')
    q=(POST/'08_questions/run17_kandy_measure_before_explain.md').read_text(encoding='utf-8')
    if len(re.findall(r'^\d+\.\s',q,re.M))<15: errors.append('Run17 question registry is too thin')
    for e in errors: print('ERROR:',e,file=sys.stderr)
    if errors: return 1
    print(f'RUN17 KANDY AUDIT OK: metrics={len(metrics)}; economic hypothesis=D; two dispossessions separated; sacred comparator bounded; terrain ceiling<=B')
    return 0
if __name__=='__main__': raise SystemExit(main())
