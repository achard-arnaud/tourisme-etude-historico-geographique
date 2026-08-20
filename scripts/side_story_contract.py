#!/usr/bin/env python3
"""Shared contract and validation helpers for narrative side-story artifacts."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

SCHEMA_VERSION = "1.0"
SIDE_STORY_CLASS = "side_story"
KINDS = {
    "detour",
    "dezoom",
    "also",
    "method",
    "false_lead",
    "portrait",
    "object_focus",
    "comparator",
    "callback",
}
STATUSES = {"candidate", "validated", "promoted", "retired"}
READER_PRESETS = {"advanced", "intermediate", "child"}
ZOOMS = {f"Z{i}" for i in range(5)}
HILS = {
    "HIL-01_institutions-chronology",
    "HIL-02_geography-environment",
    "HIL-03_economy-infrastructure",
    "HIL-04_society-demography",
    "HIL-05_religion-culture-legitimacy",
    "HIL-06_security-coercion",
    "HIL-07_regional-global-system",
    "HIL-08_historiography-bias",
}
RENDER_LABELS = {
    "detour": "Petit détour",
    "dezoom": "Dézoom",
    "also": "Mais aussi",
    "method": "Point de méthode",
    "false_lead": "Fausse piste",
    "portrait": "Personnage",
    "object_focus": "Objet / terrain",
    "comparator": "Comparaison",
    "callback": "Fil rouge",
}


def canonical_marker(side_story_id: str) -> str:
    return f"[SIDE-STORY:{side_story_id}]"


def side_story_dir(project: Path) -> Path:
    return project / "09_output" / "side_stories"


def load_side_stories(project: Path) -> list[tuple[Path, dict]]:
    root = side_story_dir(project)
    if not root.exists():
        return []
    items: list[tuple[Path, dict]] = []
    for path in sorted(root.glob("*.json")):
        items.append((path, json.loads(path.read_text(encoding="utf-8"))))
    return items


def _load_sources(project: Path) -> set[str]:
    ids: set[str] = set()
    for path in sorted((project / "05_sources").glob("source_register*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        if isinstance(data, list):
            ids.update(str(item.get("id")) for item in data if isinstance(item, dict) and item.get("id"))
    return ids


def _load_claims(project: Path) -> set[str]:
    ids: set[str] = set()
    for path in project.glob("01_arcs/*/claims/*.json"):
        item = json.loads(path.read_text(encoding="utf-8"))
        if item.get("id"):
            ids.add(str(item["id"]))
    return ids


def _load_bridges(project: Path) -> set[str]:
    ids: set[str] = set()
    for path in (project / "06_bridges").glob("*.json"):
        item = json.loads(path.read_text(encoding="utf-8"))
        if item.get("id"):
            ids.add(str(item["id"]))
    return ids


def _load_arcs(project: Path) -> set[str]:
    root = project / "01_arcs"
    return {path.name for path in root.iterdir() if path.is_dir()} if root.exists() else set()


def _nonempty_lineage(lineage: dict) -> bool:
    return any(lineage.get(key) for key in ("claim_ids", "source_ids", "bridge_ids", "drift_paths", "origin_paths"))


def validate_side_stories(project: Path, *, check_render: bool = True) -> tuple[list[str], list[str], int]:
    """Validate side-story structure, lineage and promotion/render invariants.

    Candidate records may point to an arc or evidence that does not yet exist. Once a
    record is `validated` or `promoted`, every lineage reference becomes a hard
    contract. A promoted required side story must be present in canonical Markdown;
    the final reader gate is enforced again by ``assert_rendered_side_stories``.
    """

    errors: list[str] = []
    warnings: list[str] = []
    try:
        stories = load_side_stories(project)
        claim_ids = _load_claims(project)
        source_ids = _load_sources(project)
        bridge_ids = _load_bridges(project)
        arcs = _load_arcs(project)
    except Exception as exc:
        return [f"invalid side-story registry: {exc}"], [], 0

    seen: set[str] = set()
    canonical_path = project / "09_output" / "report.md"
    canonical = canonical_path.read_text(encoding="utf-8") if canonical_path.exists() else ""

    for path, item in stories:
        sid = item.get("id")
        prefix = sid or path.name
        if item.get("schema_version") != SCHEMA_VERSION:
            errors.append(f"side story {prefix}: invalid schema_version")
        if item.get("class") != SIDE_STORY_CLASS:
            errors.append(f"side story {prefix}: invalid class")
        if not sid:
            errors.append(f"side story {path.name}: missing id")
        elif sid in seen:
            errors.append(f"duplicate side story id: {sid}")
        elif path.stem != sid:
            errors.append(f"side story {sid}: filename must equal id")
        else:
            seen.add(sid)
        kind = item.get("kind")
        if kind not in KINDS:
            errors.append(f"side story {prefix}: invalid kind {kind!r}")
        status = item.get("status")
        if status not in STATUSES:
            errors.append(f"side story {prefix}: invalid status {status!r}")
        if not item.get("title") or not item.get("purpose"):
            errors.append(f"side story {prefix}: missing title/purpose")

        lineage = item.get("lineage") or {}
        placement = item.get("placement") or {}
        render = item.get("render") or {}
        presets = set(item.get("reader_presets") or [])
        for key in ("claim_ids", "source_ids", "bridge_ids", "hil_ids", "drift_paths", "origin_paths"):
            if not isinstance(lineage.get(key, []), list):
                errors.append(f"side story {prefix}: lineage.{key} must be a list")
        if not presets <= READER_PRESETS:
            errors.append(f"side story {prefix}: invalid reader preset")
        if not placement.get("section_anchor") or not placement.get("return_to"):
            errors.append(f"side story {prefix}: missing placement section_anchor/return_to")

        expected_marker = canonical_marker(str(sid)) if sid else None
        if render.get("marker") != expected_marker:
            errors.append(f"side story {prefix}: invalid render marker")
        if kind in RENDER_LABELS and render.get("label") != RENDER_LABELS[kind]:
            errors.append(f"side story {prefix}: render label does not match kind")
        if not isinstance(render.get("required_in_reader"), bool):
            errors.append(f"side story {prefix}: required_in_reader must be boolean")

        strict = status in {"validated", "promoted"}
        if strict:
            if not _nonempty_lineage(lineage):
                errors.append(f"side story {prefix}: validated/promoted item has no lineage")
            if item.get("arc") not in arcs:
                errors.append(f"side story {prefix}: unknown arc {item.get('arc')!r}")
            unknown_claims = set(lineage.get("claim_ids") or []) - claim_ids
            unknown_sources = set(lineage.get("source_ids") or []) - source_ids
            unknown_bridges = set(lineage.get("bridge_ids") or []) - bridge_ids
            unknown_hils = set(lineage.get("hil_ids") or []) - HILS
            if unknown_claims:
                errors.append(f"side story {prefix}: unknown claims {sorted(unknown_claims)}")
            if unknown_sources:
                errors.append(f"side story {prefix}: unknown sources {sorted(unknown_sources)}")
            if unknown_bridges:
                errors.append(f"side story {prefix}: unknown bridges {sorted(unknown_bridges)}")
            if unknown_hils:
                errors.append(f"side story {prefix}: unknown HILs {sorted(unknown_hils)}")
            for rel in lineage.get("drift_paths") or []:
                if not (project / rel).exists():
                    errors.append(f"side story {prefix}: missing drift path {rel}")
            for rel in lineage.get("origin_paths") or []:
                if not (project / rel).exists():
                    errors.append(f"side story {prefix}: missing origin path {rel}")

        if kind == "dezoom":
            excursion = item.get("zoom_excursion") or {}
            for field in ("from", "to", "return_to", "mechanism", "local_payoff"):
                if not excursion.get(field):
                    errors.append(f"side story {prefix}: dezoom missing {field}")
            for field in ("from", "to", "return_to"):
                if excursion.get(field) and excursion.get(field) not in ZOOMS:
                    errors.append(f"side story {prefix}: invalid dezoom {field} {excursion.get(field)!r}")
        elif item.get("zoom_excursion") not in (None, {}):
            warnings.append(f"side story {prefix}: zoom_excursion ignored for non-dezoom kind")

        if check_render and status == "promoted":
            marker = render.get("marker")
            if marker and marker not in canonical:
                errors.append(f"side story {prefix}: promoted marker missing from canonical report")

    return errors, warnings, len(stories)


def assert_rendered_side_stories(project: Path, markdown: str) -> None:
    """Fail if a promoted reader-required side story vanished during rendering."""
    missing: list[str] = []
    for _, item in load_side_stories(project):
        if item.get("status") != "promoted":
            continue
        render = item.get("render") or {}
        if not render.get("required_in_reader"):
            continue
        marker = render.get("marker")
        if marker and marker not in markdown:
            missing.append(str(item.get("id")))
    if missing:
        raise RuntimeError(f"side-story retention gate failed: missing {', '.join(sorted(missing))}")


def validate_or_raise(project: Path, *, check_render: bool = True) -> int:
    errors, warnings, count = validate_side_stories(project, check_render=check_render)
    for warning in warnings:
        print(f"WARN: {warning}")
    if errors:
        raise ValueError("; ".join(errors))
    return count
