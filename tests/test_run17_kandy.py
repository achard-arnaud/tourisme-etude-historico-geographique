from __future__ import annotations
import json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'examples/sri_lanka_pre_1948'; POST=ROOT/'examples/sri_lanka_post_1948'

class Run17KandyTests(unittest.TestCase):
    def test_acceptance_audit_is_green(self):
        r=subprocess.run([sys.executable,'scripts/audit_run17_kandy.py'],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(0,r.returncode,r.stdout+r.stderr)
        self.assertIn('RUN17 KANDY AUDIT OK',r.stdout)

    def test_measurement_precedes_explanation_and_can_refute(self):
        m=json.loads((POST/'00_method/capture/run17_kandy_measurements.json').read_text(encoding='utf-8'))
        self.assertEqual('D',m['hypothesis_status'])
        self.assertGreaterEqual(len(m['metrics']),8)

    def test_two_dispossessions_have_distinct_lineage(self):
        base=PRE/'01_arcs/A07b_kandyan_kingdom_and_defensive_interior/claims'
        land=json.loads((base/'C-R17-KDY-LAND-001.json').read_text(encoding='utf-8'))
        labour=json.loads((base/'C-R17-KDY-LABOUR-001.json').read_text(encoding='utf-8'))
        self.assertNotEqual(set(land['source_ids']),set(labour['source_ids']))

    def test_sacred_comparator_is_mechanism_only(self):
        b=json.loads((POST/'06_bridges/B-R17-KDY-SACRED-CITY-COMPARATOR-001.json').read_text(encoding='utf-8'))
        self.assertEqual('mechanism',b['transportability'])
        self.assertTrue(any('colombo' in x.lower() for x in b['confounders']))
        self.assertTrue(b['bounded_by'])

if __name__=='__main__': unittest.main()
