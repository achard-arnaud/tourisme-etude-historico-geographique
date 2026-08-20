#!/usr/bin/env python3
import json,os,re,sys
from pathlib import Path
ALLOWED_EXECUTION_STATUS={"executed","verified"};DEBUG=bool(os.environ.get('SKILL_DEBUG'))
def latest_manifest(repo:Path)->Path:
    found=[]
    for p in (repo/'docs').glob('RUN*_MANIFEST.json'):
        m=re.match(r'RUN(\d+)',p.name)
        if m:found.append((int(m.group(1)),p.name,p))
    if not found:raise FileNotFoundError('no RUN*_MANIFEST.json found')
    return max(found)[2]
def main():
    repo=Path(__file__).resolve().parents[1];arg=sys.argv[1] if len(sys.argv)>1 else '--latest'
    try:path=latest_manifest(repo) if arg=='--latest' else (Path(arg) if Path(arg).is_absolute() else repo/arg);data=json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        if DEBUG:raise
        print(f'ERROR: invalid workflow manifest: {exc}',file=sys.stderr);return 1
    errors=[];known={p.parent.name for p in (repo/'skills').glob('*/SKILL.md')};dispatched=data.get('dispatched_skills') or [];skipped=data.get('skipped_skills') or [];seen=set()
    for entry in dispatched:
        name=entry.get('skill')
        if name not in known:errors.append(f'unknown dispatched skill: {name}')
        if name in seen:errors.append(f'duplicate skill routing: {name}')
        seen.add(name)
        if entry.get('status') not in ALLOWED_EXECUTION_STATUS:errors.append(f'invalid execution status for {name}')
        if not entry.get('reason'):errors.append(f'missing dispatch reason for {name}')
        outputs=entry.get('outputs') or []
        if not outputs:errors.append(f'missing output evidence for {name}')
        for rel in outputs:
            if not (repo/rel).exists():errors.append(f'missing workflow evidence path for {name}: {rel}')
    for entry in skipped:
        name=entry.get('skill')
        if name not in known:errors.append(f'unknown skipped skill: {name}')
        if name in seen:errors.append(f'duplicate skill routing: {name}')
        seen.add(name)
        if not entry.get('reason'):errors.append(f'missing skip reason for {name}')
    if data.get('status')=='reviewed' and seen!=known:
        if known-seen:errors.append('unrouted skills: '+', '.join(sorted(known-seen)))
        if seen-known:errors.append('unrecognized routed skills: '+', '.join(sorted(seen-known)))
    for key in ('run_id','mode','state_before','state_after','promotion_decision'):
        if not data.get(key):errors.append(f'missing manifest field: {key}')
    for e in errors:print('ERROR:',e,file=sys.stderr)
    if errors:return 1
    print(f'WORKFLOW AUDIT OK: {path.name}, {len(dispatched)} dispatched, {len(skipped)} skipped, {len(known)} known skills');return 0
if __name__=='__main__':raise SystemExit(main())
