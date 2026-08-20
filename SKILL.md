---
name: tourisme-etude-historico-geographique
description: Use when a travel, site-visit, country-reading, or historical research task needs a long-duration causal account that connects field evidence, chronology, geography, institutions, economy, culture, society, and regional systems.
---

# Tourisme étude historico-géographique

## Core principle
Build **arc-first**: rupture → claims → source anchors → bridges → drift/bias audit → wiki/graph → readable synthesis. Promote only stabilized claims. Never confuse new research, integrated Markdown and reader exports.

## State checkpoint — mandatory on long projects
At the start and end of every substantial run, state internally and persist when useful:
1. **research layer** — notes/sources/claims/bridges/drifts;
2. **canonical Markdown layer** — last promoted reading manuscript;
3. **reader-export layer** — Word/PDF or other formatted edition;
4. branch/commit/QA status and next promotion decision.

If the user asks “where did we stop?”, answer from this checkpoint rather than reconstructing from prose memory.

## Orchestration
Per-step artifact and template are indexed in `docs/skill_workflow_index.md`.
1. Capture with `capturing-field-evidence`.
2. Separate fact, claim, inference, tradition, analogy, comparator and counterfactual with `sanitizing-historical-claims`.
3. Create rupture-bounded periods with `structuring-chronological-arcs`; allow vertical themes to cross arcs without replacing chronology.
4. Apply `zooming-geographic-scales` from Z0 site to Z4 global; normalize the scale before cross-country comparison.
5. Anchor and cross-check with `sourcing-historical-anchors`.
6. Dispatch only relevant HILs:
   - `analyzing-institutions-and-power`
   - `analyzing-geography-and-environment`
   - `analyzing-economy-and-infrastructure`
   - `analyzing-society-and-demography`
   - `analyzing-religion-culture-legitimacy`
   - `analyzing-security-and-geopolitics`
7. Use `building-causal-bridges` only for missing mechanisms that change the explanation.
8. Run `auditing-historiography-and-drifts`, including comparator and success/failure narratives.
9. Store durable cross-arc knowledge with `maintaining-wiki-and-graph`.
10. Structure the chronological manuscript with `editing-historical-travel-output`.
11. Preserve the complete promoted baseline, then render for the reader. For an advanced consolidation, `storytelling-historical-travel` is optional and may tune voice or navigation only after a quantitative retention gate; it must never set a maximum length or replace the source manuscript with a delta.
12. Record dispatched and skipped skills with reasons and artefact paths in a run manifest.
13. Re-run the state checkpoint and promote outputs only after verification.

## Prompt-review loop
For multi-session projects, periodically review recent user directions as **requirements**, not as historical evidence. Extract: new questions, rejected framings, desired depth, output-state expectations, comparator requests and operating protocols. Route each change to the relevant skill, artefact or backlog. Do not silently change the canonical narrative merely because a hypothesis appeared in a prompt.

## Causal gate
A detail enters the main trunk only if it materially changes resource mobilisation, legitimacy/coalition, governing/defence costs, access to flows/opportunities, social reproduction, or a regime/centre shift. Otherwise keep it as evidence, side-box, comparator, backlog or discarded lead.

## Comparative gate
A comparator enters the causal spine only when:
- the same mechanism is defined on both sides;
- scale, period and unit of analysis are compatible or explicitly bounded;
- major confounders are named;
- each side has adequate anchors;
- the comparison changes the interpretation of the home case.
Never infer “better society”, “more caste”, “more modern”, or a growth cause from a single policy difference.

## Evidence contract
Sources are tiered by epistemic role: T0 primary/material, T1 academic, T2 institutional synthesis, T3 navigation/encyclopedia, T4 field mediation, T5 exploratory. Separately assign an anchor role. Confidence is A established, B solid/qualified, C hypothesis, D false/indirect lead, U unresolved. Major causal claims require independent corroboration unless explicitly bounded.

## Modes
- **Field:** capture/route and respect short acknowledgement protocols.
- **Research:** anchor, cross-check, bridge, compare, audit, update.
- **Synthesis:** remove duplication and integrate side-notes in place.
- **Modern:** retain HIL/zoom logic while using current institutional/economic anchors and freshness checks.
- **Promotion:** freeze evidence, run QA, promote Markdown, then regenerate reader exports deliberately.

## Verification
Before any completion or merge claim run fresh:
```bash
pip install -r requirements.txt
python -m unittest discover -s tests -v
python scripts/audit_skill.py .
python scripts/audit_workflow.py docs/RUN6_WORKFLOW_MANIFEST.json
python scripts/qa_project.py <project>
```
When wiki/graph artefacts exist, QA must validate their metadata, source references and causal-edge provenance. No completion claim without fresh verification output.
