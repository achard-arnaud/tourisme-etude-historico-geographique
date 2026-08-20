import json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PROJECT=ROOT/'examples/sri_lanka_pre_1948'
class SideStoryContractTests(unittest.TestCase):
    def test_contract_assets_exist(self):
        for rel in ['skills/composing-side-stories/SKILL.md','templates/side-story.json','scripts/side_story_contract.py','scripts/new_side_story.py','scripts/materialize_side_stories.py','docs/SOP_SIDE_STORIES.md']:self.assertTrue((ROOT/rel).exists(),rel)
    def test_pre1948_inventory_is_backfilled_and_contract_valid(self):
        sys.path.insert(0,str(ROOT/'scripts'));from side_story_contract import load_side_stories,validate_side_stories,side_story_coverage
        items=load_side_stories(PROJECT);self.assertGreaterEqual(len(items),25);errors,warnings,count,coverage=validate_side_stories(PROJECT);self.assertEqual([],errors);self.assertEqual([],warnings);self.assertEqual(count,len(items));self.assertEqual(0,coverage['untracked']);self.assertGreaterEqual(coverage['discovered'],21)
        for _,item in items:self.assertEqual('1.1',item['schema_version']);self.assertEqual('side_story',item['class']);self.assertIsInstance(item['map_eligible'],bool)
    def test_method_return_is_optional_but_validated_narrative_return_is_resolved(self):
        sys.path.insert(0,str(ROOT/'scripts'));from side_story_contract import load_side_stories
        for _,item in load_side_stories(PROJECT):
            if item['kind']=='method':self.assertFalse((item.get('placement') or {}).get('return_to'))
            if item['status'] in {'validated','promoted'} and item['kind']!='method':self.assertTrue((item.get('placement') or {}).get('return_to'))
    def test_canonical_state_is_full_reader_not_delta(self):
        state=json.loads((PROJECT/'00_method/output_state.json').read_text(encoding='utf-8'));self.assertEqual('09_output/report_v3_full.md',state['canonical_markdown']);self.assertNotEqual(state['canonical_markdown'],state['delta_markdown'])
    def test_generic_project_qa_publishes_coverage(self):
        r=subprocess.run([sys.executable,'scripts/qa_project.py',str(PROJECT)],cwd=ROOT,text=True,capture_output=True);self.assertEqual(0,r.returncode,r.stdout+r.stderr);self.assertIn('side stories',r.stdout);self.assertIn('0 untracked',r.stdout)
    def test_cli_creates_candidate_instance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'project';(root/'09_output').mkdir(parents=True)
            r=subprocess.run([sys.executable,'scripts/new_side_story.py','--project',str(root),'--id','SS-TST-001','--kind','detour','--arc','A01_test','--title','Test detour','--section-anchor','Test','--return-to','A01_test','--purpose','Exercise'],cwd=ROOT,text=True,capture_output=True);self.assertEqual(0,r.returncode,r.stdout+r.stderr)
            item=json.loads((root/'09_output/side_stories/SS-TST-001.json').read_text(encoding='utf-8'));self.assertEqual('candidate',item['status'])
    def test_latest_manifest_routes_side_story_skill(self):
        data=json.loads((ROOT/'docs/RUN11_COMPOSITION_PIPELINE_MANIFEST.json').read_text(encoding='utf-8'));routed={x['skill'] for x in data['dispatched_skills']};known={p.parent.name for p in (ROOT/'skills').glob('*/SKILL.md')};self.assertEqual(known,routed);self.assertIn('composing-side-stories',routed)
if __name__=='__main__':unittest.main()
