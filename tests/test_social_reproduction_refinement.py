from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class SocialReproductionRefinementTests(unittest.TestCase):
    def read(self, rel):
        return (ROOT / rel).read_text(encoding="utf-8")

    def test_society_skill_exposes_social_reproduction_matrix(self):
        text = self.read("skills/analyzing-society-and-demography/SKILL.md")
        self.assertIn("Social-reproduction matrix", text)
        self.assertIn("Marriage and kinship caution", text)
        self.assertIn("Cleavage overlay", text)
        self.assertIn("arranged marriage", text)

    def test_bridge_skill_gates_comparative_causality(self):
        text = self.read("skills/building-causal-bridges/SKILL.md")
        self.assertIn("Comparative bridge gate", text)
        self.assertIn("confounders", text)
        self.assertIn("comparison", text.lower())

    def test_institutions_skill_tracks_access_architecture(self):
        text = self.read("skills/analyzing-institutions-and-power/SKILL.md")
        self.assertIn("Access architecture", text)
        self.assertIn("reservations", text)
        self.assertIn("distributional intent", text)

    def test_dual_corpora_publish_vnext_without_overwriting_baseline(self):
        for project in ("sri_lanka_pre_1948", "sri_lanka_post_1948"):
            output = ROOT / "examples" / project / "09_output"
            self.assertTrue((output / "report.md").exists())
            self.assertTrue((output / "report_vnext.md").exists())

    def test_post_corpus_materializes_caste_comparator_audit(self):
        root = ROOT / "examples/sri_lanka_post_1948"
        self.assertTrue((root / "05_sources/caste_social_mobility_comparative_note.md").exists())
        self.assertTrue((root / "07_drifts/caste_comparator_audit.md").exists())
        self.assertTrue((root / "01_arcs/A12_caste_social_mobility_comparative/claims/C-POST-CASTE-002.json").exists())
        self.assertTrue((root / "06_bridges/B-COMP-TN-JAFFNA-001.json").exists())


if __name__ == "__main__":
    unittest.main()
