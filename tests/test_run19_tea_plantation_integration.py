import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRE = ROOT / 'examples' / 'sri_lanka_pre_1948'
POST = ROOT / 'examples' / 'sri_lanka_post_1948'


class Run19TeaPlantationIntegrationTests(unittest.TestCase):
    def test_four_arc_contracts_exist_and_no_tea_thread(self):
        arcs = [
            PRE / '01_arcs' / 'A07c_coffee_collapse_and_tea_conversion' / 'ARC.md',
            PRE / '01_arcs' / 'A09b_plantation_labour_system' / 'ARC.md',
            POST / '01_arcs' / 'A17b_plantation_economy_and_value_capture' / 'ARC.md',
            POST / '01_arcs' / 'A18_malaiyaha_tamils_status_and_wage' / 'ARC.md',
        ]
        for path in arcs:
            self.assertTrue(path.exists(), path)
            text = path.read_text(encoding='utf-8')
            self.assertIn('Causal question', text)
            self.assertIn('no_tea_thread: true', text)

    def test_ishikawa_fragments_precede_new_claims(self):
        pre_frag = PRE / '00_method' / 'run19_ishikawa_coffee_conversion_fragments.md'
        post_frag = POST / '00_method' / 'run19_ishikawa_value_capture_fragments.md'
        self.assertTrue(pre_frag.exists())
        self.assertTrue(post_frag.exists())
        self.assertIn('not claims', pre_frag.read_text(encoding='utf-8').lower())
        self.assertIn('not claims', post_frag.read_text(encoding='utf-8').lower())

    def test_six_rival_hypotheses_are_preregistered_on_canonical_arcs(self):
        pre = json.loads((PRE / '08_questions' / 'question_register.json').read_text(encoding='utf-8'))
        post = json.loads((POST / '08_questions' / 'question_register.json').read_text(encoding='utf-8'))
        by_id = {q['id']: q for q in pre + post}
        expected = {'Q-TEA-H1', 'Q-TEA-H2', 'Q-TEA-H3', 'Q-VALUE-M1', 'Q-VALUE-M2', 'Q-VALUE-M3'}
        self.assertTrue(expected.issubset(by_id))
        for qid in ('Q-TEA-H1', 'Q-TEA-H2', 'Q-TEA-H3'):
            self.assertEqual('A07c_coffee_collapse_and_tea_conversion', by_id[qid].get('arc'))
        for qid in ('Q-VALUE-M1', 'Q-VALUE-M2', 'Q-VALUE-M3'):
            self.assertEqual('A17b_plantation_economy_and_value_capture', by_id[qid].get('arc'))
        for qid in expected:
            self.assertTrue(by_id[qid].get('discriminating_test'))
            self.assertTrue(by_id[qid].get('falsifier'))
            self.assertEqual(by_id[qid].get('status'), 'open')

    def test_legacy_alias_collisions_do_not_reappear(self):
        self.assertFalse((PRE / '01_arcs' / 'A07b_coffee_collapse_and_tea_conversion').exists())
        self.assertFalse((POST / '01_arcs' / 'A17_plantation_economy_and_value_capture').exists())

    def test_intake_is_preserved_in_repo(self):
        intake = ROOT / 'docs' / 'intakes' / 'INTAKE_tea_plantation_economy.md'
        self.assertTrue(intake.exists())
        text = intake.read_text(encoding='utf-8')
        self.assertIn('Coffee, tea, and the plantation economy', text)
        self.assertIn('Why fair trade, organic and appellation may not be development levers', text)
        self.assertIn('The béké parallel', text)


if __name__ == '__main__':
    unittest.main()
