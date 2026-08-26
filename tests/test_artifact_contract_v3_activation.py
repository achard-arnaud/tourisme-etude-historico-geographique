import json
import subprocess
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECTS = [
    ROOT / 'examples' / 'sri_lanka_pre_1948',
    ROOT / 'examples' / 'sri_lanka_post_1948',
]


class ArtifactContractV3ActivationTests(unittest.TestCase):
    def test_both_corpora_explicitly_activate_v3(self):
        for project in PROJECTS:
            config = json.loads((project / 'project.json').read_text(encoding='utf-8'))
            self.assertEqual(3, config.get('artifact_contract_version'), project)

    def test_both_corpora_execute_v3_qa_not_fallback_v2(self):
        for project in PROJECTS:
            result = subprocess.run(
                [sys.executable, 'scripts/qa_project.py', str(project.relative_to(ROOT))],
                cwd=ROOT,
                text=True,
                capture_output=True,
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertIn('QA OK: contract v3', result.stdout)

    def test_legacy_override_is_explicit_and_id_scoped(self):
        migration = PROJECTS[1] / '00_method' / 'v3_contract_overrides.json'
        data = json.loads(migration.read_text(encoding='utf-8'))
        self.assertEqual(1, data.get('schema_version'))
        self.assertIn('Non-destructive', data.get('purpose', ''))
        for section in ('sources', 'claims', 'bridges'):
            self.assertIsInstance(data.get(section), dict)
            self.assertTrue(data[section])
        self.assertEqual('source_fact', data['claims']['C-POST-003']['type'])
        self.assertEqual('outcome', data['claims']['C-POST-003']['causal_role'])


if __name__ == '__main__':
    unittest.main()
