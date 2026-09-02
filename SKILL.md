---
name: tourisme-etude-historico-geographique
description: Use when a travel, site-visit, country-reading, or historical research task needs a long-duration causal account connecting field evidence, chronology, geography, institutions, economy, culture, society, and regional systems.
---

# Tourisme étude historico-géographique

## Core principle
Build **arc-first**: evidence → typed claims → source anchors → HIL analysis → bridges/drifts → wiki/graph → composition artefacts → canonical manuscript → reader plan/export. Composition never creates historical proof.

## State checkpoint
Track separately: research; composition (`side_story`, `arc_recap`, `map_asset`, `illustration`); canonical Markdown resolved by `00_method/output_state.json`; reader export; branch/commit/QA. Never infer canonical state from a filename.

## Orchestration
0. `extracting-youtube-evidence` → timestamped video ledgers and lead-only propositions; no direct factual promotion.
1. `capturing-field-evidence` → raw observations.
2. `sanitizing-historical-claims` → statement type.
3. `structuring-chronological-arcs` → rupture-bounded spine.
4. `zooming-geographic-scales` → Z0–Z4 transmission.
5. `sourcing-historical-anchors` → source tier/role.
6. Dispatch relevant HIL owners: `analyzing-institutions-and-power`, `analyzing-geography-and-environment`, `analyzing-economy-and-infrastructure`, `analyzing-society-and-demography`, `analyzing-religion-culture-legitimacy`, `analyzing-security-and-geopolitics`, `analyzing-regional-global-systems`; HIL-08 is owned by `auditing-historiography-and-drifts`.
7. `building-causal-bridges` only for missing mechanisms.
8. `auditing-historiography-and-drifts` for bias/non-cause/source corrections.
9. `maintaining-wiki-and-graph`; **all graph fragments must resolve before an editing run**.
10. `composing-side-stories` for useful off-trunk material; validated/promoted records require lineage and resolvable placement. `method` is self-contained and must not fabricate `return_to`; narrative kinds do.
11. `composing-arc-recaps` creates the causal end-of-arc schema, protagonist viewpoints and `prepares_next` bullets.
12. `curating-historical-map-assets` searches only for arcs or map-eligible side stories; vision review precedes explicit human approval.
12b. `curating-historical-illustrations` registers field photos or other images as `illustration` composition assets, links them to existing inputs, preserves depiction semantics and never upgrades claim confidence.
13. `tailoring-reader-profiles` resolves deterministic content temperature, side-story ordering, recap style and approved-map selection.
14. `editing-historical-travel-output` consumes the graph/composition preflight and structured artefacts; deterministic side-story insertion uses `materialize_side_stories.py`. When the active storytelling contract declares a **form-global** change, editing must treat every paragraph in the selected arc/chapter span as review-eligible rather than limiting the pass to new delta text.
15. `storytelling-historical-travel` first consumes the compact global `story_scaffold.json`, then the resolved reader plan and arc-local retrieval packs. For advanced readers it **must never set a maximum length** or silently drop required content; no more than one approved map per subsection/side-story slot. It must also consume `skills/storytelling-historical-travel/PROBLEM_FIRST_CAUSAL_DEZOOM_CONTRACT.md`: frame major sections by a bounded problem, narrate event/object/local mechanism before consequence and causal dezoom, keep analytically necessary scale changes in the core, apply the 360 viewpoint and intent→instrument→friction→adaptation→unintended-effect checks, and treat run numbers as provenance rather than reader topology. A form-global storytelling change invalidates prior paragraph-shape approval inside the selected scope while preserving factual/evidentiary approval: the iterative pass must reread and may restructure **all** paragraphs in scope. After reader rendering, it performs a dedicated illustration pass, reconciles every scaffold queue, and only then performs the final reread.
16. Record all routing in the latest reviewed run manifest and promote only after fresh verification.

## Prompt-review loop
Treat user directions as requirements, never evidence. Route new questions, rejected framings, audience changes, side-story/map/illustration requests and output-state changes to their owning contracts before prose changes.

## Causal / composition gate
A detail enters the trunk only if it changes mobilisation, legitimacy/coalition, governing/defence cost, flows/opportunity, social reproduction, or regime/centre. Otherwise: candidate `side_story`, backlog or discarded lead. `arc_recap` only summarizes stabilized claims/bridges. `map_asset` and `illustration` may clarify a validated story but never upgrade confidence.

## Comparative gate
A comparator enters the spine only when mechanism, period, scale, unit, confounders and source coverage align and it changes the home case. Otherwise use a bounded comparator side story.

## Verification
```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/audit_skill.py .
python scripts/audit_workflow.py --latest
python scripts/audit_context_budget.py --latest
python scripts/qa_project.py <project>
python scripts/qa_composition_pipeline.py <project>
```
File length is not a proxy for context safety: the budget applies to orchestrator + actually dispatched skills.
