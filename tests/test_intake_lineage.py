import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INTAKE_DIR = ROOT / 'docs' / 'intakes'
REGISTRY = INTAKE_DIR / 'intake_registry.json'


def all_registry_rows():
    rows=[]
    for path in sorted(INTAKE_DIR.glob('intake_registry*.json')):
        data=json.loads(path.read_text(encoding='utf-8'))
        if isinstance(data,list):rows.extend(data)
    return rows


class IntakeLineageTests(unittest.TestCase):
    def test_intake_lineage_audit_is_green(self):
        r = subprocess.run(
            [sys.executable, 'scripts/audit_intake_lineage.py'],
            cwd=ROOT,
            text=True,
            capture_output=True,
        )
        self.assertEqual(0, r.returncode, r.stdout + r.stderr)
        self.assertIn('INTAKE LINEAGE AUDIT OK', r.stdout)

    def test_known_legacy_intakes_are_explicit_provenance_debt(self):
        rows = json.loads(REGISTRY.read_text(encoding='utf-8'))
        by_name = {row.get('source_name'): row for row in rows}
        for name in (
            'SNAPSHOT_INTAKE_guide_and_run15.md',
            'FIELD_INTAKES_mihintale_abhayagiri_militarisation_horton.md',
            'INTAKE_kandy.md',
        ):
            self.assertIn(name, by_name)
            self.assertEqual('missing_source', by_name[name]['preservation_status'])
            self.assertTrue(by_name[name]['recovery_action'])
            self.assertIsNone(by_name[name]['repo_path'])

    def test_tea_intake_is_archived_not_reconstructed(self):
        rows = all_registry_rows()
        tea = next(row for row in rows if row.get('source_name') == 'INTAKE_tea_plantation_economy.md')
        self.assertEqual('archived', tea['preservation_status'])
        path = ROOT / tea['repo_path']
        self.assertTrue(path.exists())
        text = path.read_text(encoding='utf-8')
        self.assertIn('Coffee, tea, and the plantation economy', text)
        self.assertIn('The béké parallel', text)

    def test_future_archived_intake_cannot_bypass_registry(self):
        archived = {
            p.name for p in INTAKE_DIR.glob('*.md')
            if p.name != 'README.md'
        }
        rows = all_registry_rows()
        registered = {
            row.get('source_name') for row in rows
            if row.get('preservation_status') in {'archived','normalized_archival_copy'}
        }
        self.assertEqual(archived, registered)


if __name__ == '__main__':
    unittest.main()
