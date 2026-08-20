# Architecture

The root skill is an orchestrator. **Seventeen sub-skills** own judgment-heavy methods; scripts enforce mechanical invariants. Project artefacts are split by chronological arc, analytic HIL, reusable wiki entities, graph relations, source registers, bridges, drift audits, questions, **side-story composition**, and output.

The system is **arc-first, Zettelkasten-lite, graph-light, lineage-aware composition**: chronology remains the human reading spine; vertical themes reactivate where they change an arc; wiki/graph prevent duplication; side stories preserve useful off-trunk material without confusing it with evidence.

## Long-project state machine
Four durable layers are independent:
1. **research** — evidence, sources, claims, bridges, drifts, wiki, graph;
2. **composition** — `09_output/side_stories/*.json` with kind, lineage, placement and return-to-trunk;
3. **canonical Markdown** — deliberately promoted synthesis containing stable side-story markers;
4. **reader export** — Word/PDF or other formatted edition.

Research state follows `captured → researched → integrated`; side stories follow `candidate → validated → promoted → retired`; output follows `baseline → vnext → promoted/canonical → reader-export`. Advancing one layer never silently advances another.

## Side-story architecture
`side_story` is not a claim class. It references existing claim/source/bridge/HIL/drift/origin artefacts and controls **reader composition**. Nomenclature v1 is closed: `detour`, `dezoom`, `also`, `method`, `false_lead`, `portrait`, `object_focus`, `comparator`, `callback`.

Every validated/promoted record has one home arc, editorial purpose, off-trunk reason, payoff, placement and return point. `dezoom` additionally carries Z from/to/return, transmission mechanism and local payoff. Promoted reader-required records are guarded by stable Markdown markers and a renderer retention gate.

## Comparative architecture
Comparators remain attached to a home arc. If a comparison changes the main causal interpretation and passes scale/confounder gates it may enter the spine; otherwise it may be composed as a bounded `comparator` side story. Instrument/mechanism transport more readily than institutional package/outcome.

## Knowledge layer
`03_wiki/` stores reusable entities; `04_graph/*.jsonl` stores sourced typed relations. Side stories may reference them for navigation but do not become graph evidence merely by appearing together in prose.

## Source scalability
Several `05_sources/source_register*.json` files may coexist; IDs stay unique project-wide. Side-story lineage resolves against the same registry and never upgrades source tier/role.

## Deterministic QA
`qa_project.py` validates sources, claims, bridges, wiki, graph and side stories: schema/class/kind/status, evidence lineage, home/related arcs, HIL/zoom vocabulary, placement/return and canonical render labels/markers. The full-reader renderer independently blocks loss or relabelling of promoted `required_in_reader` side stories.

Judgment remains in skills; structural integrity and lineage survival are mechanical gates.
