import json,subprocess,sys,unittest
from pathlib import Path
REPO=Path(__file__).resolve().parents[1];PROJECT=REPO/'examples/sri_lanka_pre_1948'
class Pre1948FunctionalBaselineTests(unittest.TestCase):
    def test_canonical_project_scaffold_is_materialized(self):
        for rel in ['project.json','00_method/output_state.json','00_method/reader_profile.json','01_arcs','02_hil','03_wiki','04_graph/nodes.jsonl','05_sources','06_bridges','07_drifts','08_questions','09_output/side_stories','09_output/arc_recaps','09_output/map_assets']:self.assertTrue((PROJECT/rel).exists(),rel)
    def test_claims_persist_type_and_arc(self):
        paths=list(PROJECT.glob('01_arcs/*/claims/*.json'));self.assertGreaterEqual(len(paths),9)
        for p in paths:
            c=json.loads(p.read_text(encoding='utf-8'));self.assertIn('type',c);self.assertEqual(p.parents[1].name,c['arc'])
    def test_eight_hil_baselines_and_arc_recaps_cover_materialized_arcs(self):
        self.assertEqual(8,len(list((PROJECT/'02_hil').glob('HIL-*/baseline.json'))))
        arcs={p.name for p in (PROJECT/'01_arcs').iterdir() if p.is_dir() and (p/'ARC.md').exists()};recaps=list((PROJECT/'09_output/arc_recaps').glob('*.json'));self.assertEqual(len(arcs),len(recaps))
    def test_questions_side_story_coverage_and_latest_workflow_are_persisted(self):
        self.assertTrue((PROJECT/'08_questions/baseline_questions.md').exists());manifest=json.loads((REPO/'docs/RUN11_COMPOSITION_PIPELINE_MANIFEST.json').read_text(encoding='utf-8'));known={p.parent.name for p in (REPO/'skills').glob('*/SKILL.md')};self.assertEqual(known,{x['skill'] for x in manifest['dispatched_skills']})
        sys.path.insert(0,str(REPO/'scripts'));from side_story_contract import side_story_coverage;self.assertEqual(0,side_story_coverage(PROJECT)['untracked'])
    def test_functional_runner_passes_on_canonical_fixture(self):
        r=subprocess.run([sys.executable,'scripts/qa_functional_pre1948.py'],cwd=REPO,text=True,capture_output=True);self.assertEqual(0,r.returncode,r.stdout+r.stderr);self.assertIn('PRE1948 FUNCTIONAL QA OK',r.stdout)
if __name__=='__main__':unittest.main()
