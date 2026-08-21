# Architecture

The root skill orchestrates judgment-heavy skills while scripts enforce mechanical contracts. The system remains **arc-first + Zettelkasten-lite + graph-light**, with explicit output-state and a first-class composition layer.

## Layers
1. **Research** — field evidence, sources, typed claims, arcs/HILs, bridges, drifts, wiki/graph.
2. **Composition** — `side_story`, `arc_recap`, optional `map_asset`, and `reader_profile`/reader plan.
3. **Canonical Markdown** — path resolved from `00_method/output_state.json`, never inferred from `report.md` naming.
4. **Reader export** — DOCX/PDF generated only after preflight and retention gates.

## HIL ownership
HIL-01 institutions; HIL-02 geography; HIL-03 economy; HIL-04 society; HIL-05 religion/culture; HIL-06 security; **HIL-07 regional/global systems**; **HIL-08 historiography/bias**. HIL-07 now has a dedicated analysis skill; HIL-08 is owned by drift audit.

## Composition contracts
- `side_story`: normalized off-trunk narrative with lineage, placement, optional map eligibility and deterministic materialization.
- `arc_recap`: end-of-arc causal schema + protagonist viewpoints + what changed + next-arc teaser bullets.
- `map_asset`: optional online map candidate → vision validation → explicit human approval → dated fragment/caption; only approved assets are renderable.
- `reader_profile`: deterministic content temperature, story template, side-story selection/order, recap style and map rules.

## Pre-edit invariant
`graph_link_audit.py` resolves every graph edge endpoint. `qa_composition_pipeline.py` then resolves output state, side-story coverage/anchors, arc recaps, map lifecycle and reader profile, and writes `reader_plan.json`. Editing runs only after this gate.

## QA philosophy
No lexical-heading test substitutes for behavior. File-size limits do not proxy context safety: `audit_context_budget.py --latest` measures root orchestrator + actually dispatched skills. `audit_workflow.py --latest` resolves the highest reviewed run manifest automatically.
