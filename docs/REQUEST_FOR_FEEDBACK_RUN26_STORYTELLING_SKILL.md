# Request for Feedback — Run 26 storytelling skill architecture

## TL;DR

The current storytelling skill has accumulated useful editorial knowledge, but too much of its behaviour has historically lived as long natural-language instructions. That is fragile: rules can be skipped, reinterpreted or drift between iterations without leaving a machine-checkable trace.

Run 26 proposes a different architecture: **thin skill orchestrator + explicit state machine + bounded input packets + executable gates + render AST/block contracts + review ledger**. The LLM remains responsible for the genuinely semantic operation — writing and judging narrative quality — but it is surrounded by deterministic preconditions, outputs and failure states.

Feedback is requested on whether this is the right boundary between deterministic process and language-model judgement, and on the minimum contracts needed to make iterative document work reliable across many runs.

---

## 1. Problem statement

### 1.1 What works today

The repository already has strong ingredients:
- typed claims and evidence states;
- source/bridge contracts;
- side-story and illustration contracts;
- reader profiles;
- deterministic coverage and graph audits;
- positive and negative tests;
- long-form retention gates;
- a documented narrative voice.

The issue is not lack of editorial thinking. The issue is **where that thinking is encoded**.

### 1.2 Main architectural weakness

A large share of storytelling behaviour has been represented as prose in `SKILL.md`:

> load this, remember that, prefer X, never do Y, keep the tone, use callbacks, select only relevant dimensions, preserve uncertainty, do a final pass…

These instructions are useful to a human reviewer, but they are not sufficient as an industrial execution model. They suffer from four failure modes:

1. **No state** — an instruction says “review the paragraph”, but nothing proves that review happened for this paragraph.
2. **No transition contract** — a later step can proceed even if an earlier semantic gate was never executed.
3. **Implicit context** — “use relevant HIL dimensions” is ambiguous unless relevance is materialized from claims used in the paragraph.
4. **Renderer inference** — side-story styling attempted to infer the end of a block from `return_to`, producing visually open or partially coloured blocks.

Prompt length compounds these problems: the more policy prose the agent must retain, the easier it is to comply with the spirit while silently missing one operational invariant.

---

## 2. Run 26 target architecture

```text
structured evidence
      │
      ▼
┌──────────────────────────────┐
│ deterministic packet builder │  no old-reader prose in from-scratch mode
└──────────────┬───────────────┘
               ▼
       arc-local packet
               │
               ▼
┌──────────────────────────────┐
│ LLM paragraph writer          │  semantic work only
└──────────────┬───────────────┘
               ▼
      paragraph + lineage IDs
               │
       ┌───────┴────────┐
       ▼                ▼
 deterministic      bounded semantic
 checklist          Sarah-style review
       │                │
       └───────┬────────┘
               ▼
      HIL relevance gate
               │
               ▼
     review_state = all true
               │
               ▼
     manuscript block AST/fences
               │
               ▼
      deterministic renderer
               │
               ▼
  coverage / visual / leakage QA
```

The skill itself should mostly route these components, not repeat their full rulebooks.

---

## 3. Proposed contracts

### 3.1 Generation mode contract

Two modes must be explicit:

#### `iterative`
Input may include current canonical reader prose. The operation is a bounded delta. Retention against the existing manuscript is meaningful.

#### `from_scratch`
Input may include structured historical artefacts but **must not include previous reader prose**. The packet builder records every path read and blocks:
- `report*.md` reader outputs;
- DOCX/PDF readers;
- archive snapshots;
- generated reader scaffolds/plans that themselves summarize previous reader prose when used as drafting input.

A from-scratch output should be compared to the iterative one **after writing**, never used to seed it.

### 3.2 Paragraph review state

Each paragraph owns a fresh state:

```json
{
  "checklist_reviewed": false,
  "sarah_style_reviewed": false,
  "hil_scope_reviewed": false
}
```

A value may become true only when its corresponding gate has run and passed. No inheritance between paragraphs. A rewrite creates a new state with all values false.

Question for reviewers: should this state be persisted as JSONL per paragraph, or should the manuscript itself carry a hidden structured annotation that is extracted during QA?

### 3.3 Sarah-style review contract

“Write like Sarah” is too vague to be an executable requirement. The proposal is a bounded semantic reviewer that returns a small typed record:

```json
{
  "passed": true,
  "evaluator": "bounded_llm",
  "markers": [
    "scope_precision",
    "concrete_texture",
    "integrated_nuance"
  ],
  "notes": "..."
}
```

`scope_precision` is mandatory because style must never improve fluency by silently broadening a claim. Other markers are selected only when relevant to the paragraph.

Question: should the reviewer be asked to cite a sentence span for each selected marker? This would improve auditability but adds tokens and may encourage mechanical style checking.

### 3.4 HIL relevance contract

The eight HIL dimensions are a **search space**, not eight boxes to tick in every paragraph.

Hard rule:

```text
selected_hil_ids ⊆ HIL(claims actually used in paragraph)
```

Not required:

```text
selected_hil_ids == every HIL that could conceivably apply
```

This prevents “HIL stuffing”, where economic, religious, institutional or security angles are injected because the framework exists rather than because the paragraph needs them.

Question: should side-story lineage be allowed to introduce an HIL not present on the paragraph's direct claims, or must that side story first carry its own explicit claim lineage into the paragraph state?

### 3.5 Side-story block contract

A style is not enough to define a block. A block requires structural boundaries:

```markdown
<!-- [SIDE-STORY:SS-X] BEGIN kind=false_lead -->
**Fausse piste — ...**
...
<!-- [SIDE-STORY:SS-X] END -->
```

The DOCX renderer should consume that as **one block container** (for example a one-cell borderless/soft-border table) with:
- fill colour by kind;
- redundant symbol ①–⑩;
- padding;
- top and bottom extent visible;
- no dependence on colour to communicate kind.

Question: should the canonical Markdown evolve to a real block AST/JSON rather than Markdown comments, with Markdown becoming only one serialization of the document tree?

---

## 4. What should remain LLM-driven

The goal is not to make storytelling deterministic. The following operations are inherently semantic and should remain model-assisted:

- selecting a compelling concrete opening among several valid pieces of evidence;
- composing causal transitions without flattening uncertainty;
- deciding which relevant HIL dimension materially helps this paragraph;
- judging whether a callback feels natural rather than repetitive;
- judging whether the Sarah voice markers are present without becoming mannerisms;
- choosing whether a side story earns its space despite being contract-valid;
- reordering evidence for readability while preserving fact → mechanism → consequence.

But the model should return structured evidence of these decisions, rather than only emitting prose and claiming compliance.

---

## 5. What should be deterministic

Candidates for pure code / schema / tests:

- allowed inputs for each run mode;
- read ledger and contamination detection;
- claim/HIL eligibility set construction;
- review-state initialization and legal transitions;
- claim marker count and callback thresholds;
- side-story BEGIN/END balance;
- side-story maximum count per subsection;
- side-story colour/symbol mapping;
- reader-facing production-language blacklist;
- source/claim/bridge ID resolution;
- coverage reconciliation;
- illustration status/density/lineage;
- paragraph IDs and review-ledger completeness;
- rendering of structural blocks, TOC and legends;
- archive/snapshot creation;
- iterative-vs-from-scratch quantitative comparison.

---

## 6. Suggested document-processing model

The current system still treats Markdown as both manuscript and intermediate state. For repeated long-document iteration, a stronger architecture may be:

```text
Evidence graph
   ↓
Story scaffold / outline AST
   ↓
Section packets
   ↓
Paragraph records
   ↓
Review ledger
   ↓
Document AST
   ↓
Markdown / HTML preview / DOCX / PDF renderers
```

A paragraph record could be:

```json
{
  "id": "P-A07b-014",
  "section_id": "S-A07b-03",
  "claim_ids": ["C-...", "C-..."],
  "selected_hil_ids": ["HIL-06_security-coercion"],
  "text": "...",
  "review_state": {
    "checklist_reviewed": true,
    "sarah_style_reviewed": true,
    "hil_scope_reviewed": true
  },
  "callbacks_opened": [],
  "callbacks_closed": ["CB-KANDY-DEFENCE"],
  "side_story_ref": null
}
```

The final manuscript is then a projection, not the primary database.

Question: is this too much structure for the value gained, or is it the necessary step to support reliable multi-run editing at 50–100+ pages?

---

## 7. Iterative editing semantics

A durable skill should support explicit operations rather than “rewrite the document”:

- `insert_claim(claim_id, target_section)`
- `rewrite_paragraph(paragraph_id, reason)`
- `move_side_story(side_story_id, target_section)`
- `close_callback(callback_id, paragraph_id)`
- `rerank_false_leads(section_id)`
- `rebuild_section(section_id)`
- `rebuild_arc(arc_id)`
- `full_from_scratch(project)`

Each operation should declare:
- read scope;
- write scope;
- invalidated downstream artefacts;
- gates to rerun;
- review states reset to false;
- expected token class (L0/L1/L2/L3).

This would make the workflow closer to incremental compilation than repeated prompting.

---

## 8. Drift controls proposed

### 8.1 Prompt drift
Reduce natural-language policy in `SKILL.md`. Keep only routing, state transitions and links to executable contracts.

### 8.2 Style drift
Persist structured style review markers and compare their distribution over a document. Do not target a fixed quota; use the distribution to detect sudden generic sections.

### 8.3 Evidence drift
Every paragraph keeps claim IDs. Reconciliation checks unused/overused claims without guessing from semantic similarity.

### 8.4 HIL drift
Reject HIL dimensions not supported by claims used in the paragraph.

### 8.5 Visual drift
Side stories use structural block boundaries. Renderer tests inspect XML/container extents rather than screenshots alone.

### 8.6 Iteration drift
Archive immutable release snapshots and compute structured diffs between runs: claims added/lost, paragraphs rewritten, review states reset/revalidated, side stories moved, callbacks changed.

---

## 9. Comparison experiment — Run 25 vs Run 26

Run 25 iterative reader is frozen before Run 26.

Run 26 from scratch must not read Run 25 prose while drafting. After completion, compare:

### Structural
- total words / paragraphs / sections;
- claims evidenced at least once;
- claims >2 direct mentions;
- bridge coverage;
- side-story count/kind/placement;
- HIL distribution by paragraph;
- callback open/close balance.

### Review
- paragraphs with all three review flags true;
- failed/rewrite counts by gate;
- style markers selected;
- irrelevant-HIL rejection count.

### Narrative
A bounded blind review should compare selected matched sections for:
- concrete texture;
- causal clarity;
- continuity;
- apparent process leakage;
- generic vs distinctive voice;
- redundancy;
- loss of historical nuance.

The narrative comparison must happen only after the from-scratch manuscript is sealed.

---

## 10. Feedback requested

Please challenge the following points explicitly:

1. **State granularity** — paragraph, subsection, or both?
2. **Semantic reviewer output** — boolean + markers sufficient, or require cited spans/rationale?
3. **HIL eligibility** — direct claim links only, or allow bridge/side-story propagation under a typed rule?
4. **Document AST** — worth introducing now, or keep fenced Markdown as the source of truth?
5. **Retry semantics** — on paragraph failure, rewrite only that paragraph; on structural failure, what is the smallest safe invalidation scope?
6. **Style stability** — how to test Sarah voice across a long document without turning style into a mechanical quota?
7. **Coverage target** — should every validated claim be used, or should the system allow explicit `not_selected_for_reader` decisions with rationale?
8. **Side-story rendering** — one-cell table is robust in DOCX; is there a better cross-format block primitive for HTML/PDF/DOCX parity?
9. **LLM boundary** — which current rule is still encoded as prose but could become deterministic tomorrow?
10. **Skill size** — should `SKILL.md` be capped to an orchestration budget (for example <150 lines) with tests enforcing that detailed policy lives elsewhere?
11. **Observability** — which metrics should be mandatory in every run journal to debug narrative drift efficiently?
12. **From-scratch validity** — is a read ledger sufficient proof against contamination, or should inputs be physically copied to an isolated workspace before drafting?

---

## 11. Acceptance direction

A successful refactor should make this statement true:

> An agent can stop halfway through a 100-page document, resume later, know exactly which paragraph states are valid or invalid, load only the evidence needed for the next operation, preserve the intended narrative voice, and prove after export which gates ran — without depending on the model remembering a long list of instructions.

That is the intended standard for industrializing this skill.
