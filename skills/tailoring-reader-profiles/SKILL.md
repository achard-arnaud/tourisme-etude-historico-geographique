---
name: tailoring-reader-profiles
description: Use when the same historical corpus must deterministically select side stories, arc recaps, maps and narrative templates for different reader audiences.
---

# Tailoring reader profiles

Use versioned `reader_profile` artefacts. `content_temperature` is **content density/variety (1–5), not model sampling temperature**. It controls deterministic eligibility and ordering of side stories, recap style and map use.

`historian_enthusiast` and `child_10_plus` both keep all side-story kinds, for different reasons: the historian keeps methodological/causal richness; the child profile prioritizes people, objects and anecdotes before the larger causal structure. `educated_generalist` is selective. Resolve a reader plan with `scripts/resolve_reader_plan.py`; storytelling consumes the plan and cannot silently override eligibility.
