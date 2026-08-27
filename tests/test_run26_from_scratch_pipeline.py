import json,sys,tempfile,unittest
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))

from build_from_scratch_packets import ReadLedger,build_packets
from from_scratch_review_contract import initialize_ledger,validate_review_ledger
from materialize_side_stories import materialize_text,side_story_begin_marker,side_story_end_marker
from render_from_scratch_reader import add_side_story_block
from side_story_presentation import SIDE_STORY_PRESENTATION


class Run26PacketTests(unittest.TestCase):
    def test_read_ledger_blocks_reader_prose_and_docx(self):
        with tempfile.TemporaryDirectory() as tmp:
            project=Path(tmp);(project/"09_output/archive").mkdir(parents=True)
            report=project/"09_output/report_v3_full.md";report.write_text("old prose",encoding="utf-8")
            docx=project/"old.docx";docx.write_bytes(b"x")
            ledger=ReadLedger(project)
            with self.assertRaisesRegex(RuntimeError,"contamination blocked"):ledger.text(report)
            with self.assertRaisesRegex(RuntimeError,"contamination blocked"):ledger.text(docx)

    def test_packet_builder_uses_structured_evidence_and_initial_false_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            project=Path(tmp)/"p";(project/"01_arcs/A1/claims").mkdir(parents=True);(project/"05_sources").mkdir();(project/"06_bridges").mkdir();(project/"08_questions").mkdir();(project/"09_output/side_stories").mkdir(parents=True);(project/"00_method/capture").mkdir(parents=True)
            (project/"01_arcs/A1/ARC.md").write_text("# A1\n\nArc evidence note.",encoding="utf-8")
            claim={"id":"C1","claim":"Fact","hil":"HIL-02_geography-environment","source_ids":["S1"]}
            (project/"01_arcs/A1/claims/C1.json").write_text(json.dumps(claim),encoding="utf-8")
            (project/"05_sources/source_register.json").write_text(json.dumps([{"id":"S1","title":"Source"}]),encoding="utf-8")
            output=project/"packet_out";manifest=build_packets(project,output);packet=json.loads((output/"A1.json").read_text(encoding="utf-8"))
            self.assertFalse(manifest["contamination_check"]["reader_prose_loaded"])
            self.assertEqual(["C1"],[x["id"] for x in packet["claims"]])
            self.assertIn("HIL-02_geography-environment",packet["relevant_hil"])
            self.assertEqual({"checklist_reviewed":False,"sarah_style_reviewed":False,"hil_scope_reviewed":False},packet["drafting_contract"]["paragraph_review_state_initial"])
            self.assertTrue(all("09_output/report" not in p for p in manifest["read_ledger"]))


class Run26ReviewLedgerTests(unittest.TestCase):
    def test_ledger_initializes_all_review_flags_false(self):
        records=initialize_ledger("# T\n\nUn paragraphe. [claim:C1]\n")
        self.assertEqual(1,len(records));self.assertEqual({"checklist_reviewed":False,"sarah_style_reviewed":False,"hil_scope_reviewed":False},records[0]["initial_state"]);self.assertEqual(records[0]["initial_state"],records[0]["review_state"])

    def test_final_ledger_rejects_irrelevant_hil(self):
        with tempfile.TemporaryDirectory() as tmp:
            project=Path(tmp);(project/"01_arcs/A1/claims").mkdir(parents=True)
            (project/"01_arcs/A1/claims/C1.json").write_text(json.dumps({"id":"C1","claim":"x","hil":"HIL-06_security-coercion"}),encoding="utf-8")
            markdown="# T\n\nUn paragraphe. [claim:C1]\n";record=initialize_ledger(markdown)[0]
            record["review_state"]={"checklist_reviewed":True,"sarah_style_reviewed":True,"hil_scope_reviewed":True};record["selected_hil_ids"]=["HIL-03_economy-infrastructure"];record["sarah_style_review"]={"passed":True,"evaluator":"bounded_llm","markers":["scope_precision","concrete_texture"],"notes":""}
            errors=validate_review_ledger(project,markdown,[record]);self.assertTrue(any("irrelevant HIL" in e for e in errors))

    def test_complete_review_ledger_accepts_relevant_subset(self):
        with tempfile.TemporaryDirectory() as tmp:
            project=Path(tmp);(project/"01_arcs/A1/claims").mkdir(parents=True)
            (project/"01_arcs/A1/claims/C1.json").write_text(json.dumps({"id":"C1","claim":"x","hil_ids":["HIL-06_security-coercion","HIL-02_geography-environment"]}),encoding="utf-8")
            markdown="# T\n\nUn paragraphe. [claim:C1]\n";record=initialize_ledger(markdown)[0]
            record["review_state"]={"checklist_reviewed":True,"sarah_style_reviewed":True,"hil_scope_reviewed":True};record["selected_hil_ids"]=["HIL-06_security-coercion"];record["sarah_style_review"]={"passed":True,"evaluator":"bounded_llm","markers":["scope_precision","concrete_texture"],"notes":""}
            self.assertEqual([],validate_review_ledger(project,markdown,[record]))


class Run26SideStoryBoundaryTests(unittest.TestCase):
    def test_materializer_emits_balanced_begin_end_fences(self):
        with tempfile.TemporaryDirectory() as tmp:
            project=Path(tmp);(project/"09_output/side_stories").mkdir(parents=True)
            item={"schema_version":"1.1","class":"side_story","id":"SS-X","kind":"detour","status":"promoted","title":"Example","purpose":"p","reason_off_trunk":"r","payoff":"p","map_eligible":False,"reader_policy":{"min_age":10},"lineage":{"claim_ids":[],"source_ids":[],"bridge_ids":[],"hil_ids":[],"drift_paths":[],"origin_paths":[]},"placement":{"section_anchor":"Anchor","return_to":"anchor:Body"},"zoom_excursion":None,"content":{"takeaway":"A distinct useful conclusion.","body_markdown":"Inserted body"},"render":{"label":"Petit détour","marker":"[SIDE-STORY:SS-X]","required_in_reader":False}}
            (project/"09_output/side_stories/SS-X.json").write_text(json.dumps(item),encoding="utf-8")
            text,count=materialize_text(project,"# A\n\nAnchor\n\nBody\n");self.assertEqual(1,count);self.assertIn(side_story_begin_marker(item),text);self.assertIn(side_story_end_marker(item),text);self.assertLess(text.index("BEGIN"),text.index("Inserted body"));self.assertLess(text.index("Inserted body"),text.index(" END"))

    def test_from_scratch_side_story_is_one_filled_closed_cell(self):
        doc=Document();add_side_story_block(doc,"false_lead",["**Fausse piste — Exemple**","La réponse reste dans le même encadré."])
        self.assertEqual(1,len(doc.tables));cell=doc.tables[0].cell(0,0);tc_pr=cell._tc.get_or_add_tcPr();shd=tc_pr.find(qn("w:shd"));self.assertEqual(SIDE_STORY_PRESENTATION["false_lead"]["fill"],shd.get(qn("w:fill")))
        borders=tc_pr.find(qn("w:tcBorders"));self.assertIsNotNone(borders)
        for edge in ("top","bottom","left","right"):self.assertIsNotNone(borders.find(qn(f"w:{edge}")))
        self.assertIn("①",cell.text);self.assertIn("La réponse",cell.text)


if __name__=="__main__":unittest.main()
