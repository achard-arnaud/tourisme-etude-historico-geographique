import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


class ArtifactContractHardeningTests(unittest.TestCase):
    def run_qa(self, root):
        return subprocess.run(
            [sys.executable, str(ROOT / 'scripts' / 'qa_project.py'), str(root)],
            capture_output=True,
            text=True,
        )

    def strict_root(self, root):
        (root / 'project.json').write_text(json.dumps({
            'name': 'contract fixture',
            'method': 'tourisme-etude-historico-geographique',
            'version': 3,
            'artifact_contract_version': 3,
        }), encoding='utf-8')

    def write_claim(self, root, claim, arc='A01_test'):
        claims = root / '01_arcs' / arc / 'claims'
        claims.mkdir(parents=True, exist_ok=True)
        (claims / f"{claim['id']}.json").write_text(json.dumps(claim), encoding='utf-8')

    def write_sources(self, root, sources):
        d = root / '05_sources'
        d.mkdir(parents=True, exist_ok=True)
        (d / 'source_register.json').write_text(json.dumps(sources), encoding='utf-8')

    def base_claim(self, **overrides):
        claim = {
            'id': 'C001',
            'type': 'claim',
            'claim': 'A bounded historical statement.',
            'arc': 'A01_test',
            'zoom': 'Z2',
            'confidence': 'B',
            'causal_role': 'context',
            'source_ids': [],
            'notes': '',
        }
        claim.update(overrides)
        return claim

    def base_source(self, sid='S001', **overrides):
        source = {
            'id': sid,
            'tier': 'T1',
            'anchor_role': 'canonical anchor',
            'title': 'Academic anchor',
            'date': '2020',
            'author_or_institution': 'Example University Press',
            'scope': 'Sri Lanka',
            'claims_supported': ['C001'],
            'limitations': 'None material for this fixture.',
            'provenance': 'direct',
            'url': 'https://example.org/source',
        }
        source.update(overrides)
        return source

    def test_claim_requires_closed_statement_type(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); self.strict_root(root)
            self.write_claim(root, self.base_claim(type='made_up_type'))
            r = self.run_qa(root)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn('invalid statement type', (r.stdout + r.stderr).lower())

    def test_claim_requires_arc_field_matching_path(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); self.strict_root(root)
            self.write_claim(root, self.base_claim(arc='A99_other'))
            r = self.run_qa(root)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn('arc/path mismatch', (r.stdout + r.stderr).lower())

    def test_causal_role_is_closed_vocabulary(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); self.strict_root(root)
            self.write_claim(root, self.base_claim(causal_role='constriant'))
            r = self.run_qa(root)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn('invalid causal_role', (r.stdout + r.stderr).lower())

    def test_metric_requires_structured_metric_hygiene(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); self.strict_root(root)
            self.write_claim(root, self.base_claim(type='metric', claim='GDP rose by 12%.'))
            r = self.run_qa(root)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn('metric metadata', (r.stdout + r.stderr).lower())

    def test_major_causal_claim_requires_independent_corroboration(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); self.strict_root(root)
            self.write_sources(root, [self.base_source()])
            self.write_claim(root, self.base_claim(causal_role='driver', source_ids=['S001']))
            r = self.run_qa(root)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn('independent corroboration', (r.stdout + r.stderr).lower())

    def test_bounded_by_allows_explicit_single_source_exception(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); self.strict_root(root)
            self.write_sources(root, [self.base_source()])
            self.write_claim(root, self.base_claim(
                causal_role='driver',
                source_ids=['S001'],
                bounded_by='single-source anchor; causal scope intentionally limited',
            ))
            r = self.run_qa(root)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_source_requires_closed_anchor_role_and_provenance(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); self.strict_root(root)
            self.write_sources(root, [self.base_source(anchor_role='corroborating current anchor', provenance='snippet')])
            r = self.run_qa(root)
            self.assertNotEqual(r.returncode, 0)
            output = (r.stdout + r.stderr).lower()
            self.assertIn('invalid anchor_role', output)
            self.assertIn('invalid provenance', output)

    def test_bridge_requires_transportability_contract(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td); self.strict_root(root)
            for cid in ('C001', 'C002'):
                self.write_claim(root, self.base_claim(id=cid, confidence='C'))
            bridges = root / '06_bridges'
            bridges.mkdir(parents=True)
            (bridges / 'B001.json').write_text(json.dumps({
                'id': 'B001', 'from_claim': 'C001', 'to_claim': 'C002',
                'question': 'Does the mechanism travel?', 'mechanism': 'test',
                'result': 'C', 'source_ids': [],
            }), encoding='utf-8')
            r = self.run_qa(root)
            self.assertNotEqual(r.returncode, 0)
            self.assertIn('bridge missing transportability', (r.stdout + r.stderr).lower())

    def test_scaffold_directories_are_git_persistable(self):
        with tempfile.TemporaryDirectory() as td:
            target = Path(td) / 'project'
            r = subprocess.run([
                sys.executable, str(ROOT / 'scripts' / 'new_project.py'),
                '--name', 'Contract Test', '--output', str(target),
            ], capture_output=True, text=True)
            self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
            for rel in ('02_hil', '08_questions'):
                self.assertTrue((target / rel / '.gitkeep').exists(), rel)


if __name__ == '__main__':
    unittest.main()
