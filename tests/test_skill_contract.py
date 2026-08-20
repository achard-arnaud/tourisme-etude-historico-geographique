import json,re,subprocess,sys,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def fm(text):
    m=re.match(r'^---\n(.*?)\n---\n',text,re.S);out={}
    if not m:return out
    for line in m.group(1).splitlines():
        if ':' in line:k,v=line.split(':',1);out[k.strip()]=v.strip()
    return out
class SkillContractTests(unittest.TestCase):
    def test_all_routed_skills_are_discoverable(self):
        manifest=json.loads((ROOT/'docs/RUN11_COMPOSITION_PIPELINE_MANIFEST.json').read_text(encoding='utf-8'));routed={x['skill'] for x in manifest['dispatched_skills']}|{x['skill'] for x in manifest['skipped_skills']};known={p.parent.name for p in (ROOT/'skills').glob('*/SKILL.md')};self.assertEqual(known,routed)
        for name in known:
            meta=fm((ROOT/'skills'/name/'SKILL.md').read_text(encoding='utf-8'));self.assertEqual(name,meta.get('name'));self.assertTrue(meta.get('description','').startswith('Use when'))
    def test_root_skill_is_discoverable_and_context_budget_is_system_level(self):
        meta=fm((ROOT/'SKILL.md').read_text(encoding='utf-8'));self.assertEqual('tourisme-etude-historico-geographique',meta.get('name'));self.assertTrue(meta.get('description','').startswith('Use when'))
        r=subprocess.run([sys.executable,'scripts/audit_context_budget.py','--latest'],cwd=ROOT,text=True,capture_output=True);self.assertEqual(0,r.returncode,r.stdout+r.stderr)
    def test_composition_templates_and_scripts_exist(self):
        for rel in ['templates/side-story.json','templates/arc-recap.json','templates/map-asset.json','templates/reader-profile.json','scripts/side_story_contract.py','scripts/arc_recap_contract.py','scripts/map_asset_contract.py','scripts/reader_profile_contract.py','scripts/graph_link_audit.py','scripts/materialize_side_stories.py','scripts/resolve_reader_plan.py']:
            self.assertTrue((ROOT/rel).exists(),rel)
    def test_root_orchestrator_names_composition_capabilities(self):
        text=(ROOT/'SKILL.md').read_text(encoding='utf-8')
        for name in ['composing-side-stories','composing-arc-recaps','curating-historical-map-assets','tailoring-reader-profiles','analyzing-regional-global-systems']:self.assertIn(name,text)
if __name__=='__main__':unittest.main()
