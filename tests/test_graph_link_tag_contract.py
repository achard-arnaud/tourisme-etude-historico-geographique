import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

def load_audit():
    path=ROOT/"scripts"/"graph_link_audit.py"
    spec=importlib.util.spec_from_file_location("graph_link_audit",path)
    module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);return module

class GraphLinkTagContractTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.audit=load_audit()
    def test_run21_bridges_are_projected_with_exact_endpoints(self):
        for project in ("sri_lanka_pre_1948","sri_lanka_post_1948"):
            root=ROOT/"examples"/project
            bridges={}
            for p in (root/"06_bridges").glob("B-R21-*.json"):
                b=json.loads(p.read_text(encoding="utf-8"));bridges[b["id"]]=b
            tagged={}
            for p in (root/"04_graph").glob("edges*.jsonl"):
                for line in p.read_text(encoding="utf-8").splitlines():
                    if not line.strip():continue
                    edge=json.loads(line)
                    for bid in edge.get("bridge_ids",[]):\n                        if bid.startswith("B-R21-"): tagged.setdefault(bid,[]).append(edge)
            self.assertEqual(set(bridges),set(tagged))
            for bid,bridge in bridges.items():
                self.assertEqual(1,len(tagged[bid]))
                edge=tagged[bid][0]
                self.assertEqual(bridge["from_claim"],edge["from"])
                self.assertEqual(bridge["to_claim"],edge["to"])
                self.assertTrue(set(bridge["source_ids"]).issubset(edge["source_ids"]))
    def test_unresolved_tag_and_bridge_endpoint_mismatch_fail(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            for rel in ("01_arcs/A/claims","03_wiki","04_graph","05_sources","06_bridges"):
                (root/rel).mkdir(parents=True,exist_ok=True)
            for cid in ("C1","C2"):
                (root/"01_arcs/A/claims"/f"{cid}.json").write_text(json.dumps({"id":cid}),encoding="utf-8")
            (root/"05_sources/source_register.json").write_text(json.dumps([{"id":"S1"}]),encoding="utf-8")
            (root/"06_bridges/B1.json").write_text(json.dumps({"id":"B1","from_claim":"C1","to_claim":"C2"}),encoding="utf-8")
            edge={"from":"C2","relation":"TEST","to":"C1","claim_ids":["C1","MISSING"],"source_ids":["S1"],"bridge_ids":["B1"]}
            (root/"04_graph/edges.jsonl").write_text(json.dumps(edge)+"\n",encoding="utf-8")
            errors,_,_,_=self.audit.validate_graph_links(root)
            self.assertTrue(any("unresolved graph claim_id" in e for e in errors))
            self.assertTrue(any("endpoints do not match tagged bridge" in e for e in errors))
    def test_run20_video_leads_create_no_graph_endpoints(self):
        register=json.loads((ROOT/"docs/intakes/video_evidence/run20/video_proposition_register.json").read_text(encoding="utf-8"))
        self.assertEqual([],register["propositions"])
        graph_text="\n".join((ROOT/"examples"/p/"04_graph/edges.jsonl").read_text(encoding="utf-8") for p in ("sri_lanka_pre_1948","sri_lanka_post_1948"))
        self.assertNotIn("VP-R22",graph_text)
if __name__=="__main__":unittest.main()
