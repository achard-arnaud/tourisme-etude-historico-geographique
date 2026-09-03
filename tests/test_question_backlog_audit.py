import json
import tempfile
import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_question_backlog import audit_project, build_report, inferred_opened_run


class QuestionBacklogAuditTests(unittest.TestCase):
    def test_run_is_inferred_and_age_is_bounded(self):
        self.assertEqual(44, inferred_opened_run({"id": "Q-R44-TEST-001"}))
        with tempfile.TemporaryDirectory() as directory:
            project = Path(directory) / "project"
            questions = project / "08_questions"
            questions.mkdir(parents=True)
            items = [
                {"id": "Q-R44-OLD", "status": "open", "priority": 1},
                {"id": "Q-UNSCHEDULED", "status": "bounded", "priority": 2},
                {"id": "Q-NEW", "status": "open", "priority": 1, "opened_run": 54, "review_after_run": 58},
            ]
            (questions / "question_register.json").write_text(json.dumps(items), encoding="utf-8")
            rows = audit_project(project, current_run=56, max_age=5)
            states = {row["id"]: row["state"] for row in rows}
            self.assertEqual("stale", states["Q-R44-OLD"])
            self.assertEqual("unscheduled", states["Q-UNSCHEDULED"])
            self.assertEqual("scheduled", states["Q-NEW"])
            report = build_report([project], 56, 5)
            self.assertEqual({"stale": 1, "unscheduled": 1, "scheduled": 1}, report["counts"])


if __name__ == "__main__":
    unittest.main()
