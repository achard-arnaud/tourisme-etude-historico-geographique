# Run 27 — canonical points

Decision: `canonical_points` remains `warning_only_until_populated`.

Existing claims predate this field. Missing points therefore produce a review warning, not a false blocking guarantee. `scripts/audit_canonical_points.py` reports real coverage; its `--strict` option is the future activation switch once points have been editorially authored from claims plus their source/fragment context.

Do not populate this field by mechanically splitting or paraphrasing the existing `claim` sentence. That would be circular and would not increase fidelity.
