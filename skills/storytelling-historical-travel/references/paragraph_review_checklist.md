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
2. an **independent** Sarah-style pass validates the exact paragraph against the frozen `sarah_voice_markers.md` contract → `sarah_style_reviewed=true`;
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

## Sarah-style transition — independent, hash-bound, frozen

The voice source of truth is `references/sarah_voice_markers.md`. Runtime never searches for Sarah's voice and never silently extends its marker list.

The style flag does **not** become true because the paragraph “sounds good”, nor because a generation pass returns `passed=true`. The review must be a distinct pass and must be tied to the exact prose and exact voice contract:

```json
{
  "passed": true,
  "reviewer_role": "independent_style_gate",
  "evaluator": "bounded_llm",
  "generation_pass_id": "draft-A07b-P03-v2",
  "review_pass_id": "style-A07b-P03-v2",
  "generation_context_id": "ctx-draft-A07b-P03",
  "review_context_id": "ctx-style-A07b-P03",
  "paragraph_sha256": "<hash du paragraphe visible exact>",
  "voice_contract_id": "sarah-voice-run25-v1",
  "voice_contract_sha256": "<hash du fichier sarah_voice_markers.md>",
  "marker_results": {
    "scope_precision": {
      "status": "pass",
      "rationale": "La portée reste limitée au cas et à la période documentés."
    },
    "rigor_compressed_in_sentence": {
      "status": "pass",
      "rationale": "La réserve sur la tradition est intégrée dans la phrase."
    },
    "lived_opening_callback": {
      "status": "not_applicable",
      "rationale": "Ce paragraphe n'ouvre ni section ni séquence et ne porte pas la prise de terrain initiale."
    }
  }
}
```

### Ce que le gate vérifie mécaniquement

- `generation_pass_id != review_pass_id` ;
- `generation_context_id != review_context_id` ;
- le hash du paragraphe correspond au texte effectivement revu ;
- le hash et l'ID du contrat correspondent à la version figée courante ;
- `scope_precision` est explicitement `pass` ;
- aucun marker inconnu ;
- aucun marker applicable à `fail` ;
- chaque `pass` / `not_applicable` est justifié ;
- au moins un marker signature applicable passe, ou, si aucun marker signature n'est applicable à cette unité, au moins un marker de soutien passe.

Le jugement sémantique de style reste volontairement LLM/humain : le script ne prétend pas qu'une regex sait reconnaître Sarah. En revanche, le script rend la revue **auditable, non réutilisable après réécriture et non auto-certifiable dans la même passe**.

La source primaire prévue par la Partie 0 — mémoire exportée de l'autre assistant de Sarah — n'est pas encore importée. Tant que ce n'est pas le cas, le gate applique uniquement le contrat figé issu de la spec Run 25 et produit un warning de provenance ; il ne complète rien par invention.

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
- a changed paragraph hash invalidates the previous Sarah review automatically;
- a changed Sarah voice contract invalidates previous Sarah reviews automatically;
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

### Style review copied after rewrite

The prose changes but `paragraph_sha256` is still the hash of the previous version.

Reject: stale Sarah review.

### Style self-certification

`generation_pass_id == review_pass_id` or `generation_context_id == review_context_id`.

Reject: the style review was not independent.

## Positive fixture

> Le roi se rendit au sommet de la colline sacrée en 1765 ; la tradition du temple situe là une rencontre avec les responsables du sanctuaire. Ce geste renforça ensuite la relation politique entre la cour et l'institution religieuse.

Eligible only after deterministic checklist, **independent hash-bound Sarah review**, and relevant-only HIL scope have each passed.
