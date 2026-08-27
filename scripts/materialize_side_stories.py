#!/usr/bin/env python3
"""Deterministically insert promoted side stories at reader-scaffold boundaries."""
from __future__ import annotations
import argparse,re,string
from pathlib import Path
from side_story_contract import ANALYTICAL_FOCUS_KIND,load_side_stories,canonical_marker

STATUS_ICON={"verified":"✓","inference":"△","unknown":"?"}

def side_story_begin_marker(item:dict)->str:
    return f"<!-- {canonical_marker(item['id'])} BEGIN kind={item.get('kind','')} -->"
def side_story_end_marker(item:dict)->str:
    return f"<!-- {canonical_marker(item['id'])} END -->"
def _norm(value:str)->str:
    value=re.sub(r"<[^>]+>"," ",str(value));value=re.sub(r"[#*_`>\[\](){}]"," ",value)
    value=value.translate(str.maketrans({c:" " for c in string.punctuation+"«»“”‘’…–—≠×"}))
    return re.sub(r"\s+"," ",value).strip().casefold()
def _visible_words(value:str)->int:
    value=re.sub(r"<!--.*?-->"," ",value,flags=re.S)
    value=re.sub(r"\[[A-Z-]+:[^\]]+\]"," ",value)
    return len(re.findall(r"\b[\wÀ-ÖØ-öø-ÿĀ-ž'’.-]+\b",value,re.UNICODE))
def _validate_takeaway(item:dict)->str:
    takeaway=(item.get("content") or {}).get("takeaway","").strip();title=item.get("title","")
    if not takeaway:raise RuntimeError(f"cannot materialize {item.get('id')}: takeaway required")
    if _norm(title) and _norm(title)==_norm(takeaway):raise RuntimeError(f"cannot materialize {item.get('id')}: takeaway merely repeats title")
    return takeaway
def validate_narrative_depth(item:dict,body:str)->None:
    """New inline stories must carry enough matter to justify interrupting the trunk."""
    if item.get("materialization_mode")=="existing_fragment": return
    if item.get("kind")=="method": minimum=55
    elif item.get("kind")==ANALYTICAL_FOCUS_KIND: minimum=140
    else: minimum=90
    words=_visible_words(body)
    if words<minimum and not (item.get("reader_policy") or {}).get("compact_allowed"):
        raise RuntimeError(f"cannot materialize {item.get('id')}: side story too thin ({words} < {minimum} words)")
def render_analytical_focus(item:dict)->str:
    a=item["analysis"];takeaway=_validate_takeaway(item)
    lines=[f"**Focus analytique — {item['title']}**","",f"> **Question** — {a['core_question']}","",f"**À retenir** — {a['thesis']}","","### Contraste institutionnel"]
    for row in a["contrast"]:
        lines += [f"- **{row['label']}** — {row['position']}",f"  - *Vigilance* : {row['caveat']}"]
    lines += ["","> **Mécanisme**"]
    for row in a["mechanisms"]:
        status=row.get("evidence_status","unknown");lines.append(f"> {STATUS_ICON.get(status,'?')} **{row['name']}** — {row['explanation']}")
    if a.get("fiscal_dimension"):lines += ["","### Ressources / fiscalité",a["fiscal_dimension"]]
    if a.get("foreign_influence"):lines += ["","### Circulations extérieures",a["foreign_influence"]]
    lines += ["","### Callback"]
    for row in a["callbacks"]:lines.append(f"- **{row['target']}** — {row['relation']}")
    if a.get("open_questions"):lines += ["","### À ne pas fermer trop vite"]+[f"- {q}" for q in a["open_questions"]]
    lines += ["",f"> **Payoff** — {takeaway}"]
    return "\n".join(lines)
def _find_anchor_span(text:str,anchor:str)->tuple[int,int]|None:
    """Resolve an anchor to a full Markdown line/paragraph boundary.

    Never insert in the middle of a matching sentence. Exact normalized line
    matches win; then a paragraph containing the anchor is used.
    """
    if not anchor:return None
    lines=text.splitlines(keepends=True);offset=0;needle=_norm(anchor)
    candidates=[]
    for line in lines:
        raw=line.rstrip("\r\n");norm=_norm(raw)
        start=offset;end=offset+len(line);offset=end
        if norm==needle:return start,end
        if needle and needle in norm:candidates.append((start,end))
    if candidates:return candidates[0]
    for m in re.finditer(r"(?ms)(?:^|\n\n)([^\n].*?)(?=\n\n|\Z)",text):
        if needle in _norm(m.group(1)):return m.start(1),m.end(1)
    return None
def _insert_boundary(text:str,anchor:str,block:str,position:str="after")->str:
    span=_find_anchor_span(text,anchor)
    if span is None:raise RuntimeError(f"section_anchor not found at reader boundary: {anchor}")
    start,end=span
    pos=start if position=="before" else end
    return text[:pos]+("\n\n"+block.strip()+"\n\n")+text[pos:]
def materialize_text(project:Path,text:str)->tuple[str,int]:
    inserted=0
    for _,item in load_side_stories(project):
        if item.get("status")!="promoted":continue
        _validate_takeaway(item)
        marker=canonical_marker(item["id"])
        if marker in text or item.get("materialization_mode")=="existing_fragment":continue
        placement=item.get("placement") or {};anchor=placement.get("section_anchor") or item.get("title")
        body=(item.get("content") or {}).get("body_markdown")
        if item.get("kind")==ANALYTICAL_FOCUS_KIND and not body:body=render_analytical_focus(item)
        if not body:raise RuntimeError(f"cannot materialize {item['id']}: promoted side story has no body_markdown")
        validate_narrative_depth(item,body)
        prefix="" if item.get("kind")==ANALYTICAL_FOCUS_KIND else f"**{(item.get('render') or {}).get('label')} — {item['title']}**\n\n"
        block=f"{side_story_begin_marker(item)}\n{prefix}{body.strip()}\n{side_story_end_marker(item)}"
        text=_insert_boundary(text,anchor,block,placement.get("position","after"));inserted+=1
    return text,inserted
def materialize(project:Path,source:Path,output:Path)->int:
    text,count=materialize_text(project,source.read_text(encoding="utf-8"))
    output.parent.mkdir(parents=True,exist_ok=True);output.write_text(text,encoding="utf-8");return count
def main():
    p=argparse.ArgumentParser();p.add_argument("--project",required=True);p.add_argument("--source",required=True);p.add_argument("--output",required=True);a=p.parse_args()
    count=materialize(Path(a.project),Path(a.source),Path(a.output));print(f"SIDE STORY MATERIALIZATION OK: {count} inserted")
if __name__=="__main__":main()
