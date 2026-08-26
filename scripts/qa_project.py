#!/usr/bin/env python3
import json, os, sys, re
from pathlib import Path
from urllib.parse import urlparse
from side_story_contract import validate_side_stories
from arc_recap_contract import validate_arc_recaps
from map_asset_contract import validate_map_assets
from reader_profile_contract import validate_reader_profile
from graph_link_audit import validate_graph_links

VALID_CONF = set('ABCDU')
VALID_ZOOMS = {f'Z{i}' for i in range(5)}
VALID_TIERS = {f'T{i}' for i in range(6)}
VALID_TYPES = {
    'source_fact','claim','inference','tradition','analogy','comparator',
    'counterfactual','metric','policy_intent','policy_effect','question','discarded_lead'
}
VALID_CAUSAL_ROLES = {'driver','amplifier','constraint','context','mechanism','outcome','none'}
VALID_ANCHOR_ROLES = {'canonical anchor','specialist institutional anchor','corroborating bridge','lead'}
VALID_PROVENANCE = {'direct','index_cache'}
METRIC_FIELDS = {'denominator','geography','period','basis','source_definition'}
BRIDGE_FIELDS = {'transmission_channel','time_lag','scale','confounders','transportability','integration_action'}
DEBUG = bool(os.environ.get('SKILL_DEBUG'))


def contract_version(root):
    p = root / 'project.json'
    if not p.exists(): return 2
    try:
        data = json.loads(p.read_text(encoding='utf-8'))
        explicit = data.get('artifact_contract_version')
        return int(explicit) if explicit is not None else 2
    except Exception:
        return 2


def load_overrides(root):
    p = root/'00_method'/'v3_contract_overrides.json'
    if not p.exists(): return {'sources':{},'claims':{},'bridges':{}}, []
    errors=[]
    try: data=json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:
        if DEBUG: raise
        return {'sources':{},'claims':{},'bridges':{}}, [f'invalid v3 contract overrides: {e}']
    if not isinstance(data,dict): return {'sources':{},'claims':{},'bridges':{}}, ['v3 contract overrides must be object']
    out={}
    for key in ('sources','claims','bridges'):
        section=data.get(key,{})
        if not isinstance(section,dict): errors.append(f'v3 override section must be object: {key}'); section={}
        out[key]=section
    return out,errors


def load_sources(root, overrides=None):
    sources = {}; errors = []
    for p in sorted((root/'05_sources').glob('source_register*.json')):
        try: data=json.loads(p.read_text(encoding='utf-8'))
        except Exception as e:
            if DEBUG: raise
            errors.append(f'invalid source register: {p}: {e}'); continue
        if not isinstance(data,list): errors.append(f'invalid source register: {p}: expected JSON list'); continue
        for item in data:
            if not isinstance(item,dict) or not item.get('id'):
                errors.append(f'invalid source entry in {p.name}: {item!r}'); continue
            sid=item['id']
            if sid in sources: errors.append(f'duplicate source id across registers: {sid}'); continue
            sources[sid]=item
    patches=(overrides or {}).get('sources',{})
    for sid,patch in patches.items():
        if sid not in sources: errors.append(f'v3 source override references unknown id: {sid}'); continue
        if not isinstance(patch,dict): errors.append(f'v3 source override must be object: {sid}'); continue
        sources[sid]={**sources[sid],**patch}
    return sources,errors


def source_domain(source):
    url=source.get('url') or ''
    try: return urlparse(url).netloc.lower().removeprefix('www.')
    except Exception: return ''


def parse_frontmatter(path):
    text=path.read_text(encoding='utf-8')
    if not text.startswith('---\n'): return {},'missing YAML frontmatter'
    try: block=text.split('---\n',2)[1]
    except Exception:
        if DEBUG: raise
        return {},'invalid YAML frontmatter delimiters'
    data={}
    for line in block.splitlines():
        if ':' in line and not line.lstrip().startswith('- '):
            k,v=line.split(':',1); data[k.strip()]=v.strip().strip('"\'')
    return data,None


def validate_wiki(root,sources,errors):
    wiki=root/'03_wiki'; pages=[p for p in wiki.rglob('*.md') if p.name.lower()!='readme.md'] if wiki.exists() else []; seen=set()
    for p in pages:
        meta,err=parse_frontmatter(p)
        if err: errors.append(f'wiki {p}: {err}'); continue
        slug=meta.get('slug')
        if not slug: errors.append(f'wiki missing slug: {p}')
        elif slug in seen: errors.append(f'duplicate wiki slug: {slug}')
        else: seen.add(slug)
        if meta.get('confidence') not in VALID_CONF: errors.append(f'wiki invalid confidence: {p}')
        if not meta.get('last_reviewed'): errors.append(f'wiki missing last_reviewed: {p}')
        text=p.read_text(encoding='utf-8')
        for sid in re.findall(r'\b(?:[A-Z][A-Z0-9-]{2,})\b',text):
            if sid.startswith(('CAMBRIDGE-','WORLD-BANK-','ADB-','BPS-','TN-','SRI-LANKA-','JSTOR-','ABCFM-','DCS-','UJAFFNA-','FRUS-','IMF-','PARLIAMENT-','PRESIDENT-','SNSL-','FIELD-')) and sid not in sources:
                errors.append(f'unknown source {sid} in wiki {p.name}')
    return len(pages)


def validate_graph_edges(root,sources,errors):
    count=0
    for p in (root/'04_graph').glob('edges*.jsonl') if (root/'04_graph').exists() else []:
        for lineno,line in enumerate(p.read_text(encoding='utf-8').splitlines(),1):
            if not line.strip(): continue
            count+=1
            try: edge=json.loads(line)
            except Exception as e:
                if DEBUG: raise
                errors.append(f'invalid graph edge JSON {p}:{lineno}: {e}'); continue
            for field in ('from','relation','to','confidence','last_reviewed'):
                if not edge.get(field): errors.append(f'graph edge missing {field}: {p}:{lineno}')
            if edge.get('confidence') not in VALID_CONF: errors.append(f'graph edge invalid confidence: {p}:{lineno}')
            source_ids=edge.get('source_ids') or []
            if edge.get('relation') in {'CAUSES','AMPLIFIES','ENABLES','CONSTRAINS','LEGITIMIZES','CONTESTS','REDISTRIBUTES_ACCESS_TO','EXTERNALIZES_TO','REFINES'} and not source_ids:
                errors.append(f'unsourced interpretive graph edge: {p}:{lineno}')
            for sid in source_ids:
                if sid not in sources: errors.append(f'unknown source {sid} in graph {p}:{lineno}')
    return count


def validate_v3_sources(sources,errors):
    required_nonempty=('date','author_or_institution','scope','limitations','provenance')
    for sid,source in sources.items():
        if source.get('anchor_role') not in VALID_ANCHOR_ROLES: errors.append(f'invalid anchor_role: {sid}')
        if source.get('provenance') not in VALID_PROVENANCE: errors.append(f'invalid provenance: {sid}')
        for field in required_nonempty:
            if source.get(field) in (None,''): errors.append(f'source missing {field}: {sid}')
        if 'claims_supported' not in source or not isinstance(source.get('claims_supported'),list): errors.append(f'source missing/invalid claims_supported: {sid}')


def validate_v3_claim(c,p,sources,errors):
    cid=c.get('id') or p.stem
    if c.get('type') not in VALID_TYPES: errors.append(f'invalid statement type: {cid}')
    if c.get('causal_role') not in VALID_CAUSAL_ROLES: errors.append(f'invalid causal_role: {cid}')
    path_arc=p.parents[1].name
    if c.get('arc')!=path_arc: errors.append(f'arc/path mismatch: {cid} ({c.get("arc")} != {path_arc})')
    if c.get('type')=='metric':
        metric=c.get('metric')
        if not isinstance(metric,dict) or any(metric.get(k) in (None,'') for k in METRIC_FIELDS): errors.append(f'metric metadata incomplete: {cid}')
    sids=c.get('source_ids') or []; major=c.get('confidence') in {'A','B'} and c.get('causal_role') in {'driver','amplifier'}
    if major and sids and not c.get('bounded_by'):
        domains={source_domain(sources[sid]) for sid in sids if sid in sources and source_domain(sources[sid])}
        if len(sids)<2 or len(domains)<2: errors.append(f'independent corroboration missing: {cid}')


def validate_v3_bridge(b,errors):
    bid=b.get('id') or 'unknown'
    for field in BRIDGE_FIELDS:
        if b.get(field) in (None,'',[]): errors.append(f'bridge missing {field}: {bid}')
    if b.get('from_claim')==b.get('to_claim'): errors.append(f'bridge self-reference: {bid}')
    if b.get('comparative') is True:
        for field in ('home_claim','comparator_claim','bounded_by'):
            if not b.get(field): errors.append(f'comparative bridge missing {field}: {bid}')


def main():
    root=Path(sys.argv[1] if len(sys.argv)>1 else '.'); errors=[]; warnings=[]; strict=contract_version(root)>=3
    overrides,oe=load_overrides(root); errors+=oe
    sources,se=load_sources(root,overrides); errors+=se
    for sid,source in sources.items():
        if source.get('tier') not in VALID_TIERS: errors.append(f'invalid source tier: {sid}')
    if strict: validate_v3_sources(sources,errors)

    claims=list(root.glob('01_arcs/*/claims/*.json')); seen=set(); claim_patches=overrides.get('claims',{})
    for p in claims:
        try: c=json.loads(p.read_text(encoding='utf-8'))
        except Exception as e:
            if DEBUG: raise
            errors.append(f'invalid claim json: {p}: {e}'); continue
        cid=c.get('id')
        if cid in claim_patches:
            patch=claim_patches[cid]
            if not isinstance(patch,dict): errors.append(f'v3 claim override must be object: {cid}')
            else: c={**c,**patch}
        if not cid: errors.append(f'missing claim id: {p}')
        elif cid in seen: errors.append(f'duplicate claim id: {cid}')
        seen.add(cid)
        if c.get('confidence') not in VALID_CONF: errors.append(f'invalid confidence: {cid}')
        if c.get('zoom') not in VALID_ZOOMS: errors.append(f'invalid zoom: {cid}')
        sids=c.get('source_ids') or []; major=c.get('confidence') in {'A','B'} and c.get('causal_role') in {'driver','amplifier'}
        if major and not sids: errors.append(f'unsourced major claim: {cid}')
        for sid in sids:
            if sid not in sources: errors.append(f'unknown source {sid} in claim {cid}')
        if strict: validate_v3_claim(c,p,sources,errors)
    for cid in claim_patches:
        if cid not in seen: errors.append(f'v3 claim override references unknown id: {cid}')

    bridge_patches=overrides.get('bridges',{}); bridge_seen=set()
    for p in root.glob('06_bridges/*.json'):
        try: b=json.loads(p.read_text(encoding='utf-8'))
        except Exception as e:
            if DEBUG: raise
            errors.append(f'invalid bridge json: {p}: {e}'); continue
        bid=b.get('id',p.stem); bridge_seen.add(bid)
        if bid in bridge_patches:
            patch=bridge_patches[bid]
            if not isinstance(patch,dict): errors.append(f'v3 bridge override must be object: {bid}')
            else: b={**b,**patch}
        result=b.get('result'); frm=b.get('from_claim'); to=b.get('to_claim')
        if result not in VALID_CONF: warnings.append(f'open/invalid bridge result: {p.name}')
        if frm not in seen or to not in seen: errors.append(f'orphan bridge: {bid} ({frm} -> {to})')
        sids=b.get('source_ids') or []
        if result in {'A','B'} and not sids: errors.append(f'unsourced resolved bridge: {bid}')
        for sid in sids:
            if sid not in sources: errors.append(f'unknown source {sid} in bridge {bid}')
        if strict: validate_v3_bridge(b,errors)
    for bid in bridge_patches:
        if bid not in bridge_seen: errors.append(f'v3 bridge override references unknown id: {bid}')

    wiki_count=validate_wiki(root,sources,errors); graph_count=validate_graph_edges(root,sources,errors)
    side_count=recap_count=map_count=profile_count=0; coverage={'traced':0,'declared':0,'discovered':0,'untracked':0,'legacy_required_exemptions':0}
    if (root/'00_method/output_state.json').exists():
        e,w,side_count,coverage=validate_side_stories(root,check_render=True); errors+=e; warnings+=w
        e,w,recap_count=validate_arc_recaps(root); errors+=e; warnings+=w
        e,w,map_count=validate_map_assets(root); errors+=e; warnings+=w
    if (root/'00_method/reader_profile.json').exists():
        e,w,profile_count=validate_reader_profile(root); errors+=e; warnings+=w
    ge,gw,node_count,link_edges=validate_graph_links(root); errors+=ge; warnings+=gw
    for m in errors: print('ERROR:',m,file=sys.stderr)
    for m in warnings: print('WARN:',m,file=sys.stderr)
    if errors: return 1
    print(f"QA OK: contract v{contract_version(root)}, {len(claims)} claims, {len(sources)} sources, {wiki_count} wiki pages, {graph_count} graph edges, {node_count} graph nodes, {side_count} side stories (traced {coverage['traced']}, declared {coverage['declared']}, discovered {coverage['discovered']}, untracked {coverage['untracked']}, legacy-required-exemptions {coverage['legacy_required_exemptions']}), {recap_count} arc recaps, {map_count} map assets, {profile_count} reader profile, {len(warnings)} warnings, v3 overrides {len(overrides.get('sources',{}))}/{len(overrides.get('claims',{}))}/{len(overrides.get('bridges',{}))}")
    return 0

if __name__=='__main__': raise SystemExit(main())
