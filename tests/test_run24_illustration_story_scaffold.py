import json,sys,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"examples/sri_lanka_pre_1948"
sys.path.insert(0,str(ROOT/"scripts"))

from build_story_scaffold import build_scaffold,build_toc_from_scaffold
from illustration_contract import assert_rendered_illustrations,validate_illustrations,check_illustration_density,lint_caption_language
from resolve_reader_plan import build_plan,computed_rank
from graph_link_audit import validate_graph_links


def illustration_records():
    out=[]
    for path in sorted((PRE/"09_output/illustrations").glob("*.json")):
        data=json.loads(path.read_text(encoding="utf-8"));out.extend(data if isinstance(data,list) else [data])
    return [x for x in out if isinstance(x,dict) and x.get("id")]


class Run24IllustrationStoryScaffoldTests(unittest.TestCase):
    def test_all_illustrations_are_valid_and_non_renderable_until_approved(self):
        records_all=illustration_records();expected=len(records_all)
        errors,warnings,count=validate_illustrations(PRE)
        self.assertEqual([],errors)
        self.assertEqual(expected,count)
        expected_external=sum((x.get("source") or {}).get("binary_status")=="external_only" for x in records_all)
        self.assertEqual(expected_external,sum('binary external' in w for w in warnings))
        records=json.loads((PRE/"09_output/illustrations/ILL-KANDY-BUDDHA-LIFE-2026-08.json").read_text(encoding="utf-8"))
        self.assertTrue(all(x["status"]=="vision_validated" for x in records))
        self.assertTrue(all(x["placement"]["target_status"]=="proposed_missing" for x in records))
        self.assertTrue(all(x["source"]["sha256_status"]=="verified_at_intake" for x in records))
        self.assertTrue(all(x["render"]["marker"]==f"[ILLUSTRATION:{x['id']}]" for x in records))

    def test_reader_plan_routes_every_illustration_to_selection_review_or_retirement(self):
        records=illustration_records();expected_ids={x["id"] for x in records}
        plan=build_plan(PRE)
        routed=set(plan["selected_illustration_ids"])|set(plan["illustration_review_queue_ids"])|set(plan["retired_illustration_ids"])
        self.assertEqual(expected_ids,routed)
        self.assertFalse(set(plan["selected_illustration_ids"]) & set(plan["illustration_review_queue_ids"]))
        self.assertEqual("09_output/story_scaffold.json",plan["story_scaffold"])
        rendered=" ".join(f"[ILLUSTRATION:{iid}]" for iid in plan["selected_illustration_ids"])
        self.assertEqual(len(plan["selected_illustration_ids"]),assert_rendered_illustrations(rendered,plan["selected_illustration_ids"]))

    def test_computed_rank_prefers_evidence_then_confidence_then_human_rank(self):
        canonical={"id":"a","depiction":{"evidence_status":"canonical_text"},"vision_review":{"confidence":"medium"},"placement":{"relevance_rank":9}}
        interpretive={"id":"b","depiction":{"evidence_status":"interpretive"},"vision_review":{"confidence":"high"},"placement":{"relevance_rank":1}}
        self.assertLess(computed_rank(canonical),computed_rank(interpretive))
        high={"id":"c","depiction":{"evidence_status":"canonical_text"},"vision_review":{"confidence":"high"},"placement":{"relevance_rank":9}}
        self.assertLess(computed_rank(high),computed_rank(canonical))

    def test_density_and_caption_linter_are_bounded_and_deterministic(self):
        words=" ".join(["w"]*1000)
        text=f"[ILLUSTRATION:A] {words} [ILLUSTRATION:B]"
        self.assertEqual([],check_illustration_density(text,["A","B"],2,500))
        crowded="[ILLUSTRATION:A] "+" ".join(["w"]*20)+" [ILLUSTRATION:B]"
        self.assertTrue(check_illustration_density(crowded,["A","B"],2,500))
        self.assertTrue(lint_caption_language({"id":"X","fragment":{"caption":"Cette scène démontre que le fait est certain."}}))
        self.assertEqual([],lint_caption_language({"id":"Y","fragment":{"caption":"La tradition chronique situe cet épisode à Lanka."}}))

    def test_story_scaffold_captures_global_topology_before_arc_hydration(self):
        all_ids={x["id"] for x in illustration_records()}
        expected_ids={x["id"] for x in illustration_records() if x.get("status") in {"candidate","vision_validated"}}
        scaffold=build_scaffold(PRE)
        self.assertEqual("global topology -> arc-local retrieval packs -> cross-arc stitch -> illustration pass -> coverage reconciliation",scaffold["strategy"])
        self.assertEqual(len(all_ids),scaffold["coverage"]["illustrations"])
        arc=next(x for x in scaffold["arcs"] if x["arc"]=="A02c_anuradhapura_and_the_mahavihara")
        self.assertEqual(expected_ids,set(arc["illustration_review_queue_ids"]))
        self.assertIn("Anuradhapura",arc["title"])
        self.assertTrue(any(x["title"]=="Causal question" for x in arc["subsections"]))
        toc=build_toc_from_scaffold(scaffold)
        self.assertEqual(len(scaffold["arcs"]),len(toc))
        self.assertTrue(all("children" in item for item in toc))
        for cid in ("C-R24-BUD-BIRTH-TEXT-001","C-R24-BUD-RENUNCIATION-TEXT-001","C-R24-BUD-NALAGIRI-TEXT-001","C-R24-BUD-LANKA-VISITS-001"):
            self.assertIn(cid,arc["spine_claim_ids"])
        mermaid=(PRE/"09_output/story_scaffold.mmd").read_text(encoding="utf-8")
        self.assertIn("flowchart TD",mermaid)
        self.assertIn("ILLUSTRATED_BY",mermaid)

    def test_pending_questions_are_answered_without_overclosure(self):
        pre=json.loads((PRE/"08_questions/question_register.json").read_text(encoding="utf-8"))
        kandy=next(x for x in pre if x["id"]=="Q-KANDY-002")
        self.assertEqual("bounded",kandy["status"])
        self.assertIn("C-R24-KDY-KNOX-ROADS-001",kandy["resolution"]["claim_ids"])
        self.assertIn("Explicit Kandyan order",kandy["resolution"]["remaining_gate"])

    def test_graph_projects_textual_claims_to_typed_illustrations_in_same_arc(self):
        edges=[json.loads(line) for line in (PRE/"04_graph/edges.jsonl").read_text(encoding="utf-8").splitlines() if line]
        illustrated=[x for x in edges if x["relation"]=="ILLUSTRATED_BY"]
        self.assertEqual(5,len(illustrated))
        self.assertEqual({"ILL-KANDY-03","ILL-KANDY-04","ILL-KANDY-08","ILL-KANDY-09","ILL-KANDY-10"},{x["to"] for x in illustrated})
        errors,_,_,_=validate_graph_links(PRE)
        self.assertFalse(any("placed in" in e and "illustrates claim" in e for e in errors))


if __name__=="__main__":unittest.main()
