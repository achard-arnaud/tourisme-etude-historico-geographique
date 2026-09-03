import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
SCRIPTS=ROOT/'scripts'
if str(SCRIPTS) not in sys.path:sys.path.insert(0,str(SCRIPTS))

from materialize_storytelling_overlays import CH5,CH6,CH7,materialize,section

OUT=ROOT/'examples/sri_lanka_pre_1948/09_output'


class Run52FormGlobalTests(unittest.TestCase):
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

    def test_only_failed_form_global_chapters_get_new_signatures(self):
        self.assertEqual(1,self.result.count('Pourquoi un système aussi intégré et productif que Polonnaruwa devient-il'))
        self.assertEqual(1,self.result.count('Comment la disparition de l’optimum de Rajarata transforme-t-elle la souveraineté sri-lankaise'))
        # Chapter 7 keeps its existing causal question rather than receiving a rewrite signature.
        self.assertEqual(1,self.result.count('pourquoi, après la désarticulation de Rajarata, un royaume durable se forme-t-il dans le nord'))

    def test_legacy_dossier_openings_are_removed_from_ch5_ch6(self):
        ch5=section(self.result,CH5,CH6)
        ch6=section(self.result,CH6,CH7)
        self.assertNotIn('## **Pourquoi le système Polonnaruwa cesse d’être optimal**',ch5)
        self.assertNotIn('## **Des capitales fortifiées aux économies portuaires, puis à Kandy**',ch6)
        self.assertNotIn('## **Mise au point — La chute comme changement d\'optimum, confirmé par les sources**',ch5)
        self.assertNotIn('## **Mise au point — Quatre approfondissements structurants**',ch6)

    def test_ch5_keeps_typed_field_detours_in_context(self):
        ch5=section(self.result,CH5,CH6)
        for marker in (
            'SIDE-STORY:SS-R43-POLONNARUWA-MONEY-FOCUS-001',
            'SIDE-STORY:SS-R40-SCALPEL-OBJECT-001',
            'SIDE-STORY:SS-R40-EPIDEMIC-FALSE-LEAD-001',
        ):
            self.assertIn(marker,ch5)

    def test_ch6_keeps_regional_bridges_without_restoring_catalogue_structure(self):
        ch6=section(self.result,CH6,CH7)
        for marker in (
            'SIDE-STORY:SS-R40-PANDYA-JAFFNA-001',
            'SIDE-STORY:SS-R40-SOUTHINDIA-TRADE-001',
            'SIDE-STORY:SS-R40-ARAB-ENVOY-001',
            'SIDE-STORY:SS-R40-MING-KOTTE-001',
            'SIDE-STORY:SS-R40-VIJAYANAGARA-COMP-001',
        ):
            self.assertIn(marker,ch6)
        self.assertLess(ch6.find('Dambadeniya'),ch6.find('Yapahuwa'))
        self.assertLess(ch6.find('Yapahuwa'),ch6.find('Kotte'))

    def test_existing_special_block_inventory_is_not_reduced(self):
        for start,end in ((CH5,CH6),(CH6,CH7)):
            old=section(self.baseline,start,end)
            new=section(self.result,start,end)
            old_markers={
                line.split(']')[0]+']' for line in old.splitlines()
                if line.startswith('<!-- [SIDE-STORY:') or line.startswith('<!-- [ARC-RECAP:')
            }
            for marker in old_markers:self.assertIn(marker,new)


if __name__=='__main__':unittest.main()
