---
name: composing-arc-recaps
description: Use when a stabilized chronological arc needs an end-of-arc causal schema, protagonist viewpoints, and a concise bridge or teaser toward the next arc.
---

# Composing arc recaps

Create one `arc_recap` for every materialized arc before final editing. Reuse claims/bridges; never create new evidence. Summarize drivers, amplifiers, constraints and consequences, then show each major protagonist’s objective, constraints and perceived options only where sourced.

Finish with a few `prepares_next` bullets: what the arc makes possible, fragile or newly costly in the next age. These are causal teasers, not suspense devices. Store under `09_output/arc_recaps/` and validate with `arc_recap_contract.py`.

Every validated/promoted recap required in a reader declares `placement.before_anchor`, the stable heading that starts the next arc/section. The validator resolves that anchor against state-resolved canonical Markdown. `materialize_arc_recaps.py` renders the recap deterministically from JSON and is idempotent: rerunning replaces its own marker-delimited block rather than duplicating prose.

Editing may simplify phrasing for the selected reader profile, but must first update the structured recap; it must never hand-copy a divergent recap or alter the causal graph without changing lineage.
