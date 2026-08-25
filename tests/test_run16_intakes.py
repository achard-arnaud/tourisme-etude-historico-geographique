from __future__ import annotations
import json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'examples/sri_lanka_pre_1948'
POST=ROOT/'examples/sri_lanka_post_1948'

class Run16IntakeTests(unittest.TestCase):
    def test_acceptance_audit_is_green(self):
        r=subprocess.run([sys.executable,'scripts/audit_run16_intakes.py'],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(0,r.returncode,r.stdout+r.stderr)
        self.assertIn('RUN16 INTAKE AUDIT OK',r.stdout)

    def test_modern_stone_does_not_promote_ancient_tradition(self):
        p=PRE/'01_arcs/A02c_anuradhapura_and_the_mahavihara/claims/C-R16-MIH-TRAD-001.json'
        c=json.loads(p.read_text(encoding='utf-8'))
        self.assertEqual('tradition',c['type']);self.assertEqual('C',c['confidence']);self.assertTrue(c.get('bounded_by'))

    def test_abhayagiri_syndication_does_not_fake_corroboration(self):
        rows=json.loads((PRE/'05_sources/source_register_run16_field.json').read_text(encoding='utf-8'))
        afp=[r for r in rows if 'AFP' in r.get('id','')]
        self.assertEqual(1,len(afp))
        c=json.loads((PRE/'01_arcs/A02c_anuradhapura_and_the_mahavihara/claims/C-R16-ABH-DATE-001.json').read_text(encoding='utf-8'))
        self.assertEqual('C',c['confidence']);self.assertIn('pending',c['bounded_by'])

    def test_internal_comparator_refuses_outcome_transport(self):
        b=json.loads((POST/'06_bridges/B-R16-MIL-INTERNAL-COMPARATOR-001.json').read_text(encoding='utf-8'))
        self.assertEqual('mechanism',b['transportability']);self.assertGreaterEqual(len(b['confounders']),5);self.assertTrue(b['bounded_by'])

    def test_horton_blog_is_capture_only(self):
        for p in POST.glob('01_arcs/*/claims/C-R16-*.json'):
            c=json.loads(p.read_text(encoding='utf-8'))
            self.assertNotIn('BLOG-UPEC-HORTON-2026',c.get('source_ids',[]),p.name)

if __name__=='__main__':unittest.main()
