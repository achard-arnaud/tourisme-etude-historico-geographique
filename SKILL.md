---
name: tourisme-etude-historico-geographique
description: Use when a travel, site-visit, country-reading, or historical research task needs a long-duration causal account that connects field evidence, chronology, geography, institutions, economy, culture, and regional systems.
---

# Tourisme étude historico-géographique

## Core principle
Build **arc-first**: rupture → claims → source anchors → bridges → drift/bias audit → readable synthesis. Promote only stabilized claims into the wiki/graph layer.

## Orchestration
1. Capture with `capturing-field-evidence`.
2. Separate fact, claim, inference, tradition and analogy with `sanitizing-historical-claims`.
3. Create rupture-bounded periods with `structuring-chronological-arcs`.
4. Apply `zooming-geographic-scales` from Z0 site to Z4 global.
5. Anchor and cross-check with `sourcing-historical-anchors`.
6. Dispatch relevant analytical dimensions only:
   - `analyzing-institutions-and-power`
   - `analyzing-geography-and-environment`
   - `analyzing-economy-and-infrastructure`
   - `analyzing-society-and-demography`
   - `analyzing-religion-culture-legitimacy`
   - `analyzing-security-and-geopolitics`
7. Use `building-causal-bridges` only for necessary missing mechanisms.
8. Run `auditing-historiography-and-drifts` before synthesis.
9. Store stable cross-arc knowledge with `maintaining-wiki-and-graph`.
10. Structure the chronological reading edition with `editing-historical-travel-output`.
11. Render the final reader-facing narrative with `storytelling-historical-travel`, using an explicit reader contract for audience, language, tone, register and length budget.

## Causal gate
A detail enters the main trunk only if it changes resource mobilisation, legitimacy/coalition, the cost of governing/defending space, access to flows, or a regime/centre shift. Otherwise keep it as evidence, side-box, analogy, backlog or discarded lead.

## Standard analytical layers
Use up to eight HILs per arc: institutions/chronology; geography/environment; economy/infrastructure; society/demography; religion/culture/legitimacy; security/coercion; regional/global system; historiography/bias. Empty layers may be intentional.

## Evidence contract
Sources are tiered by epistemic role: T0 primary/material, T1 academic, T2 institutional synthesis, T3 navigation/encyclopedia, T4 field mediation, T5 exploratory. Separately assign an anchor role: canonical anchor, specialist institutional anchor, corroborating bridge, or lead. Prestige never promotes T2 material into T1. Confidence is A established, B solid/qualified, C hypothesis, D false/indirect lead, U unresolved. Major causal claims require independent corroboration unless explicitly bounded.

## Modes
- **Field:** capture/route and respect short acknowledgement protocols.
- **Research:** anchor, cross-check, bridge, audit, update.
- **Synthesis:** remove duplication/pollution and integrate side-notes in place.
- **Modern:** retain the same HIL/zoom logic while substituting modern institutional and economic anchors.

## Verification
Before delivery run:
```bash
python -m unittest discover -s tests -v
python scripts/audit_skill.py .
python scripts/qa_project.py <project>   # when a project corpus exists
```
No completion claim without fresh verification output.
