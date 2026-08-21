#!/usr/bin/env python3
import re,sys
from pathlib import Path
REQUIRED=['SKILL.md','README.md','templates/arc.md','templates/claim.md','templates/run-manifest.json','templates/side-story.json','templates/arc-recap.json','templates/map-asset.json','templates/reader-profile.json','scripts/new_project.py','scripts/new_arc.py','scripts/qa_project.py','scripts/audit_workflow.py','scripts/graph_link_audit.py','scripts/materialize_side_stories.py','scripts/resolve_reader_plan.py','scripts/render_reader_exports.py']
def fm(text):
    m=re.match(r'^---\n(.*?)\n---\n',text,re.S);out={}
    if not m:return out
    for line in m.group(1).splitlines():
        if ':' in line:k,v=line.split(':',1);out[k.strip()]=v.strip()
    return out
def main():
    root=Path(sys.argv[1] if len(sys.argv)>1 else '.');errors=[]
    for rel in REQUIRED:
        if not (root/rel).exists():errors.append(f'missing {rel}')
    for p in [root/'SKILL.md',*sorted((root/'skills').glob('*/SKILL.md'))]:
        if not p.exists():continue
        meta=fm(p.read_text(encoding='utf-8'))
        if not meta.get('name'):errors.append(f'missing name: {p}')
        if not meta.get('description','').startswith('Use when'):errors.append(f'bad trigger description: {p}')
    for e in errors:print('ERROR:',e,file=sys.stderr)
    if errors:return 1
    print('SKILL AUDIT OK: file-level length cap removed; routed context budget is audited separately');return 0
if __name__=='__main__':raise SystemExit(main())
