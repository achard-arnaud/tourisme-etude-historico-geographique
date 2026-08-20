#!/usr/bin/env python3
import json, os, sys, re
from pathlib import Path

VALID_CONF=set('ABCDU')
VALID_ZOOMS={f'Z{i}' for i in range(5)}
VALID_TIERS={f'T{i}' for i in range(6)}
DEBUG=bool(os.environ.get('SKILL_DEBUG'))


def load_sources(root):
    paths=sorted((root/'05_sources').glob('source_register*.json'))
    if not paths:
        return {}, []
    sources={}; errors=[]
    for p in paths:
        try:
            data=json.loads(p.read_text(encoding='utf-8'))
        except Exception as e:
            if DEBUG: raise
            errors.append(f'invalid source register: {p}: {e}')
            continue
        if not isinstance(data,list):
            errors.append(f'invalid source register: {p}: expected JSON list')
            continue
        for item in data:
            if not isinstance(item,dict) or not item.get('id'):
                errors.append(f'invalid source entry in {p.name}: {item!r}')
                continue
            sid=item['id']
            if sid in sources:
                errors.append(f'duplicate source id across registers: {sid}')
                continue
            sources[sid]=item
    return sources, errors


def parse_frontmatter(path):
    text=path.read_text(encoding='utf-8')
    if not text.startswith('---\n'):
        return {}, 'missing YAML frontmatter'
    try:
        block=text.split('---\n',2)[1]
    except Exception:
        if DEBUG: raise
        return {}, 'invalid YAML frontmatter delimiters'
    data={}
    for line in block.splitlines():
        if ':' not in line or line.lstrip().startswith('- '):
            continue
        k,v=line.split(':',1)
        data[k.strip()]=v.strip().strip('"\'')
    return data, None


def validate_wiki(root, sources, errors, warnings):
    wiki=root/'03_wiki'
    if not wiki.exists():
        return 0
    pages=[p for p in wiki.rglob('*.md') if p.name.lower()!='readme.md']
    seen_slugs=set()
    for p in pages:
        meta, err=parse_frontmatter(p)
        if err:
            errors.append(f'wiki {p}: {err}'); continue
        slug=meta.get('slug')
        if not slug: errors.append(f'wiki missing slug: {p}')
        elif slug in seen_slugs: errors.append(f'duplicate wiki slug: {slug}')
        else: seen_slugs.add(slug)
        if meta.get('confidence') not in VALID_CONF:
            errors.append(f'wiki invalid confidence: {p}')
        if not meta.get('last_reviewed'):
            errors.append(f'wiki missing last_reviewed: {p}')
        text=p.read_text(encoding='utf-8')
        for sid in re.findall(r'\b(?:[A-Z][A-Z0-9-]{2,})\b', text):
            if sid.startswith(('CAMBRIDGE-','WORLD-BANK-','ADB-','BPS-','TN-','SRI-LANKA-','JSTOR-','ABCFM-','DCS-','UJAFFNA-','FRUS-','IMF-','PARLIAMENT-','PRESIDENT-','SNSL-','FIELD-')) and sid not in sources:
                errors.append(f'unknown source {sid} in wiki {p.name}')
    return len(pages)


def validate_graph(root, sources, errors):
    graph=root/'04_graph'
    if not graph.exists():
        return 0
    count=0
    for p in graph.glob('*.jsonl'):
        for lineno,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
            if not line.strip(): continue
            count+=1
            try: edge=json.loads(line)
            except Exception as e:
                if DEBUG: raise
                errors.append(f'invalid graph json {p}:{lineno}: {e}'); continue
            for field in ('from','relation','to','confidence','last_reviewed'):
                if not edge.get(field): errors.append(f'graph missing {field}: {p}:{lineno}')
            if edge.get('confidence') not in VALID_CONF:
                errors.append(f'graph invalid confidence: {p}:{lineno}')
            source_ids=edge.get('source_ids') or []
            if edge.get('relation') in {'CAUSES','AMPLIFIES','ENABLES','CONSTRAINS','LEGITIMIZES','CONTESTS','REDISTRIBUTES_ACCESS_TO','EXTERNALIZES_TO','REFINES'} and not source_ids:
                errors.append(f'unsourced interpretive graph edge: {p}:{lineno}')
            for sid in source_ids:
                if sid not in sources: errors.append(f'unknown source {sid} in graph {p}:{lineno}')
    return count


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
            if DEBUG: raise
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
            if DEBUG: raise
            errors.append(f'invalid bridge json: {p}: {e}'); continue
        bid=b.get('id',p.stem); result=b.get('result')
        if result not in VALID_CONF: warnings.append(f'open/invalid bridge result: {p.name}')
        frm=b.get('from_claim'); to=b.get('to_claim')
        if frm not in seen or to not in seen:
            errors.append(f'orphan bridge: {bid} ({frm} -> {to})')
        source_ids=b.get('source_ids') or []
        if result in {'A','B'} and not source_ids: errors.append(f'unsourced resolved bridge: {bid}')
        for sid in source_ids:
            if sid not in sources: errors.append(f'unknown source {sid} in bridge {bid}')

    wiki_count=validate_wiki(root,sources,errors,warnings)
    graph_count=validate_graph(root,sources,errors)

    for m in errors: print('ERROR:',m,file=sys.stderr)
    for m in warnings: print('WARN:',m,file=sys.stderr)
    if errors: return 1
    print(f'QA OK: {len(claims)} claims, {len(sources)} sources, {wiki_count} wiki pages, {graph_count} graph edges, {len(warnings)} warnings')
    return 0

if __name__=='__main__': raise SystemExit(main())
