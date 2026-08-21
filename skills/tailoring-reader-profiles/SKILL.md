---
name: tailoring-reader-profiles
description: Use when the same historical corpus must deterministically select side stories, arc recaps, maps and narrative templates for different reader audiences.
---

# Tailoring reader profiles

Use versioned `reader_profile` artefacts. `content_temperature` is content density/variety (1–5), not model sampling temperature. It controls deterministic eligibility and ordering of side stories, recap style and map use.

All profiles enumerate every side-story kind including `analytical_focus`. `historian_enthusiast` keeps it near the front because it preserves causal/methodological complexity. `child_10_plus` also keeps it, but after people/objects/anecdotes and before the most abstract method/comparator material; the child template decomposes the same evidence into concrete steps. `educated_generalist` may include analytical focus selectively when its payoff is high enough to justify 1–2 page density.

Resolve a reader plan with `scripts/resolve_reader_plan.py`; storytelling consumes the plan and cannot silently override eligibility or evidence status.
