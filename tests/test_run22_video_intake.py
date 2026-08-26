import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
class Run22VideoIntakeAdmissionTests(unittest.TestCase):
    def test_video_intake_is_archived_and_registered(self):
        rows=json.loads((ROOT/"docs/intakes/intake_registry.json").read_text(encoding="utf-8"))
        row=next(x for x in rows if x["id"]=="I-R22-VIDEO-LEADS")
        self.assertEqual("archived",row["preservation_status"])
        self.assertTrue((ROOT/row["repo_path"]).exists())
        self.assertEqual("RUN22",row["first_run"])
    def test_four_degraded_ledgers_and_empty_proposition_register(self):
        root=ROOT/"docs/intakes/video_evidence/run20"
        ledgers=[json.loads(p.read_text(encoding="utf-8")) for p in root.glob("VE-YT-*.json")]
        self.assertEqual(4,len(ledgers))
        self.assertTrue(all(x["schema_version"]=="video-evidence/v1" for x in ledgers))
        self.assertTrue(all(x["status"]!="success" and not x["segments"] for x in ledgers))
        register=json.loads((root/"video_proposition_register.json").read_text(encoding="utf-8"))
        self.assertEqual([],register["propositions"])
    def test_video_sources_are_t5_leads_without_claim_support(self):
        rows=json.loads((ROOT/"examples/sri_lanka_post_1948/05_sources/source_register_run22_video_leads.json").read_text(encoding="utf-8"))
        self.assertEqual(4,len(rows))
        self.assertTrue(all(x["tier"]=="T5" and x["anchor_role"]=="lead" and x["claims_supported"]==[] for x in rows))
if __name__=="__main__":unittest.main()
