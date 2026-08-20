---
name: sanitizing-historical-claims
description: Use when raw historical material mixes facts, traditions, interpretations, analogies, comparators, metrics, propaganda, translations, or causal assertions that must be separated before research.
---

# Sanitizing historical claims

Split each input into `source_fact`, `claim`, `inference`, `tradition`, `analogy`, `comparator`, `counterfactual`, `metric`, `policy_intent`, `policy_effect`, `question`, or `discarded_lead`. Keep original wording when semantic drift matters. Never let a museum label, chronicle, nationalist narrative, development slogan or modern analogy silently become fact.

## Sanitize checks
- Who is speaking and when?
- Is the wording contemporary, retrospective or translated?
- What geographic/institutional scale is actually supported?
- Is causality asserted, observed or inferred?
- Is a modern category projected backwards?
- Is a programme target being mistaken for an outcome?
- Is a comparator being presented as a counterfactual proof?
- Are “success”, “failure”, “underrepresentation”, “modernity” or “segmentation” operationally defined?

## Policy separation
Store the problem definition, legal instrument, implementation and observed effect separately. A law's existence proves a rule, not enforcement; a quota's intent does not prove its distributive outcome.

## Metric hygiene
For every quantitative statement retain denominator, geography, year/period, nominal/real basis where relevant and source definition. If those are missing, downgrade the statement to an unresolved lead rather than manufacturing comparability.

## Side-story handoff
Statement type and narrative role are independent. A `comparator`, `analogy`, `discarded_lead` or other typed statement may later support a `comparator`, `false_lead`, `method` or other `side_story`, but sanitization never promotes it. Preserve its typed claim/source identity so the composition record can reference lineage instead of copying prose.

## Output
One typed statement per input fragment, each ready to become a `templates/claim.md` record once an arc/HIL/zoom and source are attached, or to remain an explicit unresolved/discarded input for later composition.

See also: `SKILL.md` orchestration step 2; `composing-side-stories`; `docs/skill_workflow_index.md`.
