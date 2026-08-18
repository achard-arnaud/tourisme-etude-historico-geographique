import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
POST = ROOT / "examples" / "sri_lanka_post_1948"
PRE = ROOT / "examples" / "sri_lanka_pre_1948"


class Run5ComparativeWikiTests(unittest.TestCase):
    def test_all_specialized_skills_are_present(self):
        skills = sorted(p.name for p in (ROOT / "skills").iterdir() if (p / "SKILL.md").exists())
        self.assertEqual(len(skills), 16)

    def test_root_skill_has_long_project_and_comparator_gates(self):
        text = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        self.assertIn("State checkpoint", text)
        self.assertIn("Comparative gate", text)
        self.assertIn("Prompt-review loop", text)

    def test_recent_method_learnings_are_encoded_in_relevant_skills(self):
        checks = {
            "analyzing-economy-and-infrastructure": "Conversion-of-advantage test",
            "analyzing-geography-and-environment": "Comparison-scale gate",
            "analyzing-institutions-and-power": "Policy instrument matrix",
            "analyzing-security-and-geopolitics": "War-development channels",
            "analyzing-society-and-demography": "Territorial versus transnational reproduction",
            "auditing-historiography-and-drifts": "Comparator audit",
            "building-causal-bridges": "Transportability test",
            "capturing-field-evidence": "Field-session checkpoint",
            "editing-historical-travel-output": "Promotion state",
            "maintaining-wiki-and-graph": "Wiki entity contract",
            "sanitizing-historical-claims": "Policy separation",
            "sourcing-historical-anchors": "Comparative sourcing",
            "storytelling-historical-travel": "Comparator storytelling",
            "structuring-chronological-arcs": "Vertical HIL threads",
            "zooming-geographic-scales": "Comparison-scale gate",
            "analyzing-religion-culture-legitimacy": "Public/private hierarchy",
        }
        for skill, marker in checks.items():
            text = (ROOT / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
            self.assertIn(marker, text, f"missing {marker} in {skill}")

    def test_run5_source_register_is_modular_and_unique(self):
        ids = set()
        for p in sorted((POST / "05_sources").glob("source_register*.json")):
            for item in json.loads(p.read_text(encoding="utf-8")):
                self.assertNotIn(item["id"], ids)
                ids.add(item["id"])
        for required in ["ADB-NORTHERN-ROADS", "CAMBRIDGE-DRAVIDIAN-CAPITAL", "BPS-INDONESIA-LANGUAGE-2024"]:
            self.assertIn(required, ids)

    def test_wiki_and_graph_materialized_for_both_corpora(self):
        for project in (PRE, POST):
            self.assertTrue((project / "03_wiki" / "README.md").exists())
            self.assertTrue((project / "04_graph" / "edges.jsonl").exists())
            self.assertGreater(len(list((project / "03_wiki").glob("*.md"))), 1)

    def test_run5_claims_and_drift_audit_exist(self):
        claims = POST / "01_arcs" / "A13_comparative_development_trajectories" / "claims"
        self.assertTrue((claims / "C-POST-WAR-TERRITORY-001.json").exists())
        self.assertTrue((claims / "C-COMP-TN-DEV-001.json").exists())
        self.assertTrue((claims / "C-COMP-ID-LANG-002.json").exists())
        self.assertTrue((POST / "07_drifts" / "run5_comparator_development_audit.md").exists())


if __name__ == "__main__":
    unittest.main()
