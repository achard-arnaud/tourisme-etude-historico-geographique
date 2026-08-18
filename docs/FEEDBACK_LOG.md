# Feedback / review log

## Review pass 1
Second-pass hardening against the requested agentic OS found that deep artefacts were descriptive rather than executable, there was no deterministic arc constructor, and bridge integrity was unchecked. Actions: `new_arc.py`, 8 HIL × 5 zoom scaffolding, bridge/source validation, README sanitation.

## Review pass 2 — PR #3
Formal PR review found malformed source registers could be silently accepted and A/B bridges could be unsourced or cite unknown sources. Three tests were committed first; CI confirmed RED; QA was hardened and returned GREEN.

## Review pass 3 — Jaffna/VOC field run, 18 August 2026
The real-world run produced four design lessons.

### 1. Source quality is two-dimensional
The Stichting Nederland–Sri Lanka fort exhibition is unusually useful because of specialist authorship and collaboration with archaeology/heritage institutions. Yet it is still an institutional public synthesis. **Fix:** separate epistemic tier from anchor role. “Specialist institutional anchor” can be first-line for routing and vocabulary without pretending to be T1 scholarship.

### 2. Field evidence should promote to the underlying corpus
A photograph of a panel is T4. Once the exhibition and authorship are identified, the curated corpus becomes T2, while load-bearing claims still route to T0/T1. This avoids both under-valuing expert exhibitions and over-promoting them.

### 3. Structural editing and storytelling are different jobs
The previous output skill could order chapters and side boxes but could not reliably control audience, length, tone or cognitive load. **Fix:** retain `editing-historical-travel-output` for manuscript architecture and add `storytelling-historical-travel` as a final reader-rendering layer.

### 4. A source family can bridge periods without becoming causal pollution
The same Dutch-Sri Lankan heritage corpus improves the pre-1948 story through forts, labour and administration, and the post-1948 story through gentrification, restitution and memory. **Fix:** route modern heritage material to a bounded HIL and use the causal gate before admitting it to the main political/economic trunk.

## Fine-tuning request-for-feedback checklist
For future runs, inspect:
- Did an institutional source become over-promoted because it looked authoritative?
- Did a field panel’s rhetoric survive sanitization as fact?
- Did the final report preserve causal bridges while changing reader level?
- Does child mode remain historically honest rather than merely entertaining?
- Did cross-references reduce repetition or create a dependency maze?
- Did a new HIL enrich the causal model or merely add interesting material?

## Reviewer independence note
No separate human reviewer is implied. Reviews are explicit requirements/diff reviews recorded in GitHub and tested through RED/GREEN CI evidence.
