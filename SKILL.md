---
name: tourisme-etude-historico-geographique
description: Use when a travel, site-visit, country-reading, or historical research task needs a long-duration causal account that connects field evidence, chronology, geography, institutions, economy, culture, society, and regional systems.
---

# Tourisme étude historico-géographique

## Core principle
Build **arc-first**: rupture → claims → source anchors → bridges → drift audit → wiki/graph → side-story composition → readable synthesis. Promote only stabilized claims. A side story is composition, never new historical proof.

## State checkpoint
At the start/end of substantial runs distinguish:
1. **research** — notes/sources/claims/bridges/drifts/wiki/graph;
2. **composition** — validated `side_story` records and placement lineage;
3. **canonical Markdown** — last promoted manuscript;
4. **reader export** — Word/PDF;
5. branch/commit/QA and next promotion decision.

## Orchestration
See `docs/skill_workflow_index.md` for contracts and artefacts.
1. Capture with `capturing-field-evidence`.
2. Type raw statements with `sanitizing-historical-claims`.
3. Create rupture-bounded periods with `structuring-chronological-arcs`.
4. Apply `zooming-geographic-scales` from Z0 site to Z4 systemic.
5. Anchor with `sourcing-historical-anchors`.
6. Dispatch only relevant HIL analysis skills: institutions/power, geography/environment, economy/infrastructure, society/demography, religion/culture/legitimacy, security/geopolitics.
7. Use `building-causal-bridges` only for missing mechanisms that change the explanation.
8. Run `auditing-historiography-and-drifts`.
9. Store reusable knowledge with `maintaining-wiki-and-graph`.
10. Route useful off-trunk material through `composing-side-stories`; every validated/promoted item has lineage, placement and return-to-trunk. `dezoom` additionally needs scale mechanism and local payoff.
11. Structure canonical Markdown with `editing-historical-travel-output`, consuming validated side stories with normalized labels/markers.
12. Render with `storytelling-historical-travel` only non-destructively for advanced readers; it **must never set a maximum length** and required promoted side stories must survive.
13. Record every dispatched/skipped skill with reasons and artefact paths in the run manifest.
14. Re-run checkpoint and promote only after verification.

## Prompt-review loop
Treat user directions as requirements, not historical evidence. Extract new questions, rejected framings, desired depth, side-story requests, comparator requests and output-state changes; route each to the proper contract before changing canonical prose.

## Causal / side-story gate
A detail enters the causal trunk only if it materially changes resource mobilisation, legitimacy/coalition, governing/defence costs, access to flows/opportunities, social reproduction, or a regime/centre shift. Useful material that fails this gate may become a **candidate side story** (`detour`, `dezoom`, `also`, `method`, `false_lead`, `portrait`, `object_focus`, `comparator`, `callback`) after its evidence is sanitized/sourced. Otherwise keep it backlog or discarded lead. Never promote from raw prompts/field notes.

## Comparative gate
A comparator enters the spine only when mechanism, period, scale/unit, confounders and source coverage are compatible and it changes the home-case interpretation. Otherwise route it as a bounded `comparator` side story or remove it.

## Evidence contract
Tier sources T0–T5 separately from anchor role. Confidence is A/B/C/D/U. Major causal claims require independent corroboration unless explicitly bounded. Side-story lineage does not upgrade evidence confidence.

## Modes
**Field** capture; **Research** source/bridge/audit; **Composition** classify/validate side stories; **Synthesis** integrate chronology; **Modern** apply freshness; **Promotion** freeze evidence, validate composition, promote Markdown, regenerate readers.

## Verification
```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/audit_skill.py .
python scripts/audit_workflow.py docs/RUN10_SIDE_STORIES_MANIFEST.json
python scripts/qa_project.py <project>
```
When wiki/graph or side stories exist, QA validates provenance, lineage and reader-retention contracts. No completion claim without fresh verification.
