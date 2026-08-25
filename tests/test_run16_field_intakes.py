import subprocess,sys
from pathlib import Path
import unittest

ROOT=Path(__file__).resolve().parents[1]

class Run16FieldIntakeTests(unittest.TestCase):
    def test_run16_acceptance_audit_is_green(self):
        r=subprocess.run([sys.executable,'scripts/audit_run16_field_intakes.py'],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(0,r.returncode,r.stdout+r.stderr)
        self.assertIn('RUN16 FIELD AUDIT OK',r.stdout)

    def test_mihintale_modern_stele_does_not_close_antiquity(self):
        r=subprocess.run([sys.executable,'scripts/audit_run16_field_intakes.py'],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(0,r.returncode,r.stdout+r.stderr)

    def test_internal_military_comparator_is_bounded(self):
        r=subprocess.run([sys.executable,'scripts/audit_run16_field_intakes.py'],cwd=ROOT,text=True,capture_output=True)
        self.assertEqual(0,r.returncode,r.stdout+r.stderr)

if __name__=='__main__': unittest.main()
