# TDD log

Method adapted from `obra/superpowers`: tests first, observe RED, implement minimum behavior, verify GREEN, then refactor.

## Cycle 1 — executable skill OS
### RED
Baseline contained only root `SKILL.md`, `README.md`, and the graph-light design note.

Command:
```bash
python -m unittest discover -s tests -v
```
Observed: **8 tests / 8 failures**.

Failures were expected: no sub-skill tree, templates, project scripts, discovery-optimized root description, or deterministic QA.

### GREEN
Implemented the orchestrator/sub-skill split, templates, project scaffolding, QA scripts and CI.

Observed locally:
```text
Ran 8 tests
OK
SKILL AUDIT OK
```

## Cycle 2 — feedback hardening: deep ARC×HIL×ZOOM + bridge integrity
### RED
Review identified that the architecture described deep HIL/zoom artefacts but did not materialize them, and that bridge references were not checked.

Added tests first.

Observed:
```text
Ran 10 tests
FAILED (failures=3)
```
Expected failures: missing `new_arc.py`, missing deep HIL/zoom scaffold, orphan bridge not rejected.

### GREEN
Implemented deep arc scaffolding and bridge/source-tier QA.

Observed locally:
```text
Ran 10 tests
OK
SKILL AUDIT OK
```
