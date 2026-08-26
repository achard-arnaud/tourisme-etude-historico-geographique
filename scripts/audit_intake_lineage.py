#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "docs" / "intakes" / "intake_registry.json"
INTAKE_DIR = ROOT / "docs" / "intakes"
MANIFEST_GLOB = "RUN*_MANIFEST.json"
VALID_STATUSES = {"archived", "missing_source", "unidentified_legacy"}
EXTERNAL_INTAKE_RE = re.compile(r"(?:[A-Z0-9_]*INTAKES?_[A-Za-z0-9_\-]+|INTAKE_[A-Za-z0-9_\-]+)\.md")


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def discover_manifest_intakes() -> dict[str, set[str]]:
    found: dict[str, set[str]] = {}
    for manifest in sorted((ROOT / "docs").glob(MANIFEST_GLOB)):
        text = manifest.read_text(encoding="utf-8")
        names = set(EXTERNAL_INTAKE_RE.findall(text))
        if names:
            found[manifest.name] = names
    return found


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []

    if not REGISTRY.exists():
        print(f"ERROR: missing registry: {REGISTRY}")
        return 1

    try:
        entries = load_json(REGISTRY)
    except Exception as exc:
        print(f"ERROR: invalid registry JSON: {exc}")
        return 1

    if not isinstance(entries, list):
        print("ERROR: intake registry must be a JSON array")
        return 1

    ids: set[str] = set()
    names: dict[str, dict] = {}
    for idx, entry in enumerate(entries):
        prefix = f"entry[{idx}]"
        if not isinstance(entry, dict):
            errors.append(f"{prefix}: must be object")
            continue
        for key in ("id", "intake_kind", "first_run", "manifest", "preservation_status", "outputs", "notes"):
            if key not in entry:
                errors.append(f"{prefix}: missing {key}")
        iid = entry.get("id")
        if not isinstance(iid, str) or not iid:
            errors.append(f"{prefix}: invalid id")
        elif iid in ids:
            errors.append(f"duplicate intake id: {iid}")
        else:
            ids.add(iid)

        status = entry.get("preservation_status")
        if status not in VALID_STATUSES:
            errors.append(f"{iid}: invalid preservation_status {status!r}")

        manifest = entry.get("manifest")
        if isinstance(manifest, str) and manifest and not (ROOT / manifest).exists():
            errors.append(f"{iid}: manifest does not exist: {manifest}")

        outputs = entry.get("outputs")
        if not isinstance(outputs, list) or not outputs:
            errors.append(f"{iid}: outputs must be a non-empty list")
        else:
            for output in outputs:
                if not isinstance(output, str) or not output:
                    errors.append(f"{iid}: invalid output path {output!r}")
                elif not (ROOT / output).exists():
                    errors.append(f"{iid}: declared output missing: {output}")

        source_name = entry.get("source_name")
        if source_name is not None:
            if not isinstance(source_name, str) or not source_name.endswith(".md"):
                errors.append(f"{iid}: source_name must be null or .md filename")
            elif source_name in names:
                errors.append(f"duplicate source_name in registry: {source_name}")
            else:
                names[source_name] = entry

        repo_path = entry.get("repo_path")
        recovery = entry.get("recovery_action")
        if status == "archived":
            if not isinstance(repo_path, str) or not repo_path.startswith("docs/intakes/"):
                errors.append(f"{iid}: archived intake requires docs/intakes repo_path")
            elif not (ROOT / repo_path).exists():
                errors.append(f"{iid}: archived source missing at {repo_path}")
            if source_name and Path(repo_path).name != source_name:
                errors.append(f"{iid}: repo_path basename must match source_name")
        elif status in {"missing_source", "unidentified_legacy"}:
            if repo_path is not None:
                errors.append(f"{iid}: {status} must not pretend to have repo_path")
            if not isinstance(recovery, str) or not recovery.strip():
                errors.append(f"{iid}: {status} requires recovery_action")
            warnings.append(f"{iid}: provenance debt remains ({status})")

    manifest_intakes = discover_manifest_intakes()
    for manifest_name, source_names in manifest_intakes.items():
        for source_name in source_names:
            if source_name not in names:
                errors.append(f"{manifest_name}: referenced intake not registered: {source_name}")
            else:
                declared_manifest = Path(str(names[source_name].get("manifest", ""))).name
                if declared_manifest != manifest_name:
                    errors.append(
                        f"{source_name}: registry manifest {declared_manifest or '<none>'} does not match {manifest_name}"
                    )

    archived_files = {
        p.name
        for p in INTAKE_DIR.glob("*.md")
        if p.name != "README.md"
    }
    registered_archived = {
        entry.get("source_name")
        for entry in entries
        if entry.get("preservation_status") == "archived"
    }
    for filename in sorted(archived_files - registered_archived):
        errors.append(f"archived intake has no registry entry: {filename}")
    for filename in sorted(registered_archived - archived_files):
        errors.append(f"registry says archived but file is absent: {filename}")

    for warning in warnings:
        print("WARN:", warning)
    if errors:
        for error in errors:
            print("ERROR:", error)
        return 1

    print(
        "INTAKE LINEAGE AUDIT OK — "
        f"registered {len(entries)} / archived {len(registered_archived)} / "
        f"manifest-referenced {sum(len(v) for v in manifest_intakes.values())} / provenance debt {len(warnings)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
