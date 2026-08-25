from pathlib import Path
import json,subprocess,sys,unittest
ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'examples/sri_lanka_pre_1948'
POST=ROOT/'examples/sri_lanka_post_1948'

class Run16FieldIntakeTests(unittest.TestCase):
    def test_acceptance_audit_is_green(self):
        r=subprocess.run([sys.executable,'scripts/audit_run16_field_intakes.py'],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(0,r.returncode,r.stdout+r.stderr)
        self.assertIn('RUN16 FIELD AUDIT OK',r.stdout)

    def test_mihintale_primary_scope_does_not_launder_antiquity(self):
        src=json.loads((PRE/'05_sources/source_register_run16_field.json').read_text(encoding='utf-8'))
        field=next(x for x in src if x['id']=='FIELD-MIHINTALE-STELE-2024')
        self.assertEqual('T0',field['tier'])
        trad=json.loads((PRE/'01_arcs/A02c_anuradhapura_and_mahavihara/claims/C-R16-MIH-TRAD-002.json').read_text(encoding='utf-8'))
        self.assertEqual('tradition',trad['type']);self.assertEqual('C',trad['confidence']);self.assertTrue(trad['bounded_by'])

    def test_abhayagiri_afp_is_single_family_and_provisional(self):
        src=json.loads((PRE/'05_sources/source_register_run16_field.json').read_text(encoding='utf-8'))
        self.assertEqual(1,len([x for x in src if x['id'].startswith('AFP-ABHAYAGIRI')]))
        claim=json.loads((PRE/'01_arcs/A02c_anuradhapura_and_mahavihara/claims/C-R16-ABH-002.json').read_text(encoding='utf-8'))
        self.assertEqual('C',claim['confidence']);self.assertIn('pending',claim['bounded_by'])

    def test_internal_military_comparator_never_transports_outcome(self):
        b=json.loads((POST/'06_bridges/B-R16-MIL-INTERNAL-COMPARATOR-001.json').read_text(encoding='utf-8'))
        self.assertEqual('mechanism',b['transportability']);self.assertGreaterEqual(len(b['confounders']),5);self.assertTrue(b['bounded_by'])

    def test_horton_metric_contradiction_remains_open(self):
        c=json.loads((POST/'07_drifts/run16_contradictions.json').read_text(encoding='utf-8'))
        row=next(x for x in c if x['id']=='CON-R16-HOR-WORLDS-END-001')
        self.assertEqual('open',row['resolution']);self.assertIn('Survey Department',row['required_anchor'])

if __name__=='__main__':unittest.main()
