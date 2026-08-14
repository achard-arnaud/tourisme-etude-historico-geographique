import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ProjectToolTests(unittest.TestCase):
    def run_script(self, rel, *args):
        return subprocess.run([sys.executable, str(ROOT / rel), *map(str, args)], capture_output=True, text=True)

    def test_new_project_creates_canonical_os_tree(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / 'voyage'
            result = self.run_script('scripts/new_project.py', '--name', 'Voyage Test', '--output', target)
            self.assertEqual(result.returncode, 0, result.stderr)
            for rel in ['README.md','00_method','01_arcs','02_hil','03_wiki','04_graph','05_sources','06_bridges','07_drifts','08_questions','09_output']:
                self.assertTrue((target / rel).exists(), rel)

    def test_qa_project_rejects_unsourced_major_claim(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / '01_arcs' / 'A01_test' / 'claims').mkdir(parents=True)
            claim = {
                'id': 'C001', 'text': 'Major causal claim', 'arc': 'A01_test',
                'hil': 'HIL-03', 'zoom': 'Z2', 'confidence': 'A',
                'causal_role': 'driver', 'source_ids': []
            }
            (root / '01_arcs' / 'A01_test' / 'claims' / 'C001.json').write_text(json.dumps(claim), encoding='utf-8')
            result = self.run_script('scripts/qa_project.py', root)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn('unsourced major claim', (result.stdout + result.stderr).lower())

    def test_qa_project_accepts_sourced_major_claim(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / '01_arcs' / 'A01_test' / 'claims').mkdir(parents=True)
            (root / '05_sources').mkdir(parents=True)
            (root / '05_sources' / 'source_register.json').write_text(json.dumps([
                {'id':'S001','tier':'T1','title':'Academic anchor'}
            ]), encoding='utf-8')
            claim = {
                'id': 'C001', 'text': 'Major causal claim', 'arc': 'A01_test',
                'hil': 'HIL-03', 'zoom': 'Z2', 'confidence': 'A',
                'causal_role': 'driver', 'source_ids': ['S001']
            }
            (root / '01_arcs' / 'A01_test' / 'claims' / 'C001.json').write_text(json.dumps(claim), encoding='utf-8')
            result = self.run_script('scripts/qa_project.py', root)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == '__main__':
    unittest.main()
