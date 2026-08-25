#!/usr/bin/env python3
"""Run 15 hard gates: capture-only T4 guide + bounded post-1948 research intakes."""
from __future__ import annotations
import json,sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'examples/sri_lanka_pre_1948'
POST=ROOT/'examples/sri_lanka_post_1948'
ARCS={
    'A14_coastal_environmental_governance':(5,7,3),
    'A15_tsunami_2004_and_reconstruction':(6,8,0),
    'A16_tourism_shock_and_fiscal_collapse':(6,8,4),
}
METRIC_FIELDS={'denominator','geography','period','basis','source_definition'}

def load_json(path):return json.loads(path.read_text(encoding='utf-8'))
def claims(arc):
    return [load_json(p) for p in sorted((POST/'01_arcs'/arc/'claims').glob('*.json'))]
def bridges(prefix):
    return [load_json(p) for p in sorted((POST/'06_bridges').glob(prefix+'*.json'))]

def main():
    errors=[]
    capture=PRE/'00_method/capture/guide_fragments.json'
    contradictions=PRE/'00_method/capture/guide_contradictions.json'
    if not capture.exists():errors.append('guide capture missing')
    else:
        data=load_json(capture);src=data.get('source_candidate') or {};frags=data.get('fragments') or []
        if data.get('source_status')!='blocked_missing_cover_metadata':errors.append('guide source must remain blocked until cover metadata exists')
        if src.get('date') or src.get('title') or src.get('author_institution'):errors.append('guide capture must not invent title/date/publisher')
        if len(frags)<45:errors.append(f'guide fragment count too low: {len(frags)}')
        promoted=[f['id'] for f in frags if f.get('promotes_to')]
        if promoted:errors.append(f'guide fragments prematurely promoted: {promoted}')
        fabricated=[f['id'] for f in frags if f.get('verbatim')]
        if fabricated:errors.append(f'snapshot summaries must not masquerade as verbatim: {fabricated}')
    if not contradictions.exists() or len(load_json(contradictions))!=4:errors.append('exactly four guide contradiction records required')
    drift=(PRE/'07_drifts/run15_guide_historiography_drift.md')
    if not drift.exists():errors.append('guide historiography drift record missing')
    else:
        text=drift.read_text(encoding='utf-8')
        for token in ('GF-349-01','GF-366-03'):
            if token not in text:errors.append(f'drift routing missing {token}')
    # A real GUIDE-FR-PRINT source is only legal once dated.
    for project in (PRE,POST):
        for p in (project/'05_sources').glob('source_register*.json'):
            rows=load_json(p)
            if not isinstance(rows,list):continue
            for row in rows:
                if str(row.get('id','')).startswith('GUIDE-FR-PRINT') and not row.get('date'):
                    errors.append(f'undated guide source registered: {p.name}:{row.get("id")}')
    for arc,(lo,hi,min_metrics) in ARCS.items():
        arc_md=POST/'01_arcs'/arc/'ARC.md'
        if not arc_md.exists() or 'Evidence status:** partial' not in arc_md.read_text(encoding='utf-8'):
            errors.append(f'{arc}: must exist and remain partial')
        rows=claims(arc)
        if not lo<=len(rows)<=hi:errors.append(f'{arc}: claim count {len(rows)} outside {lo}-{hi}')
        metrics=[r for r in rows if r.get('type')=='metric']
        if len(metrics)<min_metrics:errors.append(f'{arc}: metrics {len(metrics)} < {min_metrics}')
        for r in metrics:
            meta=r.get('metric') or {};missing=sorted(METRIC_FIELDS-set(k for k,v in meta.items() if v not in (None,'')))
            if missing:errors.append(f"{r.get('id')}: metric metadata missing {missing}")
    src=load_json(POST/'05_sources/source_register_run15.json')
    for row in src:
        for field in ('date','author_or_institution','scope','limitations','provenance','claims_supported'):
            if row.get(field) in (None,'',[]):errors.append(f"{row.get('id')}: missing source field {field}")
    a15=claims('A15_tsunami_2004_and_reconstruction')
    if not any(r.get('type')=='policy_intent' for r in a15) or not any(r.get('type')=='policy_effect' for r in a15):errors.append('A15 intent/effect pair missing')
    b15=bridges('B-R15-TSU-')
    if len(b15)<2:errors.append('A15 requires two causal bridges')
    if not any(b.get('result') in {'D','U'} for b in b15):errors.append('A15 requires D/U result')
    b16=bridges('B-R15-TOUR-')
    if not b16:errors.append('A16 bridge missing')
    else:
        b=b16[0]
        if len(b.get('confounders') or [])<6:errors.append('A16 confounder list is not genuinely long')
        if not b.get('bounded_by'):errors.append('A16 attribution bridge missing bounded_by')
        if b.get('result') not in {'D','U'}:errors.append('A16 monocausal attribution should resolve D/U')
    b14=bridges('B-R15-PLASTIC-')
    if not b14 or not any(b.get('result')=='D' for b in b14):errors.append('A14 requires explicit single-cause negative result')
    for err in errors:print('ERROR:',err,file=sys.stderr)
    if errors:return 1
    print('RUN15 INTAKE AUDIT OK: guide capture blocked/unpromoted; 4 contradictions; A14=6 claims; A15=7 claims + D/U; A16=8 claims + bounded D; all Run15 sources dated')
    return 0
if __name__=='__main__':raise SystemExit(main())
