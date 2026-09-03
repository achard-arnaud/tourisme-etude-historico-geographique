import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'scripts'
if str(SCRIPTS) not in sys.path:sys.path.insert(0,str(SCRIPTS))

from materialize_storytelling_overlays import (
    CH8,CH9,CH10,EPILOGUE,TRACE_APPENDIX,materialize,section
)

OUT=ROOT/'examples/sri_lanka_pre_1948/09_output'


class Run53TransversalReaderCleanupTests(unittest.TestCase):
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
            (OUT/'run53_transversal_reader_overlay.md').read_text(encoding='utf-8'),
        )

    def test_transversal_handoffs_render_once(self):
        self.assertEqual(1,self.result.count('[RUN53:TRANSITION-CH3-CH4] BEGIN'))
        self.assertEqual(1,self.result.count('[RUN53:TRANSITION-CH7-CH8] BEGIN'))
        self.assertIn('comment cet héritage devient-il un apogée',self.result)
        self.assertIn('Plusieurs optimums territoriaux coexistent',self.result)

    def test_absorbed_legacy_side_stories_no_longer_interrupt_reader(self):
        ch8=section(self.result,CH8,CH9)
        ch9=section(self.result,CH9,CH10)
        self.assertNotIn('SIDE-STORY:SS-PRE-004',ch8)
        for legacy_id in ('SS-PRE-003','SS-PRE-001','SS-PRE-002'):
            self.assertNotIn(legacy_id,ch9)
        self.assertEqual(1,ch9.count('[SIDE-STORY:SS-R23-KDY-SIAM-DEZOOM-001] BEGIN'))

    def test_voc_conclusion_is_not_followed_by_technical_recaps(self):
        ch9=section(self.result,CH9,CH10)
        self.assertNotIn('ARC-RECAP:',ch9)
        self.assertNotIn('### Récap causal',ch9)
        self.assertIn('suffisamment dense pour être **hérité** presque comme une machine',ch9)

    def test_legacy_recaps_are_preserved_in_traceability_appendix(self):
        appendix=section(self.result,TRACE_APPENDIX)
        for recap_id in ('RECAP-A06','RECAP-A07','RECAP-A08'):
            self.assertEqual(1,appendix.count(f'[ARC-RECAP:{recap_id}]'))
        self.assertGreater(self.result.find(TRACE_APPENDIX),self.result.find(EPILOGUE))

    def test_dispositions_are_explicit_not_silent(self):
        audit=(ROOT/'docs/RUN53_TRANSVERSAL_READER_AUDIT.md').read_text(encoding='utf-8')
        for token in ('SS-PRE-004','SS-PRE-003','SS-PRE-001','SS-PRE-002','RECAP-A06','RECAP-A07','RECAP-A08'):
            self.assertIn(token,audit)


if __name__=='__main__':unittest.main()
