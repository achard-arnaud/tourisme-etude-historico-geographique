import json, subprocess, sys, tempfile, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
PRE=ROOT/'examples/sri_lanka_pre_1948'

class AnalyticalFocusSideStoryTests(unittest.TestCase):
    def test_analytical_focus_kind_and_template_are_versioned(self):
        sys.path.insert(0,str(ROOT/'scripts'))
        from side_story_contract import ANALYTICAL_FOCUS_KIND, SUPPORTED_SCHEMA_VERSIONS, RENDER_LABELS
        self.assertEqual('analytical_focus', ANALYTICAL_FOCUS_KIND)
        self.assertIn('1.2', SUPPORTED_SCHEMA_VERSIONS)
        self.assertEqual('Focus analytique', RENDER_LABELS['analytical_focus'])
        self.assertTrue((ROOT/'templates/side-stories/analytical-focus.json').exists())
        self.assertTrue((ROOT/'templates/side-stories/analytical-focus.md').exists())

    def test_long_form_contract_requires_question_contrast_mechanism_callback_and_visual_spec(self):
        sys.path.insert(0,str(ROOT/'scripts'))
        from side_story_contract import validate_side_story_item
        item={
            'schema_version':'1.2','class':'side_story','id':'SS-X','kind':'analytical_focus','status':'candidate',
            'title':'x','arc':'LEGACY:x','purpose':'x','reason_off_trunk':'x','payoff':'x','map_eligible':True,
            'reader_policy':{'min_age':10},'lineage':{'claim_ids':[],'source_ids':[],'bridge_ids':[],'hil_ids':[],'drift_paths':[],'origin_paths':[]},
            'placement':{'section_anchor':'x','return_to':'anchor:y'},'zoom_excursion':None,
            'analysis':{},'visual':{},'content':{'takeaway':'','body_markdown':'','legacy_titles':[]},
            'render':{'label':'Focus analytique','marker':'[SIDE-STORY:SS-X]','required_in_reader':True}
        }
        errors=validate_side_story_item(item, known=None, canonical='x y', strict=False)
        for expected in ['analysis.core_question','analysis.contrast','analysis.mechanisms','analysis.callbacks','visual.format']:
            self.assertTrue(any(expected in e for e in errors), (expected,errors))

    def test_analytical_focus_materializer_renders_structured_visual_markdown(self):
        with tempfile.TemporaryDirectory() as tmp:
            project=Path(tmp); (project/'09_output/side_stories').mkdir(parents=True)
            source=project/'source.md'; output=project/'out.md'; source.write_text('# Arc\n\nAnchor\n\nReturn\n',encoding='utf-8')
            item={
                'schema_version':'1.2','class':'side_story','id':'SS-X','kind':'analytical_focus','status':'promoted','title':'Jetavana',
                'arc':'LEGACY:anuradhapura','purpose':'explain','reason_off_trunk':'semi-analytical focus','payoff':'callback','map_eligible':True,
                'reader_policy':{'min_age':10},'lineage':{'claim_ids':[],'source_ids':[],'bridge_ids':[],'hil_ids':[],'drift_paths':[],'origin_paths':[]},
                'placement':{'section_anchor':'Anchor','return_to':'anchor:Return'},'zoom_excursion':None,
                'analysis':{
                    'core_question':'Why does Jetavana matter?',
                    'thesis':'Monastic rivalry was institutional, political and economic, not a simple modern Theravada/Mahayana binary.',
                    'contrast':[{'label':'Mahavihara','position':'conservative canon lineage','caveat':'not a timeless modern bloc'},{'label':'Abhayagiri/Jetavana','position':'more open to transregional texts','caveat':'not simply identical to Mahayana'}],
                    'mechanisms':[{'name':'patronage','explanation':'royal patronage redistributed resources and legitimacy','evidence_status':'inference'}],
                    'callbacks':[{'target':'Polonnaruwa / Parakramabahu I','relation':'1165 reform unified the Sangha under Mahavihara discipline rather than fusing equal schools'}],
                    'open_questions':['How large were the fiscal transfers?']
                },
                'visual':{'format':'one_or_two_pager','orientation':'A4_landscape','layout':'historical_focus','composition':['hero_question','contrast_cards','mechanism_band','callback_strip'],'evidence_palette':{'verified':'green','inference':'orange','unknown':'red'}},
                'content':{'takeaway':'Jetavana makes later reform legible.','body_markdown':'','legacy_titles':[]},
                'render':{'label':'Focus analytique','marker':'[SIDE-STORY:SS-X]','required_in_reader':True}
            }
            (project/'09_output/side_stories/SS-X.json').write_text(json.dumps(item),encoding='utf-8')
            r=subprocess.run([sys.executable,str(ROOT/'scripts/materialize_side_stories.py'),'--project',str(project),'--source',str(source),'--output',str(output)],cwd=ROOT,text=True,capture_output=True)
            self.assertEqual(0,r.returncode,r.stdout+r.stderr)
            text=output.read_text(encoding='utf-8')
            for token in ['Focus analytique — Jetavana','Question','Mahavihara','Mécanisme','Callback','Jetavana makes later reform legible.']:
                self.assertIn(token,text)

    def test_jetavana_focus_fixture_is_present_and_map_eligible(self):
        data=json.loads((PRE/'09_output/side_stories/SS-PRE-JETAVANA-001.json').read_text(encoding='utf-8'))
        self.assertEqual('analytical_focus',data['kind'])
        self.assertEqual('1.2',data['schema_version'])
        self.assertTrue(data['map_eligible'])
        self.assertIn('Polonnaruwa',json.dumps(data,ensure_ascii=False))
        self.assertGreaterEqual(len(data['lineage']['source_ids']),4)
        self.assertEqual('field_research',data['lineage_quality'])

    def test_skill_and_sop_route_long_form_focus_without_turning_it_into_new_evidence(self):
        skill=(ROOT/'skills/composing-side-stories/SKILL.md').read_text(encoding='utf-8')
        sop=(ROOT/'docs/SOP_SIDE_STORIES.md').read_text(encoding='utf-8')
        for token in ['analytical_focus','one_or_two_pager','two-pager-nice','structured source']:
            self.assertIn(token,skill+sop)

if __name__=='__main__':unittest.main()
