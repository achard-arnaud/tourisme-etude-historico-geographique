#!/usr/bin/env python3
"""Deterministically insert promoted side-story artefacts into Markdown."""
from __future__ import annotations
import argparse
from pathlib import Path
from side_story_contract import ANALYTICAL_FOCUS_KIND,load_side_stories,canonical_marker

STATUS_ICON={"verified":"✓","inference":"△","unknown":"?"}

def render_analytical_focus(item:dict)->str:
    a=item["analysis"];title=item["title"];takeaway=(item.get("content") or {}).get("takeaway","")
    lines=[f"**Focus analytique — {title}**","",f"> **Question** — {a['core_question']}","",f"**À retenir** — {a['thesis']}","","### Contraste institutionnel"]
    for row in a["contrast"]:
        lines += [f"- **{row['label']}** — {row['position']}",f"  - *Vigilance* : {row['caveat']}"]
    lines += ["","> **Mécanisme**"]
    for row in a["mechanisms"]:
        status=row.get("evidence_status","unknown");lines.append(f"> {STATUS_ICON.get(status,'?')} **{row['name']}** — {row['explanation']}")
    if a.get("fiscal_dimension"):
        lines += ["","### Ressources / fiscalité",a["fiscal_dimension"]]
    if a.get("foreign_influence"):
        lines += ["","### Circulations extérieures",a["foreign_influence"]]
    lines += ["","### Callback"]
    for row in a["callbacks"]:lines.append(f"- **{row['target']}** — {row['relation']}")
    if a.get("open_questions"):
        lines += ["","### À ne pas fermer trop vite"]+[f"- {q}" for q in a["open_questions"]]
    lines += ["",f"> **Payoff** — {takeaway}"]
    return "\n".join(lines)

def materialize_text(project:Path,text:str)->tuple[str,int]:
    inserted=0
    for _,item in load_side_stories(project):
        if item.get("status")!="promoted":continue
        marker=canonical_marker(item["id"])
        if marker in text:continue
        body=(item.get("content") or {}).get("body_markdown")
        if item.get("kind")==ANALYTICAL_FOCUS_KIND and not body:body=render_analytical_focus(item)
        if not body:continue
        anchor=(item.get("placement") or {}).get("section_anchor")
        if not anchor or anchor not in text:raise RuntimeError(f"cannot materialize {item['id']}: section_anchor not found")
        pos=text.index(anchor)+len(anchor)
        prefix="" if item.get("kind")==ANALYTICAL_FOCUS_KIND else f"**{(item.get('render') or {}).get('label')} — {item['title']}**\n\n"
        block=f"\n\n<!-- {marker} -->\n{prefix}{body.strip()}\n"
        text=text[:pos]+block+text[pos:];inserted+=1
    return text,inserted

def materialize(project:Path,source:Path,output:Path)->int:
    text,count=materialize_text(project,source.read_text(encoding="utf-8"));output.parent.mkdir(parents=True,exist_ok=True);output.write_text(text,encoding="utf-8");return count

def main():
    p=argparse.ArgumentParser();p.add_argument("--project",required=True);p.add_argument("--source",required=True);p.add_argument("--output",required=True);a=p.parse_args()
    count=materialize(Path(a.project),Path(a.source),Path(a.output));print(f"SIDE STORY MATERIALIZATION OK: {count} inserted")
if __name__=="__main__":main()
