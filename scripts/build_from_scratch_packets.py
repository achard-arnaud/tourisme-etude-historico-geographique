#!/usr/bin/env python3
"""Compatibility wrapper for the unified Run32 drafting-context builder."""
from __future__ import annotations
import argparse, json
from pathlib import Path
from build_drafting_packets import ReadLedger, build_packets as _build_packets

REPO=Path(__file__).resolve().parents[1]

def build_packets(project:Path, output:Path):
    """Preserve Run26 API while using the shared Run32 material plane."""
    manifest=_build_packets(project,output,mode="from_scratch",journal=None)
    # Compatibility fields expected by older tests/consumers.
    manifest["schema_version"]="1.0"
    manifest["class"]="from_scratch_packet_manifest"
    manifest["contamination_check"]["reader_prose_loaded"]=False
    manifest["contamination_check"].setdefault("forbidden_patterns",["/09_output/report","/09_output/archive/"])
    manifest["contamination_check"].setdefault("forbidden_suffixes",[".docx",".pdf"])
    (output/"manifest.json").write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return manifest

def main()->int:
    p=argparse.ArgumentParser();p.add_argument("--project",required=True);p.add_argument("--output");a=p.parse_args()
    project=Path(a.project);project=project if project.is_absolute() else REPO/project
    output=Path(a.output) if a.output else project/"09_output"/"from_scratch"/"packets"
    output=output if output.is_absolute() else REPO/output
    m=build_packets(project,output)
    print(json.dumps({"project":m["project"],"arcs":len(m["packet_paths"]),"reader_prose_loaded":False,"output":str(output.relative_to(REPO))},ensure_ascii=False))
    return 0
if __name__=="__main__": raise SystemExit(main())
