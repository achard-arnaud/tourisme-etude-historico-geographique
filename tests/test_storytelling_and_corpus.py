import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class StorytellingAndCorpusTests(unittest.TestCase):
    def test_storytelling_skill_exists_and_exposes_reader_contract(self):
        p = ROOT / 'skills' / 'storytelling-historical-travel' / 'SKILL.md'
        self.assertTrue(p.exists(), 'missing storytelling-historical-travel skill')
        text = p.read_text(encoding='utf-8')
        for token in ['advanced', 'intermediate', 'child', 'length policy', 'language', 'tone', 'register', 'cross-reference']:
            self.assertIn(token, text.lower())

    def test_root_orchestrator_makes_storytelling_non_destructive_for_advanced(self):
        text = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('storytelling-historical-travel', text)
        self.assertIn('must never set a maximum length', text)

    def test_advanced_storytelling_has_no_length_cap_and_a_retention_gate(self):
        text = (ROOT / 'skills' / 'storytelling-historical-travel' / 'SKILL.md').read_text(encoding='utf-8').lower()
        for token in ['no maximum length', 'baseline', 'deltas', 'content-preservation gate', 'silent loss']:
            self.assertIn(token, text)

    def test_storytelling_second_pass_has_historical_nonfiction_gate(self):
        text = (ROOT / 'skills' / 'storytelling-historical-travel' / 'SKILL.md').read_text(encoding='utf-8').lower()
        for token in ['pace', 'but/therefore', 'invented dialogue', 'promise and continuity ledger', 'source-attested']:
            self.assertIn(token, text)

    def test_current_manifest_routes_every_repo_skill(self):
        data = __import__('json').loads((ROOT / 'docs' / 'RUN7_WORKFLOW_MANIFEST.json').read_text(encoding='utf-8'))
        routed = {item['skill'] for item in data['dispatched_skills']} | {item['skill'] for item in data['skipped_skills']}
        known = {p.parent.name for p in (ROOT / 'skills').glob('*/SKILL.md')}
        self.assertEqual(routed, known)

    def test_source_policy_distinguishes_specialist_institutional_anchor_from_t1(self):
        text = (ROOT / 'docs' / 'source_policy.md').read_text(encoding='utf-8').lower()
        self.assertIn('specialist institutional anchor', text)
        self.assertIn('does not become t1', text)

    def test_sri_lanka_dual_examples_exist(self):
        pre = ROOT / 'examples' / 'sri_lanka_pre_1948'
        post = ROOT / 'examples' / 'sri_lanka_post_1948'
        for project in [pre, post]:
            self.assertTrue((project / 'README.md').exists())
            self.assertTrue((project / '05_sources' / 'source_register.json').exists())
            self.assertTrue((project / '09_output' / 'report.md').exists())

    def test_advanced_reader_contracts_are_unconstrained(self):
        import json
        for name in ['sri_lanka_pre_1948', 'sri_lanka_post_1948']:
            contract = json.loads((ROOT / 'examples' / name / '00_method' / 'reader_contract.json').read_text(encoding='utf-8'))
            self.assertEqual(contract['audience'], 'advanced')
            self.assertEqual(contract['length_policy'], 'unconstrained')
            self.assertNotIn('length_budget', contract)
            self.assertIn('lossless', contract['baseline_policy'])

    def test_stichting_crawl_inventory_is_materialized(self):
        p = ROOT / 'examples' / 'sri_lanka_pre_1948' / '05_sources' / 'stichting_nederland_sri_lanka_inventory.md'
        self.assertTrue(p.exists())
        text = p.read_text(encoding='utf-8').lower()
        for token in ['dutch forts in sri lanka', 'slavery in pre-colonial sri lanka', 'willem de melho', 'virtual slave island', 'invented heritage']:
            self.assertIn(token, text)

    def test_sri_lanka_conversation_corpus_and_long_baselines_are_materialized(self):
        pre = ROOT / 'examples' / 'sri_lanka_pre_1948'
        corpus = pre / '05_sources' / 'conversation_corpus'
        for number in range(15):
            self.assertTrue(any(corpus.glob(f'{number:02d}_*.md')), f'missing conversation fiche {number:02d}')
        register = (pre / '00_method' / 'conversation_capitalization_register.md').read_text(encoding='utf-8')
        self.assertIn('Bus, santé, assurance', register)
        self.assertIn('Panneaux de musée', register)
        self.assertIn('Échec V2', register)
        pre_words = len((pre / '09_output' / 'report_v1_full.md').read_text(encoding='utf-8').split())
        post_words = len((ROOT / 'examples' / 'sri_lanka_post_1948' / '09_output' / 'report_v1_full.md').read_text(encoding='utf-8').split())
        self.assertGreater(pre_words, 16000)
        self.assertGreater(post_words, 5000)

    def test_v3_outputs_retain_the_long_v1_baselines(self):
        import json
        import re
        metrics_path = ROOT / 'docs' / 'RUN7_V3_RETENTION_METRICS.json'
        self.assertTrue(metrics_path.exists())
        metrics = {item['project']: item for item in json.loads(metrics_path.read_text(encoding='utf-8'))}
        self.assertGreater(metrics['pre']['v3_docx_words'], metrics['pre']['baseline_docx_words'])
        self.assertGreater(metrics['post']['v3_docx_words'], metrics['post']['baseline_docx_words'])
        self.assertGreaterEqual(metrics['pre']['retention_vs_baseline_percent'], 107.0)
        self.assertGreaterEqual(metrics['post']['retention_vs_baseline_percent'], 125.0)
        pre_pdf = ROOT / 'examples' / 'sri_lanka_pre_1948' / '09_output' / 'Sri_Lanka_Fresque_historico_geographique_vol_retour_v3.pdf'
        post_pdf = ROOT / 'examples' / 'sri_lanka_post_1948' / '09_output' / 'Sri_Lanka_1948_2026_etude_historico_geographique_v3.pdf'
        pdf_page_count = lambda path: len(re.findall(rb'/Type\s*/Page\b', path.read_bytes()))
        self.assertGreaterEqual(pdf_page_count(pre_pdf), 60)
        self.assertGreaterEqual(pdf_page_count(post_pdf), 20)

    def test_v3_docx_structurally_preserves_every_v1_paragraph_and_table(self):
        import xml.etree.ElementTree as ET
        import zipfile

        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

        def body_inventory(path):
            with zipfile.ZipFile(path) as package:
                root = ET.fromstring(package.read('word/document.xml'))
            body = root.find('w:body', ns)
            paragraphs = []
            for paragraph in body.findall('w:p', ns):
                text = ''.join(node.text or '' for node in paragraph.findall('.//w:t', ns))
                paragraphs.append(text)
            return paragraphs, len(body.findall('.//w:tbl', ns))

        cases = [
            (
                ROOT / 'examples' / 'sri_lanka_pre_1948' / '09_output' / 'archive' / 'Sri_Lanka_Fresque_historico_geographique_vol_retour_v1.docx',
                ROOT / 'examples' / 'sri_lanka_pre_1948' / '09_output' / 'Sri_Lanka_Fresque_historico_geographique_vol_retour_v3.docx',
                {3, 4, 5},
            ),
            (
                ROOT / 'examples' / 'sri_lanka_post_1948' / '09_output' / 'archive' / 'Sri_Lanka_1948_2026_etude_historico_geographique_v1.docx',
                ROOT / 'examples' / 'sri_lanka_post_1948' / '09_output' / 'Sri_Lanka_1948_2026_etude_historico_geographique_v3.docx',
                {3, 4},
            ),
        ]
        for baseline_path, v3_path, replaced_cover_indices in cases:
            baseline_paragraphs, baseline_tables = body_inventory(baseline_path)
            v3_paragraphs, v3_tables = body_inventory(v3_path)
            expected = [text for i, text in enumerate(baseline_paragraphs) if i not in replaced_cover_indices and text]
            candidate = iter(text for text in v3_paragraphs if text)
            for paragraph in expected:
                self.assertTrue(any(current == paragraph for current in candidate), f'lost V1 paragraph: {paragraph[:80]}')
            self.assertEqual(v3_tables, baseline_tables, 'V3 changed the V1 table inventory')

    def test_legacy_reader_renderer_refuses_silent_advanced_compression(self):
        import importlib.util
        path = ROOT / 'scripts' / 'reader_retention.py'
        spec = importlib.util.spec_from_file_location('reader_renderer', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        project = ROOT / 'examples' / 'sri_lanka_pre_1948'
        short_delta = (project / '09_output' / 'report.md').read_text(encoding='utf-8')
        with self.assertRaisesRegex(RuntimeError, 'Refusing silent advanced-reader compression'):
            module.enforce_advanced_retention(project, short_delta)


if __name__ == '__main__':
    unittest.main()
