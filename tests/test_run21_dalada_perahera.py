import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRE = ROOT / 'examples' / 'sri_lanka_pre_1948'
POST = ROOT / 'examples' / 'sri_lanka_post_1948'


class Run21DaladaPeraheraTests(unittest.TestCase):
    def load(self, path):
        return json.loads(path.read_text(encoding='utf-8'))

    def test_same_page_is_scoped_as_current_primary_and_historical_institutional(self):
        pre = self.load(PRE / '05_sources' / 'source_register_run21_dalada_perahera.json')[0]
        post = self.load(POST / '05_sources' / 'source_register_run21_dalada_perahera.json')[0]
        self.assertEqual(pre['url'], post['url'])
        self.assertEqual(pre['tier'], 'T2')
        self.assertEqual(post['tier'], 'T0')
        self.assertIn('not an independent', pre['limitations'])
        self.assertIn('2026 schedule', post['scope'])

    def test_historical_temple_narrative_remains_typed_as_tradition(self):
        claim = self.load(PRE / '01_arcs' / 'A07b_kandyan_kingdom_and_defensive_interior' / 'claims' / 'C-R21-KDY-PERAHERA-TRADITION-001.json')
        self.assertEqual(claim['type'], 'tradition')
        self.assertEqual(claim['confidence'], 'C')
        self.assertIn('DALADA-PERAHERA-HISTORY-OFFICIAL', claim['source_ids'])

    def test_existing_relic_claim_gains_institutional_memory_without_confidence_inflation(self):
        claim = self.load(PRE / '01_arcs' / 'A07b_kandyan_kingdom_and_defensive_interior' / 'claims' / 'C-R17-KDY-RELIC-001.json')
        self.assertEqual(claim['confidence'], 'B')
        self.assertIn('DALADA-PERAHERA-HISTORY-OFFICIAL', claim['source_ids'])
        self.assertIn('not counted as independent proof', claim['bounded_by'])

    def test_kandy_specific_ritual_anchor_strengthens_comparator_only_to_c(self):
        bridge = self.load(POST / '06_bridges' / 'B-R17-KDY-SACRED-CITY-COMPARATOR-001.json')
        self.assertEqual(bridge['result'], 'C')
        self.assertIn('DALADA-PERAHERA-OFFICIAL-2026', bridge['source_ids'])
        self.assertEqual(bridge['transportability'], 'mechanism')

    def test_perahera_to_functional_flow_bridge_is_bounded(self):
        bridge = self.load(POST / '06_bridges' / 'B-R21-KDY-PERAHERA-FUNCTIONAL-FLOW-001.json')
        self.assertEqual(bridge['result'], 'C')
        self.assertIn('no event-specific attendance denominator', bridge['confounders'])
        self.assertIn('not the share', bridge['bounded_by'])


if __name__ == '__main__':
    unittest.main()
