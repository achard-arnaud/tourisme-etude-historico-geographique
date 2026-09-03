import json
import tempfile
import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from audit_context_budget import audit, context_files, latest_manifest


class ContextBudgetRuntimeTests(unittest.TestCase):
    def test_routed_skill_companion_is_counted(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            (repo / "docs").mkdir()
            skill = repo / "skills" / "story"
            skill.mkdir(parents=True)
            (repo / "SKILL.md").write_text("root words\n", encoding="utf-8")
            (skill / "SKILL.md").write_text(
                "Must consume `CONTRACT.md` before drafting.\n", encoding="utf-8"
            )
            (skill / "CONTRACT.md").write_text(
                "companion context must be counted\n", encoding="utf-8"
            )
            manifest = {
                "dispatched_skills": [{"skill": "story", "status": "executed"}]
            }
            path = repo / "docs" / "RUN1_MANIFEST.json"
            path.write_text(json.dumps(manifest), encoding="utf-8")
            files = context_files(repo, manifest)
            self.assertIn(skill / "CONTRACT.md", files)
            report = audit(repo, path, 100)
            self.assertEqual(3, len(report["files"]))

    def test_newer_run_without_manifest_refuses_false_latest(self):
        with tempfile.TemporaryDirectory() as directory:
            repo = Path(directory)
            (repo / "docs").mkdir()
            (repo / "docs" / "RUN4_MANIFEST.json").write_text("{}", encoding="utf-8")
            (repo / "docs" / "RUN5_REVIEW.md").write_text("review", encoding="utf-8")
            with self.assertRaisesRegex(RuntimeError, "latest run is RUN5"):
                latest_manifest(repo)


if __name__ == "__main__":
    unittest.main()
