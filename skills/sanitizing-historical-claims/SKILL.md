---
name: sanitizing-historical-claims
description: Use when raw historical material mixes facts, traditions, interpretations, analogies, comparators, metrics, propaganda, translations, or causal assertions that must be separated before research.
---

# Sanitizing historical claims

Split each new input into `source_fact`, `claim`, `inference`, `tradition`, `analogy`, `comparator`, `counterfactual`, `metric`, `policy_intent`, `policy_effect`, `question`, or `discarded_lead`. Keep original wording when semantic drift matters. Never let a museum label, chronicle, nationalist narrative, development slogan or modern analogy silently become fact.

`legacy_fragment` is a migration-only virtual type for the finite corpus captured before systematic claim/source contracts. It is not a thirteenth normal intake type. It may be emitted only by `scripts/legacy_fragment_bypass.py` for explicitly allowlisted, unsourced, unclaimed legacy fragments. It never upgrades evidence, never satisfies a sourcing gate and never appears as production metadata in reader prose.

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

## Legacy debt boundary
The legacy bypass exists only to preserve old narrative material without paying a one-by-one migration tax.

- Configuration is project-local in `00_method/legacy_fragment_bypass.json`.
- Only allowlisted capture paths are eligible.
- Only fragments without a registered source and without a real claim promotion are wrapped.
- The virtual statement keeps `confidence=U`, `causal_role=context`, `legacy_unsourced=true` and `origin_fragment_ids`.
- It may preserve or help reposition narrative already present in an iterative reader.
- Any new factual assertion derived from it requires normal research and a sourced claim before promotion.
- New inputs never enter through this bypass.

## Side-story handoff
Statement type and narrative role are independent. A `comparator`, `analogy`, `discarded_lead` or other typed statement may later support a `comparator`, `false_lead`, `method` or other `side_story`, but sanitization never promotes it. Preserve its typed claim/source identity so the composition record can reference lineage instead of copying prose.

A `legacy_fragment` may help preserve an existing legacy side story, but it cannot by itself promote a new side story as verified.

## Output
One typed statement per new input fragment, each ready to become a `templates/claim.md` record once an arc/HIL/zoom and source are attached, or to remain an explicit unresolved/discarded input for later composition.

Legacy fragments are the exception: they remain capture records and are exposed as virtual claim-like statements only at drafting time.

See also: `SKILL.md` orchestration step 2; `composing-side-stories`; `docs/skill_workflow_index.md`; `docs/LEGACY_FRAGMENT_BYPASS.md`.
