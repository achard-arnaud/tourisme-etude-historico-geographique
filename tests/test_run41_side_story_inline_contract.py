import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))

import post_review_side_story_placement as placement


class Run41InlineSideStoryContractTest(unittest.TestCase):
    def setUp(self):
        self.profiles=json.loads((ROOT/'templates/side-stories/type_profiles.json').read_text(encoding='utf-8'))

    def test_every_type_has_explicit_length_and_storytelling_contract(self):
        expected={'detour','dezoom','also','method','false_lead','portrait','object_focus','comparator','callback','analytical_focus'}
        self.assertEqual(expected,set(self.profiles['profiles']))
        for kind,p in self.profiles['profiles'].items():
            self.assertGreater(p['hard_min_visible_words'],0,kind)
            lo,hi=p['target_visible_words']
            self.assertLessEqual(p['hard_min_visible_words'],lo,kind)
            self.assertLess(lo,hi,kind)
            self.assertLessEqual(hi,p['soft_upper_visible_words'],kind)
            self.assertTrue(p['required_beats'],kind)
            self.assertTrue(p['storytelling_rules'],kind)
            self.assertEqual('embedded_in_host_paragraph',p['default_placement'].split('_after_')[0].split('_at_')[0].split('_immediately_')[0] if p['default_placement']!='embedded_in_host_paragraph' else p['default_placement'])

    def test_global_density_contract_is_explicit(self):
        c=self.profiles['placement_contract']
        self.assertEqual(1,c['max_embedded_side_stories_per_paragraph'])
        self.assertEqual(3,c['density_window_paragraphs'])
        self.assertEqual(2,c['max_embedded_side_stories_in_density_window'])
        self.assertEqual(1,c['max_interstitial_side_stories_per_boundary'])
        self.assertIn('append_at_book_end',c['forbidden'])
        self.assertIn('split_sentence',c['forbidden'])

    def test_sentence_split_is_inside_host_and_keeps_context_on_both_sides(self):
        block=('This first sentence provides enough concrete historical context for the host paragraph to remain meaningful. '
               'The museum object now triggers the mechanism that the excursion must explain in detail. '
               'After the excursion the paragraph resumes with enough words to return to chronology and explain the local consequence for the reader.')
        item={'placement':{'match_terms':['museum object'],'mechanism_terms':['mechanism'],'chronology_terms':[]}}
        split=placement._choose_sentence_split(block,item)
        self.assertIsNotNone(split)
        raw,visible=split
        self.assertGreaterEqual(placement._visible_words(block[:raw]),12)
        self.assertGreaterEqual(placement._visible_words(block[raw:]),12)
        self.assertEqual(visible,placement._visible_words(block[:raw]))

    def test_three_consecutive_embeds_move_best_interstitial_type_only(self):
        blocks=[
            'First host paragraph has enough words to describe one concrete event and its mechanism in the chronological story for testing.',
            'Second host paragraph has enough words to describe the regional scale change and connect the local event to a larger historical system.',
            'Third host paragraph has enough words to return to the local sequence and update an earlier observation without opening a new chapter.'
        ]
        def row(kind,ordinal):
            return {'item':{'id':f'SS-{ordinal}','kind':kind,'placement':{'match_terms':[]}},'host_idx':ordinal,'host_ordinal':ordinal,'placement_mode':'embedded','split_raw_offset':20,'split_after_visible_words':12,'density_reason':None,'meta':{}}
        assignments=[row('object_focus',0),row('dezoom',1),row('callback',2)]
        placement._enforce_three_paragraph_density(blocks,assignments)
        modes=[a['placement_mode'] for a in assignments]
        self.assertEqual(2,modes.count('embedded'))
        self.assertEqual(1,modes.count('interstitial'))
        moved=next(a for a in assignments if a['placement_mode']=='interstitial')
        self.assertEqual('dezoom',moved['item']['kind'])
        self.assertEqual('three_paragraph_window_overflow',moved['density_reason'])

    def test_interstitial_boundary_capacity_is_one(self):
        assignments=[
            {'item':{'id':'SS-A','placement':{'position':'after'}},'host_ordinal':2,'placement_mode':'interstitial'},
            {'item':{'id':'SS-B','placement':{'position':'after'}},'host_ordinal':2,'placement_mode':'interstitial'},
        ]
        placement._reserve_interstitial_boundaries(assignments)
        boundaries=[(a['interstitial_boundary']['host_ordinal'],a['interstitial_boundary']['position']) for a in assignments]
        self.assertEqual(2,len(set(boundaries)))


if __name__=='__main__':
    unittest.main()
