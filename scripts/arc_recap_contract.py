#!/usr/bin/env python3
"""Validate and render causal end-of-arc recap artefacts."""
from __future__ import annotations
import json
import re
from pathlib import Path
from output_state import canonical_markdown_path, load_output_state

SCHEMA_VERSION = "1.0"
CLASS = "arc_recap"
STATUSES = {"candidate", "validated", "promoted", "retired"}
RENDERABLE = {"validated", "promoted"}


def load_arc_recaps(project: Path):
    root = project / "09_output" / "arc_recaps"
    out = []
    if not root.exists():
        return out
    for path in sorted(root.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        items = data if isinstance(data, list) else [data]
        out.extend((path, item) for item in items)
    return out


def _load(project: Path, pattern: str) -> set[str]:
    out = set()
    for path in project.glob(pattern):
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            continue
        if isinstance(data, dict) and data.get("id"):
            out.add(data["id"])
    return out


def _norm(text: str) -> str:
    return re.sub(r"[*_`]", "", text).strip().casefold()


def _anchor_resolves(markdown: str, anchor: str) -> bool:
    needle = _norm(anchor)
    return any(needle in _norm(line).lstrip("# ") for line in markdown.splitlines())


def render_arc_recap_markdown(item: dict) -> str:
    """Render one recap from structured data only; no new historical prose is invented."""
    rid = item["id"]
    arc = item.get("arc", "")
    marker = (item.get("render") or {}).get("marker", f"[ARC-RECAP:{rid}]")
    label = (item.get("render") or {}).get("label", "Récap causal")
    lines = [f"<!-- {marker} -->", f"### {label} — {arc}", "", "**Schéma causal**"]
    labels = {"drivers": "Moteurs", "amplifiers": "Amplificateurs", "constraints": "Contraintes", "consequences": "Conséquences"}
    causal = item.get("causal_schema") or {}
    for key in ("drivers", "amplifiers", "constraints", "consequences"):
        rows = causal.get(key) or []
        summaries = [row.get("summary", "").strip() for row in rows if isinstance(row, dict) and row.get("summary")]
        if summaries:
            lines.append(f"- **{labels[key]}** : " + " ; ".join(summaries))
    protagonists = item.get("protagonists") or []
    if protagonists:
        lines.extend(["", "**Du point de vue des protagonistes**"])
        for actor in protagonists:
            detail = []
            if actor.get("objective"):
                detail.append(f"objectif : {actor['objective']}")
            if actor.get("constraints"):
                detail.append("contraintes : " + ", ".join(actor["constraints"]))
            if actor.get("perceived_options"):
                detail.append("options perçues : " + ", ".join(actor["perceived_options"]))
            role = f" ({actor['role']})" if actor.get("role") else ""
            lines.append(f"- **{actor.get('name', 'Acteur')}{role}** — " + " ; ".join(detail))
    changed = item.get("what_changed") or []
    if changed:
        lines.extend(["", "**Ce qui change à la fin de l’arc**"])
        lines.extend(f"- {value}" for value in changed)
    teasers = item.get("prepares_next") or []
    if teasers:
        lines.extend(["", "**Ce que cela prépare pour la suite**"])
        lines.extend(f"- {row['bullet']}" for row in teasers if row.get("bullet"))
    lines.extend(["", f"<!-- [/ARC-RECAP:{rid}] -->"])
    return "\n".join(lines)


def assert_rendered_arc_recaps(project: Path, markdown: str) -> int:
    required = [item for _, item in load_arc_recaps(project) if item.get("status") in RENDERABLE and (item.get("render") or {}).get("required_in_reader")]
    for item in required:
        marker = (item.get("render") or {}).get("marker")
        if markdown.count(marker) != 1:
            raise RuntimeError(f"required arc recap {item.get('id')} must appear exactly once in rendered Markdown")
    return len(required)


def validate_arc_recaps(project: Path, check_render: bool = False) -> tuple[list[str], list[str], int]:
    errors = []
    warnings = []
    recaps = load_arc_recaps(project)
    arcs = {p.name for p in (project / "01_arcs").iterdir() if p.is_dir() and (p / "ARC.md").exists()} if (project / "01_arcs").exists() else set()
    claims = _load(project, "01_arcs/*/claims/*.json")
    bridges = _load(project, "06_bridges/*.json")
    by_arc = {}
    seen = set()
    canonical_text = None
    try:
        canonical = canonical_markdown_path(project)
        canonical_text = canonical.read_text(encoding="utf-8") if canonical.exists() else None
    except Exception:
        canonical_text = None

    for path, item in recaps:
        rid = item.get("id")
        arc = item.get("arc")
        status = item.get("status")
        if item.get("schema_version") != SCHEMA_VERSION or item.get("class") != CLASS:
            errors.append(f"arc recap {rid or path.name}: invalid class/schema")
        if not rid or rid in seen:
            errors.append(f"arc recap {rid or path.name}: missing/duplicate id")
        else:
            seen.add(rid)
        if status not in STATUSES:
            errors.append(f"arc recap {rid}: invalid status")
        if status in RENDERABLE and arc not in arcs:
            errors.append(f"arc recap {rid}: unknown materialized arc {arc!r}")
        by_arc.setdefault(arc, []).append(item)

        causal = item.get("causal_schema") or {}
        for key in ("drivers", "amplifiers", "constraints", "consequences"):
            values = causal.get(key)
            if not isinstance(values, list):
                errors.append(f"arc recap {rid}: causal_schema.{key} must be list")
            else:
                for row in values:
                    cid = row.get("claim_id") if isinstance(row, dict) else None
                    if cid and cid not in claims:
                        errors.append(f"arc recap {rid}: unknown claim {cid}")
                    if status in RENDERABLE and (not isinstance(row, dict) or not row.get("summary")):
                        errors.append(f"arc recap {rid}: causal row requires summary")

        protagonists = item.get("protagonists") or []
        if status in RENDERABLE and not protagonists:
            errors.append(f"arc recap {rid}: protagonists required")
        for actor in protagonists:
            for cid in actor.get("claim_ids") or []:
                if cid not in claims:
                    errors.append(f"arc recap {rid}: protagonist unknown claim {cid}")
        if status in RENDERABLE and not (item.get("what_changed") or []):
            errors.append(f"arc recap {rid}: what_changed required")
        teasers = item.get("prepares_next") or []
        if status in RENDERABLE and not teasers:
            errors.append(f"arc recap {rid}: prepares_next required")
        for row in teasers:
            if not row.get("bullet"):
                errors.append(f"arc recap {rid}: empty teaser bullet")
            for bid in row.get("bridge_ids") or []:
                if bid not in bridges:
                    errors.append(f"arc recap {rid}: unknown teaser bridge {bid}")

        render = item.get("render") or {}
        marker = render.get("marker")
        if marker != f"[ARC-RECAP:{rid}]":
            errors.append(f"arc recap {rid}: invalid marker")
        if status in RENDERABLE and render.get("required_in_reader"):
            anchor = (item.get("placement") or {}).get("before_anchor")
            if not anchor:
                errors.append(f"arc recap {rid}: placement.before_anchor required")
            elif canonical_text is not None and not _anchor_resolves(canonical_text, anchor):
                errors.append(f"arc recap {rid}: placement anchor not found in canonical Markdown: {anchor!r}")

    try:
        required = bool(load_output_state(project).get("composition", {}).get("require_arc_recaps"))
    except Exception:
        required = False
    if required:
        missing = sorted(arc for arc in arcs if not any(item.get("status") in RENDERABLE for item in by_arc.get(arc, [])))
        if missing:
            errors.append("missing validated arc recaps: " + ", ".join(missing))
    if check_render and canonical_text is not None:
        try:
            assert_rendered_arc_recaps(project, canonical_text)
        except Exception as exc:
            errors.append(str(exc))
    return errors, warnings, len(recaps)
