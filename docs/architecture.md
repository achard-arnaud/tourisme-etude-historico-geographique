# Architecture

The root skill is an orchestrator. Sixteen sub-skills own judgment-heavy methods; scripts enforce mechanical invariants. Project artefacts are split by chronological arc, analytic HIL, reusable wiki entities, graph relations, source registers, bridges, drift audits, questions and output.

The system is deliberately **arc-first, Zettelkasten-lite, graph-light**: chronology remains the human reading spine; vertical themes reactivate where they change an arc; the wiki prevents entity duplication; the graph stores only typed, sourced relations needed for cross-arc reasoning.

## Long-project state machine
Three output layers are independent:
1. **research** — raw/processed evidence, sources, claims, bridges, drifts, wiki, graph;
2. **canonical Markdown** — deliberately promoted synthesis;
3. **reader export** — Word/PDF or other formatted edition.

State transitions are explicit: `captured → researched → integrated/vnext → promoted/canonical → reader-export`. A field or research run may advance one layer without advancing the next.

## Comparative architecture
Comparators remain attached to a home arc. The system normalizes the institutional/geographic unit and asks what can travel from one case to another:
- instrument;
- mechanism;
- institutional package;
- outcome.

The farther right the comparison moves, the stronger the confounder and evidence burden. Province, federated state, peninsula and sovereign country are never treated as equivalent containers by default.

## Knowledge layer
`03_wiki/` stores durable reusable entities with slug, type, confidence, sources, related claims, limits and review date. `04_graph/*.jsonl` stores typed edges with provenance and confidence. Raw field notes and unresolved analogies stay outside the wiki.

## Source scalability
A project may contain several `05_sources/source_register*.json` files. Source IDs remain globally unique within the project. Modular registers allow new research runs to append bounded source families without repeatedly rewriting one monolithic registry.

## Deterministic QA
`qa_project.py` validates:
- source tiers and duplicate IDs across modular registers;
- claim confidence/zoom/source references;
- bridge closure, claim endpoints and provenance;
- wiki frontmatter, unique slugs, review dates and source references;
- graph JSONL structure, confidence and provenance for interpretive edges.

Judgment remains in skills; structural integrity is enforced mechanically.
