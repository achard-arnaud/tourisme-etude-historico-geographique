# Paragraph review checklist — storytelling historical travel

Backstage QA only. Never render this file or its state flags into reader prose.

## State machine

Every paragraph review is a **new state instance**. It always starts exactly as:

```json
{
  "checklist_reviewed": false,
  "sarah_style_reviewed": false,
  "hil_scope_reviewed": false
}
```

No previous paragraph may donate a `true` value to the next one.

Transitions are independent:

1. deterministic form/fund checklist passes → `checklist_reviewed=true`;
2. bounded Sarah-style reviewer records a passing structured review → `sarah_style_reviewed=true`;
3. paragraph-local HIL scope is explicitly declared and contains no irrelevant dimension → `hil_scope_reviewed=true`.

The paragraph is eligible for final manuscript only when all three values are `true` and no violation remains. A failed transition triggers **full paragraph rewrite**, then a fresh review state.

## Fund — deterministic checklist

1. **Canonical coverage** — all structured `canonical_points` of the source claim are retained. Legacy claims without structured points require targeted semantic review; the deterministic gate does not invent points.
2. **Input texture** — retain concrete material when available: place, date, actor, institution, object, gesture or documented practice.
3. **Narrative order** — attested fact/action → mechanism → perspective/consequence. Do not open on a conclusion and hide the evidence in a retrospective subordinate clause.
4. **Citation/callback** — more than two direct `[claim:<id>]` citations is a review signal. If an active callback exists, a third direct citation is non-compliant.
5. **Density** — strong source/rendered-volume divergence is warning-only, not an automatic rejection.

## Form — deterministic checklist

6. **No production leakage** — no `TL;DR`, canonical-status heading, HIL label, run/version, baseline/delta/lineage, writing instruction or production table in reader prose.
7. **Acronyms explained** — reader-facing acronyms are expanded at first use. Hidden traceability IDs are not prose.
8. **Foreign technical terms glossed** — francise or explain terms such as *clearing house* at first use.
9. **False leads** — maximum 1–2 per subsection and always a naïve/semi-rhetorical question with its answer inside the same side-story block.

## Sarah-style transition

The style flag never becomes true because the paragraph “sounds good”. The reviewer records:

```json
{
  "passed": true,
  "evaluator": "bounded_llm",
  "markers": ["scope_precision", "concrete_texture"]
}
```

Allowed markers are defined by `paragraph_review_gate.py`. `scope_precision` is mandatory; at least one additional paragraph-relevant marker is required. The evaluator must check only the paragraph plus immediate previous/next context, not the whole manuscript.

## HIL transition — relevance only, never quota

HIL dimensions are **not a checklist of eight angles to force into every paragraph**.

For each paragraph:

1. determine the claims actually used from `[claim:<id>]` markers;
2. build the candidate HIL set from those claims' `hil` / `hil_ids` and explicitly linked composition records;
3. select only dimensions that materially help explain this paragraph;
4. reject any selected HIL that has no support in a claim used by the paragraph;
5. allow relevant HIL dimensions to remain unselected when they add no explanatory value here.

Therefore:

- `selected_hil_ids ⊆ relevant_hil_ids` is a hard gate;
- `selected_hil_ids == relevant_hil_ids` is **not** required;
- HIL names/IDs remain backstage and never appear in reader prose.

## Decision

- any fund/form/style/HIL violation → rewrite the **whole paragraph**;
- warning only → targeted review, no automatic failure;
- every rewrite resets all three review flags to `false`;
- tests require both accepting and rejecting fixtures.

## Negative fixtures

### Production leakage

> TL;DR : ce claim établit un statut canonique fort pour la relique.

Reject.

### Unglossed foreign term

> Le clearing house régional organisait les échanges du port.

Reject.

### Incomplete canonical coverage

A three-point claim is rendered only as:

> Le roi fit construire un temple.

Reject.

### Reversed narrative order

> Cela eut pour conséquence un renforcement du pouvoir royal, après que le roi eut visité le site.

Reject.

### Irrelevant HIL

A paragraph sourced only by a religious-legitimacy claim selects `HIL-03_economy-infrastructure` without another supporting claim.

Reject with `hil_dimension_not_relevant_to_paragraph`.

### Style review omitted

The paragraph passes deterministic checks but has no structured `sarah_style_review` record.

Reject: `sarah_style_reviewed` remains `false`.

## Positive fixture

> Le roi se rendit au sommet de la colline sacrée en 1765 ; la tradition du temple situe là une rencontre avec les responsables du sanctuaire. Ce geste renforça ensuite la relation politique entre la cour et l'institution religieuse.

Eligible only after deterministic checklist, Sarah-style record and relevant-only HIL scope have each passed.
