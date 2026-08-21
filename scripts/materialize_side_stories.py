#!/usr/bin/env python3
"""Deterministically insert promoted side-story artefacts into Markdown."""
from __future__ import annotations
import argparse
from pathlib import Path
from side_story_contract import load_side_stories, canonical_marker

def materialize(project:Path, source:Path, output:Path)->int:
    text=source.read_text(encoding="utf-8"); inserted=0
    for _,item in load_side_stories(project):
        if item.get("status")!="promoted":continue
        body=(item.get("content") or {}).get("body_markdown")
        if not body:continue
        marker=canonical_marker(item["id"])
        if marker in text:continue
        anchor=(item.get("placement") or {}).get("section_anchor")
        if not anchor or anchor not in text: raise RuntimeError(f"cannot materialize {item['id']}: section_anchor not found")
        pos=text.index(anchor)+len(anchor)
        block=f"\n\n<!-- {marker} -->\n**{(item.get('render') or {}).get('label')} — {item['title']}**\n\n{body.strip()}\n"
        text=text[:pos]+block+text[pos:]; inserted+=1
    output.parent.mkdir(parents=True,exist_ok=True); output.write_text(text,encoding="utf-8"); return inserted

def main():
    p=argparse.ArgumentParser();p.add_argument("--project",required=True);p.add_argument("--source",required=True);p.add_argument("--output",required=True);a=p.parse_args()
    count=materialize(Path(a.project),Path(a.source),Path(a.output));print(f"SIDE STORY MATERIALIZATION OK: {count} inserted")
if __name__=="__main__":main()
