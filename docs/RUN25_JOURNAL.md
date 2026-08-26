# Run 25 — journal

> Artefact backstage append-only. Les scripts `run_journal.py`, `build_heat_map.py` et `reciprocal_coverage_check.py` ajoutent de nouvelles entrées ; les entrées existantes ne sont jamais réécrites. Ce contenu ne doit jamais être rendu dans le reader.

## Étape 1 — 2026-08-27 — Séparation process / voix
- artefacts touchés : `skills/storytelling-historical-travel/SKILL.md`, `skills/storytelling-historical-travel/references/paragraph_review_checklist.md`
- déclencheur : spécification Run 25 storytelling — process et voix narrative
- cohérence croisée : OK au niveau contrat — backstage explicitement exclu du frontstage ; brique d'embedding image laissée hors scope

## Étape 2 — 2026-08-27 — Artefacts de transition L0
- artefacts touchés : `scripts/run_journal.py`, `scripts/build_heat_map.py`, `scripts/reciprocal_coverage_check.py`
- déclencheur : manque de contrôle graphe ↔ sommaire ↔ couverture entre scaffold et drafting
- cohérence croisée : contrôle réciproque protège le legacy non instrumenté (`coverage_unknown_legacy`) au lieu de le déclarer artificiellement inutilisé ; densité = warning uniquement

## Étape 3 — 2026-08-27 — Gate paragraphe et fixtures
- artefacts touchés : `scripts/paragraph_review_gate.py`, `tests/test_run25_paragraph_review_gate.py`
- déclencheur : besoin d'un contrat de relecture forme + fond avec tests positifs et négatifs
- cohérence croisée : en attente de CI — règles déterministes séparées des revues sémantiques ciblées (ton / legacy sans canonical_points)
