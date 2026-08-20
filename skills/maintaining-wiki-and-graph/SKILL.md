---
name: maintaining-wiki-and-graph
description: Use when stabilized claims, people, places, institutions, commodities, policies, sources, or repeated relationships need reusable cross-arc storage without duplicating prose.
---

# Maintaining wiki and graph

The wiki stores durable entities; arcs store temporal context; HILs store analytic views. The graph stores typed relations, not a second narrative.

## Promotion gate
Promote an entity/relation when reused across arcs or resolving repeated ambiguity. Prefer A/B claims; C appears only with explicit hypothesis status. Do not copy raw field notes into the wiki as settled facts.

## Wiki / graph contracts
Wiki pages carry stable slug/name, entity type/aliases, scope, durable description, related arcs/claims, source IDs, confidence/limits and `last_reviewed`. Graph edges carry `from`, typed relation, `to`, confidence, source IDs, optional claim IDs and `last_reviewed`; interpretive edges require provenance.

## Side-story boundary
A `portrait`, `object_focus` or `callback` may reference wiki entities/graph relations for navigation, but side-story prose is not a new wiki fact or graph proof. Conversely, repeated side-story subjects should be promoted to wiki only when the underlying stabilized evidence meets the wiki gate. Do not create graph edges merely because two elements co-occur in a box.

## Lifecycle
After substantial research: update touched entities, add/remove edges, flag contradictions, run duplicate/source QA, and expose reusable IDs to downstream `composing-side-stories` without duplicating their evidence.

## Output
Wiki pages (`03_wiki/**/*.md`) and typed graph edges (`04_graph/*.jsonl`), both validated by `scripts/qa_project.py` and reusable as navigation context for composition.

See also: `SKILL.md` orchestration step 9; `composing-side-stories`; `docs/skill_workflow_index.md`.
