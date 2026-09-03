import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'scripts'
if str(SCRIPTS) not in sys.path:sys.path.insert(0,str(SCRIPTS))

from materialize_storytelling_overlays import (
    CH4,CH5,CH6,CH7,CH8,CH9,CH10,EPILOGUE,materialize,section
)

OUT=ROOT/'examples/sri_lanka_pre_1948/09_output'


class Run51StorytellingMaterializerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline=(OUT/'report_v3_full.md').read_text(encoding='utf-8')
        cls.result=materialize(
            cls.baseline,
            (OUT/'run47_storytelling_iterative_two_arcs.md').read_text(encoding='utf-8'),
            (OUT/'run50_A02_A03_canonical_overlay.md').read_text(encoding='utf-8'),
            (OUT/'run51_storytelling_ch4_polonnaruwa.md').read_text(encoding='utf-8'),
            (OUT/'run51_storytelling_ch8_portugal_kandy.md').read_text(encoding='utf-8'),
            (OUT/'run52_storytelling_ch5_fall_polonnaruwa.md').read_text(encoding='utf-8'),
            (OUT/'run52_storytelling_ch6_mobile_capitals.md').read_text(encoding='utf-8'),
        )

    def test_run51_problem_first_signatures_are_materialized_once(self):
        self.assertEqual(1,self.result.count('Comment une monarchie restaurée transforme-t-elle eau, fiscalité, Saṅgha'))
        self.assertEqual(1,self.result.count('Comment le Portugal convertit-il supériorité navale, ports, alliances dynastiques'))
        self.assertNotIn('## **Apogée : eau, Saṅgha, légitimité, savoir et projection**',section(self.result,CH4,CH5))

    def test_all_target_chapter_boundaries_remain_unique(self):
        for anchor in (CH4,CH5,CH6,CH7,CH8,CH9,CH10,EPILOGUE):
            self.assertEqual(1,self.result.count(anchor),anchor)

    def test_existing_special_blocks_are_not_dropped(self):
        old_ch4=section(self.baseline,CH4,CH5)
        new_ch4=section(self.result,CH4,CH5)
        old_ch8=section(self.baseline,CH8,CH9)
        new_ch8=section(self.result,CH8,CH9)
        for marker in ('SIDE-STORY:SS-R43-GALVIHARA-OBJECT-001',):
            if marker in old_ch4:self.assertIn(marker,new_ch4)
        for line in old_ch8.splitlines():
            if line.startswith('<!-- [SIDE-STORY:') or line.startswith('<!-- [ARC-RECAP:'):
                marker=line.split(']')[0]+']'
                self.assertIn(marker,new_ch8)

    def test_run50_overlays_and_run47_rewrites_survive_run51(self):
        self.assertEqual(1,self.result.count('[RUN50:A02-A03-MARITIME] BEGIN'))
        self.assertEqual(1,self.result.count('[RUN50:GOKANNA-POLONNARUWA] BEGIN'))
        self.assertGreater(len(section(self.result,CH9,CH10)),1000)
        self.assertGreater(len(section(self.result,CH10,EPILOGUE)),1000)

    def test_global_retention_guard_is_conservative(self):
        self.assertGreaterEqual(len(self.result),int(len(self.baseline)*0.78))


if __name__=='__main__':unittest.main()
