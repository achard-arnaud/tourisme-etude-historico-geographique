# Sri Lanka — longue durée jusqu’à 1948

Worked corpus for `tourisme-etude-historico-geographique`.

## Current pipeline state
- `09_output/archive/*_v1.docx` and `09_output/report_v1_full.md` preserve the complete 61-page baseline.
- `09_output/report.md` is the Jaffna/VOC + European-war **delta**, not a replacement manuscript.
- `09_output/report_v3_full.md` and the V3 DOCX/PDF are the current complete reader edition: 21 236 DOCX words and 68 PDF pages.
- `05_sources/conversation_corpus/` and `00_method/conversation_capitalization_register.md` preserve and route the Sri Lanka 2026 conversations.

## Current causal additions
The previous run reframed the Portuguese → VOC → British transition through fort networks, political economy, the paper state and the 1744–1763 / 1793–1815 geopolitical reorderings.

The current pass adds a vertical social bridge:

`precolonial hierarchy -> VOC thombo/legal legibility -> possible hardening of dominant intermediaries -> British formal emancipation without instant social dissolution -> missionary education/English as new mobility capital -> post-1948 redistribution`.

This explicitly rejects both extremes: colonialism did **not invent caste**, but colonial administration was not a neutral camera either; registration, law and service obligations could rework and stabilize hierarchy.

## Read order
1. `09_output/report_v3_full.md`
2. `00_method/conversation_capitalization_register.md`
3. `05_sources/conversation_corpus/`
4. `05_sources/jaffna_caste_colonial_note.md`
5. `01_arcs/A08_jaffna_caste_colonial_codification/claims/`.

The advanced reader contract is unconstrained. `scripts/render_full_reader_v3.py` starts from V1 and inserts promoted deltas chronologically; the legacy compact renderer refuses silent compression.
