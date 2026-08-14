# QA log

## Local verification before PR fine-tuning
```bash
python -m unittest discover -s tests -v
python scripts/audit_skill.py .
```
Result before review refinement: **10/10 tests pass**, `SKILL AUDIT OK`.

## TDD / GitHub CI evidence
- dev commit `91e3f42`: GREEN push CI;
- PR #3 on `91e3f42`: GREEN pull-request CI;
- test-only refinement commit `64af3cb`: RED by design, **13 tests / 3 expected failures**;
- implementation commit `d9c330d`: GREEN PR CI run #8; test step + skill audit both passed;
- merged `main` commit `48668d4`: GREEN push CI run #9.

## Delivery state
- PR #3 merged to `main`;
- issue #2 automatically closed as completed;
- `main` and `dev` synchronized to `48668d4953ac1db8f5f89866da4d4e3661293663` after merge;
- compare `main...dev`: identical, ahead 0 / behind 0.

## QA coverage
The deterministic project QA rejects:
- malformed source registers and duplicate/invalid source metadata;
- unsourced A/B causal drivers/amplifiers;
- unknown source references;
- invalid confidence, source-tier and zoom values;
- duplicate claim IDs;
- orphan bridges;
- resolved A/B bridges without source evidence or with unknown source IDs.

The skill audit validates required files, trigger-oriented skill frontmatter and root-orchestrator size.
