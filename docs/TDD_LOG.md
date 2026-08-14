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

Added tests first. Observed locally:
```text
Ran 10 tests
FAILED (failures=3)
```

### GREEN
Implemented deep arc scaffolding and bridge/source-tier QA. Observed locally:
```text
Ran 10 tests
OK
SKILL AUDIT OK
```

## Cycle 3 — PR review: provenance integrity
### RED
PR review found that malformed source registers were silently accepted and resolved bridges could be unsourced or cite unknown sources. Three tests were added before implementation.

GitHub Actions run `31787289210` on test-only commit `64af3cb` proved RED:
```text
Ran 13 tests
FAILED (failures=3)
```
The three failures matched the intended missing behaviors exactly.

### GREEN
`qa_project.py` now treats malformed/duplicate source metadata as errors and applies provenance checks to resolved bridges. Final GREEN is established by the subsequent CI run recorded in `QA_LOG.md`.
