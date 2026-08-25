import json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'examples/sri_lanka_pre_1948';POST=ROOT/'examples/sri_lanka_post_1948'

class Run15IntakeTests(unittest.TestCase):
    def test_acceptance_audit_is_green(self):
        r=subprocess.run([sys.executable,'scripts/audit_run15_intakes.py'],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(0,r.returncode,r.stdout+r.stderr)
        self.assertIn('RUN15 INTAKE AUDIT OK',r.stdout)

    def test_guide_snapshot_cannot_promote_without_identity(self):
        data=json.loads((PRE/'00_method/capture/guide_fragments.json').read_text(encoding='utf-8'))
        self.assertEqual('blocked_missing_cover_metadata',data['source_status'])
        self.assertIsNone(data['source_candidate']['date'])
        self.assertTrue(all(not f['promotes_to'] for f in data['fragments']))
        self.assertTrue(all(f['verbatim'] is None for f in data['fragments']))

    def test_recent_intakes_materialize_negative_results(self):
        bridges=[json.loads(p.read_text(encoding='utf-8')) for p in POST.glob('06_bridges/B-R15-*.json')]
        self.assertGreaterEqual(len(bridges),4)
        self.assertTrue(any(b['result']=='D' for b in bridges))
        self.assertTrue(any(b['result']=='U' for b in bridges))

    def test_tourism_metrics_do_not_swap_denominators(self):
        rows=[json.loads(p.read_text(encoding='utf-8')) for p in (POST/'01_arcs/A16_tourism_shock_and_fiscal_collapse/claims').glob('*.json')]
        metrics=[r for r in rows if r.get('type')=='metric']
        self.assertGreaterEqual(len(metrics),4)
        for row in metrics:
            meta=row['metric']
            for field in ('denominator','geography','period','basis','source_definition'):
                self.assertTrue(meta.get(field),f"{row['id']} missing {field}")

if __name__=='__main__':unittest.main()
