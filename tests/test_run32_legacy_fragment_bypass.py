import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from build_drafting_packets import build_packets
from legacy_fragment_bypass import virtual_legacy_statements


class LegacyFragmentBypassTests(unittest.TestCase):
    def test_allowlisted_unsourced_unclaimed_fragment_becomes_virtual_statement(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "00_method").mkdir()
            (project / "00_method/legacy_fragment_bypass.json").write_text(json.dumps({
                "enabled": True,
                "capture_paths": ["00_method/capture/legacy.json"],
            }), encoding="utf-8")
            fragments = {
                "GF-1": {
                    "id": "GF-1",
                    "assertion_summary": "Legacy narrative material.",
                    "candidate_arc": "A1",
                    "zoom": "Z2",
                    "_capture_path": "00_method/capture/legacy.json",
                }
            }
            result = virtual_legacy_statements(project, fragments, set(), set())
            self.assertEqual(1, len(result))
            self.assertEqual("legacy_fragment", result[0]["type"])
            self.assertEqual("LEGACY::GF-1", result[0]["id"])
            self.assertTrue(result[0]["legacy_unsourced"])
            self.assertFalse(result[0]["drafting_policy"]["may_establish_new_fact_without_source"])

    def test_new_or_sourced_fragments_do_not_use_bypass(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "00_method").mkdir()
            (project / "00_method/legacy_fragment_bypass.json").write_text(json.dumps({
                "enabled": True,
                "capture_paths": ["00_method/capture/legacy.json"],
            }), encoding="utf-8")
            fragments = {
                "GF-SOURCED": {
                    "id": "GF-SOURCED", "summary": "x", "candidate_arc": "A1",
                    "source_id": "S1", "_capture_path": "00_method/capture/legacy.json",
                },
                "GF-NEW": {
                    "id": "GF-NEW", "summary": "y", "candidate_arc": "A1",
                    "_capture_path": "00_method/capture/new.json",
                },
            }
            self.assertEqual([], virtual_legacy_statements(project, fragments, set(), set()))

    def test_claimed_legacy_fragment_is_not_duplicated(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp)
            (project / "00_method").mkdir()
            (project / "00_method/legacy_fragment_bypass.json").write_text(json.dumps({
                "enabled": True,
                "capture_paths": ["00_method/capture/legacy.json"],
            }), encoding="utf-8")
            fragments = {
                "GF-1": {
                    "id": "GF-1", "summary": "x", "candidate_arc": "A1",
                    "_capture_path": "00_method/capture/legacy.json",
                }
            }
            self.assertEqual([], virtual_legacy_statements(project, fragments, {"GF-1"}, {"C1"}))

    def test_shared_packet_builder_appends_virtual_claim_and_fragment(self):
        with tempfile.TemporaryDirectory() as tmp:
            project = Path(tmp) / "p"
            (project / "01_arcs/A1/claims").mkdir(parents=True)
            (project / "05_sources").mkdir()
            (project / "06_bridges").mkdir()
            (project / "08_questions").mkdir()
            (project / "09_output/side_stories").mkdir(parents=True)
            (project / "00_method/capture").mkdir(parents=True)
            (project / "01_arcs/A1/ARC.md").write_text("# A1\n", encoding="utf-8")
            (project / "00_method/legacy_fragment_bypass.json").write_text(json.dumps({
                "enabled": True,
                "capture_paths": ["00_method/capture/legacy.json"],
            }), encoding="utf-8")
            (project / "00_method/capture/legacy.json").write_text(json.dumps([
                {"id": "GF-LEGACY", "assertion_summary": "Rich old fragment.", "candidate_arc": "A1", "zoom": "Z1"}
            ]), encoding="utf-8")
            output = project / "out"
            manifest = build_packets(project, output)
            packet = json.loads((output / "A1.json").read_text(encoding="utf-8"))
            self.assertEqual(1, manifest["legacy_fragment_bypass"]["virtual_claim_count"])
            self.assertEqual(["LEGACY::GF-LEGACY"], [x["id"] for x in packet["claims"]])
            self.assertEqual(1, packet["counts"]["legacy_virtual_claims"])
            self.assertEqual("GF-LEGACY", packet["fragments"][0]["id"])


if __name__ == "__main__":
    unittest.main()
