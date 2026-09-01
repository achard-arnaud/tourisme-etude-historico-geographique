import json,subprocess,sys,unittest,zipfile,xml.etree.ElementTree as ET
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
class StorytellingAndCorpusTests(unittest.TestCase):
    def test_storytelling_contract_and_reader_profiles_exist(self):
        text=(ROOT/'skills/storytelling-historical-travel/SKILL.md').read_text(encoding='utf-8').lower()
        for token in ['advanced','intermediate','child','no maximum length','content-preservation gate','invented dialogue','reader plan']:self.assertIn(token,text)
        for name in ['historian_enthusiast','child_10_plus','educated_generalist']:self.assertTrue((ROOT/'reader_profiles'/f'{name}.json').exists())
    def test_root_orchestrator_is_non_destructive_for_advanced(self):
        text=(ROOT/'SKILL.md').read_text(encoding='utf-8');self.assertIn('storytelling-historical-travel',text);self.assertIn('must never set a maximum length',text)
    def test_latest_manifest_routes_every_repo_skill(self):
        data=json.loads((ROOT/'docs/RUN11_COMPOSITION_PIPELINE_MANIFEST.json').read_text(encoding='utf-8'));routed={x['skill'] for x in data['dispatched_skills']}|{x['skill'] for x in data['skipped_skills']};known={p.parent.name for p in (ROOT/'skills').glob('*/SKILL.md')};self.assertEqual(routed,known)
    def test_source_policy_distinguishes_specialist_institutional_anchor_from_t1(self):
        text=(ROOT/'docs/source_policy.md').read_text(encoding='utf-8').lower();self.assertIn('specialist institutional anchor',text);self.assertIn('does not become t1',text)
    def test_dual_long_baselines_and_advanced_contracts_exist(self):
        for name,min_words in [('sri_lanka_pre_1948',16000),('sri_lanka_post_1948',5000)]:
            p=ROOT/'examples'/name;self.assertTrue((p/'09_output/report.md').exists());self.assertGreater(len((p/'09_output/report_v1_full.md').read_text(encoding='utf-8').split()),min_words);c=json.loads((p/'00_method/reader_contract.json').read_text(encoding='utf-8'));self.assertEqual('advanced',c['audience']);self.assertEqual('unconstrained',c['length_policy'])
    def test_v3_outputs_retain_long_v1_baselines(self):
        metrics={x['project']:x for x in json.loads((ROOT/'docs/RUN7_V3_RETENTION_METRICS.json').read_text(encoding='utf-8'))};self.assertGreaterEqual(metrics['pre']['retention_vs_baseline_percent'],107.0);self.assertGreaterEqual(metrics['post']['retention_vs_baseline_percent'],125.0)
    def test_v3_docx_preserves_baseline_table_inventory(self):
        ns={'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        def inspect(path):
            with zipfile.ZipFile(path) as z:root=ET.fromstring(z.read('word/document.xml'))
            tables=len(root.findall('.//w:tbl',ns));text=' '.join((node.text or '') for node in root.findall('.//w:t',ns));return tables,text
        sys.path.insert(0,str(ROOT/'scripts'))
        from post_review_side_story_placement import is_post_review_materializable
        from side_story_contract import load_side_stories
        for name,prefix in [('sri_lanka_pre_1948','Sri_Lanka_Fresque_historico_geographique_vol_retour'),('sri_lanka_post_1948','Sri_Lanka_1948_2026_etude_historico_geographique')]:
            project=ROOT/'examples'/name;o=project/'09_output';baseline,_=inspect(o/'archive'/f'{prefix}_v1.docx');rendered,text=inspect(o/f'{prefix}_v3.docx')
            self.assertGreaterEqual(rendered,baseline)
            # Run41 intentionally materializes one closed DOCX table per reader-eligible
            # side story. Preserve every baseline table, then bound additions by the
            # eligible-story inventory plus at most one presentation legend. This keeps
            # the old anti-proliferation gate without forbidding the new inline stories.
            eligible=sum(1 for _,item in load_side_stories(project) if is_post_review_materializable(item) and item.get('materialization_mode')!='existing_fragment')
            self.assertLessEqual(rendered,baseline+eligible+1)
            if rendered>baseline:self.assertIn('Légende des encadrés',text)
    def test_legacy_renderer_refuses_silent_advanced_compression(self):
        import importlib.util
        spec=importlib.util.spec_from_file_location('ret',ROOT/'scripts/reader_retention.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);p=ROOT/'examples/sri_lanka_pre_1948'
        with self.assertRaisesRegex(RuntimeError,'Refusing silent advanced-reader compression'):m.enforce_advanced_retention(p,(p/'09_output/report.md').read_text(encoding='utf-8'))
if __name__=='__main__':unittest.main()
