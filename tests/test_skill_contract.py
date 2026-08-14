import re
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_SUBSKILLS = [
    'capturing-field-evidence',
    'sanitizing-historical-claims',
    'sourcing-historical-anchors',
    'structuring-chronological-arcs',
    'zooming-geographic-scales',
    'analyzing-institutions-and-power',
    'analyzing-geography-and-environment',
    'analyzing-economy-and-infrastructure',
    'analyzing-society-and-demography',
    'analyzing-religion-culture-legitimacy',
    'analyzing-security-and-geopolitics',
    'auditing-historiography-and-drifts',
    'building-causal-bridges',
    'maintaining-wiki-and-graph',
    'editing-historical-travel-output',
]

REQUIRED_TEMPLATES = [
    'templates/arc.md',
    'templates/claim.md',
    'templates/source-note.md',
    'templates/bridge.md',
    'templates/drift-audit.md',
    'templates/wiki-entity.md',
    'templates/output-outline.md',
]

REQUIRED_SCRIPTS = [
    'scripts/new_project.py',
    'scripts/new_arc.py',
    'scripts/qa_project.py',
    'scripts/audit_skill.py',
]


def frontmatter(text: str):
    m = re.match(r'^---\n(.*?)\n---\n', text, re.S)
    if not m:
        return {}
    out = {}
    for line in m.group(1).splitlines():
        if ':' in line:
            k, v = line.split(':', 1)
            out[k.strip()] = v.strip()
    return out


class SkillContractTests(unittest.TestCase):
    def test_root_skill_is_discoverable_and_concise(self):
        text = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        fm = frontmatter(text)
        self.assertEqual(fm.get('name'), 'tourisme-etude-historico-geographique')
        self.assertTrue(fm.get('description', '').startswith('Use when'))
        self.assertLessEqual(len(text.split()), 650)

    def test_required_subskills_exist_and_have_trigger_descriptions(self):
        for name in REQUIRED_SUBSKILLS:
            path = ROOT / 'skills' / name / 'SKILL.md'
            self.assertTrue(path.exists(), name)
            fm = frontmatter(path.read_text(encoding='utf-8'))
            self.assertEqual(fm.get('name'), name)
            self.assertTrue(fm.get('description', '').startswith('Use when'), name)

    def test_required_templates_exist(self):
        for rel in REQUIRED_TEMPLATES:
            self.assertTrue((ROOT / rel).exists(), rel)

    def test_required_scripts_exist(self):
        for rel in REQUIRED_SCRIPTS:
            self.assertTrue((ROOT / rel).exists(), rel)

    def test_root_skill_names_required_subskills_without_force_loading(self):
        text = (ROOT / 'SKILL.md').read_text(encoding='utf-8')
        self.assertNotIn('@skills/', text)
        for name in ['sourcing-historical-anchors', 'sanitizing-historical-claims',
                     'auditing-historiography-and-drifts', 'editing-historical-travel-output']:
            self.assertIn(name, text)


if __name__ == '__main__':
    unittest.main()
