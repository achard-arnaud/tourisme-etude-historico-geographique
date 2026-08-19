---
name: maintaining-wiki-and-graph
description: Use when stabilized claims, people, places, institutions, commodities, policies, sources, or repeated relationships need reusable cross-arc storage without duplicating prose.
---

# Maintaining wiki and graph

The wiki stores durable entities; arcs store temporal context; HILs store analytic views. The graph stores typed relations, not a second narrative.

## Promotion gate
Promote an entity or relation when it is reused across arcs or resolves repeated ambiguity. Prefer A/B claims; a C item may appear only with explicit hypothesis status. Do not copy raw field notes into the wiki as settled facts.

## Wiki entity contract
Each entity page should contain:
- stable `slug` and canonical name;
- entity type and aliases;
- scope / why reusable;
- concise durable description;
- related arcs and claim IDs;
- source IDs;
- confidence and material limits;
- `last_reviewed` date.
Aliases must redirect conceptually to one canonical slug; do not fork duplicate pages for spelling variants.

## Graph-light contract
Use typed relations such as `CAUSES`, `AMPLIFIES`, `ENABLES`, `CONSTRAINS`, `LOCATED_IN`, `LEGITIMIZES`, `CONTESTS`, `MIGRATES_TO`, `TRADES_WITH`, `SOURCES`, `CONTRADICTS`, `REFINES`, `REDISTRIBUTES_ACCESS_TO`, `EXTERNALIZES_TO`, `COMPARES_WITH`.

Every edge records `from`, `relation`, `to`, `confidence`, `source_ids`, optional `claim_ids`, and `last_reviewed`. Causal/interpretive edges require provenance. Descriptive identity/location edges may use an empty source list only when trivially structural and QA permits it.

## Lifecycle
After a substantial research run:
1. update entities touched by stabilized claims;
2. add/remove graph edges;
3. flag contradictions rather than overwriting silently;
4. run duplicate-slug and unknown-source QA;
5. save a project checkpoint identifying wiki/graph freshness.

## Output
Wiki entity pages (`templates/wiki-entity.md` → `03_wiki/**/*.md`) and typed graph edges (`04_graph/*.jsonl`), both validated by `scripts/qa_project.py`.

See also: `SKILL.md` orchestration step 9; `docs/skill_workflow_index.md`.
