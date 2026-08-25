#!/usr/bin/env python3
from __future__ import annotations
import json
from pathlib import Path
from side_story_contract import validate_side_stories
ROOT=Path(__file__).resolve().parents[1];PRE=ROOT/'examples/sri_lanka_pre_1948';POST=ROOT/'examples/sri_lanka_post_1948';ERRORS=[]
def err(m):ERRORS.append(m)
def load(p):return json.loads(p.read_text(encoding='utf-8'))
def claims(project):
 out=[]
 for p in project.glob('01_arcs/*/claims/C-R18-*.json'):
  try:out.append((p,load(p)))
  except Exception as e:err(f'invalid claim {p}: {e}')
 return out
def bridges(project):
 out=[]
 for p in project.glob('06_bridges/B-R18-*.json'):
  try:out.append((p,load(p)))
  except Exception as e:err(f'invalid bridge {p}: {e}')
 return out
def stories(project):
 out=[]
 for p in project.glob('09_output/side_stories/SS-R18-*.json'):
  try:
   d=load(p);out.extend(d if isinstance(d,list) else [d])
  except Exception as e:err(f'invalid side story {p}: {e}')
 return out
for p in [PRE/'00_method/capture/run18_ishikawa_coffee_to_tea.json',POST/'00_method/capture/run18_ishikawa_value_capture.json']:
 if not p.exists():err(f'missing Ishikawa capture: {p}')
 elif 'ishikawa' not in json.dumps(load(p)).lower():err(f'Ishikawa contract not explicit: {p}')
for p in [PRE/'01_arcs/A07c_coffee_collapse_and_tea_conversion/ARC.md',PRE/'01_arcs/A09b_plantation_labour_system/ARC.md',POST/'01_arcs/A17b_plantation_economy_and_value_capture/ARC.md',POST/'01_arcs/A18_malaiyaha_tamils_status_and_wage/ARC.md']:
 if not p.exists():err(f'missing Run18 arc: {p}')
 else:
  t=p.read_text(encoding='utf-8')
  if 'evidence_status: partial' not in t:err(f'{p}: must remain partial')
  if 'threads: labour, land, water, caste/ethnicity, trade' not in t or 'no_tea_thread: true' not in t:err(f'{p}: thread contract missing')
if (POST/'01_arcs/A17_plantation_economy_and_value_capture').exists():err('numeric A17 collision survived; use A17b')
qpre=(PRE/'08_questions/run18_tea_conversion_hypotheses.md').read_text(encoding='utf-8');qpost=(POST/'08_questions/run18_value_capture_hypotheses.md').read_text(encoding='utf-8')
for t in ('H1','H2','H3'):
 if t not in qpre:err(f'missing {t}')
for t in ('M1','M2','M3'):
 if t not in qpost:err(f'missing {t}')
if 'discrimin' not in qpre.lower():err('conversion discriminating test missing')
if 'discrimin' not in qpost.lower():err('value discriminating test missing')
src=[]
for project in (PRE,POST):
 p=project/'05_sources/source_register_run18_tea.json';d=load(p);src.extend(d if isinstance(d,list) else [])
dom=sum(1 for s in src if s.get('domestic') is True);loc=sum(1 for s in src if str(s.get('language','')).lower() in {'si','ta','sinhala','tamil'})
if dom*3<len(src):err(f'domestic sources below 1/3: {dom}/{len(src)}')
if loc<4:err(f'need >=4 Sinhala/Tamil anchors, found {loc}')
cs=claims(PRE)+claims(POST)
for _,c in cs:
 if c.get('type')=='metric':
  m=c.get('metric') or {}
  for k in ('denominator','geography','period','basis','source_definition'):
   if not m.get(k):err(f'{c.get("id")}: metric.{k} missing')
wdir=POST/'01_arcs/A18_malaiyaha_tamils_status_and_wage/claims'
for cid,typ in {'C-R18-WAGE-2026-FACT':'metric','C-R18-WAGE-2026-EFFECT':'policy_effect','C-R18-WAGE-2026-INFERENCE':'inference'}.items():
 p=wdir/f'{cid}.json'
 if not p.exists():err(f'missing {cid}')
 elif load(p).get('type')!=typ:err(f'{cid}: expected {typ}')
bs=bridges(PRE)+bridges(POST);du=[b for _,b in bs if b.get('result') in {'D','U'}]
if len(du)<2:err(f'need >=2 D/U bridges, found {len(du)}')
for _,b in bs:
 for k in ('mechanism','transmission_channel','time_lag','scale','confounders','transportability','integration_action','bounded_by'):
  if b.get(k) in (None,'',[]):err(f'{b.get("id")}: bridge {k} missing')
ss=stories(PRE)+stories(POST)
if len(ss)<13:err(f'need >=13 Run18 side stories, found {len(ss)}')
kinds=[s.get('kind') for s in ss]
if kinds.count('object_focus')<2:err('need at least two object_focus instances')
if kinds.count('portrait')<1:err('missing portrait instance')
for s in ss:
 if s.get('status')!='candidate' or (s.get('render') or {}).get('required_in_reader') is not False:err(f'{s.get("id")}: Run18 story must remain non-reader candidate')
for project in (PRE,POST):
 e,_,_,_=validate_side_stories(project);ERRORS.extend(e)
byid={c.get('id'):c for _,c in cs}
if byid.get('C-R18-COFFEE-H1-001',{}).get('confidence')!='D':err('rust-only sufficiency must be D')
for cid in ('C-R18-COFFEE-H2-001','C-R18-COFFEE-H3-001'):
 if byid.get(cid,{}).get('confidence')=='A':err(f'{cid} cannot be A before estate-level lag test')
if byid.get('C-R18-2021-UPMARKET-FALSE-001',{}).get('type')!='discarded_lead' or byid.get('C-R18-2021-UPMARKET-FALSE-001',{}).get('confidence')!='D':err('2021 forced-upmarket false lead must be D')
gi=byid.get('C-R18-GI-PENDING-001',{}).get('claim','').lower()
if 'application' not in gi or 'not a completed' not in gi:err('GI state must remain pending application, not registration')
if byid.get('C-R18-M3-001',{}).get('type')!='question' or byid.get('C-R18-M3-001',{}).get('confidence') not in {'U','C'}:err('M3 must remain a bounded question before capex test')
wb=next((b for _,b in bs if b.get('id')=='B-R18-WAGE-SUBSIDY-PRODUCTIVITY-001'),None)
if not wb or wb.get('result')!='U':err('wage subsidy/productivity bridge must remain U')
if ERRORS:
 for e in ERRORS:print('ERROR:',e)
 raise SystemExit(1)
print(f'RUN18 TEA AUDIT OK — claims {len(cs)} / bridges {len(bs)} / D-U bridges {len(du)} / side stories {len(ss)} / domestic {dom}/{len(src)} / Sinhala-Tamil {loc}')
