import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    path = ROOT / "scripts" / name
    spec = importlib.util.spec_from_file_location(name.removesuffix(".py"), path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class YoutubeTranscriptTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.mod = load_script("youtube_transcript.py")

    def test_video_id_variants(self):
        for url in (
            "https://youtu.be/gNFQPFp-NWg?si=x",
            "https://www.youtube.com/watch?v=gNFQPFp-NWg",
            "https://youtube.com/shorts/gNFQPFp-NWg",
        ):
            self.assertEqual(self.mod.video_id_from_url(url), "gNFQPFp-NWg")

    def test_json3_preserves_timestamps(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / "captions.json3"
            path.write_text(json.dumps({"events": [
                {"tStartMs": 1250, "dDurationMs": 2500, "segs": [{"utf8": "Hello "}, {"utf8": "world"}]},
                {"tStartMs": 4000, "dDurationMs": 1000, "segs": [{"utf8": "again"}]},
            ]}), encoding="utf-8")
            got = self.mod.parse_json3(path)
        self.assertEqual(got[0], {"start_s": 1.25, "end_s": 3.75, "text": "Hello world"})
        self.assertEqual(got[1]["start_s"], 4.0)

    def test_missing_dependency_writes_typed_degradation(self):
        with mock.patch.object(self.mod.shutil, "which", return_value=None):
            result = self.mod.acquire("https://youtu.be/gNFQPFp-NWg", "fr.*,en.*", False, 10)
        self.assertEqual(result["status"], "missing_dependency")
        self.assertEqual(result["schema_version"], "video-evidence/v1")


class VideoClaimContractTests(unittest.TestCase):
    def run_contract(self, evidence, register):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            ep = root / "evidence.json"; rp = root / "register.json"
            ep.write_text(json.dumps(evidence), encoding="utf-8")
            rp.write_text(json.dumps(register), encoding="utf-8")
            return subprocess.run([sys.executable, str(ROOT / "scripts" / "video_claim_contract.py"),
                                   "--evidence", str(ep), "--register", str(rp)], capture_output=True, text=True)

    def evidence(self):
        return {"schema_version": "video-evidence/v1", "id": "VE-YT-gNFQPFp-NWg", "url": "https://youtu.be/gNFQPFp-NWg",
                "video_id": "gNFQPFp-NWg", "status": "success", "acquired_at": "2026-08-26T00:00:00+00:00",
                "segments": [{"start_s": 1.0, "end_s": 2.0, "text": "claim"}], "transcript_text": "claim", "transcript_sha256": "x"}

    def register(self):
        return {"schema_version": "video-proposition-register/v1", "propositions": [{
            "id": "VP-01", "statement": "A speaker asserts something.", "claim_class": "reported_claim", "status": "lead_only",
            "video_evidence_id": "VE-YT-gNFQPFp-NWg", "timestamp_start_s": 1.0, "timestamp_end_s": 2.0,
            "transcript_excerpt": "claim", "research_queries": ["Which sources confirm this?"], "promoted_claim_ids": []}]}

    def test_valid_lead_passes(self):
        result = self.run_contract(self.evidence(), self.register())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_unresolved_evidence_fails(self):
        register = self.register(); register["propositions"][0]["video_evidence_id"] = "VE-YT-unknown0000"
        result = self.run_contract(self.evidence(), register)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("unresolved video_evidence_id", result.stdout)

    def test_promotion_requires_claim_lineage(self):
        register = self.register(); register["propositions"][0]["status"] = "promoted"
        result = self.run_contract(self.evidence(), register)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("promoted without promoted_claim_ids", result.stdout)


if __name__ == "__main__":
    unittest.main()
