#!/usr/bin/env python3
"""Render the existing lossless V3 reader with deterministic structured composition injected first."""
from __future__ import annotations
import argparse
import json
from arc_recap_contract import assert_rendered_arc_recaps
from materialize_arc_recaps import materialize_arc_recaps
import render_full_reader_v3 as base


def build(key: str) -> dict:
    spec = base.SPECS[key]
    project = spec["project"]
    delta_path = project / "09_output" / spec["delta"]
    original = delta_path.read_bytes()
    recap_count = 0
    try:
        composed, recap_count = materialize_arc_recaps(project, original.decode("utf-8"))
        delta_path.write_text(composed, encoding="utf-8")
        metric = base.build(key)
    finally:
        delta_path.write_bytes(original)
    reader = (project / "09_output" / spec["markdown_output"]).read_text(encoding="utf-8")
    required = assert_rendered_arc_recaps(project, reader)
    if required != recap_count:
        raise RuntimeError(f"arc recap render count mismatch for {key}: materialized={recap_count}, required={required}")
    metric["arc_recaps"] = recap_count
    return metric


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", choices=["pre", "post", "all"], default="all")
    args = parser.parse_args()
    keys = list(base.SPECS) if args.project == "all" else [args.project]
    metrics = [build(key) for key in keys]
    metrics_path = base.REPO / "docs" / "RUN11_COMPOSITION_RENDER_METRICS.json"
    metrics_path.write_text(json.dumps(metrics, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(metrics, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
