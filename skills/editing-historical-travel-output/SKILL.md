---
name: editing-historical-travel-output
description: Use when a researched travel-history corpus must become a chronological, readable personal report without unread annexes, repeated analytical silos, or hidden output-state ambiguity.
---

# Editing historical travel output

This skill controls **structure**, not reader voice. Write chronologically by arc. Open each arc with the causal question and a short orientation. Integrate HILs into one narrative rather than repeated analytical sections. Use `Mais aussi`, `Petit détour`, `Point de méthode`, and `Fausse piste` only when side material deepens or corrects the trunk.

## Vertical-thread policy
Some mechanisms cross many arcs — caste, language, education, water, religion, trade, migration. Keep chronology as the spine but reactivate a vertical thread at the moments where it changes the governing optimum. Use short callbacks rather than creating a second parallel book.

## Comparator placement
A comparator belongs next to the home-case mechanism it illuminates. State what is comparable and the confounders in the prose. If it does not change the home-case interpretation, demote it to `Petit détour` or delete it.

## Arc close
End each arc with:
- what materially changed;
- which prior optimum stopped working;
- what persisted beneath the rupture;
- the bridge forward.

## Promotion state
Every manuscript must be identifiable as one of: `baseline`, `vnext`, `promoted/canonical`, `reader-export`. Do not silently overwrite the last known reading edition with unverified research. After research stabilizes, deliberately promote the Markdown before producing Word/PDF.

Before handoff, remove duplicate entity biographies, orphan annexes, repeated source discussions and unclosed hypotheses. Then pass the structured manuscript to `storytelling-historical-travel`.

## Output
A chronological manuscript in `09_output/`, structured per `templates/output-outline.md` and tagged with its promotion state (`baseline`, `vnext`, `promoted/canonical`, `reader-export`).

See also: `SKILL.md` orchestration step 10; `docs/skill_workflow_index.md`.
