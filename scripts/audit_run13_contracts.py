#!/usr/bin/env python3
"""Run 13 cross-layer contract audit.

Hard gates only: promoted LEGACY arcs and contradictory analytical evidence status.
Candidate/validated legacy records remain migration debt and are reported, not blocked.
"""
import json,sys
from pathlib import Path

STATUS_BY_CONF={'A':'verified','B':'verified','C':'inference','D':'unknown','U':'unknown'}


def load_claims(project):
    out={}
    for p in project.glob('01_arcs/*/claims/*.json'):
        try:c=json.loads(p.read_text(encoding='utf-8'))
        except Exception:continue
        if isinstance(c,dict) and c.get('id'):out[c['id']]=c
    return out


def records(project):
    root=project/'09_output'/'side_stories'
    if not root.exists():return []
    out=[]
    for p in sorted(root.glob('*.json')):
        data=json.loads(p.read_text(encoding='utf-8'))
        for item in (data if isinstance(data,list) else [data]):out.append((p,item))
    return out


def audit(project):
    claims=load_claims(project);errors=[];warnings=[];legacy=0
    for path,item in records(project):
        sid=item.get('id',path.name);arc=str(item.get('arc') or '')
        if arc.startswith('LEGACY:'):
            legacy+=1
            if item.get('status')=='promoted':errors.append(f'{sid}: promoted side story cannot use {arc}')
        if item.get('kind')!='analytical_focus' or item.get('status') not in {'validated','promoted'}:continue
        for i,mechanism in enumerate((item.get('analysis') or {}).get('mechanisms') or []):
            claim_ids=mechanism.get('claim_ids') or []
            if not claim_ids:
                if mechanism.get('evidence_status')!='unknown':
                    errors.append(f'{sid}: mechanism[{i}] without claim_ids must be unknown')
                continue
            statuses=[]
            for cid in claim_ids:
                c=claims.get(cid);statuses.append(STATUS_BY_CONF.get((c or {}).get('confidence'),'unknown'))
            expected='unknown' if 'unknown' in statuses else ('inference' if 'inference' in statuses else 'verified')
            if mechanism.get('evidence_status')!=expected:
                errors.append(f'{sid}: mechanism[{i}] evidence_status {mechanism.get("evidence_status")!r} contradicts derived {expected!r}')
    if legacy:warnings.append(f'legacy_arc_count={legacy}')
    return errors,warnings,legacy


def main():
    roots=[Path(x) for x in sys.argv[1:]] or [Path('examples/sri_lanka_pre_1948'),Path('examples/sri_lanka_post_1948')]
    total=0
    for root in roots:
        errors,warnings,legacy=audit(root);total+=legacy
        for m in warnings:print(f'WARN {root}: {m}')
        for m in errors:print(f'ERROR {root}: {m}',file=sys.stderr)
        if errors:return 1
    print(f'Run13 contract audit OK; legacy_arc_count={total}')
    return 0
if __name__=='__main__':raise SystemExit(main())
