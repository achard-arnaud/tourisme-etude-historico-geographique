import json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PRE=ROOT/'examples/sri_lanka_pre_1948';POST=ROOT/'examples/sri_lanka_post_1948'
class CompositionPipelineTests(unittest.TestCase):
    def test_canonical_is_state_resolved_not_report_name(self):
        from scripts.output_state import canonical_markdown_path
        self.assertEqual('report_v3_full.md',canonical_markdown_path(PRE).name)
    def test_legacy_side_story_inventory_has_zero_untracked(self):
        sys.path.insert(0,str(ROOT/'scripts'))
        from side_story_contract import side_story_coverage,load_side_stories
        pre=side_story_coverage(PRE);post=side_story_coverage(POST)
        self.assertGreaterEqual(pre['discovered'],21);self.assertEqual(0,pre['untracked']);self.assertGreaterEqual(len(load_side_stories(PRE)),25)
        self.assertGreaterEqual(post['discovered'],3);self.assertEqual(0,post['untracked'])
    def test_method_has_no_fake_return_and_validated_narrative_returns_resolve(self):
        sys.path.insert(0,str(ROOT/'scripts'))
        from side_story_contract import load_side_stories,validate_side_stories
        for _,item in load_side_stories(PRE):
            if item['kind']=='method':self.assertFalse((item.get('placement') or {}).get('return_to'))
        errors,_,_,_=validate_side_stories(PRE);self.assertEqual([],errors)
    def test_three_pre_arc_recaps_cover_materialized_arcs_and_tease_forward(self):
        sys.path.insert(0,str(ROOT/'scripts'))
        from arc_recap_contract import validate_arc_recaps,load_arc_recaps
        errors,_,count=validate_arc_recaps(PRE);self.assertEqual([],errors);self.assertEqual(3,count)
        for _,item in load_arc_recaps(PRE):self.assertTrue(item['protagonists']);self.assertTrue(item['prepares_next']);self.assertTrue(item['placement']['before_anchor'])
    def test_arc_recap_materializer_is_deterministic_and_idempotent(self):
        sys.path.insert(0,str(ROOT/'scripts'))
        from materialize_arc_recaps import materialize_arc_recaps
        source=(PRE/'09_output/report.md').read_text(encoding='utf-8')
        once,count=materialize_arc_recaps(PRE,source);twice,count2=materialize_arc_recaps(PRE,once)
        self.assertEqual(3,count);self.assertEqual(3,count2);self.assertEqual(once,twice)
        for rid in ('RECAP-A06','RECAP-A07','RECAP-A08'):self.assertEqual(1,once.count(f'[ARC-RECAP:{rid}]'))
        self.assertLess(once.index('[ARC-RECAP:RECAP-A06]'),once.index('## 4. 1744–1763'))
        self.assertLess(once.index('[ARC-RECAP:RECAP-A07]'),once.index('## 6. Bridge vers 1948'))
        self.assertLess(once.index('[ARC-RECAP:RECAP-A08]'),once.index('## 6. Bridge vers 1948'))
    def test_graph_preflight_is_clean_before_editing(self):
        for project in (PRE,POST):
            r=subprocess.run([sys.executable,'scripts/graph_link_audit.py',str(project)],cwd=ROOT,text=True,capture_output=True);self.assertEqual(0,r.returncode,r.stdout+r.stderr);self.assertIn('0 unresolved',r.stdout)
    def test_reader_profiles_are_deterministic_and_child_and_historian_keep_all_kinds(self):
        kinds={'detour','dezoom','also','method','false_lead','portrait','object_focus','comparator','callback'}
        for name in ('historian_enthusiast','child_10_plus'):
            p=json.loads((ROOT/'reader_profiles'/f'{name}.json').read_text(encoding='utf-8'));self.assertEqual('all',p['side_story_policy']['coverage_mode']);self.assertEqual(kinds,set(p['side_story_policy']['priority_order']));self.assertEqual(5,p['content_temperature'])
        child=json.loads((ROOT/'reader_profiles/child_10_plus.json').read_text(encoding='utf-8'));self.assertEqual(10,child['min_age']);self.assertEqual('portrait',child['side_story_policy']['priority_order'][0])
    def test_map_asset_requires_vision_then_human_approval(self):
        sys.path.insert(0,str(ROOT/'scripts'))
        from map_asset_contract import validate_map_assets
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'01_arcs/A1').mkdir(parents=True);(p/'09_output/map_assets').mkdir(parents=True);(p/'09_output/side_stories').mkdir(parents=True);(p/'00_method').mkdir()
            (p/'00_method/reader_profile.json').write_text(json.dumps({'language':'fr'}),encoding='utf-8')
            candidate={'schema_version':'1.0','class':'map_asset','id':'MAP1','status':'human_approved','story_ref':{'type':'arc','id':'A1'},'source':{'url':'https://example.test/map','image_path':'map.png','language':'fr'},'historical_context':{'map_date':'1815'},'vision_review':{'checks':{'geography_matches':True,'historical_scope_matches':True,'labels_legible':True,'no_obvious_anachronism':True}},'human_review':{'status':'pending','reviewed_at':None},'fragment':{'caption':'x','what_it_shows':'x','why_here':'x','limits':'x'},'placement':{'subsection_ref':'x'}}
            (p/'09_output/map_assets/MAP1.json').write_text(json.dumps(candidate),encoding='utf-8');errors,_,_=validate_map_assets(p);self.assertTrue(any('human approval' in e for e in errors))
    def test_deterministic_materializer_inserts_promoted_json_content(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);project=root/'p';(project/'09_output/side_stories').mkdir(parents=True);source=root/'source.md';output=root/'out.md';source.write_text('# A\n\nAnchor\n\nBody\n',encoding='utf-8')
            item={'schema_version':'1.1','class':'side_story','id':'SS-X','kind':'detour','status':'promoted','title':'Example','purpose':'p','reason_off_trunk':'r','payoff':'p','map_eligible':False,'reader_policy':{'min_age':10},'lineage':{'claim_ids':[],'source_ids':[],'bridge_ids':[],'hil_ids':[],'drift_paths':[],'origin_paths':[]},'placement':{'section_anchor':'Anchor','return_to':'anchor:Body'},'zoom_excursion':None,'content':{'body_markdown':'Inserted body'},'render':{'label':'Petit détour','marker':'[SIDE-STORY:SS-X]','required_in_reader':True}}
            (project/'09_output/side_stories/SS-X.json').write_text(json.dumps(item),encoding='utf-8')
            r=subprocess.run([sys.executable,str(ROOT/'scripts/materialize_side_stories.py'),'--project',str(project),'--source',str(source),'--output',str(output)],cwd=ROOT,text=True,capture_output=True);self.assertEqual(0,r.returncode,r.stdout+r.stderr);text=output.read_text(encoding='utf-8');self.assertIn('[SIDE-STORY:SS-X]',text);self.assertIn('Inserted body',text)
    def test_full_composition_preflight_passes(self):
        for project in (PRE,POST):
            r=subprocess.run([sys.executable,'scripts/qa_composition_pipeline.py',str(project)],cwd=ROOT,text=True,capture_output=True);self.assertEqual(0,r.returncode,r.stdout+r.stderr);self.assertIn('COMPOSITION PREFLIGHT OK',r.stdout)
if __name__=='__main__':unittest.main()
