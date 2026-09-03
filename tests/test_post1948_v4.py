import tempfile
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from materialize_post1948_v4 import materialize


class Post1948V4MaterializerTests(unittest.TestCase):
    def test_moves_question_first_and_preserves_evidence(self):
        chapters = []
        for number in range(1, 9):
            chapters.append(
                f"# ARC A{number:02d} — title {number}\n\n"
                f"## Complément V3 — Contexte\n\nMais Cette passe ajoute une correction centrale. Texte [SOURCE-{number}].\n\n---\n\n"
                f"**Question causale : question {number} ?**\n\n## TL;DR\n\nRésumé {number}.\n\n"
                f"### HIL-01 — Suite\n\nCorps {number}.\n"
            )
        source = "# Méthode de lecture\n\n" + "\n".join(chapters) + "\n# Synthèse — fin\n"
        output = materialize(source)
        self.assertEqual(8, output.count("# Chapitre "))
        self.assertNotIn("## TL;DR", output)
        self.assertNotIn("Complément V3", output)
        self.assertNotIn("### HIL-01", output)
        self.assertNotIn("Mais Cette passe ajoute", output)
        for number in range(1, 9):
            section = output.split(f"# Chapitre {number} —", 1)[1]
            nonempty = [line for line in section.splitlines() if line.strip()]
            self.assertTrue(nonempty[1].startswith("**Question causale :"))
            self.assertIn(f"[SOURCE-{number}]", section)


if __name__ == "__main__":
    unittest.main()
