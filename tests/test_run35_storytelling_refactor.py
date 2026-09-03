import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_drafting_packets import build_packets
from reader_retention import enforce_advanced_retention


class Run35StorytellingRefactorTests(unittest.TestCase):
    def fixture(self, tmp: str) -> Path:
        p = Path(tmp) / "project"
        (p / "00_method").mkdir(parents=True)
        (p / "00_method/capture").mkdir(parents=True)
        (p / "01_arcs/A1/claims").mkdir(parents=True)
        (p / "05_sources").mkdir()
        (p / "06_bridges").mkdir()
        (p / "08_questions").mkdir()
        (p / "09_output/side_stories").mkdir(parents=True)
        (p / "09_output").mkdir(exist_ok=True)
        (p / "01_arcs/A1/ARC.md").write_text("# A1\n", encoding="utf-8")
        (p / "01_arcs/A1/claims/C1.json").write_text(json.dumps({
            "id": "C1", "claim": "Control skeleton", "source_ids": ["S1"],
            "input_refs": [{"id": "GF-1"}]
        }), encoding="utf-8")
        (p / "05_sources/source_register.json").write_text(json.dumps([
            {"id": "S1", "title": "Source one"}
        ]), encoding="utf-8")
        (p / "00_method/capture/fragments.json").write_text(json.dumps({
            "fragments": [{"id": "GF-1", "candidate_arc": "A1", "summary": "Rich narrative material."}]
        }), encoding="utf-8")
        (p / "09_output/reader_scaffold.json").write_text(json.dumps({
            "class": "reader_scaffold", "nodes": [{"type": "heading", "title": "A1"}]
        }), encoding="utf-8")
        (p / "09_output/custom_reader.md").write_text(
            "# Book\n\nAnchor paragraph for the story.\n\nNext paragraph.\n", encoding="utf-8"
        )
        (p / "09_output/custom_baseline.md").write_text(
            "one two three four five six seven eight nine ten", encoding="utf-8"
        )
        (p / "00_method/output_state.json").write_text(json.dumps({
            "schema_version": 1,
            "baseline_markdown": "09_output/custom_baseline.md",
            "canonical_markdown": "09_output/custom_reader.md",
            "reader_markdown": "09_output/custom_reader.md",
            "composition": {"side_story_coverage_required": False}
        }), encoding="utf-8")
        return p

    def test_iterative_bootstrap_uses_output_state_canonical_reader(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = self.fixture(tmp)
            out = Path(tmp) / "packets"
            build_packets(p, out, mode="iterative")
            packet = json.loads((out / "A1.json").read_text(encoding="utf-8"))
            self.assertTrue(packet["bootstrap"]["reader_prose_loaded"])
            self.assertTrue(packet["bootstrap"]["canonical_manuscript_path"].endswith("09_output/custom_reader.md"))
            self.assertIn("Anchor paragraph for the story.", packet["bootstrap"]["canonical_manuscript"])

    def test_from_scratch_never_loads_output_state_reader(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = self.fixture(tmp)
            out = Path(tmp) / "packets"
            build_packets(p, out, mode="from_scratch")
            packet = json.loads((out / "A1.json").read_text(encoding="utf-8"))
            self.assertFalse(packet["bootstrap"]["reader_prose_loaded"])
            self.assertEqual("", packet["bootstrap"]["canonical_manuscript"])

    def test_advanced_retention_uses_output_state_baseline(self):
        with tempfile.TemporaryDirectory() as tmp:
            p = self.fixture(tmp)
            with self.assertRaises(RuntimeError):
                enforce_advanced_retention(p, "one two three")

    def test_paragraph_review_plan_maps_story_to_claim_fragment_source(self):
        from build_paragraph_review_plan import build_review_plan
        with tempfile.TemporaryDirectory() as tmp:
            p = self.fixture(tmp)
            story = {
                "schema_version": "1.2", "class": "side_story", "id": "SS-1",
                "kind": "detour", "status": "promoted", "title": "Story",
                "purpose": "Explain the mechanism.", "map_eligible": False,
                "arc": "A1", "lineage_quality": "sourced",
                "lineage": {"claim_ids": ["C1"], "source_ids": ["S1"], "bridge_ids": [], "hil_ids": [], "drift_paths": [], "origin_paths": []},
                "placement": {"section_anchor": "Anchor paragraph for the story.", "return_to": "C1"},
                "content": {"takeaway": "A distinct payoff.", "body_markdown": " ".join(["history"] * 100)},
                "render": {"label": "Petit détour", "marker": "[SIDE-STORY:SS-1]", "required_in_reader": True}
            }
            (p / "09_output/side_stories/SS-1.json").write_text(json.dumps(story), encoding="utf-8")
            packets = Path(tmp) / "packets"
            build_packets(p, packets, mode="iterative")
            plan = build_review_plan(p, packets)
            self.assertEqual(1, plan["counts"]["required_promoted_side_stories"])
            self.assertEqual(1, plan["counts"]["resolved_required_side_stories"])
            item = plan["work_items"][0]
            self.assertEqual(["SS-1"], item["side_story_ids"])
            self.assertEqual(["C1"], item["claim_control_ids"])
            self.assertEqual(["GF-1"], item["narrative_fragment_ids"])
            self.assertEqual(["S1"], item["source_ids"])
            self.assertEqual("resolved", item["disposition"])


if __name__ == "__main__":
    unittest.main()
