import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from materialize_storytelling_overlays import legacy_skip_keys, load_story_dispositions


class StoryDispositionLedgerTests(unittest.TestCase):
    def test_run53_absorptions_are_executable_data(self):
        rows = load_story_dispositions()
        self.assertEqual(8, len(rows))
        self.assertEqual({"SIDE-STORY:SS-PRE-004"}, legacy_skip_keys("ch8", rows))
        self.assertEqual(
            {
                "SIDE-STORY:SS-PRE-003",
                "SIDE-STORY:SS-PRE-001",
                "SIDE-STORY:SS-PRE-002",
                "SIDE-STORY:SS-R23-KDY-SIAM-DEZOOM-001",
                "ARC-RECAP:RECAP-A06",
                "ARC-RECAP:RECAP-A07",
                "ARC-RECAP:RECAP-A08",
            },
            legacy_skip_keys("ch9", rows),
        )


if __name__ == "__main__":
    unittest.main()
