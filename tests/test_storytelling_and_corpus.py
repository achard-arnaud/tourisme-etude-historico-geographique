import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class StorytellingAndCorpusTests(unittest.TestCase):
    def test_storytelling_skill_exists_and_exposes_reader_contract(self):
        p = ROOT / 'skills' / 'storytelling-historical-travel' / 'SKILL.md'
        self.assertTrue(p.exists(), 'missing storytelling-historical-travel skill')
        text = p.read_text(encoding='utf-8')
        for token in ['advanced', 'intermediate', 'child', 'length budget', 'language', 'tone', 'register', 'cross-reference']:
            self.assertIn(token, text.lower())

    def test_root_orchestrator_routes_final_narrative_to_storytelling(self):
        text = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        self.assertIn('storytelling-historical-travel', text)

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

    def test_stichting_crawl_inventory_is_materialized(self):
        p = ROOT / 'examples' / 'sri_lanka_pre_1948' / '05_sources' / 'stichting_nederland_sri_lanka_inventory.md'
        self.assertTrue(p.exists())
        text = p.read_text(encoding='utf-8').lower()
        for token in ['dutch forts in sri lanka', 'slavery in pre-colonial sri lanka', 'willem de melho', 'virtual slave island', 'invented heritage']:
            self.assertIn(token, text)


if __name__ == '__main__':
    unittest.main()
