# QA log

## Core regression history
- original executable-OS cycle: RED then GREEN;
- provenance review cycle: RED 13/3 failures then GREEN;
- Run-2 Jaffna/storytelling cycle A: RED `32107479318` (18 tests / 5 expected failures), GREEN `32107998725`;
- Run-2 review cycle B: RED `32108098907`, GREEN `32108190963`.

## Current CI gates
```bash
python -m unittest discover -s tests -v
python scripts/audit_skill.py .
python scripts/qa_project.py examples/sri_lanka_pre_1948
python scripts/qa_project.py examples/sri_lanka_post_1948
```

## QA coverage
Deterministic project QA rejects malformed/duplicate source metadata, unsourced A/B causal drivers or amplifiers, unknown source references, invalid confidence/tier/zoom values, duplicate claim IDs, orphan bridges, and resolved A/B bridges without valid provenance.

The skill audit validates required files, trigger-oriented frontmatter and root-orchestrator size. Run-2 tests additionally validate reader-contract storytelling, two-axis source handling, materialized site inventory, dual Sri Lanka project artefacts, exact academic provenance and current institutional anchors.

## Merge gate
No Run-2 merge until the PR is mergeable and the final CI — including both example-project QA commands — is GREEN.
