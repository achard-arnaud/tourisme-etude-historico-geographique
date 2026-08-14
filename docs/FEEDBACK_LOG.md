# Feedback / review log

## Review pass 1
Scope: second-pass hardening against the requested agentic OS and the `requesting-code-review` discipline from `obra/superpowers`.

### Important findings
1. **Deep artefact tree was descriptive, not executable.** README/root skill described ARC×HIL×ZOOM but `new_project.py` only created top-level folders.
2. **No arc constructor.** There was no deterministic way to create a chronological arc with its HIL and geographic zoom structure.
3. **Bridge integrity was unchecked.** QA could accept a bridge referring to nonexistent claims.

### Fine-tuning actions
- added `scripts/new_arc.py`;
- `new_project.py` scaffolds all eight top-level HIL views;
- each arc gets 8 HIL × 5 zoom directories plus claims/evidence and a drift artefact;
- `qa_project.py` rejects orphan bridges and invalid source tiers;
- README references were sanitized.

## Review pass 2 — PR #3
Formal PR review after the first green CI identified two additional provenance defects:
1. malformed `source_register.json` was silently converted to an empty register;
2. A/B bridges could be accepted without source IDs or with unknown source IDs.

### TDD response
Three tests were committed first. GitHub Actions confirmed exactly three expected failures. The implementation then made malformed registers explicit QA errors and applied source validation to resolved bridges.

## Reviewer independence note
No separate reviewer-agent runtime was available. Review pass 1 was an explicit requirements/diff review; review pass 2 was submitted as a GitHub PR review and then verified by test-only RED + CI GREEN evidence. It is not represented as independent human review.
