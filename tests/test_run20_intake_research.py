import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRE = ROOT / 'examples' / 'sri_lanka_pre_1948'
POST = ROOT / 'examples' / 'sri_lanka_post_1948'
BACKLOG = ROOT / 'docs' / 'intakes' / 'intake_research_backlog.json'


class Run20IntakeResearchTests(unittest.TestCase):
    def test_every_registered_intake_has_research_workstream(self):
        registry = json.loads((ROOT / 'docs' / 'intakes' / 'intake_registry.json').read_text(encoding='utf-8'))
        backlog = json.loads(BACKLOG.read_text(encoding='utf-8'))
        registered = {row['id'] for row in registry}
        covered = {row['intake_id'] for row in backlog}
        self.assertTrue(registered.issubset(covered))
        self.assertGreaterEqual(sum(row['priority'] == 1 for row in backlog), 10)

    def test_pending_external_work_has_review_date(self):
        backlog = json.loads(BACKLOG.read_text(encoding='utf-8'))
        pending = [row for row in backlog if row['status'] == 'pending_external']
        self.assertTrue(pending)
        for row in pending:
            self.assertTrue(row.get('review_by'))

    def test_kandy_final_census_metric_supersedes_old_value(self):
        claim = json.loads((POST / '01_arcs' / 'A19_kandy_second_city_paradox' / 'claims' / 'C-R17-KDY-MET-006.json').read_text(encoding='utf-8'))
        text = json.dumps(claim)
        self.assertIn('172,489', text)
        self.assertIn('287,823', text)
        self.assertIn('-115,334', text)
        self.assertNotIn('157,921', claim['claim'])
        self.assertNotIn('-124,874', claim['claim'])
        self.assertIn('final DCS', claim['notes'])

    def test_plastic_enforcement_is_not_laundered_into_environmental_effect(self):
        claim = json.loads((POST / '01_arcs' / 'A14_coastal_environmental_governance' / 'claims' / 'C-R20-PLASTIC-ENFORCEMENT-001.json').read_text(encoding='utf-8'))
        self.assertEqual('policy_effect', claim['type'])
        self.assertIn('7,236 raids', claim['claim'])
        self.assertIn('does not establish', claim['bounded_by'])
        self.assertIn('ecological improvement', claim['bounded_by'])

    def test_targeted_research_sources_keep_primary_mirror_bounded(self):
        post_sources = json.loads((POST / '05_sources' / 'source_register_run20_intake_research.json').read_text(encoding='utf-8'))
        byid = {row['id']: row for row in post_sources}
        ptoms = byid['PTOMS-SC-2005-ARCHIVE-MIRROR']
        self.assertEqual('T3', ptoms['tier'])
        self.assertEqual('lead', ptoms['anchor_role'])
        self.assertIn('non-official', ptoms['limitations'])
        self.assertEqual([], ptoms['claims_supported'])

    def test_conservation_research_does_not_fake_gazette_facsimile(self):
        pre_sources = json.loads((PRE / '05_sources' / 'source_register_run20_intake_research.json').read_text(encoding='utf-8'))
        text = json.dumps(pre_sources)
        self.assertIn('Gazette 8356', text)
        self.assertIn('not the 1938 Gazette facsimile', text)
        backlog = {row['id']: row for row in json.loads(BACKLOG.read_text(encoding='utf-8'))}
        self.assertEqual('partially_resolved', backlog['IRB-R13-CONSERVATION']['status'])


if __name__ == '__main__':
    unittest.main()
