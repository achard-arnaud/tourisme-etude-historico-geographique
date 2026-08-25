import json,subprocess,sys,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];PRE=ROOT/'examples/sri_lanka_pre_1948'
class Run14LegacyBoundaryTests(unittest.TestCase):
    def test_acceptance_audit_is_green(self):
        r=subprocess.run([sys.executable,'scripts/audit_run14_legacy.py'],cwd=ROOT,text=True,capture_output=True);self.assertEqual(0,r.returncode,r.stdout+r.stderr);self.assertIn('traced 8 / declared 17 / untracked 0',r.stdout)
    def test_materializer_rejects_title_echo_takeaway(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);project=root/'p';(project/'09_output/side_stories').mkdir(parents=True);source=root/'in.md';out=root/'out.md';source.write_text('Anchor\n',encoding='utf-8')
            item={'schema_version':'1.1','class':'side_story','id':'SS-ECHO','kind':'detour','status':'promoted','title':'Same title','purpose':'p','map_eligible':False,'lineage':{'claim_ids':[],'source_ids':[],'bridge_ids':[],'hil_ids':[],'drift_paths':[],'origin_paths':[]},'placement':{'section_anchor':'Anchor','return_to':'anchor:Anchor'},'content':{'takeaway':'Same title','body_markdown':'body'},'render':{'label':'Petit détour','marker':'[SIDE-STORY:SS-ECHO]','required_in_reader':False}}
            (project/'09_output/side_stories/SS-ECHO.json').write_text(json.dumps(item),encoding='utf-8')
            r=subprocess.run([sys.executable,'scripts/materialize_side_stories.py','--project',str(project),'--source',str(source),'--output',str(out)],cwd=ROOT,text=True,capture_output=True);self.assertNotEqual(0,r.returncode);self.assertIn('takeaway merely repeats title',r.stdout+r.stderr)
    def test_legacy_promotion_is_rejected(self):
        sys.path.insert(0,str(ROOT/'scripts'));from side_story_contract import validate_side_story_item
        item={'schema_version':'1.1','class':'side_story','id':'SS-X','kind':'method','status':'promoted','lineage_quality':'legacy_fragment','title':'x','purpose':'x','map_eligible':False,'lineage':{'claim_ids':[],'source_ids':[],'bridge_ids':[],'hil_ids':[],'drift_paths':[],'origin_paths':[]},'placement':{'return_to':None},'content':{'takeaway':'Different conclusion'},'legacy_retention_reason':'temporary','render':{'label':'Point de méthode','marker':'[SIDE-STORY:SS-X]','required_in_reader':True}}
        self.assertTrue(any('legacy_fragment cannot be promoted' in e for e in validate_side_story_item(item)))
if __name__=='__main__':unittest.main()
