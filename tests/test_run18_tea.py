import json,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PRE=ROOT/'examples/sri_lanka_pre_1948';POST=ROOT/'examples/sri_lanka_post_1948'
def load(p):return json.loads(p.read_text(encoding='utf-8'))
class Run18TeaTests(unittest.TestCase):
 def test_acceptance_audit_is_green(self):
  r=subprocess.run([sys.executable,'scripts/audit_run18_tea.py'],cwd=ROOT,text=True,capture_output=True);self.assertEqual(0,r.returncode,r.stdout+r.stderr);self.assertIn('RUN18 TEA AUDIT OK',r.stdout)
 def test_wage_fact_effect_inference_are_distinct(self):
  d=POST/'01_arcs/A18_malaiyaha_tamils_status_and_wage/claims';self.assertEqual('source_fact',load(d/'C-R18-WAGE-2026-FACT.json')['type']);self.assertEqual('policy_effect',load(d/'C-R18-WAGE-2026-EFFECT.json')['type']);self.assertEqual('inference',load(d/'C-R18-WAGE-2026-INFERENCE.json')['type'])
 def test_m3_remains_bounded(self):
  c=load(POST/'01_arcs/A17b_plantation_economy_and_value_capture/claims/C-R18-M3-001.json');self.assertIn(c.get('confidence'),{'U','C'})
 def test_object_focus_and_portrait_are_exercised(self):
  ss=[]
  for project in (PRE,POST):
   for p in project.glob('09_output/side_stories/SS-R18-*.json'):
    d=load(p);ss.extend(d if isinstance(d,list) else [d])
  self.assertGreaterEqual(len(ss),13);k={x.get('kind') for x in ss};self.assertIn('object_focus',k);self.assertIn('portrait',k)
if __name__=='__main__':unittest.main()
