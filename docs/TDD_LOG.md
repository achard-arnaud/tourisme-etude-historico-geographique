# TDD log

## Cycle 1 — RED
Baseline: root `SKILL.md` + `README.md` + graph-light decision only.

Command run locally against the baseline:

```bash
python -m unittest discover -s tests -v
```

Observed result: **8 tests, 8 failures**.

Expected failures:
- no sub-skill tree;
- no templates;
- no executable project scripts;
- root skill description not optimized for `Use when...` discovery;
- root orchestrator does not reference required sub-skills;
- project QA behavior absent.

This is the intentional RED state required before implementation.
