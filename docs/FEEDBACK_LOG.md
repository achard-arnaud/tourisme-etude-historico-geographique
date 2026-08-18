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

## Review pass 4 — caste, mobility and Run 5 comparative development
The last project directions added five reusable product lessons.

### 1. Long projects need an explicit state checkpoint
A historically correct answer is insufficient if the user cannot tell whether material is only captured, fully researched, integrated into Markdown or already present in the formatted reader edition. **Fix:** root state checkpoint, field-session checkpoint, explicit `baseline → vnext → canonical → reader-export` lifecycle and `CURRENT_OUTPUT_STATUS.md`.

### 2. Social hierarchy belongs in the causal model without becoming a master cause
Caste, marriage, property, temple authority, education and diaspora can structure mobility while language, constitution and war remain the political spine. **Fix:** social-reproduction matrix, public/private persistence distinction, cleavage overlay and territorial/transnational reproduction.

### 3. “Success story” comparators require transportability gates
Tamil Nadu and Indonesia became useful only after separating policy instrument, mechanism, institutional package and outcome. **Fix:** comparator-scale normalization, explicit confounders and a transportability test. A comparator shows another route was possible; it does not prove what the home case would have become.

### 4. Human capital must be separated from territorial capture
A highly educated population can migrate and prosper while the origin territory loses firms, jobs, tax capacity and network spillovers. **Fix:** conversion-of-advantage chain and war-development channels across economy, geography, security and society skills.

### 5. Architecture claims must be operational
The repo described a wiki and graph-light layer, but the Sri Lanka worked examples had not materialized them. **Fix:** `03_wiki/` and `04_graph/edges.jsonl` are now real project artefacts and QA validates their metadata, sources and provenance.

## Fine-tuning request-for-feedback checklist
For future runs, inspect:
- Did an institutional source become over-promoted because it looked authoritative?
- Did a field panel’s rhetoric survive sanitization as fact?
- Did the final report preserve causal bridges while changing reader level?
- Does child mode remain historically honest rather than merely entertaining?
- Did cross-references reduce repetition or create a dependency maze?
- Did a new HIL enrich the causal model or merely add interesting material?
- Is the output-state checkpoint explicit enough to recover the project after a long pause?
- Is a comparator transporting only a mechanism, or silently importing a whole success narrative?
- Are programme targets being mistaken for observed outcomes?
- Is diaspora success being confused with development of the origin territory?

## Reviewer independence note
No separate human reviewer is implied. Reviews are explicit requirements/diff reviews recorded in GitHub and tested through RED/GREEN CI evidence.
