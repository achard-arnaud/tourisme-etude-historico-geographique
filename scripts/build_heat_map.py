#!/usr/bin/env python3
"""L0 graph ↔ story-outline heat map; diagnostic only, never a blocking gate."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
from statistics import mean, pstdev

from run_journal import append_entry


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "section"


def _load_edges(project: Path) -> list[dict]:
    out: list[dict] = []
    for path in sorted((project / "04_graph").glob("edges*.jsonl")):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                out.append(json.loads(line))
    return out


def compute_claim_degrees(edges: list[dict]) -> dict[str, int]:
    degrees: dict[str, int] = {}
    for edge in edges:
        for key in ("from", "to"):
            node = edge.get(key)
            if node:
                node = str(node)
                degrees[node] = degrees.get(node, 0) + 1
    return degrees


def flatten_subsections(scaffold: dict) -> list[dict]:
    rows: list[dict] = []
    for arc in scaffold.get("arcs", []):
        arc_id = str(arc.get("arc") or arc.get("id") or "")
        rows.append({
            "id": arc_id,
            "title": arc.get("title", arc_id),
            "level": 1,
            "claim_ids": list(arc.get("spine_claim_ids") or []),
        })
        for index, subsection in enumerate(arc.get("subsections") or [], 1):
            title = str(subsection.get("title") or f"section-{index}")
            rows.append({
                "id": subsection.get("id") or f"{arc_id}::{_slug(title)}",
                "title": title,
                "level": int(subsection.get("level") or 2),
                "claim_ids": list(subsection.get("claim_ids") or []),
            })
    return rows


def build_heat_map(project: Path, scaffold: dict) -> dict:
    """Pure degree calculation. No claim prose is loaded."""
    degrees = compute_claim_degrees(_load_edges(project))
    all_claim_ids = [cid for arc in scaffold.get("arcs", []) for cid in arc.get("spine_claim_ids", [])]
    claim_degrees = [degrees.get(str(cid), 0) for cid in all_claim_ids]
    global_mean = mean(claim_degrees) if claim_degrees else 0.0
    global_std = pstdev(claim_degrees) if len(claim_degrees) > 1 else 0.0
    hot_threshold = global_mean + global_std

    sections = []
    for section in flatten_subsections(scaffold):
        claim_ids = [str(x) for x in section["claim_ids"]]
        if not claim_ids:
            avg = None
            status = "unmapped"
        else:
            avg = mean(degrees.get(cid, 0) for cid in claim_ids)
            # The definitions can overlap when mean+std < 1. Hot wins because it
            # denotes relative concentration; cold applies only after that test.
            if avg > hot_threshold:
                status = "hot"
            elif avg <= 1:
                status = "cold"
            else:
                status = "normal"
        sections.append({**section, "avg_degree": avg, "status": status})

    return {
        "project": project.name,
        "global_mean_degree": round(global_mean, 3),
        "global_std_degree": round(global_std, 3),
        "hot_threshold": round(hot_threshold, 3),
        "sections": sections,
    }


def render_markdown(data: dict, run: int) -> str:
    lines = [
        f"# Heat map — Run {run}",
        "",
        f"Projet : `{data['project']}`",
        "",
        "Diagnostic L0 uniquement. `hot/cold` indique la connectivité du graphe, pas l'importance historique intrinsèque.",
        "Les sous-sections sans `claim_ids` restent `unmapped` : le script refuse d'inventer un mapping à partir des seuls titres.",
        "",
        f"Degré moyen global : **{data['global_mean_degree']}** — écart-type : **{data['global_std_degree']}** — seuil hot : **{data['hot_threshold']}**",
        "",
        "| Section | Niveau | Claims mappés | Degré moyen | Statut |",
        "|---|---:|---:|---:|---|",
    ]
    for row in data["sections"]:
        avg = "—" if row["avg_degree"] is None else f"{row['avg_degree']:.2f}"
        lines.append(f"| {row['title']} | {row['level']} | {len(row['claim_ids'])} | {avg} | {row['status']} |")
    lines.extend([
        "",
        "## Lecture",
        "- **hot** : degré moyen > moyenne globale + 1 écart-type ; priorité sur `cold` si les seuils se chevauchent.",
        "- **cold** : hors zone hot, degré moyen <= 1 ; zone orpheline ou quasi-orpheline à inspecter.",
        "- **unmapped** : section présente au scaffold sans mapping explicite de claim ; dette de structuration, pas preuve d'absence de matière.",
        "",
    ])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--run", type=int, required=True)
    parser.add_argument("--output")
    args = parser.parse_args()

    repo = Path(__file__).resolve().parents[1]
    project = Path(args.project)
    if not project.is_absolute():
        project = repo / project
    scaffold_path = project / "09_output" / "story_scaffold.json"
    scaffold = json.loads(scaffold_path.read_text(encoding="utf-8"))
    data = build_heat_map(project, scaffold)
    output = Path(args.output) if args.output else repo / "docs" / f"HEAT_MAP_RUN{args.run}.md"
    if not output.is_absolute():
        output = repo / output
    output.write_text(render_markdown(data, args.run), encoding="utf-8")
    append_entry(
        repo,
        args.run,
        "Heat map graphe ↔ sommaire",
        [str(output.relative_to(repo))],
        "story_scaffold disponible",
        f"OK — {len(data['sections'])} sections classées; diagnostic non bloquant",
    )
    print(output.relative_to(repo))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
