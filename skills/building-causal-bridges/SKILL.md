---
name: building-causal-bridges
description: Use when two well-supported historical anchors are both necessary to a narrative but the mechanism connecting them is not yet evidenced, including bounded cross-case comparison.
---

# Building causal bridges

Create a bridge only between established anchors when the missing relation changes the explanation. Ask one question, research the smallest mechanism needed, close as `A/B/C/D/U`, then integrate or discard. Prevent bridge proliferation: curiosity without causal necessity belongs in a side box or backlog.

## Bridge contract
Record:
- `from_claim` and `to_claim`;
- precise causal question;
- mechanism and transmission channel;
- time lag;
- geographic/institutional scale;
- alternative mechanisms/confounders;
- source IDs and result confidence.
A bridge is not a restatement of correlation.

## Comparative bridge gate
A cross-case bridge requires:
1. the same mechanism on both sides;
2. comparable starting conditions or explicit differences;
3. the policy/institution operating at a comparable level;
4. war/peace, market size, federal transfers, migration and geography treated as confounders where relevant;
5. a bounded counterfactual: what the comparator shows is **possible**, not what the home case would certainly have become.

## Transportability test
Classify what is portable:
- **instrument** (quota, language rule, school expansion);
- **mechanism** (reduced access cost, broadened recruitment);
- **institutional package** (federalism + fiscal capacity + implementation);
- **outcome** (growth, cohesion, sectoral change).
Usually only the first two travel cleanly. Never transport an outcome when the institutional package differs.

## Closure
`A/B` bridges may enter the causal spine when adequately sourced. `C` stays explicitly hypothetical. `D` is retained only if the rejected analogy teaches a useful correction. `U` remains backlog and must not be narrated as fact.

## Output
One bridge record per mechanism gap, shaped by `templates/bridge.md` and stored in `06_bridges/*.json`, with `from_claim`/`to_claim`, source IDs and a closed `result`.

See also: `SKILL.md` orchestration step 7; `docs/skill_workflow_index.md`.
