import json,sys,tempfile,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))

from build_heat_map import build_heat_map
from paragraph_review_gate import review_paragraph
from reciprocal_coverage_check import reciprocal_coverage_check
from run_journal import append_entry

SAMPLE_CLAIM={
    "id":"C-SAMPLE",
    "canonical_points":[
        "Le roi se rendit au sommet de la colline sacrée en 1765.",
        "La tradition du temple situe une rencontre avec les responsables du sanctuaire.",
        "Le geste renforça la relation politique avec l'institution religieuse.",
    ],
}
LEGACY_CLAIM={"id":"C-LEGACY","claim":"Le roi visita le site avant un renforcement du pouvoir royal."}


class Run25ParagraphReviewGateTests(unittest.TestCase):
    def test_gate_rejects_methodological_leakage(self):
        bad="TL;DR : ce claim établit un statut canonique fort pour la relique."
        result=review_paragraph(bad,claim=SAMPLE_CLAIM)
        self.assertFalse(result.passed)
        self.assertEqual("Don't",result.violations[0].category)

    def test_gate_rejects_unglossed_foreign_term(self):
        bad="Le clearing house régional organisait les échanges du port."
        result=review_paragraph(bad,claim=SAMPLE_CLAIM)
        self.assertFalse(result.passed)
        self.assertEqual("terme_technique_non_glose",result.violations[0].rule)

    def test_gate_accepts_glossed_foreign_term(self):
        text=("Le clearing house, c'est-à-dire la chambre de compensation régionale, "
              "organisait les échanges du port.")
        result=review_paragraph(text,claim=LEGACY_CLAIM)
        self.assertTrue(result.passed)

    def test_gate_rejects_incomplete_canonical_coverage(self):
        bad="Le roi fit construire un temple."
        result=review_paragraph(bad,claim=SAMPLE_CLAIM)
        self.assertFalse(result.passed)
        self.assertEqual("fond",result.violations[0].category)
        self.assertEqual("couverture_canonique_incomplete",result.violations[0].rule)

    def test_gate_rejects_wrong_narrative_order(self):
        bad="Cela eut pour conséquence un renforcement du pouvoir royal, après que le roi eut visité le site."
        result=review_paragraph(bad,claim=LEGACY_CLAIM)
        self.assertFalse(result.passed)
        self.assertEqual("ordre_fait_avant_consequence",result.violations[0].rule)

    def test_gate_accepts_conformant_paragraph(self):
        good=("Le roi se rendit au sommet de la colline sacrée en 1765 ; la tradition du temple "
              "situe là une rencontre avec les responsables du sanctuaire. Ce geste renforça ensuite "
              "la relation politique entre la cour et l'institution religieuse.")
        result=review_paragraph(good,claim=SAMPLE_CLAIM,arc_context={"neighbor_context_loaded":True})
        self.assertTrue(result.passed,result.violations)

    def test_gate_prefers_callback_over_third_citation(self):
        text="Le fait revient ici comme une nouvelle preuve. [claim:C-LEGACY]"
        result=review_paragraph(text,claim=LEGACY_CLAIM,arc_context={"mention_count":{"C-LEGACY":2},"active_callbacks":["C-LEGACY"]})
        self.assertFalse(result.passed)
        self.assertEqual("citation_evidentielle_au_dela_du_callback_disponible",result.violations[0].rule)

    def test_false_lead_is_socratic_and_reranked(self):
        result=review_paragraph("Une réponse sans question.",claim=LEGACY_CLAIM,arc_context={"false_lead":True,"false_lead_count_in_subsection":2})
        self.assertFalse(result.passed)
        rules={v.rule for v in result.violations}
        self.assertIn("false_lead_rerank_limit",rules)
        self.assertIn("false_lead_socratic_format",rules)


class Run25ProcessContractTests(unittest.TestCase):
    def test_heat_map_classifies_without_loading_claim_prose(self):
        with tempfile.TemporaryDirectory() as tmp:
            project=Path(tmp);(project/"04_graph").mkdir()
            edges=[{"from":"C1","to":"C2"},{"from":"C1","to":"C3"},{"from":"C1","to":"C4"}]
            (project/"04_graph/edges.jsonl").write_text("\n".join(json.dumps(x) for x in edges)+"\n",encoding="utf-8")
            scaffold={"arcs":[{"arc":"A1","title":"Arc","spine_claim_ids":["C1","C2","C3","C4"],"subsections":[{"title":"Sans mapping","level":2}]}]}
            data=build_heat_map(project,scaffold)
            self.assertEqual("unmapped",data["sections"][1]["status"])
            self.assertEqual(4,len(data["sections"][0]["claim_ids"]))

    def test_legacy_without_markers_is_unknown_not_unused(self):
        with tempfile.TemporaryDirectory() as tmp:
            project=Path(tmp);(project/"01_arcs/A1/claims").mkdir(parents=True);(project/"09_output/side_stories").mkdir(parents=True)
            (project/"01_arcs/A1/claims/C1.json").write_text(json.dumps({"id":"C1","claim":"x"}),encoding="utf-8")
            data=reciprocal_coverage_check(project,{"arcs":[{"spine_claim_ids":["C1"]}]},"Legacy paragraph without hidden marker.")
            self.assertEqual([],data["unused_claims"])
            self.assertEqual(["C1"],data["coverage_unknown_legacy"])

    def test_complete_instrumentation_can_report_unused_claim(self):
        with tempfile.TemporaryDirectory() as tmp:
            project=Path(tmp);(project/"01_arcs/A1/claims").mkdir(parents=True);(project/"09_output/side_stories").mkdir(parents=True)
            (project/"01_arcs/A1/claims/C1.json").write_text(json.dumps({"id":"C1","claim":"x"}),encoding="utf-8")
            data=reciprocal_coverage_check(project,{"arcs":[{"spine_claim_ids":["C1"]}]},"No marker.",instrumentation_complete=True)
            self.assertEqual(["C1"],data["unused_claims"])
            self.assertEqual([],data["coverage_unknown_legacy"])

    def test_run_journal_appends_instead_of_rewriting(self):
        with tempfile.TemporaryDirectory() as tmp:
            repo=Path(tmp);(repo/"docs").mkdir()
            path=append_entry(repo,25,"Étape 1",["a.json"],"claim added","OK",timestamp="2026-08-27T01:00+05:30")
            first=path.read_text(encoding="utf-8")
            append_entry(repo,25,"Étape 2",["b.json"],"coverage","OK",timestamp="2026-08-27T01:05+05:30")
            second=path.read_text(encoding="utf-8")
            self.assertTrue(second.startswith(first))
            self.assertIn("Étape 2",second)


if __name__=="__main__":unittest.main()
