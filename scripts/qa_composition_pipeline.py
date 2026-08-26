#!/usr/bin/env python3
"""Hard pre-edit composition gate: graph links → state → side stories → recaps → profile/maps/illustrations → reader plan."""
from __future__ import annotations
import json,sys
from pathlib import Path
from output_state import canonical_markdown_path
from graph_link_audit import validate_graph_links
from side_story_contract import validate_side_stories
from arc_recap_contract import validate_arc_recaps,load_arc_recaps,RENDERABLE
from materialize_arc_recaps import materialize_arc_recaps
from map_asset_contract import validate_map_assets
from illustration_contract import validate_illustrations,load_illustrations,assert_rendered_illustrations,check_illustration_density
from reader_profile_contract import validate_reader_profile,load_reader_profile
from resolve_reader_plan import build_plan
from build_story_scaffold import write_scaffold

def main():
    project=Path(sys.argv[1]);errors=[];warnings=[]
    ge,gw,nodes,edges=validate_graph_links(project);errors+=ge;warnings+=gw
    try:canonical=canonical_markdown_path(project)
    except Exception as exc:errors.append(str(exc));canonical=None
    se,sw,stories,coverage=validate_side_stories(project,check_render=True);errors+=se;warnings+=sw
    re,rw,recaps=validate_arc_recaps(project);errors+=re;warnings+=rw
    required_recaps=sum(1 for _,item in load_arc_recaps(project) if item.get('status') in RENDERABLE and (item.get('render') or {}).get('required_in_reader'))
    if canonical is not None and not errors:
        try:
            _,materializable=materialize_arc_recaps(project,canonical.read_text(encoding='utf-8'))
            if materializable!=required_recaps:errors.append(f'arc recap materialization mismatch: {materializable}/{required_recaps} required ({recaps} registered)')
        except Exception as exc:errors.append(f'arc recap materialization: {exc}')
    me,mw,maps=validate_map_assets(project);errors+=me;warnings+=mw
    ie,iw,illustrations=validate_illustrations(project);errors+=ie;warnings+=iw
    pe,pw,profiles=validate_reader_profile(project);errors+=pe;warnings+=pw
    plan=None;scaffold=None
    if not errors:
        try:
            scaffold=write_scaffold(project);plan=build_plan(project)
            known_illustrations={x.get('id') for _,x in load_illustrations(project)}
            routed_illustrations=set(plan['selected_illustration_ids'])|set(plan['illustration_review_queue_ids'])|set(plan['retired_illustration_ids'])
            if known_illustrations!=routed_illustrations:errors.append(f"illustration plan coverage mismatch: routed {len(routed_illustrations)}/{len(known_illustrations)}")
            if canonical is not None:
                markdown=canonical.read_text(encoding='utf-8')
                assert_rendered_illustrations(markdown,plan['selected_illustration_ids'])
                density=load_reader_profile(project)['illustration_density_policy']
                errors+=check_illustration_density(markdown,plan['selected_illustration_ids'],density['max_per_n_pages'],density['words_per_page'])
            (project/'09_output'/'reader_plan.json').write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        except Exception as exc:errors.append(f'reader plan: {exc}')
    for x in warnings:print('WARN:',x,file=sys.stderr)
    for x in errors:print('ERROR:',x,file=sys.stderr)
    if errors:return 1
    print(f"COMPOSITION PREFLIGHT OK: canonical={canonical.name}, graph={nodes} nodes/{edges} edges/0 unresolved, scaffold={len(scaffold['arcs'])} arcs/{len(scaffold['diagnostics']['graph_components'])} components, side-stories=traced {coverage['traced']} / declared {coverage['declared']} / discovered {coverage['discovered']} / untracked {coverage['untracked']}, recaps={required_recaps}/{recaps} reader-required/registered, maps={maps}, illustrations={illustrations}, profile={plan['profile_id']}")
    return 0
if __name__=='__main__':raise SystemExit(main())
