#!/usr/bin/env python3
"""Build arc-local drafting packets without reading any previous reader prose.

Run 26 uses these packets as the only prose-generation inputs. The builder may read
structured composition artefacts (side stories, recaps, illustrations) but refuses
reader Markdown, DOCX, archives and generated reader plans/scaffolds. This makes the
from-scratch vs iterative comparison auditable rather than rhetorical.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Iterable

REPO = Path(__file__).resolve().parents[1]

FORBIDDEN_PARTS = (
    "/09_output/report",
    "/09_output/archive/",
    "/09_output/story_scaffold.json",
    "/09_output/reader_plan.json",
)
FORBIDDEN_SUFFIXES = {".docx", ".pdf"}
ALLOWED_STRUCTURED_OUTPUT_ROOTS = {
    "side_stories",
    "arc_recaps",
    "illustrations",
    "maps",
}


class ReadLedger:
    def __init__(self, project: Path):
        self.project = project.resolve()
        self.paths: list[str] = []

    def _check(self, path: Path) -> None:
        resolved = path.resolve()
        try:
            rel = resolved.relative_to(self.project)
        except ValueError as exc:
            raise RuntimeError(f"from-scratch read escaped project: {path}") from exc
        key = "/" + rel.as_posix()
        if path.suffix.lower() in FORBIDDEN_SUFFIXES:
            raise RuntimeError(f"from-scratch reader-prose contamination blocked: {rel}")
        if any(token in key for token in FORBIDDEN_PARTS):
            raise RuntimeError(f"from-scratch reader-prose contamination blocked: {rel}")
        if rel.parts and rel.parts[0] == "09_output":
            if len(rel.parts) < 2 or rel.parts[1] not in ALLOWED_STRUCTURED_OUTPUT_ROOTS:
                raise RuntimeError(f"from-scratch generated-output read blocked: {rel}")
        self.paths.append(rel.as_posix())

    def text(self, path: Path) -> str:
        self._check(path)
        return path.read_text(encoding="utf-8")

    def json(self, path: Path) -> Any:
        return json.loads(self.text(path))


def as_records(data: Any) -> list[dict]:
    if isinstance(data, dict):
        return [data]
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    return []


def load_records(ledger: ReadLedger, paths: Iterable[Path]) -> list[dict]:
    records: list[dict] = []
    for path in sorted(paths):
        try:
            records.extend(as_records(ledger.json(path)))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
    return records


def walk(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)


def fragment_refs(item: dict) -> set[str]:
    refs: set[str] = set()
    for node in walk(item):
        for ref in node.get("input_refs") or []:
            if isinstance(ref, dict) and ref.get("id"):
                refs.add(str(ref["id"]))
            elif isinstance(ref, str):
                refs.add(ref)
        for key in ("fragment_ids", "origin_fragment_ids", "input_fragment_ids"):
            refs |= {str(x) for x in node.get(key) or []}
    return refs


def fragment_index(project: Path, ledger: ReadLedger) -> dict[str, dict]:
    root = project / "00_method" / "capture"
    out: dict[str, dict] = {}
    if not root.exists():
        return out
    for path in sorted(root.rglob("*.json")):
        try:
            data = ledger.json(path)
        except Exception:
            continue
        for item in walk(data):
            iid = str(item.get("id") or "")
            if iid.startswith(("GF-", "FRAG-", "FIELD-")) or item.get("class") in {"fragment", "field_fragment"}:
                out[iid] = item
    return out


def claim_hils(claim: dict) -> set[str]:
    out: set[str] = set()
    value = claim.get("hil")
    if isinstance(value, str) and value:
        out.add(value)
    for value in claim.get("hil_ids") or []:
        if isinstance(value, str) and value:
            out.add(value)
    return out


def source_register(project: Path, ledger: ReadLedger) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for path in sorted((project / "05_sources").glob("source_register*.json")):
        for item in as_records(ledger.json(path)):
            if item.get("id"):
                out[str(item["id"])] = item
    return out


def side_stories(project: Path, ledger: ReadLedger) -> list[dict]:
    stories = load_records(ledger, (project / "09_output" / "side_stories").glob("*.json"))
    safe: list[dict] = []
    for item in stories:
        copy = json.loads(json.dumps(item, ensure_ascii=False))
        # Legacy backfill may carry prose copied from an old reader. Keep only its
        # structured placement/lineage metadata so it cannot seed the new wording.
        if copy.get("lineage_quality") == "legacy_fragment":
            content = copy.get("content") or {}
            copy["content"] = {
                key: value for key, value in content.items()
                if key in {"takeaway", "legacy_titles"}
            }
            copy["legacy_reader_prose_redacted"] = True
        safe.append(copy)
    return safe


def all_questions(project: Path, ledger: ReadLedger) -> list[dict]:
    root = project / "08_questions"
    if not root.exists():
        return []
    return load_records(ledger, root.glob("*.json"))


def bridge_matches(bridge: dict, claim_ids: set[str], arc_id: str) -> bool:
    endpoints = {
        str(bridge.get(key) or "")
        for key in ("from_claim", "to_claim", "from", "to")
    }
    if endpoints & claim_ids:
        return True
    return arc_id in {
        str(bridge.get("arc") or ""),
        str(bridge.get("from_arc") or ""),
        str(bridge.get("to_arc") or ""),
    }


def story_matches(story: dict, claim_ids: set[str], arc_id: str) -> bool:
    if str(story.get("arc") or "") == arc_id:
        return True
    lineage = story.get("lineage") or {}
    return bool({str(x) for x in lineage.get("claim_ids") or []} & claim_ids)


def question_matches(question: dict, claim_ids: set[str], arc_id: str) -> bool:
    if str(question.get("arc") or "") == arc_id:
        return True
    linked = set()
    for key in ("claim_ids", "related_claim_ids", "target_claim_ids"):
        linked |= {str(x) for x in question.get(key) or []}
    return bool(linked & claim_ids)


def selected_source_ids(*groups: Iterable[dict]) -> set[str]:
    out: set[str] = set()
    for group in groups:
        for item in group:
            out |= {str(x) for x in item.get("source_ids") or []}
            lineage = item.get("lineage") or {}
            out |= {str(x) for x in lineage.get("source_ids") or []}
    return out


def build_packet(project: Path, arc_dir: Path, shared: dict, ledger: ReadLedger) -> dict:
    arc_id = arc_dir.name
    arc_path = arc_dir / "ARC.md"
    arc_note = ledger.text(arc_path) if arc_path.exists() else ""
    claims = load_records(ledger, (arc_dir / "claims").glob("*.json")) if (arc_dir / "claims").exists() else []
    claim_ids = {str(item["id"]) for item in claims if item.get("id")}

    bridges = [item for item in shared["bridges"] if bridge_matches(item, claim_ids, arc_id)]
    stories = [item for item in shared["side_stories"] if story_matches(item, claim_ids, arc_id)]
    questions = [item for item in shared["questions"] if question_matches(item, claim_ids, arc_id)]

    hils: dict[str, dict[str, list[str]]] = {}
    for claim in claims:
        cid = str(claim.get("id") or "")
        for hil in sorted(claim_hils(claim)):
            hils.setdefault(hil, {"claim_ids": [], "side_story_ids": []})["claim_ids"].append(cid)
    for story in stories:
        sid = str(story.get("id") or "")
        for hil in (story.get("lineage") or {}).get("hil_ids") or []:
            hils.setdefault(str(hil), {"claim_ids": [], "side_story_ids": []})["side_story_ids"].append(sid)

    source_ids = selected_source_ids(claims, bridges, stories)
    sources = [shared["sources"][sid] for sid in sorted(source_ids) if sid in shared["sources"]]

    refs: set[str] = set()
    for item in [*claims, *bridges, *stories]:
        refs |= fragment_refs(item)
    fragments = [shared["fragments"][fid] for fid in sorted(refs) if fid in shared["fragments"]]

    return {
        "schema_version": "1.0",
        "class": "from_scratch_arc_packet",
        "project": project.name,
        "arc": arc_id,
        "drafting_contract": {
            "input_mode": "from_scratch",
            "reader_prose_loaded": False,
            "previous_reader_prose_forbidden": True,
            "allowed_hil_policy": "only HIL dimensions linked to claims/side stories actually used in the paragraph",
            "paragraph_review_state_initial": {
                "checklist_reviewed": False,
                "sarah_style_reviewed": False,
                "hil_scope_reviewed": False,
            },
        },
        "arc_note": arc_note,
        "claims": claims,
        "bridges": bridges,
        "side_story_candidates": stories,
        "questions": questions,
        "relevant_hil": hils,
        "sources": sources,
        "fragments": fragments,
        "counts": {
            "claims": len(claims),
            "bridges": len(bridges),
            "side_stories": len(stories),
            "questions": len(questions),
            "hils": len(hils),
            "sources": len(sources),
            "fragments": len(fragments),
        },
    }


def build_packets(project: Path, output: Path) -> dict:
    project = project.resolve()
    ledger = ReadLedger(project)
    shared = {
        "sources": source_register(project, ledger),
        "fragments": fragment_index(project, ledger),
        "bridges": load_records(ledger, (project / "06_bridges").glob("*.json")),
        "side_stories": side_stories(project, ledger),
        "questions": all_questions(project, ledger),
    }
    output.mkdir(parents=True, exist_ok=True)
    packet_paths: list[str] = []
    summaries: list[dict] = []
    for arc_dir in sorted(path for path in (project / "01_arcs").iterdir() if path.is_dir()):
        packet = build_packet(project, arc_dir, shared, ledger)
        path = output / f"{arc_dir.name}.json"
        path.write_text(json.dumps(packet, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        packet_paths.append(path.name)
        summaries.append({"arc": arc_dir.name, **packet["counts"]})

    manifest = {
        "schema_version": "1.0",
        "class": "from_scratch_packet_manifest",
        "project": project.name,
        "packet_paths": packet_paths,
        "arc_summaries": summaries,
        "read_ledger": sorted(set(ledger.paths)),
        "contamination_check": {
            "passed": True,
            "forbidden_patterns": list(FORBIDDEN_PARTS),
            "forbidden_suffixes": sorted(FORBIDDEN_SUFFIXES),
            "reader_prose_loaded": False,
        },
    }
    (output / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--output")
    args = parser.parse_args()
    project = Path(args.project)
    project = project if project.is_absolute() else REPO / project
    output = Path(args.output) if args.output else project / "09_output" / "from_scratch" / "packets"
    output = output if output.is_absolute() else REPO / output
    manifest = build_packets(project, output)
    print(json.dumps({
        "project": manifest["project"],
        "arcs": len(manifest["packet_paths"]),
        "reader_prose_loaded": manifest["contamination_check"]["reader_prose_loaded"],
        "output": str(output.relative_to(REPO)),
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
