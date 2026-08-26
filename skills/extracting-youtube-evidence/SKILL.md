---
name: extracting-youtube-evidence
description: Use when one or more YouTube links must be transcribed, converted into timestamped proposition leads, historically corroborated, and inserted into the arc-first corpus and graph-light without treating video assertions as established facts.
---

# Extracting YouTube evidence

Treat a video as evidence of what a speaker or production asserts. Do not treat it as proof that the assertion is historically true.

## Acquisition

1. Run `scripts/youtube_transcript.py <URLs> --output <project>/00_method/video_evidence`.
2. Prefer manual captions, then automatic captions. Use `--audio-fallback` only when speech-to-text processing is authorized and a configured provider is available.
3. Preserve one `video-evidence/v1` ledger per URL, including metadata, method, timestamps, transcript hash, limitations and degraded status.
4. Never reconstruct a private, deleted or unresolved video's content from title associations or nearby search results.

## Proposition split

Create one `video-proposition-register/v1` record from `templates/video-proposition-register.json`.

- Make every proposition atomic and quote-bounded by `timestamp_start_s`, `timestamp_end_s` and `transcript_excerpt`.
- Separate reported claims, interpretations, traditions, questions, metric leads and causal leads.
- Keep every new proposition `lead_only` or `researching`; a video transcript cannot promote itself.
- Preserve the speaker/channel, original language and translation status when attribution or wording matters.
- Run `scripts/video_claim_contract.py` before research.

## Historical corroboration

Dispatch `sanitizing-historical-claims`, then search proposition by proposition with `sourcing-historical-anchors`.

1. Turn the speaker assertion into falsifiable research queries.
2. Register the video as `T5`, anchor role `lead`, with scope limited to discourse/theme discovery unless the claim is specifically about the video or speaker.
3. Seek T0/T1 anchors first; use bounded T2 specialist syntheses where appropriate. Record contradictions and failed searches.
4. Split a complex assertion into separately sourced actor, period, place, metric and mechanism claims.
5. Never cite the video as the sole support for a historical fact, metric, policy effect or causal relation.

## Promotion and graph handoff

Promote only by creating normal typed claim files under the owning arc. Set `origin_lead_ids` to the proposition IDs and attach independently qualifying `source_ids`. Mark the proposition `promoted` and populate `promoted_claim_ids` only after project QA passes.

Insert graph-light relations only between resolved claims, bridges, wiki slugs or explicit nodes. A transcript proposition is not itself a graph endpoint. Run:

```bash
python scripts/video_claim_contract.py --evidence <ledgers...> --register <register.json>
python scripts/qa_project.py <project>
python scripts/graph_link_audit.py <project>
```

Zero unresolved graph endpoints and the existing causal/source gates remain mandatory.
