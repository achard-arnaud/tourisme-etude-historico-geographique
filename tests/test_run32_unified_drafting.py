import json,sys,tempfile,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from build_drafting_packets import build_packets
from materialize_side_stories import materialize_text

class UnifiedDraftingTests(unittest.TestCase):
    def fixture(self,tmp):
        p=Path(tmp)/"project"
        (p/"01_arcs/A1/claims").mkdir(parents=True)
        (p/"00_method/capture").mkdir(parents=True)
        (p/"05_sources").mkdir();(p/"06_bridges").mkdir();(p/"08_questions").mkdir()
        (p/"09_output/side_stories").mkdir(parents=True)
        (p/"01_arcs/A1/ARC.md").write_text("# A1\n",encoding="utf-8")
        (p/"01_arcs/A1/claims/C1.json").write_text(json.dumps({"id":"C1","claim":"Skeleton only","source_ids":["S1"]}),encoding="utf-8")
        (p/"05_sources/source_register.json").write_text(json.dumps([{"id":"S1","title":"Source"}]),encoding="utf-8")
        (p/"00_method/capture/fragments.json").write_text(json.dumps({"fragments":[
            {"id":"GF-LINKLESS","candidate_arc":"A1","summary":"Rich material that has not yet been linked to a claim."}
        ]}),encoding="utf-8")
        (p/"09_output/reader_scaffold.json").write_text(json.dumps({"class":"reader_scaffold","nodes":[{"type":"heading","title":"A1 reader"}]}),encoding="utf-8")
        return p

    def test_candidate_arc_fragment_survives_without_claim_link(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=self.fixture(tmp);out=Path(tmp)/"out"
            build_packets(p,out,mode="from_scratch")
            packet=json.loads((out/"A1.json").read_text(encoding="utf-8"))
            self.assertEqual(["GF-LINKLESS"],[x["id"] for x in packet["fragments"]])
            self.assertEqual(1,packet["counts"]["unlinked_arc_fragments"])
            self.assertEqual("primary_narrative_material",packet["drafting_contract"]["fragment_role"])

    def test_modes_share_evidence_payload_and_only_bootstrap_differs(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=self.fixture(tmp)
            (p/"09_output/report_v3_full.md").write_text("# Existing reader\n",encoding="utf-8")
            a=Path(tmp)/"scratch";b=Path(tmp)/"iter"
            build_packets(p,a,mode="from_scratch")
            build_packets(p,b,mode="iterative")
            pa=json.loads((a/"A1.json").read_text());pb=json.loads((b/"A1.json").read_text())
            self.assertEqual(pa["evidence"],pb["evidence"])
            self.assertFalse(pa["bootstrap"]["reader_prose_loaded"])
            self.assertTrue(pb["bootstrap"]["reader_prose_loaded"])
            self.assertEqual("sources_only_no_claim_ids",pb["drafting_contract"]["frontstage_citation_policy"])

    def test_side_story_is_inserted_after_full_anchor_boundary(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/"09_output/side_stories").mkdir(parents=True)
            body=" ".join(["mot"]*95)
            story={"schema_version":"1.2","class":"side_story","id":"SS-X","kind":"detour","status":"promoted",
                   "title":"Détour","purpose":"p","map_eligible":False,
                   "lineage":{"claim_ids":["C1"],"source_ids":["S1"],"bridge_ids":[],"hil_ids":[],"drift_paths":[],"origin_paths":[]},
                   "placement":{"section_anchor":"Paragraphe ancre complet.","return_to":"C1"},
                   "content":{"takeaway":"Un payoff distinct.","body_markdown":body},
                   "render":{"label":"Petit détour","marker":"[SIDE-STORY:SS-X]","required_in_reader":False}}
            (p/"09_output/side_stories/SS-X.json").write_text(json.dumps(story),encoding="utf-8")
            original="# T\n\nParagraphe ancre complet.\n\nSuite du récit.\n"
            rendered,count=materialize_text(p,original)
            self.assertEqual(1,count)
            self.assertLess(rendered.index("Paragraphe ancre complet."),rendered.index("SIDE-STORY:SS-X"))
            self.assertLess(rendered.index("SIDE-STORY:SS-X"),rendered.index("Suite du récit."))

if __name__=="__main__":unittest.main()
