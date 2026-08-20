#!/usr/bin/env python3
"""Deterministic end-to-end functional QA for the canonical Sri Lanka pre-1948 fixture."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
PROJECT = REPO / "examples" / "sri_lanka_pre_1948"
STATEMENT_TYPES = {"source_fact", "claim", "inference", "tradition", "analogy", "comparator", "counterfactual", "metric", "policy_intent", "policy_effect", "question", "discarded_lead"}
CAUSAL_ROLES = {"driver", "amplifier", "constraint", "consequence", "non-cause", "context"}
ANCHOR_ROLES = {"canonical anchor", "specialist institutional anchor", "corroborating bridge", "lead"}
HILS = ["HIL-01_institutions-chronology", "HIL-02_geography-environment", "HIL-03_economy-infrastructure", "HIL-04_society-demography", "HIL-05_religion-culture-legitimacy", "HIL-06_security-coercion", "HIL-07_regional-global-system", "HIL-08_historiography-bias"]
EXPECTED = {"claims": 9, "sources": 37, "bridges": 3, "wiki": 3, "graph": 4, "hils": 8}


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    result = subprocess.run(command, cwd=REPO, text=True, capture_output=True)
    if result.returncode:
        if result.stdout:
            print(result.stdout, end="", file=sys.stderr)
        if result.stderr:
            print(result.stderr, end="", file=sys.stderr)
        raise RuntimeError(f"command failed ({result.returncode}): {' '.join(command)}")
    return result


def load_sources() -> list[dict]:
    sources: list[dict] = []
    for path in sorted((PROJECT / "05_sources").glob("source_register*.json")):
        sources.extend(json.loads(path.read_text(encoding="utf-8")))
    return sources


def main() -> int:
    errors: list[str] = []
    for rel in ["project.json", "00_method", "01_arcs", "02_hil", "03_wiki", "04_graph", "05_sources", "06_bridges", "07_drifts", "08_questions", "09_output"]:
        if not (PROJECT / rel).exists():
            errors.append(f"missing canonical scaffold path: {rel}")

    claims = sorted(PROJECT.glob("01_arcs/*/claims/*.json"))
    if len(claims) != EXPECTED["claims"]:
        errors.append(f"claim count {len(claims)} != {EXPECTED['claims']}")
    for path in claims:
        try:
            claim = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            errors.append(f"invalid claim JSON {path}: {exc}")
            continue
        for field in ("id", "type", "claim", "confidence", "zoom", "causal_role", "arc", "source_ids"):
            if field not in claim:
                errors.append(f"{path.name}: missing {field}")
        if claim.get("type") not in STATEMENT_TYPES:
            errors.append(f"{path.name}: invalid statement type {claim.get('type')!r}")
        if claim.get("causal_role") not in CAUSAL_ROLES:
            errors.append(f"{path.name}: invalid causal role {claim.get('causal_role')!r}")
        expected_arc = path.parents[1].name
        if claim.get("arc") != expected_arc:
            errors.append(f"{path.name}: arc {claim.get('arc')!r} != {expected_arc!r}")

    arcs = sorted(path for path in (PROJECT / "01_arcs").iterdir() if path.is_dir())
    if len(arcs) != 3:
        errors.append(f"arc count {len(arcs)} != 3")
    for arc in arcs:
        arc_file = arc / "ARC.md"
        if not arc_file.exists():
            errors.append(f"missing ARC.md: {arc.name}")
            continue
        text = arc_file.read_text(encoding="utf-8")
        for heading in ("## Entry rupture", "## Causal question", "## Exit rupture / bridge forward"):
            if heading not in text:
                errors.append(f"{arc.name}: missing {heading}")

    for hil in HILS:
        path = PROJECT / "02_hil" / hil / "baseline.json"
        if not path.exists():
            errors.append(f"missing HIL baseline: {hil}")
            continue
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("hil_id") != hil:
            errors.append(f"{hil}: mismatched hil_id")
        if "claim_ids" not in payload or "non_findings" not in payload:
            errors.append(f"{hil}: incomplete baseline contract")

    sources = load_sources()
    if len(sources) != EXPECTED["sources"]:
        errors.append(f"source count {len(sources)} != {EXPECTED['sources']}")
    source_ids = {source.get("id") for source in sources}
    if len(source_ids) != len(sources):
        errors.append("duplicate source ids across pre-1948 registers")
    for source in sources:
        if source.get("anchor_role") not in ANCHOR_ROLES:
            errors.append(f"{source.get('id')}: invalid anchor role {source.get('anchor_role')!r}")

    bridges = sorted((PROJECT / "06_bridges").glob("*.json"))
    if len(bridges) != EXPECTED["bridges"]:
        errors.append(f"bridge count {len(bridges)} != {EXPECTED['bridges']}")
    wiki = [path for path in (PROJECT / "03_wiki").rglob("*.md") if path.name.lower() != "readme.md"]
    if len(wiki) != EXPECTED["wiki"]:
        errors.append(f"wiki page count {len(wiki)} != {EXPECTED['wiki']}")
    graph_edges = sum(sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip()) for path in (PROJECT / "04_graph").glob("*.jsonl"))
    if graph_edges != EXPECTED["graph"]:
        errors.append(f"graph edge count {graph_edges} != {EXPECTED['graph']}")
    if not (PROJECT / "08_questions" / "baseline_questions.md").exists():
        errors.append("missing functional question backlog")
    for rel in ("09_output/report_v3_full.md", "09_output/Sri_Lanka_Fresque_historico_geographique_vol_retour_v3.docx"):
        if not (PROJECT / rel).exists():
            errors.append(f"missing reader output: {rel}")

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    try:
        for command in ([sys.executable, "scripts/audit_skill.py", "."], [sys.executable, "scripts/audit_workflow.py", "docs/RUN9_PRE1948_FUNCTIONAL_BASELINE.json"], [sys.executable, "scripts/qa_project.py", "examples/sri_lanka_pre_1948"]):
            run(command)
        rendered = run([sys.executable, "scripts/render_full_reader_v3.py", "--project", "pre"])
    except RuntimeError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    try:
        metric = json.loads(rendered.stdout)[0]
    except Exception as exc:
        print(f"ERROR: invalid renderer metrics: {exc}", file=sys.stderr)
        return 1
    baseline_words = int(metric.get("baseline_docx_words", 0))
    output_words = int(metric.get("v3_docx_words", 0))
    retention = float(metric.get("retention_vs_baseline_percent", 0))
    if metric.get("project") != "pre" or output_words < baseline_words or retention < 100:
        print(f"ERROR: retention gate failed: baseline={baseline_words}, output={output_words}, retention={retention}%", file=sys.stderr)
        return 1

    print("PRE1948 FUNCTIONAL QA OK: " f"{len(claims)} claims, {len(sources)} sources, {len(bridges)} bridges, " f"{len(wiki)} wiki pages, {graph_edges} graph edges, {len(HILS)} HIL baselines, " f"retention {retention}% ({baseline_words} -> {output_words} words)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
