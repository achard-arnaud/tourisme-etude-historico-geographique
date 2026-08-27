import json,sys,tempfile,unittest
from dataclasses import dataclass
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
from paragraph_repair_loop import MAX_ATTEMPTS,repair_paragraph,validate_disposition
from return_target_resolution import marker_for,resolve_return_to,validate_research_resolution,materialize_supported_marker
from evidence_coverage_contract import build_claim_manifest,coverage_completeness
from audit_canonical_points import audit as audit_canonical_points

@dataclass
class FakeResult:
    passed:bool
    violations:list

SOURCES=[
    {'url':'https://archive.example/a','role':'official_archive','independence_family':'Archive A'},
    {'url':'https://journal.example/b','role':'peer_reviewed','independence_family':'Journal B'},
]

class Run27SalvageContracts(unittest.TestCase):
    def test_repair_loop_never_silently_drops(self):
        row=repair_paragraph('C-X',lambda a,v:f'draft {a}',lambda text:FakeResult(False,[{'message':'still bad'}]))
        self.assertEqual('not_selected_for_reader',row.status)
        self.assertEqual(MAX_ATTEMPTS,row.attempts)
        self.assertEqual([],validate_disposition(row.to_dict()))

    def test_return_target_requires_marker_not_visible_id(self):
        self.assertEqual('needs_research',resolve_return_to('C-X','Visible C-X but no marker.').status)
        self.assertEqual('resolved_marker',resolve_return_to('C-X','Fact. [claim:C-X]').status)

    def test_supported_research_materializes_marker(self):
        record={'target_id':'C-X','proposition':'x','verdict':'supported','paragraph_anchor':'Phrase cible','sources':SOURCES}
        self.assertEqual([],validate_research_resolution(record))
        out=materialize_supported_marker('Phrase cible établit le mécanisme.',record)
        self.assertIn(marker_for('C-X'),out)

    def _project(self,tmp):
        p=tmp/'p';(p/'01_arcs/A/claims').mkdir(parents=True);(p/'00_method/capture').mkdir(parents=True)
        (p/'01_arcs/A/claims/C1.json').write_text(json.dumps({'id':'C1','claim':'one'}),encoding='utf-8')
        (p/'01_arcs/A/claims/C2.json').write_text(json.dumps({'id':'C2','claim':'two'}),encoding='utf-8')
        (p/'00_method/capture/run_field_fragments.json').write_text(json.dumps([{'id':'F1','promotes_to':'C1'}]),encoding='utf-8')
        return p

    def test_coverage_detects_thin_and_unaccounted(self):
        with tempfile.TemporaryDirectory() as d:
            p=self._project(Path(d));md='Long enough paragraph for claim one and mechanism detail. [claim:C1]'
            manifest=build_claim_manifest(p,md)
            self.assertEqual(1,manifest['C1']['paragraph_count'])
            report=coverage_completeness(p,md,{'dispositions':{}})
            self.assertIn('claim:C2',report['unaccounted'])
            self.assertTrue(report['errors'])

    def test_canonical_points_stays_warning_only(self):
        report=audit_canonical_points();self.assertEqual('warning_only_until_populated',report['mode']);self.assertGreater(report['claims_total'],0)

if __name__=='__main__':unittest.main()
