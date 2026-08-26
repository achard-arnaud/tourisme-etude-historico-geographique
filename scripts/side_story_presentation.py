#!/usr/bin/env python3
"""Reader-facing presentation contract for side stories.

This module is deliberately visual/frontstage. It never changes evidence, lineage,
status or side-story kind. Colour is redundant with a stable symbol + label so the
reader keeps the distinction in grayscale/print and with poor colour perception.
"""
from __future__ import annotations

import re
import unicodedata
from pathlib import Path

from docx import Document
from docx.enum.style import WD_STYLE_TYPE
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Inches, Pt, RGBColor

from side_story_contract import KINDS, RENDER_LABELS, SIDE_STORY_CLASS, load_side_stories


KIND_ORDER = [
    "false_lead",
    "detour",
    "dezoom",
    "also",
    "method",
    "portrait",
    "object_focus",
    "comparator",
    "callback",
    "analytical_focus",
]

SIDE_STORY_PRESENTATION = {
    "false_lead": {"symbol": "①", "fill": "FFF6D8", "border": "D6B656", "usage": "Question intuitive à tester puis corriger."},
    "detour": {"symbol": "②", "fill": "E3EEF7", "border": "7FA6C4", "usage": "Détour bref qui éclaire le fil principal."},
    "dezoom": {"symbol": "③", "fill": "E7EBF0", "border": "8797A8", "usage": "Changement d’échelle géographique ou historique."},
    "also": {"symbol": "④", "fill": "E7F3E8", "border": "83AA88", "usage": "Dimension complémentaire utile au mécanisme principal."},
    "method": {"symbol": "⑤", "fill": "F0EDE7", "border": "A69A88", "usage": "Méthode historique lue par le lecteur : dater, attribuer, comparer une source."},
    "portrait": {"symbol": "⑥", "fill": "F7E7E1", "border": "C88F7A", "usage": "Personnage replacé dans son rôle historique."},
    "object_focus": {"symbol": "⑦", "fill": "F5EFDD", "border": "B8A56C", "usage": "Objet, inscription, monument ou indice de terrain."},
    "comparator": {"symbol": "⑧", "fill": "EEE7F5", "border": "9D87B1", "usage": "Comparaison contrôlée avec limites explicites."},
    "callback": {"symbol": "⑨", "fill": "FBE6E3", "border": "C9877E", "usage": "Fil rouge : reprise narrative d’un fait déjà noué."},
    "analytical_focus": {"symbol": "⑩", "fill": "DCE6EE", "border": "6F8FA8", "usage": "Question analytique, contrastes, mécanismes et payoff."},
}

INK = RGBColor(32, 55, 72)
MUTED = RGBColor(92, 99, 108)
LEGEND_HEADING = "Légende des encadrés"


def _norm(value: str) -> str:
    value = re.sub(r"^[①②③④⑤⑥⑦⑧⑨⑩]\s*", "", value or "")
    value = unicodedata.normalize("NFKD", value)
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return re.sub(r"\s+", " ", value.casefold()).strip()


def style_name(kind: str) -> str:
    return f"Side Story — {kind}"


def detect_kind(text: str) -> str | None:
    normalized = _norm(text)
    for kind in KIND_ORDER:
        if normalized.startswith(_norm(RENDER_LABELS[kind])):
            return kind
    return None


def _remove_children(parent, tag: str) -> None:
    for node in list(parent.findall(qn(tag))):
        parent.remove(node)


def _decorate_ppr(p_pr, kind: str) -> None:
    presentation = SIDE_STORY_PRESENTATION[kind]
    _remove_children(p_pr, "w:shd")
    _remove_children(p_pr, "w:pBdr")
    shd = OxmlElement("w:shd")
    shd.set(qn("w:fill"), presentation["fill"])
    p_pr.append(shd)
    borders = OxmlElement("w:pBdr")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), "18")
    left.set(qn("w:color"), presentation["border"])
    left.set(qn("w:space"), "8")
    borders.append(left)
    p_pr.append(borders)


def ensure_side_story_styles(doc: Document) -> None:
    missing = set(KINDS) - set(SIDE_STORY_PRESENTATION)
    extra = set(SIDE_STORY_PRESENTATION) - set(KINDS)
    if missing or extra:
        raise RuntimeError(f"side-story presentation drift: missing={sorted(missing)}, extra={sorted(extra)}")
    for kind in KIND_ORDER:
        name = style_name(kind)
        style = doc.styles[name] if name in doc.styles else doc.styles.add_style(name, WD_STYLE_TYPE.PARAGRAPH)
        style.font.name = "Calibri"
        style.font.size = Pt(10.5)
        style.font.color.rgb = INK
        style.paragraph_format.left_indent = Inches(0.18)
        style.paragraph_format.right_indent = Inches(0.12)
        style.paragraph_format.space_before = Pt(5)
        style.paragraph_format.space_after = Pt(6)
        style.paragraph_format.line_spacing = 1.18
        style.paragraph_format.keep_together = True
        _decorate_ppr(style._element.get_or_add_pPr(), kind)


def _decorate_paragraph(paragraph, kind: str, *, header: bool) -> None:
    _decorate_ppr(paragraph._p.get_or_add_pPr(), kind)
    if header:
        paragraph.style = style_name(kind)
        symbol = SIDE_STORY_PRESENTATION[kind]["symbol"]
        if not paragraph.text.lstrip().startswith(symbol):
            target = next((run for run in paragraph.runs if run.text), None)
            if target is not None:
                target.text = f"{symbol} {target.text}"
                target.bold = True
            else:
                run = paragraph.add_run(f"{symbol} ")
                run.bold = True


def _find_return_index(paragraphs, start: int, return_to: str | None) -> int | None:
    if not return_to:
        return None
    target = return_to.split(":", 1)[1] if return_to.startswith("anchor:") else return_to
    normalized_target = _norm(target)
    if not normalized_target or re.match(r"^[A-Z]+-[A-Z0-9-]+$", target):
        return None
    for index in range(start + 1, min(len(paragraphs), start + 60)):
        if normalized_target in _norm(paragraphs[index].text):
            return index
    return None


def _story_header_index(paragraphs, item: dict, used: set[int]) -> int | None:
    kind = item.get("kind")
    label = _norm(RENDER_LABELS.get(kind, ""))
    aliases = [item.get("title", "")] + list((item.get("content") or {}).get("legacy_titles") or [])
    aliases = [_norm(alias) for alias in aliases if _norm(alias)]
    for index, paragraph in enumerate(paragraphs):
        if index in used or detect_kind(paragraph.text) != kind:
            continue
        text = _norm(paragraph.text)
        if label and any(alias in text for alias in aliases):
            return index
    return None


def apply_side_story_palette(doc: Document, project: Path | None = None) -> dict:
    """Apply colour + redundant symbols. Body shading is bounded by explicit return anchors.

    Every identifiable header is styled. A whole block is shaded only when the story
    artefact gives a resolvable textual return anchor; otherwise the header remains the
    safe visual carrier rather than guessing a range and colouring unrelated prose.
    """
    ensure_side_story_styles(doc)
    paragraphs = doc.paragraphs
    header_kinds: dict[int, str] = {}
    for index, paragraph in enumerate(paragraphs):
        kind = detect_kind(paragraph.text)
        if kind:
            _decorate_paragraph(paragraph, kind, header=True)
            header_kinds[index] = kind

    body_count = 0
    resolved_blocks = 0
    if project is not None:
        used_headers: set[int] = set()
        for _, item in load_side_stories(project):
            if item.get("class") != SIDE_STORY_CLASS or item.get("status") not in {"validated", "promoted"}:
                continue
            kind = item.get("kind")
            if kind not in SIDE_STORY_PRESENTATION:
                continue
            start = _story_header_index(paragraphs, item, used_headers)
            if start is None:
                continue
            used_headers.add(start)
            end = _find_return_index(paragraphs, start, (item.get("placement") or {}).get("return_to"))
            if end is None or end <= start + 1:
                continue
            resolved_blocks += 1
            for index in range(start + 1, end):
                if index in header_kinds:
                    break
                _decorate_paragraph(paragraphs[index], kind, header=False)
                body_count += 1

    return {
        "headers_styled": len(header_kinds),
        "body_paragraphs_styled": body_count,
        "resolved_blocks": resolved_blocks,
        "kinds_seen": sorted(set(header_kinds.values())),
    }


def _shade_cell(cell, fill: str) -> None:
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = tc_pr.find(qn("w:shd"))
    if shd is None:
        shd = OxmlElement("w:shd")
        tc_pr.append(shd)
    shd.set(qn("w:fill"), fill)


def add_side_story_legend(doc: Document) -> int:
    if any(p.text.strip() == LEGEND_HEADING for p in doc.paragraphs):
        return 0
    doc.add_page_break()
    heading = doc.add_heading(LEGEND_HEADING, level=1)
    heading.paragraph_format.keep_with_next = True
    p = doc.add_paragraph(
        "La couleur facilite le repérage, mais le symbole et le libellé portent le sens en noir et blanc. "
        "Les numéros ne sont pas un ordre de priorité. « Point de méthode » décrit une méthode historique "
        "utile au lecteur ; il ne désigne jamais le processus de production de ce document."
    )
    p.paragraph_format.space_after = Pt(8)
    table = doc.add_table(rows=1, cols=3)
    table.autofit = False
    headers = ("Repère", "Type d’encadré", "Usage")
    for cell, text in zip(table.rows[0].cells, headers):
        cell.text = text
        _shade_cell(cell, "E7EBF0")
        for run in cell.paragraphs[0].runs:
            run.bold = True
            run.font.color.rgb = INK
    for kind in KIND_ORDER:
        row = table.add_row().cells
        presentation = SIDE_STORY_PRESENTATION[kind]
        row[0].text = presentation["symbol"]
        row[0].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        row[1].text = RENDER_LABELS[kind]
        row[2].text = presentation["usage"]
        _shade_cell(row[0], presentation["fill"])
        _shade_cell(row[1], presentation["fill"])
    return len(KIND_ORDER)


def markdown_legend() -> str:
    lines = [
        f"## {LEGEND_HEADING}",
        "",
        "La couleur facilite le repérage, mais le symbole et le libellé portent le sens en noir et blanc. Les numéros ne sont pas un ordre de priorité.",
        "",
    ]
    for kind in KIND_ORDER:
        p = SIDE_STORY_PRESENTATION[kind]
        lines.append(f"- {p['symbol']} **{RENDER_LABELS[kind]}** — {p['usage']}")
    lines.extend([
        "",
        "**Point de méthode** désigne ici une méthode historique utile au lecteur ; il ne décrit jamais le processus de production, les runs, les statuts ou les versions du document.",
    ])
    return "\n".join(lines)