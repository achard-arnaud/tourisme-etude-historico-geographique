import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'scripts'
if str(SCRIPTS) not in sys.path:sys.path.insert(0,str(SCRIPTS))
from build_story_scaffold import build_scaffold,build_toc_from_scaffold
from illustration_contract import check_illustration_density,computed_rank,lint_caption_language,load_illustrations

PRE=ROOT/'examples/sri_lanka_pre_1948'

def illustration_records():
    return [item for _,item in load_illustrations(PRE)]

class Run24IllustrationStoryScaffoldTests(unittest.TestCase):
    def test_all_illustrations_are_valid_and_non_renderable_until_approved(self):
        from illustration_contract import validate_illustrations
        errors,_,_,_=validate_illustrations(PRE)
        self.assertEqual([],errors)
        for item in illustration_records():
            if item.get('status')!='reader_eligible':
                self.assertNotEqual('approved',(item.get('human_review') or {}).get('status'))

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
        all_records=illustration_records()
        all_ids={x["id"] for x in all_records}
        scaffold=build_scaffold(PRE)
        self.assertEqual("global topology -> arc-local retrieval packs -> cross-arc stitch -> illustration pass -> coverage reconciliation",scaffold["strategy"])
        self.assertEqual(len(all_ids),scaffold["coverage"]["illustrations"])
        arc_name="A02c_anuradhapura_and_the_mahavihara"
        expected_ids={
            x["id"] for x in all_records
            if x.get("status") in {"candidate","vision_validated"}
            and (x.get("placement") or {}).get("arc_ref")==arc_name
        }
        arc=next(x for x in scaffold["arcs"] if x["arc"]==arc_name)
        self.assertEqual(expected_ids,set(arc["illustration_review_queue_ids"]))
        # New illustrations assigned to A02/A03 must stay in their own arc queues rather than leaking globally.
        for item in all_records:
            if item.get("status") not in {"candidate","vision_validated"}:continue
            target=(item.get("placement") or {}).get("arc_ref")
            if not target:continue
            target_arc=next((x for x in scaffold["arcs"] if x["arc"]==target),None)
            if target_arc is not None:self.assertIn(item["id"],target_arc["illustration_review_queue_ids"])
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

if __name__=='__main__':unittest.main()
