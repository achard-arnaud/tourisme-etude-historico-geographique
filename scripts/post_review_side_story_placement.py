#!/usr/bin/env python3
"""Place reader-eligible side stories only after the reviewed core reader exists.

The planner works on paragraph boundaries in the final Markdown reader. It prefers
explicit chronological/causal match terms, penalizes side-story density in the
previous/current/next paragraph and uses paragraph length only as a fallback among
historically equivalent candidates. It never appends a story at book end.

Candidate evidence status is allowed to remain candidate when
`reader_eligibility.basis == museum_plus_independent_corroboration` and the
qualification contract is complete. This is reader eligibility, not claim promotion.
"""
from __future__ import annotations

import json,re,string
from pathlib import Path
from typing import Iterable

from docx import Document
from docx.text.paragraph import Paragraph

from materialize_side_stories import (
    side_story_begin_marker,side_story_end_marker,validate_narrative_depth,
)
from side_story_contract import ANALYTICAL_FOCUS_KIND,canonical_marker,load_side_stories
from side_story_presentation import style_side_story_cell

ELIGIBILITY_BASIS="museum_plus_independent_corroboration"
PLAN_NAME="side_story_placement_plan.json"
SIDE_MARKER="[SIDE-STORY:"


def _norm(value:str)->str:
    value=re.sub(r"<[^>]+>"," ",str(value));value=re.sub(r"[#*_`>\[\](){}]"," ",value)
    value=value.translate(str.maketrans({c:" " for c in string.punctuation+"«»“”‘’…–—≠×"}))
    return re.sub(r"\s+"," ",value).strip().casefold()


def _visible_words(value:str)->int:
    return len(re.findall(r"\b[\wÀ-ÖØ-öø-ÿĀ-ž'’.-]+\b",re.sub(r"<[^>]+>"," ",value),re.UNICODE))


def _content_body(item:dict)->str:
    body=((item.get("content") or {}).get("body_markdown") or "").strip()
    return body


def candidate_reader_eligible(item:dict)->tuple[bool,list[str]]:
    """Return (eligible, errors) without changing evidence status."""
    if item.get("status")!="candidate":return False,[]
    q=item.get("reader_eligibility") or {};errors=[]
    if q.get("basis")!=ELIGIBILITY_BASIS:return False,[]
    if q.get("status")!="eligible":errors.append("reader_eligibility.status must be eligible")
    if q.get("forced_pipeline") is not True:errors.append("reader_eligibility.forced_pipeline must be true")
    museum=list(q.get("museum_source_ids") or [])
    corroborating=list(q.get("corroborating_source_ids") or [])
    origin=list(q.get("museum_origin_paths") or [])
    if not museum and not origin:errors.append("museum source or museum origin path required")
    if not corroborating:errors.append("at least one independent corroborating source required")
    if set(museum)&set(corroborating):errors.append("museum and corroborating source sets must be disjoint")
    lineage_sources=set((item.get("lineage") or {}).get("source_ids") or [])
    if set(museum)-lineage_sources:errors.append("museum_source_ids must be in lineage.source_ids")
    if set(corroborating)-lineage_sources:errors.append("corroborating_source_ids must be in lineage.source_ids")
    if not q.get("uncertainty_boundary"):errors.append("explicit uncertainty_boundary required")
    body=_content_body(item)
    if not body:errors.append("reader-eligible candidate requires content.body_markdown")
    if not (item.get("placement") or {}).get("section_anchor"):errors.append("reader-eligible candidate requires placement.section_anchor")
    if not ((item.get("placement") or {}).get("match_terms") or []):errors.append("reader-eligible candidate requires placement.match_terms")
    return not errors,errors


def is_post_review_materializable(item:dict)->bool:
    render=item.get("render") or {}
    if not render.get("required_in_reader"):return False
    if item.get("status") in {"promoted","validated"}:return True
    eligible,errors=candidate_reader_eligible(item)
    if errors:raise RuntimeError(f"{item.get('id')}: "+"; ".join(errors))
    return eligible


def _markdown_story_block(item:dict)->str:
    body=_content_body(item)
    if not body:
        raise RuntimeError(f"{item.get('id')}: post-review placement requires body_markdown")
    validate_narrative_depth(item,body)
    label=(item.get("render") or {}).get("label") or item.get("kind")
    prefix=f"**{label} — {item['title']}**"
    return "\n".join([side_story_begin_marker(item),prefix,"",body,side_story_end_marker(item)])


def _split_blocks(text:str)->list[str]:
    # Preserve paragraph/heading/table blocks without splitting inside a paragraph.
    return re.split(r"\n{2,}",text.strip())


def _is_plain_candidate(block:str)->bool:
    s=block.strip()
    if not s or SIDE_MARKER in s:return False
    if s.startswith(("#","<!--","```","|","<table","<tr","<td","---")):return False
    if re.match(r"^(?:[-*+] |\d+[.)] )",s):return False
    return _visible_words(s)>=12


def _heading_level(block:str)->int|None:
    first=block.strip().splitlines()[0] if block.strip() else ""
    m=re.match(r"^(#{1,6})\s+",first)
    return len(m.group(1)) if m else None


def _find_section_range(blocks:list[str],anchor:str)->tuple[int,int]:
    needle=_norm(anchor)
    hits=[i for i,b in enumerate(blocks) if needle and needle in _norm(b)]
    if not hits:raise RuntimeError(f"section anchor not found in reviewed reader: {anchor}")
    start=hits[0];level=_heading_level(blocks[start])
    if level is None:
        # Find nearest preceding heading and use its section.
        heading=next((i for i in range(start,-1,-1) if _heading_level(blocks[i]) is not None),None)
        if heading is None:return 0,len(blocks)
        start=heading;level=_heading_level(blocks[start])
    end=len(blocks)
    for i in range(start+1,len(blocks)):
        lv=_heading_level(blocks[i])
        if lv is not None and lv<=level:
            end=i;break
    return start,end


def _neighbor_density(blocks:list[str],idx:int)->int:
    density=0
    for j in range(max(0,idx-1),min(len(blocks),idx+2)):
        if SIDE_MARKER in blocks[j]:density+=1
    return density


def _score_block(blocks:list[str],idx:int,item:dict)->dict:
    placement=item.get("placement") or {};norm=_norm(blocks[idx])
    terms=[_norm(x) for x in placement.get("match_terms") or [] if _norm(x)]
    chronology=[_norm(x) for x in placement.get("chronology_terms") or [] if _norm(x)]
    mechanism=[_norm(x) for x in placement.get("mechanism_terms") or [] if _norm(x)]
    term_hits=[t for t in terms if t in norm]
    chronology_hits=[t for t in chronology if t in norm]
    mechanism_hits=[t for t in mechanism if t in norm]
    density=_neighbor_density(blocks,idx);words=_visible_words(blocks[idx])
    semantic=120*len(term_hits)+80*len(chronology_hits)+70*len(mechanism_hits)
    density_penalty=220*density
    richness=min(words,180)/18.0
    return {"score":semantic-density_penalty+richness,"semantic":semantic,"density_penalty":density_penalty,"words":words,
            "term_hits":term_hits,"chronology_hits":chronology_hits,"mechanism_hits":mechanism_hits}


def choose_boundary(blocks:list[str],item:dict)->tuple[int,dict]:
    placement=item.get("placement") or {};start,end=_find_section_range(blocks,placement["section_anchor"])
    candidates=[]
    for i in range(start+1,end):
        if not _is_plain_candidate(blocks[i]):continue
        scored=_score_block(blocks,i,item);candidates.append((i,scored))
    if not candidates:raise RuntimeError(f"{item.get('id')}: no paragraph boundary inside section {placement['section_anchor']!r}")
    semantic=[row for row in candidates if row[1]["semantic"]>0]
    fallback_used=False
    pool=semantic
    if not pool:
        fallback_used=True
        # Longest relevant paragraph is the fallback, but density still wins first.
        min_density=min(_neighbor_density(blocks,i) for i,_ in candidates)
        pool=[row for row in candidates if _neighbor_density(blocks,row[0])==min_density]
        pool=sorted(pool,key=lambda row:(row[1]["words"],row[1]["score"]),reverse=True)
    else:
        pool=sorted(pool,key=lambda row:(row[1]["score"],row[1]["words"]),reverse=True)
    idx,meta=pool[0];meta=dict(meta);meta["fallback_longest_fragment"]=fallback_used;meta["section_range"]=[start,end]
    return idx,meta


def _insert_block(blocks:list[str],idx:int,story_block:str,position:str)->list[str]:
    if position=="before":return blocks[:idx]+[story_block]+blocks[idx:]
    return blocks[:idx+1]+[story_block]+blocks[idx+1:]


def place_markdown(project:Path,text:str)->tuple[str,list[dict]]:
    blocks=_split_blocks(text);plan=[]
    queue=[]
    for _,item in load_side_stories(project):
        if not is_post_review_materializable(item):continue
        marker=canonical_marker(item["id"])
        if marker in text or item.get("materialization_mode")=="existing_fragment":continue
        queue.append(item)
    # Resolve in reader order, not file/id order, so density penalties are chronological.
    queue.sort(key=lambda item:_find_section_range(blocks,(item.get("placement") or {})["section_anchor"])[0])
    for item in queue:
        idx,meta=choose_boundary(blocks,item);placement=item.get("placement") or {};position=placement.get("position","after")
        excerpt=re.sub(r"\s+"," ",re.sub(r"[*_`#>]","",blocks[idx])).strip()[:240]
        story=_markdown_story_block(item)
        blocks=_insert_block(blocks,idx,story,position)
        plan.append({"id":item["id"],"kind":item.get("kind"),"status":item.get("status"),"section_anchor":placement.get("section_anchor"),
                     "position":position,"paragraph_excerpt":excerpt,"score":round(meta["score"],2),"semantic_score":meta["semantic"],
                     "density_penalty":meta["density_penalty"],"paragraph_words":meta["words"],"term_hits":meta["term_hits"],
                     "chronology_hits":meta["chronology_hits"],"mechanism_hits":meta["mechanism_hits"],
                     "fallback_longest_fragment":meta["fallback_longest_fragment"]})
    return "\n\n".join(blocks).strip()+"\n",plan


def _clean_docx_text(markdown:str)->list[str]:
    text=re.sub(r"<!--.*?-->","",markdown,flags=re.S)
    paras=[]
    for block in re.split(r"\n{2,}",text):
        block=block.strip()
        if not block:continue
        block=re.sub(r"^#{1,6}\s+","",block)
        block=re.sub(r"^[-*+]\s+","",block,flags=re.M)
        block=re.sub(r"[*_`]","",block)
        block=re.sub(r"\[([^\]]+)\]\([^\)]+\)",r"\1",block)
        block=re.sub(r"\s+"," ",block).strip()
        if block:paras.append(block)
    return paras


def _find_docx_paragraph(doc:Document,excerpt:str)->Paragraph|None:
    needle=_norm(excerpt)
    if not needle:return None
    # Exact/containment match first.
    for p in doc.paragraphs:
        n=_norm(p.text)
        if n and (needle in n or n in needle) and min(len(n),len(needle))>=35:return p
    # Fallback on the first 12 normalized words; still deterministic and local.
    words=needle.split()[:12];short=" ".join(words)
    for p in doc.paragraphs:
        if short and short in _norm(p.text):return p
    return None


def _insert_story_table(doc:Document,paragraph:Paragraph,item:dict,position:str)->None:
    table=doc.add_table(rows=1,cols=1);cell=table.cell(0,0);cell.text="";style_side_story_cell(cell,item["kind"])
    label=(item.get("render") or {}).get("label") or item.get("kind")
    head=cell.paragraphs[0];run=head.add_run(f"{label} — {item['title']}");run.bold=True
    for text in _clean_docx_text(_content_body(item)):
        cell.add_paragraph(text)
    if position=="before":paragraph._p.addprevious(table._tbl)
    else:paragraph._p.addnext(table._tbl)


def place_docx(project:Path,docx_path:Path,plan:list[dict])->int:
    if not plan:return 0
    by_id={item["id"]:item for _,item in load_side_stories(project)};doc=Document(docx_path);inserted=0
    for row in plan:
        item=by_id[row["id"]];paragraph=_find_docx_paragraph(doc,row["paragraph_excerpt"])
        if paragraph is None:raise RuntimeError(f"{row['id']}: Markdown placement could not be resolved in DOCX core")
        _insert_story_table(doc,paragraph,item,row.get("position","after"));inserted+=1
    doc.save(docx_path);return inserted


def place_reader(project:Path,markdown_path:Path,docx_path:Path)->dict:
    core=markdown_path.read_text(encoding="utf-8");placed,plan=place_markdown(project,core)
    markdown_path.write_text(placed,encoding="utf-8")
    docx_count=place_docx(project,docx_path,plan)
    plan_path=project/"09_output"/PLAN_NAME;plan_path.write_text(json.dumps({"schema_version":"1.0","stage":"post_core_review","placements":plan},ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    return {"post_review_side_stories":len(plan),"post_review_side_stories_docx":docx_count,"side_story_placement_plan":str(plan_path)}
