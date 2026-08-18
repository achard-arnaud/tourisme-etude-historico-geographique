# QA log

## Core regression history
- original executable-OS cycle: RED then GREEN;
- provenance review cycle: RED 13/3 failures then GREEN;
- Run-2 Jaffna/storytelling cycle A: RED `32107479318` (18 tests / 5 expected failures), GREEN `32107998725`;
- Run-2 review cycle B: RED `32108098907`, GREEN `32108190963`;
- Run-5 comparative/wiki cycle: RED `32130754362`, GREEN `32130831894`.
- Run-6 storytelling/reader-export cycle: one local RED contract mismatch, then **34/34 GREEN** before publication.

## Run 5 RED → GREEN details
Initial Run 5 CI failed two unit contracts:
1. the geography skill had the correct scale logic but no longer exposed the exact `Comparison-scale gate` marker required by its contract test;
2. the institutions skill preserved intent/effect separation semantically but dropped the existing literal `distributional intent` marker.

Both were fixed in the skills rather than weakening the tests. Final run `32130831894`:
- **32/32 unit tests GREEN**;
- `python scripts/audit_skill.py .` — **GREEN**;
- pre-1948 QA — **9 claims, 20 sources, 3 wiki pages, 4 graph edges, 0 warnings**;
- post-1948 QA — **30 claims, 48 sources, 7 wiki pages, 10 graph edges, 0 warnings**.

## Run 6 RED → GREEN details
The Run 6 review encoded a historical-nonfiction safety contract before final packaging. The first complete local run found one exact mismatch: the skill prohibited fabricated dialogue semantically, while the test required the explicit phrase `invented dialogue`. The skill wording was made explicit; the test was not weakened.

Final local Run 6 gate:
- **34/34 unit tests GREEN**;
- `python scripts/audit_skill.py .` — **GREEN**;
- `python scripts/audit_workflow.py docs/RUN6_WORKFLOW_MANIFEST.json` — **16 dispatched, 0 skipped, 16 known skills**;
- pre-1948 QA — **9 claims, 37 sources, 3 wiki pages, 4 graph edges, 0 warnings**;
- post-1948 QA — **30 claims, 48 sources, 7 wiki pages, 10 graph edges, 0 warnings**;
- both DOCX archives and both PDF renderings verified; all 22 rendered pages inspected.

## Current CI gates
```bash
python -m unittest discover -s tests -v
python scripts/audit_skill.py .
python scripts/audit_workflow.py docs/RUN6_WORKFLOW_MANIFEST.json
python scripts/qa_project.py examples/sri_lanka_pre_1948
python scripts/qa_project.py examples/sri_lanka_post_1948
```

## QA coverage
Deterministic project QA rejects malformed source metadata, duplicate source IDs across modular `source_register*.json` files, unsourced A/B causal drivers or amplifiers, unknown source references, invalid confidence/tier/zoom values, duplicate claim IDs, orphan bridges, and resolved A/B bridges without valid provenance.

Run 5 extends deterministic checks to the knowledge layer:
- wiki frontmatter, unique slugs, confidence and `last_reviewed`;
- wiki source references;
- graph JSONL structure and confidence;
- provenance on interpretive/causal graph edges;
- unknown graph source IDs.

The skill audit validates required files, trigger-oriented frontmatter and root-orchestrator constraints. Run 5 tests additionally validate all 16 specialised skills, long-project state checkpoints, comparator gates, modular sources, wiki/graph materialisation, A13 comparative claims and drift audit.

Run 6 adds deterministic workflow evidence: a full-review manifest must name every known specialised skill, justify its dispatch and point to inputs and outputs. The new reader renderer is also part of the required repository contract.

## Merge gate
Run 6 is eligible for merge only after the branch CI is GREEN, followed by the promotion PR from `dev` to `main`. The final pull-request records are the authoritative remote merge evidence.
