import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from question_contract import validate_question_registers


class QuestionRegisterContractTests(unittest.TestCase):
    def _project(self, records):
        td = tempfile.TemporaryDirectory()
        root = Path(td.name)
        qdir = root / '08_questions'
        qdir.mkdir(parents=True)
        (qdir / 'question_register.json').write_text(json.dumps(records), encoding='utf-8')
        return td, root

    def test_valid_gate_pair_passes(self):
        records = [
            {
                'id': 'Q-A-000', 'question': 'Does the gate exist?', 'kind': 'metric',
                'status': 'open', 'discriminating_test': 'Measure it.',
                'falsifier': 'No measurable population.', 'priority': 1,
                'is_gate_for': ['Q-A-001']
            },
            {
                'id': 'Q-A-001', 'question': 'Does the parent claim hold?', 'kind': 'causal',
                'status': 'open', 'discriminating_test': 'Compare two series.',
                'falsifier': 'The series diverge.', 'priority': 1, 'gate': 'Q-A-000'
            }
        ]
        td, root = self._project(records)
        try:
            errors, warnings, count = validate_question_registers(root)
            self.assertEqual(errors, [])
            self.assertEqual(count, 2)
        finally:
            td.cleanup()

    def test_missing_falsifier_fails(self):
        td, root = self._project([{
            'id': 'Q-B-001', 'question': 'Is this decidable?', 'kind': 'epistemic',
            'status': 'open', 'discriminating_test': 'Read the record.', 'priority': 1
        }])
        try:
            errors, _, _ = validate_question_registers(root)
            self.assertTrue(any('missing falsifier' in e for e in errors))
        finally:
            td.cleanup()

    def test_unknown_gate_fails(self):
        td, root = self._project([{
            'id': 'Q-C-001', 'question': 'Does this depend on a gate?', 'kind': 'causal',
            'status': 'open', 'discriminating_test': 'Run the gate first.',
            'falsifier': 'Gate fails.', 'priority': 1, 'gate': 'Q-C-000'
        }])
        try:
            errors, _, _ = validate_question_registers(root)
            self.assertTrue(any('unknown question gate' in e for e in errors))
        finally:
            td.cleanup()

    def test_repo_registers_pass(self):
        for project in ('sri_lanka_pre_1948', 'sri_lanka_post_1948'):
            errors, _, count = validate_question_registers(ROOT / 'examples' / project)
            self.assertEqual(errors, [], project)
            self.assertGreater(count, 0, project)


if __name__ == '__main__':
    unittest.main()
