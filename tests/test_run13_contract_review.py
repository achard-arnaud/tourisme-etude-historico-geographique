import importlib.util,json,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SPEC=importlib.util.spec_from_file_location('run13',ROOT/'scripts/audit_run13_contracts.py');M=importlib.util.module_from_spec(SPEC);SPEC.loader.exec_module(M)

class Run13ReviewTests(unittest.TestCase):
    def story(self,status='validated',arc='LEGACY:test',mechanism=None):
        return {'id':'SS1','kind':'analytical_focus','status':status,'arc':arc,'analysis':{'mechanisms':[mechanism or {'name':'m','evidence_status':'unknown'}]}}
    def fixture(self,story,claim=None):
        td=tempfile.TemporaryDirectory();root=Path(td.name);(root/'09_output/side_stories').mkdir(parents=True)
        (root/'09_output/side_stories/s.json').write_text(json.dumps(story),encoding='utf-8')
        if claim:
            p=root/'01_arcs/A01/claims';p.mkdir(parents=True);(p/f"{claim['id']}.json").write_text(json.dumps(claim),encoding='utf-8')
        return td,root
    def test_validated_legacy_is_reported_not_blocked(self):
        td,root=self.fixture(self.story());self.addCleanup(td.cleanup);e,w,n=M.audit(root);self.assertEqual([],e);self.assertEqual(1,n)
    def test_promoted_legacy_is_blocked(self):
        td,root=self.fixture(self.story(status='promoted'));self.addCleanup(td.cleanup);e,_,_=M.audit(root);self.assertTrue(any('cannot use' in x for x in e))
    def test_evidence_status_is_derived_from_claim_confidence(self):
        story=self.story(arc='A01',mechanism={'name':'m','claim_ids':['C1'],'evidence_status':'verified'})
        td,root=self.fixture(story,{'id':'C1','confidence':'C'});self.addCleanup(td.cleanup);e,_,_=M.audit(root);self.assertTrue(any('derived' in x for x in e))
    def test_unbound_mechanism_must_be_unknown_once_validated(self):
        story=self.story(arc='A01',mechanism={'name':'m','evidence_status':'verified'})
        td,root=self.fixture(story);self.addCleanup(td.cleanup);e,_,_=M.audit(root);self.assertTrue(any('without claim_ids' in x for x in e))
if __name__=='__main__':unittest.main()
