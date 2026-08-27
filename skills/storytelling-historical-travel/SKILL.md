---
name: storytelling-historical-travel
description: Use when validated historical evidence must become a reader-facing narrative without changing evidence, reader-scaffold or uncertainty contracts.
---

# Storytelling historical travel

This file is an **orchestrator**, not a prose prompt. Executable contracts win over prose if they conflict.

## Core architecture — one composition engine, two bootstraps

Run32 removes the false split between an “iterative writer” and a “from-scratch writer”. At least 80% of the pipeline is shared.

### Shared composition layers

1. **Reader scaffold — authoritative editorial topology**
   - ordered parts, chapters, subsections and inline side-story slots;
   - imported from an approved reader DOCX when a human scaffold exists;
   - never rebuilt by sorting evidence arcs alphabetically;
   - `reader_scaffold.json` controls *where* prose belongs.

2. **Evidence control plane**
   - claims, bridges, questions, source registers, uncertainty and HIL;
   - claims are an **ossature / contract**, not the prose unit;
   - bridge records are relationship instructions, not paragraphs.

3. **Narrative material plane**
   - all relevant capture/field fragments, including candidate-arc fragments not yet referenced by a claim;
   - preserved archived intakes when relevant to the arc;
   - side-story body material, recaps and approved illustration interpretation;
   - source-attested texture is preferred over claim paraphrase.

4. **Draft / review / repair**
   - draft into the reader scaffold;
   - source-attested fact or observed texture before mechanism;
   - preserve scope and uncertainty;
   - paragraph review and repair remain common to both modes;
   - no invented dialogue, invented thoughts, invented motives, composite characters or fabricated sensory facts.

5. **Composition**
   - side stories are inserted **inside the chronological trunk at their reader anchor**;
   - no end-of-book side-story gallery unless an apparatus is explicitly defined as such;
   - new inline stories must be narratively substantial enough to justify leaving the trunk.

6. **Frontstage**
   - reader prose contains simple source citations;
   - `[claim:<id>]`, bridge IDs, machine HIL identifiers (for example `HIL-01_institutions-chronology`), run IDs and lineage remain backstage; reader-facing HIL display labels such as `HIL-01` may remain when the approved scaffold uses them;
   - a separate ledger binds paragraphs to claims/sources.

### The only mode-specific layer: bootstrap

`iterative`
- load the approved canonical manuscript and append-only construction journal;
- preserve the approved reader scaffold;
- apply bounded, chronologically placed deltas;
- retention against the baseline is a hard concern.

`from_scratch`
- load **no previous reader prose**;
- use the same reader scaffold topology where one is approved;
- use the same evidence/material packets and the same drafting/review/composition engine;
- the packet manifest must report `reader_prose_loaded=false`.

Executable entry point:

`python scripts/build_drafting_packets.py --project <project> --mode iterative|from_scratch`

Compatibility:

`python scripts/build_from_scratch_packets.py --project <project>`

## Reader profiles and preservation contract

Supported reader profiles remain **advanced**, **intermediate** and **child**. The reader plan selects one profile and controls presentation, never evidence strength.

For advanced work there is **no maximum length**. Use the **content-preservation gate** and explicit dispositions instead of compression by budget. Intermediate and child modes may simplify structure and vocabulary, but they may not silently delete required evidence or uncertainty.

The reader plan, paragraph review state and Sarah-voice review remain deterministic inputs to composition QA. A profile changes exposition; it does not authorize invented dialogue, invented motives, source inflation or claim loss.

## Input priority for prose generation

When constructing a paragraph, use this order:

1. source-attested fragments / field material;
2. relevant archived intake as a **research/narrative prompt only**, never as evidence by itself;
3. source records and quotations/notes within allowed scope;
4. claim canonical points and uncertainty as a control check;
5. bridge relation for causal stitching.

Never turn a short claim into the maximum amount of prose available. A short claim can control a paragraph supported by several richer fragments and sources.

### Legacy-fragment migration bypass

`legacy_fragment` is a **finite migration bypass**, shared by both modes, for explicitly allowlisted old fragments that predate full sourcing/lineage instrumentation. It is virtual drafting context only: it may preserve or reposition already-existing narrative and may seed a research question, but it **cannot establish a new fact, satisfy a sourcing gate, or silently upgrade evidence**. New or sourced fragments must use the normal evidence path. The type never renders in the reader.

## Reader scaffold contract

`story_scaffold.json` is the evidence/graph topology. `reader_scaffold.json` is the narrative topology.

They are not interchangeable.

- `reader_scaffold.json` controls order and placement.
- `story_scaffold.json` helps retrieval and cross-arc coverage.
- an evidence arc may map into several reader sections;
- several evidence arcs may be narrated in one chronological reader chapter.

## Side stories

A side story is an excursion with a return, not a label + takeaway.

- place it beside the event/mechanism that makes the excursion useful;
- keep its own internal mini-arc: question/object → evidence → explanation → limit → payoff/return;
- use `placement.section_anchor` that resolves to the reader scaffold;
- insert only at full paragraph/heading boundaries;
- new non-method side stories should normally exceed ~90 visible words; analytical focuses are longer;
- `existing_fragment` side stories inherited from an approved reader are exempt from artificial expansion.

Typical kinds: detour, dezoom, also, method, false_lead, portrait, object_focus, comparator, callback, analytical_focus.

## Claims and sources in the final reader

Claims are backstage.

During drafting they:
- constrain factual scope;
- identify source lineage;
- carry confidence/type/causal role;
- support coverage accounting.

During export:
- strip all `[claim:*]` markers;
- render simple source references already used by the book (`[SOURCE-ID]` or compact human-readable source note);
- keep the full claim→paragraph→source mapping in a separate QA ledger.

A “100% claims present” statement is not a reader-quality objective. The objective is **historical matter preserved and sourced**, with claims accounted for backstage.

## Review and conservation

Every final eligible historical unit gets one disposition:
- `included`;
- `included_as_side_story`;
- `not_selected_for_reader` with rationale.

Coverage must include **promoted fragments and rich intakes/capture units**, not claims alone. A claim referenced once by a thin sentence does not prove narrative conservation.

## Stop conditions

Do not export final if:
- reader scaffold order is violated;
- an iterative run silently drops baseline material;
- a required side story is appended outside its intended chronological context;
- a promoted new side story is only a title/takeaway when richer source material exists;
- claim/bridge/run metadata or machine HIL identifiers leak into frontstage;
- a from-scratch run reads previous reader prose;
- an evidence state is silently upgraded;
- a new or sourced fragment enters through the legacy bypass;
- eligible promoted narrative material has no disposition.

## Executable contracts

- `scripts/import_reader_scaffold.py`
- `scripts/build_drafting_packets.py`
- `scripts/build_from_scratch_packets.py` (compatibility wrapper)
- `scripts/materialize_side_stories.py`
- `scripts/paragraph_review_gate.py`
- `scripts/paragraph_repair_loop.py`
- `scripts/reciprocal_coverage_check.py`
- `scripts/evidence_coverage_contract.py`
- `scripts/frontstage_reader_contract.py`
