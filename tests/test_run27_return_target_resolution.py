import json,sys,tempfile,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))

from return_target_resolution import (
    apply_project_research_resolutions,
    marker_for,
    materialize_supported_marker,
    resolve_return_to,
    validate_research_resolution,
    validate_required_return_targets,
)


SOURCES=[
    {"url":"https://archive.example/a","role":"official_archive","independence_family":"Archive A"},
    {"url":"https://journal.example/b","role":"peer_reviewed","independence_family":"Journal B"},
]
DIRECT_SOURCE={
    "url":"https://archive.example/direct",
    "role":"official_archive",
    "independence_family":"Archive Direct",
    "directly_closes_proposition":True,
    "scope_fit":"direct",
}


class Run27ReturnResolutionUnitTests(unittest.TestCase):
    def test_marker_resolves_without_research(self):
        md="Un fait canonique. [claim:C-X]"
        result=resolve_return_to("C-X",md)
        self.assertEqual("resolved_marker",result.status)

    def test_missing_marker_routes_to_research_not_semantic_guess(self):
        md="C-X est écrit comme texte visible, mais sans marqueur canonique."
        result=resolve_return_to("C-X",md)
        self.assertEqual("needs_research",result.status)

    def test_one_generic_qualified_source_is_insufficient(self):
        record={"target_id":"C-X","proposition":"x","verdict":"supported","paragraph_anchor":"Phrase","sources":SOURCES[:1]}
        self.assertTrue(validate_research_resolution(record))

    def test_one_authoritative_direct_source_can_close_narrow_proposition(self):
        record={"target_id":"C-X","proposition":"x","verdict":"supported","paragraph_anchor":"Phrase","sources":[DIRECT_SOURCE]}
        self.assertEqual([],validate_research_resolution(record))

    def test_two_independent_qualified_sources_close_by_consensus(self):
        record={"target_id":"C-X","proposition":"x","verdict":"supported","paragraph_anchor":"Phrase","sources":SOURCES}
        self.assertEqual([],validate_research_resolution(record))

    def test_supported_research_materializes_hidden_marker_at_existing_paragraph(self):
        record={"target_id":"C-X","proposition":"x","verdict":"supported","paragraph_anchor":"La phrase cible","sources":SOURCES}
        md="# Arc\n\nLa phrase cible établit le mécanisme.\n\nSuite."
        out=materialize_supported_marker(md,record)
        self.assertIn("La phrase cible établit le mécanisme. [claim:C-X]",out)
        self.assertEqual("resolved_marker",resolve_return_to("C-X",out).status)

    def test_challenged_research_must_redirect_or_retire(self):
        record={"target_id":"C-X","proposition":"x","verdict":"challenged","sources":SOURCES}
        errors=validate_research_resolution(record)
        self.assertTrue(any("replacement_return_to" in x for x in errors))


class Run27ReturnResolutionProjectTests(unittest.TestCase):
    def _project(self,tmp:Path)->Path:
        project=tmp/"p";(project/"09_output/side_stories").mkdir(parents=True);(project/"08_questions").mkdir(parents=True)
        story={
            "schema_version":"1.2","class":"side_story","id":"SS-X","kind":"detour","status":"validated",
            "title":"x","purpose":"x","map_eligible":False,"lineage":{"claim_ids":["C-X"],"source_ids":[],"bridge_ids":[],"hil_ids":[],"drift_paths":[],"origin_paths":[]},
            "placement":{"section_anchor":"Départ","return_to":"C-X"},"content":{"takeaway":"Retour"},
            "render":{"label":"Petit détour","marker":"[SIDE-STORY:SS-X]","required_in_reader":True}
        }
        (project/"09_output/side_stories/SS-X.json").write_text(json.dumps(story),encoding="utf-8")
        return project

    def test_required_return_blocks_before_research_marker(self):
        with tempfile.TemporaryDirectory() as d:
            p=self._project(Path(d));errors,report=validate_required_return_targets(p,"Départ.\n\nLa phrase cible.")
            self.assertTrue(errors);self.assertEqual("needs_research",report[0]["status"])

    def test_project_research_resolution_closes_required_return(self):
        with tempfile.TemporaryDirectory() as d:
            p=self._project(Path(d));record={"target_id":"C-X","proposition":"x","verdict":"supported","paragraph_anchor":"La phrase cible","sources":SOURCES}
            (p/"08_questions/return_target_research_run27.json").write_text(json.dumps([record]),encoding="utf-8")
            md,metrics=apply_project_research_resolutions(p,"Départ.\n\nLa phrase cible établit le mécanisme.")
            self.assertEqual(["C-X"],metrics["applied"]);self.assertEqual([],metrics["errors"])
            errors,report=validate_required_return_targets(p,md)
            self.assertEqual([],errors);self.assertEqual("resolved_marker",report[0]["status"])


if __name__=="__main__":unittest.main()
