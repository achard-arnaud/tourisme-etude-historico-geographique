import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PROJECT = REPO / "examples" / "sri_lanka_pre_1948"
KINDS = {
    "detour", "dezoom", "also", "method", "false_lead", "portrait",
    "object_focus", "comparator", "callback",
}


class SideStoryContractTests(unittest.TestCase):
    def test_contract_assets_exist(self):
        for rel in [
            "skills/composing-side-stories/SKILL.md",
            "templates/side-story.json",
            "scripts/side_story_contract.py",
            "scripts/new_side_story.py",
            "docs/SOP_SIDE_STORIES.md",
        ]:
            self.assertTrue((REPO / rel).exists(), rel)

    def test_pre1948_side_stories_have_lineage_and_return_contract(self):
        paths = sorted((PROJECT / "09_output" / "side_stories").glob("*.json"))
        self.assertGreaterEqual(len(paths), 3)
        claims = {
            json.loads(path.read_text(encoding="utf-8"))["id"]
            for path in PROJECT.glob("01_arcs/*/claims/*.json")
        }
        sources = set()
        for path in (PROJECT / "05_sources").glob("source_register*.json"):
            sources.update(item["id"] for item in json.loads(path.read_text(encoding="utf-8")))
        bridges = {
            json.loads(path.read_text(encoding="utf-8"))["id"]
            for path in (PROJECT / "06_bridges").glob("*.json")
        }
        arcs = {p.name for p in (PROJECT / "01_arcs").iterdir() if p.is_dir()}
        for path in paths:
            item = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual("side_story", item["class"])
            self.assertEqual("1.0", item["schema_version"])
            self.assertIn(item["kind"], KINDS)
            self.assertIn(item["arc"], arcs)
            self.assertTrue(item["lineage"]["claim_ids"] or item["lineage"]["source_ids"] or item["lineage"]["bridge_ids"] or item["lineage"]["origin_paths"])
            self.assertTrue(set(item["lineage"]["claim_ids"]) <= claims)
            self.assertTrue(set(item["lineage"]["source_ids"]) <= sources)
            self.assertTrue(set(item["lineage"]["bridge_ids"]) <= bridges)
            self.assertTrue(item["placement"]["section_anchor"])
            self.assertTrue(item["placement"]["return_to"])
            self.assertEqual(f"[SIDE-STORY:{item['id']}]", item["render"]["marker"])
            if item["kind"] == "dezoom":
                for field in ("from", "to", "return_to", "mechanism", "local_payoff"):
                    self.assertTrue(item["zoom_excursion"].get(field), f"{item['id']}: {field}")

    def test_promoted_required_side_stories_survive_markdown_render(self):
        canonical = (PROJECT / "09_output" / "report.md").read_text(encoding="utf-8")
        reader = (PROJECT / "09_output" / "report_v3_full.md").read_text(encoding="utf-8")
        for path in (PROJECT / "09_output" / "side_stories").glob("*.json"):
            item = json.loads(path.read_text(encoding="utf-8"))
            if item["status"] == "promoted" and item["render"]["required_in_reader"]:
                marker = item["render"]["marker"]
                self.assertIn(marker, canonical, item["id"])
                self.assertIn(marker, reader, item["id"])

    def test_generic_project_qa_validates_side_stories(self):
        result = subprocess.run(
            [sys.executable, "scripts/qa_project.py", "examples/sri_lanka_pre_1948"],
            cwd=REPO,
            text=True,
            capture_output=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("side stories", result.stdout)

    def test_cli_creates_candidate_instance(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "project"
            (root / "09_output").mkdir(parents=True)
            result = subprocess.run(
                [
                    sys.executable, "scripts/new_side_story.py",
                    "--project", str(root),
                    "--id", "SS-TST-001",
                    "--kind", "detour",
                    "--arc", "A01_test",
                    "--title", "Test detour",
                    "--section-anchor", "## Test",
                    "--return-to", "A01_test",
                    "--purpose", "Exercise the creation contract",
                ],
                cwd=REPO,
                text=True,
                capture_output=True,
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            item = json.loads((root / "09_output" / "side_stories" / "SS-TST-001.json").read_text(encoding="utf-8"))
            self.assertEqual("candidate", item["status"])
            self.assertEqual("[SIDE-STORY:SS-TST-001]", item["render"]["marker"])

    def test_run10_manifest_routes_side_story_skill(self):
        manifest = json.loads((REPO / "docs" / "RUN10_SIDE_STORIES_MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual("reviewed", manifest["status"])
        known = {p.parent.name for p in (REPO / "skills").glob("*/SKILL.md")}
        dispatched = {item["skill"] for item in manifest["dispatched_skills"]}
        self.assertEqual(known, dispatched)
        self.assertIn("composing-side-stories", dispatched)


if __name__ == "__main__":
    unittest.main()
