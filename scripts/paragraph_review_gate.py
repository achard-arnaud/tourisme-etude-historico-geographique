#!/usr/bin/env python3
"""Deterministic L1 paragraph gate for storytelling-historical-travel."""
from __future__ import annotations

import argparse
from dataclasses import asdict,dataclass,field
import json
from pathlib import Path
import re
import unicodedata
from typing import Any

@dataclass(frozen=True)
class Violation:
    category:str
    rule:str
    message:str

@dataclass
class ReviewResult:
    passed:bool
    violations:list[Violation]=field(default_factory=list)
    warnings:list[str]=field(default_factory=list)

METHOD_LEAKAGE=(
    (r"\bTL;DR\b","tldr_reader_leak"),
    (r"\bstatut canonique\b","statut_canonique_reader_leak"),
    (r"\bce qu['’]on ne doit pas en déduire\b","method_heading_reader_leak"),
    (r"\bpourquoi l['’]insérer directement dans notre arc\b","method_heading_reader_leak"),
    (r"\bHIL[- _]?\d*\b","hil_reader_leak"),
    (r"\brun\s*\d+\b","run_reader_leak"),
    (r"\bversion\s+[vV]?\d+\b","version_reader_leak"),
)
FOREIGN_TERMS={
    "clearing house":("chambre de compensation","centre de compensation","plateforme de compensation"),
    "trade-off":("arbitrage","compromis"),
    "path dependency":("dépendance au sentier","dépendance de trajectoire"),
}
STOPWORDS={"avec","dans","pour","mais","donc","ainsi","apres","avant","cette","cela","comme","plus","moins","entre","sous","vers","leur","leurs","dont","avait","avoir","etre","fait","faire","site","roi","royal","reine","puis","parce","tradition","texte","claim","source","point","durant","depuis","elle"}

def _norm(value:str)->str:
    value=unicodedata.normalize("NFKD",value or "");value="".join(ch for ch in value if not unicodedata.combining(ch));return re.sub(r"\s+"," ",value.lower()).strip()

def _tokens(value:str)->set[str]:
    return {token for token in re.findall(r"[a-z0-9]+",_norm(value)) if len(token)>=4 and token not in STOPWORDS}

def _canonical_points(claim:dict[str,Any])->list[str]:
    explicit=claim.get("canonical_points") or claim.get("canonical_summary_points")
    if not isinstance(explicit,list):return []
    out=[]
    for item in explicit:
        if isinstance(item,str) and item.strip():out.append(item.strip())
        elif isinstance(item,dict):
            text=item.get("text") or item.get("summary")
            if text:out.append(str(text).strip())
    return out

def _point_is_covered(point:str,paragraph:str)->bool:
    required=_tokens(point)
    if not required:return _norm(point) in _norm(paragraph)
    observed=_tokens(paragraph);threshold=1 if len(required)==1 else min(2,len(required));return len(required&observed)>=threshold

def _has_foreign_gloss(text:str,term:str,glosses:tuple[str,...])->bool:
    lowered=_norm(text)
    if _norm(term) not in lowered:return True
    if any(_norm(gloss) in lowered for gloss in glosses):return True
    return bool(re.search(re.escape(term)+r"\s*\([^)]{4,100}\)",text,flags=re.I))

def _unexplained_acronyms(text:str,arc_context:dict[str,Any])->list[str]:
    explained={str(x).upper() for x in arc_context.get("explained_acronyms",[])};hidden=re.sub(r"\[(?:claim|ILLUSTRATION|SIDE-STORY|ARC-RECAP):[^\]]+\]","",text,flags=re.I);candidates=sorted(set(re.findall(r"\b[A-ZÀ-ÖØ-Þ]{2,6}\b",hidden)));out=[]
    for acronym in candidates:
        if acronym in explained:continue
        if re.search(rf"[A-Za-zÀ-ÿ][A-Za-zÀ-ÿ '\-]{{5,80}}\({re.escape(acronym)}\)",hidden):continue
        out.append(acronym)
    return out

def review_paragraph(text:str,claim:dict[str,Any],arc_context:dict[str,Any]|None=None)->ReviewResult:
    """Review one paragraph without loading the manuscript."""
    arc_context=arc_context or {};violations=[];warnings=[]
    for pattern,rule in METHOD_LEAKAGE:
        if re.search(pattern,text,flags=re.I):violations.append(Violation("Don't",rule,"Backstage methodological language leaked into reader-facing prose."));break
    for term,glosses in FOREIGN_TERMS.items():
        if not _has_foreign_gloss(text,term,glosses):violations.append(Violation("forme","terme_technique_non_glose",f"Foreign technical term '{term}' is not glossed or francised."));break
    acronyms=_unexplained_acronyms(text,arc_context)
    if acronyms:violations.append(Violation("forme","sigle_non_explicite","Unexplained acronym(s): "+", ".join(acronyms)))
    points=_canonical_points(claim)
    if points:
        missing=[point for point in points if not _point_is_covered(point,text)]
        if missing:violations.append(Violation("fond","couverture_canonique_incomplete",f"Missing {len(missing)}/{len(points)} canonical point(s)."))
    else:warnings.append("canonical_points_missing: legacy claim requires targeted semantic review; deterministic gate does not invent canonical points")
    normalized=_norm(text)
    if re.search(r"(?:consequence|par consequent|donc|ainsi|renforc\w*)[^.;]{0,220}(?:apres que|apres avoir)",normalized):violations.append(Violation("fond","ordre_fait_avant_consequence","Consequence/perspective precedes the source-attested action."))
    claim_id=str(claim.get("id") or "");marker=f"[claim:{claim_id}]" if claim_id else "";mention_count=(arc_context.get("mention_count") or {}).get(claim_id,0);active_callbacks=set(arc_context.get("active_callbacks") or [])
    if marker and marker in text and mention_count>=2 and claim_id in active_callbacks:violations.append(Violation("fond","citation_evidentielle_au_dela_du_callback_disponible","A third direct evidentiary citation is used while an active callback is available."))
    elif marker and marker in text and mention_count>=2:warnings.append("over_mentioned_claim: more than two direct citations; review whether a callback should replace this citation")
    if arc_context.get("false_lead"):
        if int(arc_context.get("false_lead_count_in_subsection",0))>=2:violations.append(Violation("forme","false_lead_rerank_limit","Subsection already contains the maximum two false leads."))
        if "?" not in text:violations.append(Violation("forme","false_lead_socratic_format","False lead must contain a naïve or semi-rhetorical question."))
    if not arc_context.get("neighbor_context_loaded",False):warnings.append("tone_not_checked: load only previous/next paragraph for bounded L2 continuity review")
    return ReviewResult(passed=not violations,violations=violations,warnings=warnings)

def main()->int:
    parser=argparse.ArgumentParser();parser.add_argument("--paragraph",required=True);parser.add_argument("--claim-json",required=True);parser.add_argument("--arc-context-json");args=parser.parse_args()
    text=Path(args.paragraph).read_text(encoding="utf-8");claim=json.loads(Path(args.claim_json).read_text(encoding="utf-8"));context=json.loads(Path(args.arc_context_json).read_text(encoding="utf-8")) if args.arc_context_json else {}
    result=review_paragraph(text,claim,context);print(json.dumps({"passed":result.passed,"violations":[asdict(x) for x in result.violations],"warnings":result.warnings},ensure_ascii=False,indent=2));return 0 if result.passed else 1
if __name__=="__main__":raise SystemExit(main())
