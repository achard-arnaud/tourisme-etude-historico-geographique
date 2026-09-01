#!/usr/bin/env python3
"""Run 14 hard gates for bounded legacy side stories and arc shells."""
from __future__ import annotations
import json,sys
from pathlib import Path
from side_story_contract import load_side_stories,side_story_coverage,validate_side_stories
from arc_recap_contract import arc_evidence_status

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'examples/sri_lanka_pre_1948'
SLICE_IDS={'SS-PRE-L003','SS-PRE-L004','SS-PRE-L005','SS-PRE-L016'}
APPARATUS_IDS={'SS-PRE-L001','SS-PRE-L009'}
SHELL_ARCS={
    'A01_settlement_and_early_polity',
    'A02b_anuradhapura_hydraulic_order',
    'A03_indian_ocean_and_regional_systems',
    'A05b_dry_zone_collapse_and_mobile_capitals',
    'A06b_portuguese_maritime_violence',
    'A09_british_unification_1833',
}

def main():
    errors=[]
    for p in PRE.rglob('*'):
        if p.is_file():
            try:text=p.read_text(encoding='utf-8')
            except Exception:continue
            if 'LEGACY:' in text:errors.append(f'LEGACY token remains in pre corpus: {p.relative_to(PRE)}')
    items={item['id']:item for _,item in load_side_stories(PRE)}
    coverage=side_story_coverage(PRE)
    # Run14 established a minimum of 8 traced stories and exactly 17 bounded legacy
    # exemptions. Later runs are expected to increase traced coverage; that is progress,
    # not a regression. Declared legacy debt and untracked reader fragments remain hard gates.
    if coverage['traced']<8 or coverage['declared']!=17 or coverage['untracked']!=0:
        errors.append(f"unexpected coverage: traced={coverage['traced']} declared={coverage['declared']} untracked={coverage['untracked']} (expected traced>=8 / declared 17 / untracked 0)")
    if coverage['legacy_required_exemptions']!=17:
        errors.append(f"legacy required exemptions={coverage['legacy_required_exemptions']} (expected 17)")
    for sid in APPARATUS_IDS:
        item=items.get(sid,{})
        if item.get('class')!='apparatus' or item.get('scope')!='book' or item.get('arc') not in (None,'') or (item.get('placement') or {}).get('return_to') not in (None,''):
            errors.append(f'{sid}: invalid book apparatus contract')
    for sid in SLICE_IDS:
        item=items.get(sid,{})
        lineage=item.get('lineage') or {}
        if item.get('status')!='promoted' or item.get('lineage_quality')!='full':errors.append(f'{sid}: slice not promoted/full')
        if not lineage.get('claim_ids') or not lineage.get('source_ids'):errors.append(f'{sid}: slice lineage incomplete')
        if not (item.get('content') or {}).get('takeaway'):errors.append(f'{sid}: takeaway missing')
    for _,item in load_side_stories(PRE):
        if item.get('lineage_quality')=='legacy_fragment' and item.get('status')=='promoted':errors.append(f"{item.get('id')}: legacy fragment promoted")
        lineage=item.get('lineage') or {}
        if (item.get('render') or {}).get('required_in_reader') and not (lineage.get('claim_ids') or lineage.get('source_ids')):
            if not (item.get('lineage_quality')=='legacy_fragment' and item.get('legacy_retention_reason')):errors.append(f"{item.get('id')}: ungrounded required box lacks retention reason")
    for arc in SHELL_ARCS:
        p=PRE/'01_arcs'/arc/'ARC.md'
        if not p.exists() or arc_evidence_status(p)!='shell':errors.append(f'{arc}: missing or not shell')
    a04=PRE/'01_arcs/A04_chola_interlude_and_polonnaruwa/ARC.md'
    if arc_evidence_status(a04)!='partial':errors.append('A04 must remain partial after vertical slice')
    source_path=PRE/'05_sources/source_register_run14_legacy_slice.json'
    source_rows=json.loads(source_path.read_text(encoding='utf-8')) if source_path.exists() else []
    if len(source_rows)!=5:errors.append(f'Run14 source count {len(source_rows)} != 5')
    required={'date','author_or_institution','limitations','provenance','claims_supported','scope'}
    for row in source_rows:
        missing=sorted(k for k in required if row.get(k) in (None,'',[]))
        if missing:errors.append(f"source {row.get('id')}: missing {missing}")
    e,_,_,_=validate_side_stories(PRE)
    errors+=e
    for err in errors:print('ERROR:',err,file=sys.stderr)
    if errors:return 1
    print(f"RUN14 LEGACY AUDIT OK: traced {coverage['traced']} / declared {coverage['declared']} / untracked {coverage['untracked']}; exemptions {coverage['legacy_required_exemptions']}; A04 slice 4 records / 4 claims / 5 sources")
    return 0
if __name__=='__main__':raise SystemExit(main())
