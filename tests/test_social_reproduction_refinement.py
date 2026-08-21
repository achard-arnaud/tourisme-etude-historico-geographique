from pathlib import Path
import unittest
ROOT=Path(__file__).resolve().parents[1]
class SocialReproductionRefinementTests(unittest.TestCase):
    def read(self,rel):return (ROOT/rel).read_text(encoding='utf-8')
    def test_society_skill_preserves_behavioral_social_reproduction_rules(self):
        text=self.read('skills/analyzing-society-and-demography/SKILL.md').lower()
        for concept in ['social-reproduction matrix','arranged marriage','forced marriage','endogamy','diaspora','side-story handoff']:self.assertIn(concept,text)
    def test_bridge_skill_gates_comparative_causality(self):
        text=self.read('skills/building-causal-bridges/SKILL.md').lower();self.assertIn('comparative bridge gate',text);self.assertIn('confounders',text);self.assertIn('institutional package',text)
    def test_institutions_skill_tracks_access_architecture(self):
        text=self.read('skills/analyzing-institutions-and-power/SKILL.md');self.assertIn('Access architecture',text);self.assertIn('reservations',text);self.assertIn('distributional intent',text)
    def test_dual_corpora_publish_vnext_without_overwriting_baseline(self):
        for project in ('sri_lanka_pre_1948','sri_lanka_post_1948'):
            output=ROOT/'examples'/project/'09_output';self.assertTrue((output/'report.md').exists());self.assertTrue((output/'report_vnext.md').exists());self.assertTrue((ROOT/'examples'/project/'00_method'/'output_state.json').exists())
    def test_post_corpus_materializes_caste_comparator_audit(self):
        root=ROOT/'examples/sri_lanka_post_1948';self.assertTrue((root/'05_sources/caste_social_mobility_comparative_note.md').exists());self.assertTrue((root/'07_drifts/caste_comparator_audit.md').exists());self.assertTrue((root/'01_arcs/A12_caste_social_mobility_comparative/claims/C-POST-CASTE-002.json').exists());self.assertTrue((root/'06_bridges/B-COMP-TN-JAFFNA-001.json').exists())
if __name__=='__main__':unittest.main()
