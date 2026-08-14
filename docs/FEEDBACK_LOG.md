# Feedback / review log

## Review pass 1
Scope: second-pass hardening against the requested agentic OS and the `requesting-code-review` discipline from `obra/superpowers`.

### Important findings
1. **Deep artefact tree was descriptive, not executable.** README/root skill described ARC×HIL×ZOOM but `new_project.py` only created top-level folders.
2. **No arc constructor.** There was no deterministic way to create a chronological arc with its HIL and geographic zoom structure.
3. **Bridge integrity was unchecked.** QA could accept a bridge referring to nonexistent claims.

### Minor findings
- source tiers should be validated mechanically;
- root README should reference only paths that actually exist;
- skill descriptions should remain trigger-only and concise.

## Fine-tuning actions
- added `scripts/new_arc.py`;
- `new_project.py` now scaffolds all eight top-level HIL views;
- each arc gets 8 HIL × 5 zoom directories plus claims/evidence and a drift artefact;
- `qa_project.py` rejects orphan bridges and invalid source tiers;
- README references were sanitized;
- root orchestrator remains <650 words and sub-skills are loaded by name, not forced paths.

No separate reviewer agent was available in this runtime; the review was therefore performed as an explicit requirements/diff pass and recorded here rather than represented as independent-agent feedback.
