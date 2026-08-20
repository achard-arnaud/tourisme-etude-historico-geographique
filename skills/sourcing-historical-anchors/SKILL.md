---
name: sourcing-historical-anchors
description: Use when a historical claim, chronology, place, institution, economic mechanism, current comparison, or causal relation needs reliable anchoring and source-role decisions.
---

# Sourcing historical anchors

Use two axes. **Tier** describes how knowledge was produced: T0 primary/material, T1 academic, T2 institutional synthesis, T3 navigation/encyclopedia, T4 field mediation, T5 exploratory. **Anchor role** describes use in this investigation: canonical anchor, specialist institutional anchor, corroborating bridge, or lead.

A specialist institutional anchor remains T2; co-production by archaeology departments, UNESCO, museums, embassies, development banks or foundations does not turn it into T1. A narrow T1 paper can be excellent for one mechanism but poor as a general synthesis.

## Claim-to-source fit
For each source note record tier, anchor role, date, author/institution, scope, claim supported, limitations, provenance and whether the origin was directly fetched or only discovered through an index/cache. Major causal claims should normally have independent corroboration.

## Comparative sourcing
Before using a statistic across cases, align time window, denominator, administrative level, definition/method, monetary basis and conflict exposure. If alignment fails, use the source qualitatively and state the limit.

## Current-data freshness
Current office-holders, programmes, laws, budgets, rankings and economic indicators require a dated current source. Distinguish official statistical output, programme/press-release claims and political/promotional claims.

Wikipedia/search snippets may navigate but should not close contested causal claims. Field panels may be promoted to their underlying curated/academic source while the photo remains T4.

## Side-story handoff
A side story may reference source IDs directly when the source is itself the object/microhistory, but the `side_story` never upgrades tier, anchor role or confidence. Prefer lineage through stabilized claims where available. `portrait` and `object_focus` need especially tight scope control: one biography, panel or object cannot stand for a population without separate evidence.

## Output
A source-note entry per anchor (`templates/source-note.md`) appended to `05_sources/source_register*.json`, carrying tier, anchor role, scope and limitations so QA can validate claims, bridges, wiki/graph and side-story lineage.

See also: `SKILL.md` orchestration step 5; `composing-side-stories`; `docs/skill_workflow_index.md`.
