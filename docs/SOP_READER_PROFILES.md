# SOP — Reader profiles and content temperature

`content_temperature` is a deterministic content-selection dimension, not an LLM sampling parameter.

- 1–2: trunk-first, very few eligible side stories.
- 3: balanced generalist.
- 4–5: high side-story density and richer callbacks/comparators.

Presets are versioned in `reader_profiles/`. `historian_enthusiast` and `child_10_plus` both use `coverage_mode=all`; their priority orders and storytelling templates differ. Run `resolve_reader_plan.py` before storytelling. The resulting plan controls side-story order, recap inclusion and approved map selection.
