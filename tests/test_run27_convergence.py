import json,sys,tempfile,unittest
from dataclasses import dataclass
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))

from paragraph_repair_loop import MAX_ATTEMPTS,repair_paragraph,validate_disposition
from run27_coverage_contract import build_claim_manifest,coverage_completeness
from audit_canonical_points import audit as audit_canonical_points


@dataclass
class FakeResult:
    passed:bool
    violations:list


class Run27RepairLoopTests(unittest.TestCase):
    def test_failed_gate_rewrites_then_includes(self):
        calls=[]
        def draft(attempt,violations):
            calls.append((attempt,violations));return "draft one" if attempt==1 else "draft repaired"
        def review(text):
            return FakeResult(text=="draft repaired",[] if text=="draft repaired" else [{"category":"fond","rule":"x","message":"repair this"}])
        row=repair_paragraph("C-X",draft,review)
        self.assertEqual("included",row.status);self.assertEqual(2,row.attempts)
        self.assertEqual("repair this",calls[1][1][0]["message"])

    def test_three_failures_become_explicit_not_selected(self):
        row=repair_paragraph("C-X",lambda attempt,violations:f"draft {attempt}",lambda text:FakeResult(False,[{"message":"still bad"}]))
        self.assertEqual("not_selected_for_reader",row.status);self.assertEqual(MAX_ATTEMPTS,row.attempts)
        self.assertIn("still bad",row.rationale);self.assertEqual([],validate_disposition(row.to_dict()))

    def test_side_story_routing_is_explicit(self):
        row=repair_paragraph("C-X",lambda a,v:"ok",lambda t:FakeResult(True,[]),route_to_side_story=lambda t:"SS-X")
        self.assertEqual("included_as_side_story",row.status);self.assertEqual("SS-X",row.side_story_id)


class Run27CoverageTests(unittest.TestCase):
    def _project(self,tmp:Path)->Path:
        project=tmp/"p";(project/"01_arcs/A/claims").mkdir(parents=True);(project/"00_method/capture").mkdir(parents=True)
        (project/"01_arcs/A/claims/C1.json").write_text(json.dumps({"id":"C1","claim":"one"}),encoding="utf-8")
        (project/"01_arcs/A/claims/C2.json").write_text(json.dumps({"id":"C2","claim":"two"}),encoding="utf-8")
        (project/"00_method/capture/run_field_fragments.json").write_text(json.dumps([{"id":"F1","promotes_to":"C1"}]),encoding="utf-8")
        return project

    def test_manifest_distinguishes_depth(self):
        with tempfile.TemporaryDirectory() as d:
            p=self._project(Path(d));md="Un paragraphe assez long pour le premier claim et son mécanisme. [claim:C1]\n\nCourt. [claim:C2]"
            m=build_claim_manifest(p,md)
            self.assertGreater(m["C1"]["gross_word_count"],m["C2"]["gross_word_count"])
            self.assertEqual(1,m["C1"]["paragraph_count"])

    def test_unaccounted_blocks_run(self):
        with tempfile.TemporaryDirectory() as d:
            p=self._project(Path(d));md="Présent. [claim:C1]";report=coverage_completeness(p,md,{"dispositions":{}})
            self.assertIn("claim:C2",report["unaccounted"]);self.assertTrue(report["errors"])

    def test_promoted_fragment_inherits_claim_disposition(self):
        with tempfile.TemporaryDirectory() as d:
            p=self._project(Path(d));md="Un. [claim:C1]\n\nDeux. [claim:C2]";report=coverage_completeness(p,md,{"dispositions":{}})
            self.assertEqual([],report["unaccounted"]);self.assertEqual("included",report["dispositions"]["fragment:F1"]["status"])


class Run27CorpusClosureTests(unittest.TestCase):
    def test_run16_pre_fragment_backlog_has_no_empty_promotes_to(self):
        path=ROOT/"examples/sri_lanka_pre_1948/00_method/capture/run16_field_fragments.json";items=json.loads(path.read_text(encoding="utf-8"))
        self.assertTrue(items);self.assertFalse([x["id"] for x in items if not str(x.get("promotes_to") or "").strip()])

    def test_iconography_method_story_keeps_panel_identification_bounded(self):
        path=ROOT/"examples/sri_lanka_pre_1948/09_output/side_stories/SS-R27-BUDDHIST-ICONOGRAPHY-METHOD-001.json";item=json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual("method",item["kind"]);self.assertIn("Kusa Jātaka",item["content"]["body_markdown"]);self.assertIn("question ouverte",item["content"]["body_markdown"])

    def test_canonical_points_audit_declares_warning_only_mode(self):
        report=audit_canonical_points();self.assertEqual("warning_only_until_populated",report["mode"]);self.assertGreater(report["claims_total"],0)


if __name__=="__main__":unittest.main()
