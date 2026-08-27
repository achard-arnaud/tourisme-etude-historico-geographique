#!/usr/bin/env python3
"""Shared drafting-context builder for iterative and from-scratch readers.

Run32 deliberately separates:
- reader scaffold: ordered narrative topology;
- evidence control plane: claims, bridges, questions and source registers;
- narrative material plane: field/capture fragments and archived intakes.

The two generation modes share the same evidence/material packet. They differ
only in their bootstrap:
- iterative: may load the current canonical manuscript + append-only journal;
- from_scratch: loads no previous reader prose.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
from typing import Any, Iterable

from legacy_fragment_bypass import virtual_legacy_statements

REPO = Path(__file__).resolve().parents[1]

FORBIDDEN_FROM_SCRATCH_PARTS = (
    "/09_output/report",
    "/09_output/archive/",
    "/09_output/from_scratch/",
)
FORBIDDEN_FROM_SCRATCH_SUFFIXES = {".docx", ".pdf"}

class ReadLedger:
    """Auditable reads with mode-specific contamination checks."""
    def __init__(self, project: Path, mode: str = "from_scratch"):
        if mode not in {"from_scratch", "iterative"}:
            raise ValueError(f"unsupported drafting mode: {mode}")
        self.project = project.resolve()
        self.mode = mode
        self.paths: list[str] = []

    def _check(self, path: Path) -> None:
        resolved = path.resolve()
        try:
            rel_project = resolved.relative_to(self.project)
            rel_repo = Path(self.project.name) / rel_project
            project_local = True
        except ValueError:
            project_local = False
            try:
                rel_repo = resolved.relative_to(REPO.resolve())
            except ValueError as exc:
                raise RuntimeError(f"drafting read escaped repository/project: {path}") from exc
        key = "/" + rel_repo.as_posix()
        if self.mode == "from_scratch" and project_local:
            if path.suffix.lower() in FORBIDDEN_FROM_SCRATCH_SUFFIXES:
                raise RuntimeError(f"from-scratch reader-prose contamination blocked: {rel_repo}")
            if any(token in key for token in FORBIDDEN_FROM_SCRATCH_PARTS):
                structured = any(
                    token in key
                    for token in (
                        "/09_output/side_stories/",
                        "/09_output/arc_recaps/",
                        "/09_output/illustrations/",
                        "/09_output/maps/",
                        "/09_output/map_assets/",
                        "/09_output/reader_scaffold.json",
                        "/09_output/story_scaffold.json",
                    )
                )
                if not structured:
                    raise RuntimeError(f"from-scratch reader-prose contamination blocked: {rel_repo}")
        self.paths.append(rel_repo.as_posix())

    def text(self, path: Path) -> str:
        self._check(path)
        return path.read_text(encoding="utf-8")

    def json(self, path: Path) -> Any:
        return json.loads(self.text(path))

def as_records(data: Any) -> list[dict]:
    if isinstance(data, dict):
        out = []
        for key in ("fragments", "items", "records", "questions", "claims", "bridges", "side_stories", "sources"):
            if isinstance(data.get(key), list):
                out.extend(x for x in data[key] if isinstance(x, dict))
        if data.get("id"):
            out.append(data)
        return out
    if isinstance(data, list):
        return [x for x in data if isinstance(x, dict)]
    return []

def load_records(ledger: ReadLedger, paths: Iterable[Path]) -> list[dict]:
    out: list[dict] = []
    for path in sorted(paths):
        try:
            out.extend(as_records(ledger.json(path)))
        except (json.JSONDecodeError, UnicodeDecodeError):
            continue
    return out

def walk(value: Any):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk(child)

def fragment_index(project: Path, ledger: ReadLedger) -> dict[str, dict]:
    """Index all captured fragments, including nested records."""
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
                row = json.loads(json.dumps(item, ensure_ascii=False))
                row.setdefault("_capture_path", str(path.relative_to(project)))
                out[iid] = row
    return out

def fragment_refs(item: dict) -> set[str]:
    refs: set[str] = set()
    for node in walk(item):
        for ref in node.get("input_refs") or []:
            if isinstance(ref, dict) and ref.get("id"):
                refs.add(str(ref["id"]))
            elif isinstance(ref, str):
                refs.add(ref)
        for key in ("fragment_ids", "origin_fragment_ids", "input_fragment_ids"):
            refs |= {str(x) for x in node.get(key) or [] if x}
    return refs

def source_register(project: Path, ledger: ReadLedger) -> dict[str, dict]:
    out: dict[str, dict] = {}
    root = project / "05_sources"
    if not root.exists():
        return out
    for path in sorted(root.glob("source_register*.json")):
        for item in as_records(ledger.json(path)):
            if item.get("id"):
                out[str(item["id"])] = item
    return out

def claim_hils(claim: dict) -> set[str]:
    out = set()
    if isinstance(claim.get("hil"), str) and claim["hil"]:
        out.add(claim["hil"])
    out |= {str(x) for x in claim.get("hil_ids") or [] if x}
    return out

def _records(project: Path, ledger: ReadLedger, pattern: str) -> list[dict]:
    return load_records(ledger, project.glob(pattern))

def _bridge_matches(item: dict, claim_ids: set[str], arc_id: str) -> bool:
    endpoints = {str(item.get(k) or "") for k in ("from_claim", "to_claim", "from", "to")}
    if endpoints & claim_ids:
        return True
    return arc_id in {str(item.get(k) or "") for k in ("arc", "from_arc", "to_arc")}

def _story_matches(item: dict, claim_ids: set[str], arc_id: str) -> bool:
    if str(item.get("arc") or "") == arc_id:
        return True
    return bool({str(x) for x in (item.get("lineage") or {}).get("claim_ids") or []} & claim_ids)

def _question_matches(item: dict, claim_ids: set[str], arc_id: str) -> bool:
    if str(item.get("arc") or "") == arc_id:
        return True
    linked = set()
    for key in ("claim_ids", "related_claim_ids", "target_claim_ids"):
        linked |= {str(x) for x in item.get(key) or []}
    return bool(linked & claim_ids)

def _source_ids(*groups: Iterable[dict]) -> set[str]:
    out = set()
    for group in groups:
        for item in group:
            out |= {str(x) for x in item.get("source_ids") or []}
            out |= {str(x) for x in (item.get("lineage") or {}).get("source_ids") or []}
    return out

def _reader_scaffold(project: Path, ledger: ReadLedger) -> dict:
    path = project / "09_output" / "reader_scaffold.json"
    if not path.exists():
        return {"schema_version":"1.0","class":"reader_scaffold","source":"missing","nodes":[]}
    return ledger.json(path)

def _story_scaffold(project: Path, ledger: ReadLedger) -> dict:
    path = project / "09_output" / "story_scaffold.json"
    return ledger.json(path) if path.exists() else {}

def _intake_material(arc_id: str, project: Path, ledger: ReadLedger) -> list[dict]:
    """Load archived intakes as narrative/research context, never as evidence."""
    registry = REPO / "docs" / "intakes" / "intake_registry.json"
    if not registry.exists():
        return []
    try:
        rows = json.loads(ledger.text(registry))
    except Exception:
        return []
    out = []
    for row in rows if isinstance(rows, list) else []:
        repo_path = row.get("repo_path")
        if row.get("preservation_status") != "archived" or not repo_path:
            continue
        ipath = REPO / repo_path
        if not ipath.exists():
            continue
        try:
            text = ledger.text(ipath)
        except Exception:
            continue
        output_paths = " ".join(str(x) for x in row.get("outputs") or [])
        relevant = arc_id in output_paths or re.search(rf"\b{re.escape(arc_id)}\b", text) is not None
        if not relevant:
            continue
        out.append({
            "id": row.get("id"),
            "path": repo_path,
            "intake_kind": row.get("intake_kind"),
            "evidence_role": "research_trigger_not_evidence",
            "text": text,
        })
    return out

def _display_path(path: Path, project: Path) -> str:
    for base in (REPO.resolve(), project.resolve()):
        try:
            return str(path.resolve().relative_to(base))
        except ValueError:
            continue
    return str(path)

def _iterative_bootstrap(project: Path, ledger: ReadLedger, journal: Path | None) -> dict:
    output = project / "09_output"
    candidates = [output/"report_v3_full.md", output/"report.md"]
    manuscript = next((p for p in candidates if p.exists()), None)
    data = {
        "mode":"iterative",
        "reader_prose_loaded": manuscript is not None,
        "canonical_manuscript_path": None,
        "canonical_manuscript": "",
        "construction_journal_path": None,
        "construction_journal": "",
    }
    if manuscript:
        data["canonical_manuscript_path"] = _display_path(manuscript, project)
        data["canonical_manuscript"] = ledger.text(manuscript)
    if journal and journal.exists():
        data["construction_journal_path"] = _display_path(journal, project)
        data["construction_journal"] = ledger.text(journal)
    return data

def _from_scratch_bootstrap() -> dict:
    return {
        "mode":"from_scratch",
        "reader_prose_loaded":False,
        "canonical_manuscript_path":None,
        "canonical_manuscript":"",
        "construction_journal_path":None,
        "construction_journal":"",
    }

def build_packet(project: Path, arc_dir: Path, shared: dict, ledger: ReadLedger, mode: str, journal: Path|None) -> dict:
    arc_id = arc_dir.name
    arc_path = arc_dir / "ARC.md"
    arc_note = ledger.text(arc_path) if arc_path.exists() else ""
    claims = load_records(ledger, (arc_dir/"claims").glob("*.json")) if (arc_dir/"claims").exists() else []
    claim_ids = {str(x["id"]) for x in claims if x.get("id")}
    bridges = [x for x in shared["bridges"] if _bridge_matches(x, claim_ids, arc_id)]
    stories = [x for x in shared["side_stories"] if _story_matches(x, claim_ids, arc_id)]
    questions = [x for x in shared["questions"] if _question_matches(x, claim_ids, arc_id)]

    refs=set()
    for item in [*claims,*bridges,*stories]:
        refs |= fragment_refs(item)
    linked_fragments=[shared["fragments"][fid] for fid in sorted(refs) if fid in shared["fragments"]]
    candidate_arc_fragments=[
        item for fid,item in sorted(shared["fragments"].items())
        if str(item.get("candidate_arc") or item.get("arc") or "") == arc_id and fid not in refs
    ]
    fragments=linked_fragments+candidate_arc_fragments

    hils={}
    for c in claims:
        for hil in sorted(claim_hils(c)):
            hils.setdefault(hil,{"claim_ids":[],"side_story_ids":[]})["claim_ids"].append(str(c.get("id")))
    for s in stories:
        for hil in (s.get("lineage") or {}).get("hil_ids") or []:
            hils.setdefault(str(hil),{"claim_ids":[],"side_story_ids":[]})["side_story_ids"].append(str(s.get("id")))

    sids=_source_ids(claims,bridges,stories)
    sources=[shared["sources"][sid] for sid in sorted(sids) if sid in shared["sources"]]

    evidence_payload={
        "arc_note":arc_note,
        "claims":claims,
        "bridges":bridges,
        "side_story_candidates":stories,
        "questions":questions,
        "relevant_hil":hils,
        "sources":sources,
        "fragments":fragments,
        "linked_fragments":linked_fragments,
        "unlinked_arc_fragments":candidate_arc_fragments,
        "intakes":_intake_material(arc_id,project,ledger),
        "reader_scaffold":shared["reader_scaffold"],
        "story_scaffold":shared["story_scaffold"],
    }
    bootstrap = _iterative_bootstrap(project, ledger, journal) if mode=="iterative" else _from_scratch_bootstrap()
    return {
        "schema_version":"2.0",
        "class":"drafting_arc_packet",
        "project":project.name,
        "arc":arc_id,
        "drafting_contract":{
            "mode":mode,
            "claim_role":"control_plane_not_reader_prose",
            "fragment_role":"primary_narrative_material",
            "intake_role":"research_context_not_evidence",
            "frontstage_citation_policy":"sources_only_no_claim_ids",
            "reader_scaffold_authoritative":True,
            "reader_prose_loaded": mode=="iterative" and bootstrap.get("reader_prose_loaded", False),
            "previous_reader_prose_forbidden": mode=="from_scratch",
            "allowed_hil_policy":"only HIL dimensions linked to evidence actually used in the paragraph",
            "paragraph_review_state_initial":{
                "checklist_reviewed":False,
                "sarah_style_reviewed":False,
                "hil_scope_reviewed":False,
            },
        },
        "bootstrap":bootstrap,
        "evidence":evidence_payload,
        **{k:evidence_payload[k] for k in ("arc_note","claims","bridges","side_story_candidates","questions","relevant_hil","sources","fragments")},
        "counts":{
            "claims":len(claims),"bridges":len(bridges),"side_stories":len(stories),
            "questions":len(questions),"hils":len(hils),"sources":len(sources),
            "fragments":len(fragments),"unlinked_arc_fragments":len(candidate_arc_fragments),
            "intakes":len(evidence_payload["intakes"]),
        },
    }

def build_packets(project: Path, output: Path, mode: str="iterative", journal: Path|None=None) -> dict:
    project=project.resolve()
    ledger=ReadLedger(project,mode)
    shared={
        "sources":source_register(project,ledger),
        "fragments":fragment_index(project,ledger),
        "bridges":_records(project,ledger,"06_bridges/*.json"),
        "side_stories":_records(project,ledger,"09_output/side_stories/*.json"),
        "questions":_records(project,ledger,"08_questions/*.json"),
        "reader_scaffold":_reader_scaffold(project,ledger),
        "story_scaffold":_story_scaffold(project,ledger),
    }

    all_claims=_records(project,ledger,"01_arcs/*/claims/*.json")
    known_claim_ids={str(c.get("id")) for c in all_claims if c.get("id")}
    claimed_fragment_ids=set()
    for claim in all_claims:
        claimed_fragment_ids |= fragment_refs(claim)
    valid_arcs={p.name for p in (project/"01_arcs").iterdir() if p.is_dir()}
    legacy_virtuals=[
        x for x in virtual_legacy_statements(project,shared["fragments"],claimed_fragment_ids,known_claim_ids)
        if str(x.get("arc") or "") in valid_arcs
    ]
    legacy_by_arc={}
    for item in legacy_virtuals:
        legacy_by_arc.setdefault(str(item["arc"]),[]).append(item)

    output.mkdir(parents=True,exist_ok=True)
    packet_paths=[]; summaries=[]
    for arc_dir in sorted(p for p in (project/"01_arcs").iterdir() if p.is_dir()):
        packet=build_packet(project,arc_dir,shared,ledger,mode,journal)
        items=legacy_by_arc.get(arc_dir.name,[])
        packet["drafting_contract"]["legacy_fragment_bypass"]={
            "enabled":True,
            "virtual_only":True,
            "statement_type":"legacy_fragment",
            "may_preserve_existing_narrative":True,
            "may_establish_new_fact_without_source":False,
            "may_satisfy_sourcing_gate":False,
            "render_type_in_reader":False,
        }
        packet["counts"]["persisted_claims"]=packet["counts"]["claims"]
        packet["counts"]["legacy_virtual_claims"]=len(items)
        if items:
            packet["claims"].extend(items)
            packet["evidence"]["claims"].extend(items)
            packet["evidence"]["legacy_fragments"]=items
            packet["legacy_fragments"]=items
            packet["counts"]["claims"]=len(packet["claims"])
        path=output/f"{arc_dir.name}.json"
        path.write_text(json.dumps(packet,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        packet_paths.append(path.name); summaries.append({"arc":arc_dir.name,**packet["counts"]})
    reader_loaded=False
    if packet_paths:
        first=json.loads((output/packet_paths[0]).read_text(encoding="utf-8"))
        reader_loaded=bool((first.get("bootstrap") or {}).get("reader_prose_loaded"))
    manifest={
        "schema_version":"2.0",
        "class":"drafting_packet_manifest",
        "project":project.name,
        "mode":mode,
        "packet_paths":packet_paths,
        "arc_summaries":summaries,
        "read_ledger":sorted(set(ledger.paths)),
        "contamination_check":{
            "passed":True,
            "reader_prose_loaded":reader_loaded,
        },
        "legacy_fragment_bypass":{
            "enabled":True,
            "virtual_claim_count":len(legacy_virtuals),
            "virtual_claim_ids":[x["id"] for x in legacy_virtuals],
            "policy":"allowlisted unsourced legacy debt only; no evidentiary upgrade",
        },
    }
    (output/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return manifest

def main()->int:
    p=argparse.ArgumentParser()
    p.add_argument("--project",required=True)
    p.add_argument("--mode",choices=["iterative","from_scratch"],default="iterative")
    p.add_argument("--output")
    p.add_argument("--journal")
    a=p.parse_args()
    project=Path(a.project); project=project if project.is_absolute() else REPO/project
    output=Path(a.output) if a.output else project/"09_output"/"drafting"/a.mode/"packets"
    output=output if output.is_absolute() else REPO/output
    journal=Path(a.journal) if a.journal else (REPO/"docs"/"RUN25_JOURNAL.md" if a.mode=="iterative" else None)
    if journal and not journal.is_absolute(): journal=REPO/journal
    m=build_packets(project,output,a.mode,journal)
    print(json.dumps({"project":m["project"],"mode":a.mode,"arcs":len(m["packet_paths"]),"output":str(output.relative_to(REPO))},ensure_ascii=False))
    return 0
if __name__=="__main__":
    raise SystemExit(main())
