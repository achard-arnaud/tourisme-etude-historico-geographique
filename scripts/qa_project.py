#!/usr/bin/env python3
import json, sys
from pathlib import Path

VALID_CONF=set('ABCDU')
VALID_ZOOMS={f'Z{i}' for i in range(5)}
VALID_TIERS={f'T{i}' for i in range(6)}

def load_sources(root):
    p=root/'05_sources'/'source_register.json'
    if not p.exists():
        return {}, []
    try:
        data=json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:
        return {}, [f'invalid source register: {p}: {e}']
    if not isinstance(data,list):
        return {}, [f'invalid source register: {p}: expected JSON list']
    sources={}; errors=[]
    for item in data:
        if not isinstance(item,dict) or not item.get('id'):
            errors.append(f'invalid source entry in register: {item!r}')
            continue
        sid=item['id']
        if sid in sources:
            errors.append(f'duplicate source id: {sid}')
            continue
        sources[sid]=item
    return sources, errors

def main():
    root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
    errors=[]; warnings=[]
    sources, source_errors=load_sources(root)
    errors.extend(source_errors)
    for sid, source in sources.items():
        if source.get('tier') not in VALID_TIERS:
            errors.append(f'invalid source tier: {sid}')
    claims=list(root.glob('01_arcs/*/claims/*.json'))
    seen=set()
    for p in claims:
        try: c=json.loads(p.read_text(encoding='utf-8'))
        except Exception as e:
            errors.append(f'invalid claim json: {p}: {e}'); continue
        cid=c.get('id')
        if not cid: errors.append(f'missing claim id: {p}')
        elif cid in seen: errors.append(f'duplicate claim id: {cid}')
        seen.add(cid)
        if c.get('confidence') not in VALID_CONF: errors.append(f'invalid confidence: {cid}')
        if c.get('zoom') not in VALID_ZOOMS: errors.append(f'invalid zoom: {cid}')
        source_ids=c.get('source_ids') or []
        major=c.get('confidence') in {'A','B'} and c.get('causal_role') in {'driver','amplifier'}
        if major and not source_ids: errors.append(f'unsourced major claim: {cid}')
        for sid in source_ids:
            if sid not in sources: errors.append(f'unknown source {sid} in claim {cid}')
    for p in root.glob('06_bridges/*.json'):
        try: b=json.loads(p.read_text(encoding='utf-8'))
        except Exception as e:
            errors.append(f'invalid bridge json: {p}: {e}'); continue
        bid=b.get('id',p.stem)
        result=b.get('result')
        if result not in VALID_CONF:
            warnings.append(f'open/invalid bridge result: {p.name}')
        frm=b.get('from_claim'); to=b.get('to_claim')
        if frm not in seen or to not in seen:
            errors.append(f'orphan bridge: {bid} ({frm} -> {to})')
        source_ids=b.get('source_ids') or []
        if result in {'A','B'} and not source_ids:
            errors.append(f'unsourced resolved bridge: {bid}')
        for sid in source_ids:
            if sid not in sources:
                errors.append(f'unknown source {sid} in bridge {bid}')
    for m in errors: print('ERROR:',m)
    for m in warnings: print('WARN:',m)
    if errors: return 1
    print(f'QA OK: {len(claims)} claims, {len(sources)} sources, {len(warnings)} warnings')
    return 0

if __name__=='__main__': raise SystemExit(main())
