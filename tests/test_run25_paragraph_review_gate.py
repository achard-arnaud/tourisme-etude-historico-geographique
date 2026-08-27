import json,sys,tempfile,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))

from build_heat_map import build_heat_map
from paragraph_review_gate import initialize_review_state,review_paragraph
from reciprocal_coverage_check import reciprocal_coverage_check
from run_journal import append_entry
from sarah_voice_contract import review_skeleton

SAMPLE_CLAIM={
    "id":"C-SAMPLE",
    "hil":"HIL-05_religion-culture-legitimacy",
    "canonical_points":[
        "Le roi se rendit au sommet de la colline sacrée en 1765.",
        "La tradition du temple situe une rencontre avec les responsables du sanctuaire.",
        "Le geste renforça la relation politique avec l'institution religieuse.",
    ],
}
LEGACY_CLAIM={"id":"C-LEGACY","claim":"Le roi visita le site avant un renforcement du pouvoir royal."}


def passing_style_review(text,*,signature=True):
    record=review_skeleton(text,generation_pass_id="gen-pass-1",generation_context_id="ctx-generation-1")
    record.update({
        "passed":True,
        "evaluator":"bounded_llm",
        "review_pass_id":"style-pass-1",
        "review_context_id":"ctx-style-1",
    })
    record["marker_results"]={
        "scope_precision":{"status":"pass","rationale":"La portée du paragraphe reste bornée au cas décrit."},
        "continuous_prose_not_social_format":{"status":"pass","rationale":"La prose reste continue et n'imite pas un post social."},
        "lived_opening_callback":{
            "status":"not_applicable",
            "rationale":"Ce paragraphe n'ouvre pas une séquence disposant d'une prise de terrain vécue."
        },
        "rigor_compressed_in_sentence":{
            "status":"pass" if signature else "not_applicable",
            "rationale":"La réserve sur la tradition est intégrée à la phrase." if signature else "Aucune réserve méthodologique spécifique n'est portée par cette unité."
        },
    }
    if not signature:
        record["marker_results"]["concrete_texture_before_abstraction"]={
            "status":"pass","rationale":"Le paragraphe garde un élément concret avant sa conclusion."
        }
    return record


def reviewed_context(text,claim_id="C-SAMPLE",hil="HIL-05_religion-culture-legitimacy",*,signature=True,**extra):
    context={
        "neighbor_context_loaded":True,
        "sarah_style_review":passing_style_review(text,signature=signature),
        "hil_scope_declared":True,
        "selected_hil_ids":[hil] if hil else [],
        "claim_hil_map":{claim_id:[hil]} if hil else {claim_id:[]},
    }
    context.update(extra)
    return context


class Run25ParagraphReviewGateTests(unittest.TestCase):
    def test_review_state_always_starts_false(self):
        state=initialize_review_state()
        self.assertFalse(state.checklist_reviewed)
        self.assertFalse(state.sarah_style_reviewed)
        self.assertFalse(state.hil_scope_reviewed)
        self.assertFalse(state.complete)

    def test_gate_rejects_methodological_leakage(self):
        bad="TL;DR : ce claim établit un statut canonique fort pour la relique."
        result=review_paragraph(bad,claim=SAMPLE_CLAIM,arc_context=reviewed_context(bad))
        self.assertFalse(result.passed)
        self.assertEqual("Don't",result.violations[0].category)
        self.assertFalse(result.review_state.checklist_reviewed)

    def test_gate_rejects_unglossed_foreign_term(self):
        bad="Le clearing house régional organisait les échanges du port."
        result=review_paragraph(bad,claim=SAMPLE_CLAIM,arc_context=reviewed_context(bad))
        self.assertFalse(result.passed)
        self.assertEqual("terme_technique_non_glose",result.violations[0].rule)

    def test_gate_accepts_glossed_foreign_term(self):
        text="Le clearing house, c'est-à-dire la chambre de compensation régionale, organisait les échanges du port."
        result=review_paragraph(text,claim=LEGACY_CLAIM,arc_context=reviewed_context(text,"C-LEGACY",None,signature=False))
        self.assertTrue(result.passed,result.violations)
        self.assertTrue(result.review_state.complete)

    def test_gate_rejects_incomplete_canonical_coverage(self):
        bad="Le roi fit construire un temple."
        result=review_paragraph(bad,claim=SAMPLE_CLAIM,arc_context=reviewed_context(bad))
        self.assertFalse(result.passed)
        self.assertEqual("couverture_canonique_incomplete",result.violations[0].rule)

    def test_gate_rejects_wrong_narrative_order(self):
        bad="Cela eut pour conséquence un renforcement du pouvoir royal, après que le roi eut visité le site."
        result=review_paragraph(bad,claim=LEGACY_CLAIM,arc_context=reviewed_context(bad,"C-LEGACY",None,signature=False))
        self.assertFalse(result.passed)
        self.assertEqual("ordre_fait_avant_consequence",result.violations[0].rule)

    def test_gate_accepts_conformant_paragraph_only_after_all_three_reviews(self):
        good=("Le roi se rendit au sommet de la colline sacrée en 1765 ; la tradition du temple "
              "situe là une rencontre avec les responsables du sanctuaire. Ce geste renforça ensuite "
              "la relation politique entre la cour et l'institution religieuse.")
        result=review_paragraph(good,claim=SAMPLE_CLAIM,arc_context=reviewed_context(good))
        self.assertTrue(result.passed,result.violations)
        self.assertTrue(result.review_state.complete)
        self.assertTrue(any("primary external-memory source is not imported" in w for w in result.warnings))

    def test_style_flag_stays_false_without_explicit_style_review(self):
        good=("Le roi se rendit au sommet de la colline sacrée en 1765 ; la tradition du temple "
              "situe là une rencontre avec les responsables du sanctuaire. Ce geste renforça ensuite "
              "la relation politique entre la cour et l'institution religieuse.")
        context=reviewed_context(good);context.pop("sarah_style_review")
        result=review_paragraph(good,claim=SAMPLE_CLAIM,arc_context=context)
        self.assertFalse(result.passed)
        self.assertFalse(result.review_state.sarah_style_reviewed)
        self.assertIn("sarah_style_review_required",{v.rule for v in result.violations})

    def test_style_gate_rejects_same_generation_and_review_pass(self):
        good=("Le roi se rendit au sommet de la colline sacrée en 1765 ; la tradition du temple "
              "situe là une rencontre avec les responsables du sanctuaire. Ce geste renforça ensuite "
              "la relation politique entre la cour et l'institution religieuse.")
        context=reviewed_context(good);context["sarah_style_review"]["review_pass_id"]="gen-pass-1"
        result=review_paragraph(good,claim=SAMPLE_CLAIM,arc_context=context)
        self.assertFalse(result.review_state.sarah_style_reviewed)
        self.assertTrue(any("distinct from generation pass" in v.message for v in result.violations))

    def test_style_gate_rejects_stale_review_after_rewrite(self):
        old="Le roi visite le site."
        good=("Le roi se rendit au sommet de la colline sacrée en 1765 ; la tradition du temple "
              "situe là une rencontre avec les responsables du sanctuaire. Ce geste renforça ensuite "
              "la relation politique entre la cour et l'institution religieuse.")
        context=reviewed_context(old)
        context["hil_scope_declared"]=True;context["selected_hil_ids"]=["HIL-05_religion-culture-legitimacy"]
        result=review_paragraph(good,claim=SAMPLE_CLAIM,arc_context=context)
        self.assertFalse(result.review_state.sarah_style_reviewed)
        self.assertTrue(any("paragraph hash is stale" in v.message for v in result.violations))

    def test_style_gate_rejects_marker_name_box_ticking(self):
        good=("Le roi se rendit au sommet de la colline sacrée en 1765 ; la tradition du temple "
              "situe là une rencontre avec les responsables du sanctuaire. Ce geste renforça ensuite "
              "la relation politique entre la cour et l'institution religieuse.")
        context=reviewed_context(good)
        context["sarah_style_review"]["marker_results"]={
            "scope_precision":{"status":"pass","rationale":"Portée exacte."}
        }
        result=review_paragraph(good,claim=SAMPLE_CLAIM,arc_context=context)
        self.assertFalse(result.review_state.sarah_style_reviewed)
        self.assertTrue(any("must be explicitly evaluated" in v.message for v in result.violations))

    def test_hil_flag_stays_false_without_explicit_scope_review(self):
        good=("Le roi se rendit au sommet de la colline sacrée en 1765 ; la tradition du temple "
              "situe là une rencontre avec les responsables du sanctuaire. Ce geste renforça ensuite "
              "la relation politique entre la cour et l'institution religieuse.")
        context=reviewed_context(good);context["hil_scope_declared"]=False
        result=review_paragraph(good,claim=SAMPLE_CLAIM,arc_context=context)
        self.assertFalse(result.review_state.hil_scope_reviewed)
        self.assertIn("hil_scope_review_required",{v.rule for v in result.violations})

    def test_hil_rejects_dimension_not_supported_by_claim_used_in_paragraph(self):
        good=("Le roi se rendit au sommet de la colline sacrée en 1765 ; la tradition du temple "
              "situe là une rencontre avec les responsables du sanctuaire. Ce geste renforça ensuite "
              "la relation politique entre la cour et l'institution religieuse.")
        context=reviewed_context(good);context["selected_hil_ids"].append("HIL-03_economy-infrastructure")
        result=review_paragraph(good,claim=SAMPLE_CLAIM,arc_context=context)
        self.assertFalse(result.review_state.hil_scope_reviewed)
        self.assertIn("hil_dimension_not_relevant_to_paragraph",{v.rule for v in result.violations})

    def test_hil_does_not_require_every_relevant_dimension(self):
        multi=dict(SAMPLE_CLAIM);multi["hil_ids"]=["HIL-06_security-coercion"]
        good=("Le roi se rendit au sommet de la colline sacrée en 1765 ; la tradition du temple "
              "situe là une rencontre avec les responsables du sanctuaire. Ce geste renforça ensuite "
              "la relation politique entre la cour et l'institution religieuse.")
        context=reviewed_context(good);context["claim_hil_map"]["C-SAMPLE"]=["HIL-05_religion-culture-legitimacy","HIL-06_security-coercion"]
        result=review_paragraph(good,claim=multi,arc_context=context)
        self.assertTrue(result.passed,result.violations)
        self.assertTrue(any("hil_relevant_but_not_selected" in w for w in result.warnings))

    def test_gate_prefers_callback_over_third_citation(self):
        text="Le fait revient ici comme une nouvelle preuve. [claim:C-LEGACY]"
        context=reviewed_context(text,"C-LEGACY",None,signature=False,mention_count={"C-LEGACY":2},active_callbacks=["C-LEGACY"])
        result=review_paragraph(text,claim=LEGACY_CLAIM,arc_context=context)
        self.assertFalse(result.passed)
        self.assertEqual("citation_evidentielle_au_dela_du_callback_disponible",result.violations[0].rule)

    def test_false_lead_is_socratic_and_reranked(self):
        text="Une réponse sans question."
        context=reviewed_context(text,"C-LEGACY",None,signature=False,false_lead=True,false_lead_count_in_subsection=2)
        result=review_paragraph(text,claim=LEGACY_CLAIM,arc_context=context)
        rules={v.rule for v in result.violations}
        self.assertIn("false_lead_rerank_limit",rules)
        self.assertIn("false_lead_socratic_format",rules)

    def test_review_state_does_not_leak_between_paragraphs(self):
        good=("Le roi se rendit au sommet de la colline sacrée en 1765 ; la tradition du temple "
              "situe là une rencontre avec les responsables du sanctuaire. Ce geste renforça ensuite "
              "la relation politique entre la cour et l'institution religieuse.")
        first=review_paragraph(good,claim=SAMPLE_CLAIM,arc_context=reviewed_context(good))
        second=review_paragraph(good,claim=SAMPLE_CLAIM,arc_context={})
        self.assertTrue(first.review_state.complete)
        self.assertFalse(second.review_state.complete)
        self.assertFalse(second.review_state.sarah_style_reviewed)


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

    def test_downstream_illustration_reference_counts_fragment_as_used(self):
        with tempfile.TemporaryDirectory() as tmp:
            project=Path(tmp);(project/"01_arcs/A1/claims").mkdir(parents=True);(project/"09_output/side_stories").mkdir(parents=True);(project/"09_output/illustrations").mkdir(parents=True);(project/"00_method/capture").mkdir(parents=True)
            (project/"01_arcs/A1/claims/C1.json").write_text(json.dumps({"id":"C1","claim":"x"}),encoding="utf-8")
            (project/"00_method/capture/fragments.json").write_text(json.dumps([{"id":"GF-1","class":"field_fragment","text":"used"},{"id":"GF-2","class":"field_fragment","text":"legacy unknown"}]),encoding="utf-8")
            (project/"09_output/illustrations/I1.json").write_text(json.dumps({"id":"I1","input_refs":[{"type":"field_fragment","id":"GF-1"}]}),encoding="utf-8")
            data=reciprocal_coverage_check(project,{"arcs":[{"spine_claim_ids":["C1"]}]},"Legacy paragraph.")
            self.assertEqual(["GF-1"],data["referenced_fragments"])
            self.assertEqual([],data["unused_fragments"])
            self.assertEqual(["GF-2"],data["coverage_unknown_legacy_fragments"])

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
