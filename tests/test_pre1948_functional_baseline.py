import json
import subprocess
import sys
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PROJECT = REPO / "examples" / "sri_lanka_pre_1948"
STATEMENT_TYPES = {
    "source_fact", "claim", "inference", "tradition", "analogy", "comparator",
    "counterfactual", "metric", "policy_intent", "policy_effect", "question", "discarded_lead",
}
CAUSAL_ROLES = {"driver", "amplifier", "constraint", "consequence", "non-cause", "context"}
ANCHOR_ROLES = {"canonical anchor", "specialist institutional anchor", "corroborating bridge", "lead"}
HILS = [
    "HIL-01_institutions-chronology", "HIL-02_geography-environment",
    "HIL-03_economy-infrastructure", "HIL-04_society-demography",
    "HIL-05_religion-culture-legitimacy", "HIL-06_security-coercion",
    "HIL-07_regional-global-system", "HIL-08_historiography-bias",
]


class Pre1948FunctionalBaselineTests(unittest.TestCase):
    def test_canonical_project_scaffold_is_materialized(self):
        for rel in [
            "project.json", "00_method", "01_arcs", "02_hil", "03_wiki", "04_graph",
            "05_sources", "06_bridges", "07_drifts", "08_questions", "09_output",
            "09_output/side_stories",
        ]:
            self.assertTrue((PROJECT / rel).exists(), rel)

    def test_claims_persist_statement_type_and_arc_identity(self):
        claims = sorted(PROJECT.glob("01_arcs/*/claims/*.json"))
        self.assertEqual(9, len(claims))
        for path in claims:
            claim = json.loads(path.read_text(encoding="utf-8"))
            for field in ("id", "type", "claim", "confidence", "zoom", "causal_role", "arc", "source_ids"):
                self.assertIn(field, claim, f"{path}: {field}")
            self.assertIn(claim["type"], STATEMENT_TYPES)
            self.assertIn(claim["causal_role"], CAUSAL_ROLES)
            self.assertEqual(path.parents[1].name, claim["arc"])

    def test_arc_metadata_and_hil_layers_are_durable(self):
        arcs = sorted(p for p in (PROJECT / "01_arcs").iterdir() if p.is_dir())
        self.assertEqual(3, len(arcs))
        for arc in arcs:
            text = (arc / "ARC.md").read_text(encoding="utf-8")
            for heading in ("## Entry rupture", "## Causal question", "## Exit rupture / bridge forward"):
                self.assertIn(heading, text, f"{arc.name}: {heading}")
        for hil in HILS:
            payload = json.loads((PROJECT / "02_hil" / hil / "baseline.json").read_text(encoding="utf-8"))
            self.assertEqual(hil, payload["hil_id"])
            self.assertIn("claim_ids", payload)
            self.assertIn("non_findings", payload)

    def test_source_anchor_roles_are_closed_vocabulary(self):
        sources = []
        for path in sorted((PROJECT / "05_sources").glob("source_register*.json")):
            sources.extend(json.loads(path.read_text(encoding="utf-8")))
        self.assertEqual(37, len(sources))
        for source in sources:
            self.assertIn(source.get("anchor_role"), ANCHOR_ROLES, source.get("id"))

    def test_questions_side_stories_and_current_workflow_are_persisted(self):
        self.assertTrue((PROJECT / "08_questions" / "baseline_questions.md").exists())
        self.assertEqual(4, len(list((PROJECT / "09_output" / "side_stories").glob("*.json"))))
        manifest = json.loads((REPO / "docs" / "RUN10_SIDE_STORIES_MANIFEST.json").read_text(encoding="utf-8"))
        self.assertEqual("reviewed", manifest["status"])
        known = {p.parent.name for p in (REPO / "skills").glob("*/SKILL.md")}
        dispatched = {item["skill"] for item in manifest["dispatched_skills"]}
        self.assertEqual(known, dispatched)
        self.assertEqual([], manifest.get("skipped_skills"))

    def test_functional_runner_passes_on_canonical_fixture(self):
        result = subprocess.run(
            [sys.executable, "scripts/qa_functional_pre1948.py"],
            cwd=REPO, text=True, capture_output=True,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        self.assertIn("PRE1948 FUNCTIONAL QA OK", result.stdout)
        self.assertIn("9 claims", result.stdout)
        self.assertIn("37 sources", result.stdout)
        self.assertIn("4 side stories", result.stdout)


if __name__ == "__main__":
    unittest.main()
