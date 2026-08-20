---
name: editing-historical-travel-output
description: Use when a researched travel-history corpus must become a chronological, readable personal report without unread annexes, repeated analytical silos, or hidden output-state ambiguity.
---

# Editing historical travel output

This skill controls **structure**, not reader voice. Write chronologically by arc. Open each arc with the causal question and a short orientation. Integrate HILs into one narrative rather than repeated analytical sections.

## Side-story consumption contract
Do not invent ad-hoc side-box labels in prose. Consume `validated`/`promoted` records from `09_output/side_stories/` and use their closed kind→label mapping: `Petit détour`, `Dézoom`, `Mais aussi`, `Point de méthode`, `Fausse piste`, `Personnage`, `Objet / terrain`, `Comparaison`, `Fil rouge`.

Place the hidden `[SIDE-STORY:<id>]` marker immediately before the visible box, respect `placement.section_anchor` and `placement.return_to`, and preserve the evidence lineage. If material has no valid side-story record yet, send it back to `composing-side-stories` rather than freezing an untraceable box in canonical Markdown.

## Vertical-thread policy
Some mechanisms cross many arcs — caste, language, education, water, religion, trade, migration. Keep chronology as the spine but reactivate a vertical thread where its role changes. Use a `callback` side story when the return is reader-facing but not a new rupture.

## Comparator placement
A comparator belongs next to the home-case mechanism it illuminates. If it changes the causal interpretation and passes the comparative gate it may enter the trunk; otherwise route it as a bounded `comparator` side story or delete it.

## Arc close
End each arc with what materially changed, which prior optimum stopped working, what persisted and the bridge forward.

## Promotion state
Every manuscript is `baseline`, `vnext`, `promoted/canonical`, or `reader-export`. Do not silently overwrite the last known reading edition. A side-story record becomes `promoted` only when the canonical Markdown contains its marker and normalized label and all lineage checks pass.

Before handoff, remove duplicate biographies, orphan annexes, repeated source discussions and unclosed hypotheses. Then pass the structured manuscript to `storytelling-historical-travel`.

## Output
A chronological manuscript in `09_output/`, structured per `templates/output-outline.md`, plus promoted side-story markers whose JSON lineage remains in `09_output/side_stories/`.

See also: `SKILL.md` orchestration step 11; `composing-side-stories`; `docs/SOP_SIDE_STORIES.md`.
