import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class Run2ReviewHardeningTests(unittest.TestCase):
    def test_worked_examples_materialize_claims_and_bridges(self):
        for name in ['sri_lanka_pre_1948', 'sri_lanka_post_1948']:
            project = ROOT / 'examples' / name
            claims = list((project / '01_arcs').glob('*/claims/*.json'))
            bridges = list((project / '06_bridges').glob('*.json'))
            self.assertGreaterEqual(len(claims), 2, f'{name}: expected atomic causal claims')
            self.assertGreaterEqual(len(bridges), 1, f'{name}: expected at least one bridge')

    def test_pre_1948_cambridge_sources_use_exact_resources(self):
        p = ROOT / 'examples' / 'sri_lanka_pre_1948' / '05_sources' / 'source_register.json'
        sources = json.loads(p.read_text(encoding='utf-8'))
        urls = {s['id']: s['url'] for s in sources}
        self.assertIn('/classifications-at-work-social-categories-and-dutch-bureaucracy-in-colonial-sri-lanka/', urls['CAMBRIDGE-CLASSIFICATION'])
        self.assertIn('/lawmaking-in-dutch-sri-lanka/', urls['CAMBRIDGE-LAWMAKING'])

    def test_post_1948_registers_current_presidency_anchor(self):
        p = ROOT / 'examples' / 'sri_lanka_post_1948' / '05_sources' / 'source_register.json'
        sources = json.loads(p.read_text(encoding='utf-8'))
        urls = [s['url'] for s in sources]
        self.assertTrue(any('presidentsoffice.gov.lk/president/current' in u for u in urls))


if __name__ == '__main__':
    unittest.main()
