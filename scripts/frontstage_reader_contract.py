#!/usr/bin/env python3
"""Final reader-facing cleanup after deterministic composition.

Claim IDs and production lineage stay backstage. Reader prose exposes only
human-readable source citations and historical uncertainty.
"""
from __future__ import annotations
import re
from pathlib import Path
from docx import Document
from side_story_presentation import LEGEND_HEADING, add_side_story_legend, apply_side_story_palette, markdown_legend

VISIBLE_REPLACEMENTS={
    "ÉDITION V3 INTÉGRALE DE LECTURE — VOL RETOUR":"FRESQUE HISTORICO-GÉOGRAPHIQUE — VOLUME RETOUR",
    "V1 longue conservée, fiches de conversation et ajouts promus intégrés sans compression.":"Lecture intégrale : lieux, mécanismes, changements d’échelle et approfondissements de terrain.",
    "V3 intégrale — arcs chronologiques, HIL, comparateurs et zooms géographiques":"Lecture intégrale — arcs chronologiques, comparaisons et changements d’échelle",
    "État des données : 20 août 2026 · Usage personnel · Baseline V1 conservée":"Usage personnel · Sri Lanka · août 2026",
    "Appareil de sources des compléments V3":"Sources des approfondissements",
    "Ces notices donnent la source exacte des développements ajoutés à la V1. Le tier décrit la nature de la source, non une autorisation à généraliser au-delà de son champ.":"Ces notices donnent la source exacte des approfondissements. Le niveau de source décrit la nature du document, sans autoriser une généralisation au-delà de son champ.",
}
KNOWN_BACKSTAGE_FRAGMENTS=(
    "Politique éditoriale de la V3 intégrale","V1 longue conservée","Baseline V1 conservée",
    "Complément V3","Appareil de sources des compléments V3","Le petit report.md est traité comme un delta",
    "side-story lineage",
)
CLAIM_MARKER=re.compile(r"\s*\[claim:[^\]]+\]",re.I)
BRIDGE_MARKER=re.compile(r"\s*\[bridge:[^\]]+\]",re.I)
RUN_TOKEN=re.compile(r"\bRun\s+\d+\b",re.I)
TECH_ARC_TOKEN=re.compile(r"\bA\d{2}[A-Za-z0-9-]*_[A-Za-z0-9_-]+\b")
MACHINE_HIL_TOKEN=re.compile(r"\bHIL-\d{2}_[A-Za-z0-9_-]+\b")

def _plain_markdown_line(line:str)->str:
    line=re.sub(r"^#{1,6}\s+","",line.strip());line=re.sub(r"[*_`]","",line)
    return re.sub(r"\s+"," ",line).strip()
def _remove_paragraph(paragraph)->None:
    element=paragraph._element;element.getparent().remove(element);paragraph._p=paragraph._element=None
def strip_method_block_from_docx(doc:Document,method_block:str)->int:
    targets={_plain_markdown_line(line) for line in method_block.splitlines() if _plain_markdown_line(line)};removed=0
    for p in list(doc.paragraphs):
        if _plain_markdown_line(p.text) in targets:_remove_paragraph(p);removed+=1
    return removed
def _replace_paragraph_text_preserving_first_run(p,text:str)->None:
    if p.runs:
        p.runs[0].text=text
        for run in p.runs[1:]:run.text=""
    else:p.add_run(text)
def clean_visible_docx_text(doc:Document)->int:
    changed=0
    for p in doc.paragraphs:
        text=p.text
        replacement=VISIBLE_REPLACEMENTS.get(text.strip())
        new=BRIDGE_MARKER.sub("",CLAIM_MARKER.sub("",replacement if replacement is not None else text))
        if "Complément V3 —" in new:new=new.replace("Complément V3 —","Approfondissement —")
        if new!=text:_replace_paragraph_text_preserving_first_run(p,new);changed+=1
    for table in doc.tables:
        for row in table.rows:
            for cell in row.cells:
                for p in cell.paragraphs:
                    text=p.text;new=BRIDGE_MARKER.sub("",CLAIM_MARKER.sub("",text))
                    if new!=text:_replace_paragraph_text_preserving_first_run(p,new);changed+=1
    return changed
def strip_method_block_from_markdown(markdown:str,method_block:str)->str:
    block=method_block.strip()
    if block:markdown=markdown.replace(block,"")
    markdown=markdown.replace("Complément V3 —","Approfondissement —")
    for old,new in VISIBLE_REPLACEMENTS.items():markdown=markdown.replace(old,new)
    markdown=BRIDGE_MARKER.sub("",CLAIM_MARKER.sub("",markdown))
    markdown=re.sub(r"\n{3,}","\n\n",markdown)
    return markdown.strip()+"\n"
def visible_docx_text(doc:Document)->str:
    chunks=[p.text for p in doc.paragraphs]
    for table in doc.tables:
        for row in table.rows:
            chunks.extend(cell.text for cell in row.cells)
    return "\n".join(chunks)
def assert_no_known_backstage_leak(text:str)->None:
    normalized=text.replace("`","")
    found=[x for x in KNOWN_BACKSTAGE_FRAGMENTS if x.casefold() in normalized.casefold()]
    if CLAIM_MARKER.search(normalized):found.append("[claim:*]")
    if BRIDGE_MARKER.search(normalized):found.append("[bridge:*]")
    if RUN_TOKEN.search(normalized):found.append("Run <id>")
    if TECH_ARC_TOKEN.search(normalized):found.append("technical arc id")
    if MACHINE_HIL_TOKEN.search(normalized):found.append("machine HIL id")
    if found:raise RuntimeError(f"reader-facing backstage leakage remains: {found}")
def finalize_reader(project:Path,spec:dict)->dict:
    output_dir=project/"09_output";docx_path=output_dir/spec["output"];markdown_path=output_dir/spec["markdown_output"]
    doc=Document(docx_path);removed=strip_method_block_from_docx(doc,spec.get("method_block",""));replacements=clean_visible_docx_text(doc)
    palette=apply_side_story_palette(doc,project);legend_rows=add_side_story_legend(doc);assert_no_known_backstage_leak(visible_docx_text(doc));doc.save(docx_path)
    markdown=strip_method_block_from_markdown(markdown_path.read_text(encoding="utf-8"),spec.get("method_block",""))
    if f"## {LEGEND_HEADING}" not in markdown:markdown=markdown.rstrip()+"\n\n"+markdown_legend()+"\n"
    assert_no_known_backstage_leak(markdown);markdown_path.write_text(markdown,encoding="utf-8")
    return {"backstage_paragraphs_removed":removed,"frontstage_replacements":replacements,
            "side_story_headers_styled":palette["headers_styled"],"side_story_body_paragraphs_styled":palette["body_paragraphs_styled"],
            "side_story_blocks_resolved":palette["resolved_blocks"],"side_story_kinds_seen":palette["kinds_seen"],"side_story_legend_rows":legend_rows}
