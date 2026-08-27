#!/usr/bin/env python3
"""Import the *reader* scaffold from an authoritative DOCX.

This is intentionally different from story_scaffold.json:
- reader_scaffold preserves editorial order, heading hierarchy and inline boxes;
- story_scaffold describes evidence/graph topology.
The reader scaffold is authoritative for composition order in both modes.
"""
from __future__ import annotations
import argparse,json,re,hashlib
from pathlib import Path
from docx import Document
from docx.text.paragraph import Paragraph
from docx.table import Table

SIDE_LABELS=("POINT DE MÉTHODE","PETIT DÉTOUR","MAIS AUSSI","FAUSSE PISTE","DÉZOOM","PERSONNAGE","OBJET / TERRAIN","COMPARAISON","FIL ROUGE","FOCUS ANALYTIQUE")

def _body_blocks(doc):
    for child in doc.element.body.iterchildren():
        if child.tag.endswith("}p"):
            yield "paragraph",Paragraph(child,doc)
        elif child.tag.endswith("}tbl"):
            yield "table",Table(child,doc)

def _kind(text:str)->str|None:
    up=re.sub(r"\s+"," ",text.strip()).upper()
    mapping={
        "POINT DE MÉTHODE":"method","PETIT DÉTOUR":"detour","MAIS AUSSI":"also",
        "FAUSSE PISTE":"false_lead","DÉZOOM":"dezoom","PERSONNAGE":"portrait",
        "OBJET / TERRAIN":"object_focus","COMPARAISON":"comparator","FIL ROUGE":"callback",
        "FOCUS ANALYTIQUE":"analytical_focus",
    }
    for label,kind in mapping.items():
        if up.startswith(label): return kind
    return None

def import_scaffold(path:Path, corpus:str)->dict:
    doc=Document(path)
    nodes=[]; last_heading=None
    for ordinal,(typ,obj) in enumerate(_body_blocks(doc)):
        if typ=="paragraph":
            text=obj.text.strip()
            style=obj.style.name if obj.style else ""
            m=re.search(r"(\d+)$",style) if style.startswith("Heading ") else None
            if style in {"Part Title","Chapter Title"} or m:
                level=1 if style=="Part Title" else 2 if style=="Chapter Title" else 2+int(m.group(1))
                nodes.append({"type":"heading","ordinal":ordinal,"level":level,"style":style,"title":text}); last_heading=text
        else:
            text="\n".join(cell.text.strip() for row in obj.rows for cell in row.cells).strip()
            kind=_kind(text)
            if kind:
                first=text.splitlines()[0] if text else ""
                nodes.append({"type":"side_story","ordinal":ordinal,"kind":kind,"title":first,"after_heading":last_heading,"materialization_mode":"existing_fragment"})
    raw=path.read_bytes()
    return {
        "schema_version":"1.0","class":"reader_scaffold","corpus":corpus,
        "source":{"kind":"authoritative_docx","filename":path.name,"sha256":hashlib.sha256(raw).hexdigest()},
        "policy":{"authoritative_order":True,"story_scaffold_is_evidence_topology_not_reader_order":True,"new_sections_must_resolve_to_existing_heading_or_explicit_insertion_slot":True,"side_stories_must_be_inline_not_appended_gallery":True},
        "nodes":nodes,
        "counts":{"headings":sum(1 for x in nodes if x["type"]=="heading"),"inline_side_stories":sum(1 for x in nodes if x["type"]=="side_story")},
    }

def main()->int:
    p=argparse.ArgumentParser();p.add_argument("docx");p.add_argument("--corpus",required=True);p.add_argument("--output",required=True);a=p.parse_args()
    data=import_scaffold(Path(a.docx),a.corpus)
    Path(a.output).write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(data["counts"]));return 0
if __name__=="__main__":raise SystemExit(main())
