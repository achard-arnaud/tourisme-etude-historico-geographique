import json,sys,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/"examples/sri_lanka_pre_1948"
sys.path.insert(0,str(ROOT/"scripts"))

from build_story_scaffold import build_scaffold
from illustration_contract import assert_rendered_illustrations,validate_illustrations
from resolve_reader_plan import build_plan


class Run24IllustrationStoryScaffoldTests(unittest.TestCase):
    def test_all_illustrations_are_valid_and_non_renderable_until_approved(self):
        errors,warnings,count=validate_illustrations(PRE)
        self.assertEqual([],errors)
        self.assertEqual(10,count)
        self.assertEqual(10,len(warnings))
        records=json.loads((PRE/"09_output/illustrations/ILL-KANDY-BUDDHA-LIFE-2026-08.json").read_text(encoding="utf-8"))
        self.assertTrue(all(x["status"]=="vision_validated" for x in records))
        self.assertTrue(all(x["placement"]["target_status"]=="proposed_missing" for x in records))
        self.assertTrue(all(x["source"]["sha256_status"]=="verified_at_intake" for x in records))
        self.assertTrue(all(x["render"]["marker"]==f"[ILLUSTRATION:{x['id']}]" for x in records))

    def test_reader_plan_has_complete_review_queue_and_no_false_embedding(self):
        plan=build_plan(PRE)
        self.assertEqual([],plan["selected_illustration_ids"])
        self.assertEqual(10,len(plan["illustration_review_queue_ids"]))
        self.assertEqual("09_output/story_scaffold.json",plan["story_scaffold"])
        self.assertEqual(set(f"ILL-KANDY-{i:02d}" for i in range(1,11)),set(plan["illustration_review_queue_ids"]))
        self.assertEqual(0,assert_rendered_illustrations("reader without selected images",plan["selected_illustration_ids"]))

    def test_story_scaffold_captures_global_topology_before_arc_hydration(self):
        scaffold=build_scaffold(PRE)
        self.assertEqual("global topology -> arc-local retrieval packs -> cross-arc stitch -> illustration pass -> coverage reconciliation",scaffold["strategy"])
        self.assertEqual(10,scaffold["coverage"]["illustrations"])
        arc=next(x for x in scaffold["arcs"] if x["arc"]=="A02c_anuradhapura_and_the_mahavihara")
        self.assertEqual(10,len(arc["illustration_review_queue_ids"]))
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

    def test_graph_projects_textual_claims_to_typed_illustrations(self):
        edges=[json.loads(line) for line in (PRE/"04_graph/edges.jsonl").read_text(encoding="utf-8").splitlines() if line]
        illustrated=[x for x in edges if x["relation"]=="ILLUSTRATED_BY"]
        self.assertEqual(5,len(illustrated))
        self.assertEqual({"ILL-KANDY-03","ILL-KANDY-04","ILL-KANDY-08","ILL-KANDY-09","ILL-KANDY-10"},{x["to"] for x in illustrated})


if __name__=="__main__":unittest.main()
