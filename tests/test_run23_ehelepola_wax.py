import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRE = ROOT / "examples" / "sri_lanka_pre_1948"
ARC = PRE / "01_arcs" / "A07b_kandyan_kingdom_and_defensive_interior"


class Run23EhelepolaWaxTests(unittest.TestCase):
    def load(self, path):
        return json.loads(path.read_text(encoding="utf-8"))

    def test_museum_is_navigation_not_historical_closure(self):
        sources = self.load(PRE / "05_sources" / "source_register_run23_ehelepola_wax.json")
        museum = next(x for x in sources if x["id"] == "EHELEPOLA-WAX-MUSEUM-2025")
        self.assertEqual("T3", museum["tier"])
        self.assertEqual("lead", museum["anchor_role"])
        self.assertEqual(["C-R23-KDY-MUSEUM-MEMORY-001"], museum["claims_supported"])
        self.assertIn("not independent proof", museum["limitations"])

    def test_selected_claims_keep_statement_types_and_limits(self):
        expected = {
            "C-R23-KDY-MUSEUM-MEMORY-001": "source_fact",
            "C-R23-KDY-DONA-CATHERINA-001": "source_fact",
            "C-R23-KDY-SIAM-ORDINATION-001": "source_fact",
            "C-R23-KDY-COSMOPOLITAN-001": "inference",
            "C-R23-KDY-DOYLY-KNOWLEDGE-001": "inference",
        }
        for claim_id, statement_type in expected.items():
            claim = self.load(ARC / "claims" / f"{claim_id}.json")
            self.assertEqual(statement_type, claim["type"])
            self.assertTrue(claim["bounded_by"])

    def test_doyly_bridge_is_bounded_and_projected(self):
        bridge = self.load(PRE / "06_bridges" / "B-R23-KDY-DOYLY-1815-001.json")
        self.assertEqual("B", bridge["result"])
        self.assertEqual("C-R23-KDY-DOYLY-KNOWLEDGE-001", bridge["from_claim"])
        self.assertEqual("C-R17-KDY-1815-001", bridge["to_claim"])
        edges = [json.loads(line) for line in (PRE / "04_graph" / "edges.jsonl").read_text(encoding="utf-8").splitlines() if line]
        edge = next(x for x in edges if "B-R23-KDY-DOYLY-1815-001" in x.get("bridge_ids", []))
        self.assertEqual(bridge["from_claim"], edge["from"])
        self.assertEqual(bridge["to_claim"], edge["to"])

    def test_only_three_narrative_candidates_are_created(self):
        paths = sorted((PRE / "09_output" / "side_stories").glob("SS-R23-KDY-*.json"))
        self.assertEqual(3, len(paths))
        stories = [self.load(path) for path in paths]
        self.assertTrue(all(x["status"] == "candidate" for x in stories))
        self.assertEqual({"portrait", "dezoom"}, {x["kind"] for x in stories})

    def test_intake_is_archived_and_research_closed(self):
        rows = self.load(ROOT / "docs" / "intakes" / "intake_registry.json")
        row = next(x for x in rows if x["id"] == "I-R23-EHELEPOLA-WAX")
        self.assertEqual("archived", row["preservation_status"])
        self.assertTrue((ROOT / row["repo_path"]).exists())
        backlog = self.load(ROOT / "docs" / "intakes" / "intake_research_backlog.json")
        work = next(x for x in backlog if x["id"] == "IRB-R23-EHELEPOLA-WAX")
        self.assertEqual("resolved", work["status"])


if __name__ == "__main__":
    unittest.main()

