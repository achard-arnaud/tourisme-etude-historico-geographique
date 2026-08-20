#!/usr/bin/env python3
"""Machine-readable output-state resolution for long-form projects."""
from __future__ import annotations
import json
from pathlib import Path

STATE_REL = Path("00_method/output_state.json")


def load_output_state(project: Path) -> dict:
    path = project / STATE_REL
    if not path.exists():
        raise FileNotFoundError(f"missing output state: {path}")
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError(f"unsupported output-state schema in {path}")
    return data


def resolve_state_path(project: Path, key: str, *, must_exist: bool = True) -> Path:
    state = load_output_state(project)
    rel = state.get(key)
    if not rel:
        raise ValueError(f"output state has no {key!r}")
    path = (project / rel).resolve()
    root = project.resolve()
    if root not in path.parents and path != root:
        raise ValueError(f"output-state path escapes project: {rel}")
    if must_exist and not path.exists():
        raise FileNotFoundError(f"output-state target missing for {key}: {rel}")
    return path


def canonical_markdown_path(project: Path) -> Path:
    return resolve_state_path(project, "canonical_markdown")


def reader_markdown_path(project: Path) -> Path:
    return resolve_state_path(project, "reader_markdown")
