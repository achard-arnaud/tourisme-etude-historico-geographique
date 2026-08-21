import json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];POST=ROOT/'examples/sri_lanka_post_1948';PRE=ROOT/'examples/sri_lanka_pre_1948'
class Run5ComparativeWikiTests(unittest.TestCase):
    def test_required_capabilities_are_present_without_hardcoded_skill_count(self):
        skills={p.name for p in (ROOT/'skills').iterdir() if (p/'SKILL.md').exists()}
        required={'analyzing-economy-and-infrastructure','analyzing-geography-and-environment','analyzing-institutions-and-power','analyzing-security-and-geopolitics','analyzing-society-and-demography','auditing-historiography-and-drifts','building-causal-bridges','capturing-field-evidence','editing-historical-travel-output','maintaining-wiki-and-graph','sanitizing-historical-claims','sourcing-historical-anchors','storytelling-historical-travel','structuring-chronological-arcs','zooming-geographic-scales','analyzing-religion-culture-legitimacy','analyzing-regional-global-systems','composing-side-stories','composing-arc-recaps','curating-historical-map-assets','tailoring-reader-profiles'}
        self.assertTrue(required<=skills)
    def test_root_skill_has_long_project_and_comparator_gates(self):
        text=(ROOT/'SKILL.md').read_text(encoding='utf-8');self.assertIn('State checkpoint',text);self.assertIn('Comparative gate',text);self.assertIn('Prompt-review loop',text)
    def test_method_contracts_are_executable_not_heading_snapshots(self):
        for rel in ['scripts/graph_link_audit.py','scripts/side_story_contract.py','scripts/arc_recap_contract.py','scripts/reader_profile_contract.py','templates/side-story.json','templates/arc-recap.json']:
            self.assertTrue((ROOT/rel).exists(),rel)
        result=subprocess.run([sys.executable,'scripts/audit_workflow.py','--latest'],cwd=ROOT,text=True,capture_output=True);self.assertEqual(0,result.returncode,result.stdout+result.stderr)
    def test_run5_source_register_is_modular_and_unique(self):
        ids=set()
        for p in sorted((POST/'05_sources').glob('source_register*.json')):
            for item in json.loads(p.read_text(encoding='utf-8')):self.assertNotIn(item['id'],ids);ids.add(item['id'])
        for required in ['ADB-NORTHERN-ROADS','CAMBRIDGE-DRAVIDIAN-CAPITAL','BPS-INDONESIA-LANGUAGE-2024']:self.assertIn(required,ids)
    def test_wiki_and_graph_materialized_and_graph_links_resolve(self):
        for project in (PRE,POST):
            self.assertTrue((project/'03_wiki'/'README.md').exists());self.assertTrue((project/'04_graph'/'edges.jsonl').exists());self.assertTrue((project/'04_graph'/'nodes.jsonl').exists())
            r=subprocess.run([sys.executable,'scripts/graph_link_audit.py',str(project)],cwd=ROOT,text=True,capture_output=True);self.assertEqual(0,r.returncode,r.stdout+r.stderr);self.assertIn('0 unresolved',r.stdout)
    def test_run5_claims_and_drift_audit_exist(self):
        claims=POST/'01_arcs'/'A13_comparative_development_trajectories'/'claims'
        for n in ['C-POST-WAR-TERRITORY-001.json','C-COMP-TN-DEV-001.json','C-COMP-ID-LANG-002.json']:self.assertTrue((claims/n).exists())
        self.assertTrue((POST/'07_drifts'/'run5_comparator_development_audit.md').exists())
if __name__=='__main__':unittest.main()
