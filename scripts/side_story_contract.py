#!/usr/bin/env python3
"""Contract, lineage, coverage and render gates for side-story composition."""
from __future__ import annotations
import json,re,string
from pathlib import Path
from output_state import canonical_markdown_path,load_output_state

SCHEMA_VERSION="1.2"
SUPPORTED_SCHEMA_VERSIONS={"1.1","1.2"}
SIDE_STORY_CLASS="side_story"
APPARATUS_CLASS="apparatus"
VALID_CLASSES={SIDE_STORY_CLASS,APPARATUS_CLASS}
ANALYTICAL_FOCUS_KIND="analytical_focus"
KINDS={"detour","dezoom","also","method","false_lead","portrait","object_focus","comparator","callback",ANALYTICAL_FOCUS_KIND}
STATUSES={"candidate","validated","promoted","retired"}
RETURN_REQUIRED=KINDS-{"method"}
ZOOMS={f"Z{i}" for i in range(5)}
HILS={"HIL-01_institutions-chronology","HIL-02_geography-environment","HIL-03_economy-infrastructure","HIL-04_society-demography","HIL-05_religion-culture-legitimacy","HIL-06_security-coercion","HIL-07_regional-global-system","HIL-08_historiography-bias"}
RENDER_LABELS={"detour":"Petit détour","dezoom":"Dézoom","also":"Mais aussi","method":"Point de méthode","false_lead":"Fausse piste","portrait":"Personnage","object_focus":"Objet / terrain","comparator":"Comparaison","callback":"Fil rouge",ANALYTICAL_FOCUS_KIND:"Focus analytique"}
EVIDENCE_STATUSES={"verified","inference","unknown"}

def canonical_marker(sid):return f"[SIDE-STORY:{sid}]"
def side_story_dir(project):return project/"09_output"/"side_stories"
def _read_records(path):
    data=json.loads(path.read_text(encoding="utf-8"));return data if isinstance(data,list) else [data]
def load_side_stories(project):
    root=side_story_dir(project);out=[]
    if not root.exists():return out
    for p in sorted(root.glob("*.json")):
        for item in _read_records(p):out.append((p,item))
    return out
def _ids(project,pattern):
    out=set()
    for p in project.glob(pattern):
        try:item=json.loads(p.read_text(encoding="utf-8"))
        except Exception:continue
        if isinstance(item,dict) and item.get("id"):out.add(str(item["id"]))
    return out
def _sources(project):
    out=set()
    for p in (project/"05_sources").glob("source_register*.json"):
        data=json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data,list):out|={str(x["id"]) for x in data if isinstance(x,dict) and x.get("id")}
    return out
def _strip_markup(text):
    text=re.sub(r"<[^>]+>"," ",str(text));text=re.sub(r"[#*_`>\[\](){}]"," ",text)
    text=text.translate(str.maketrans({c:" " for c in string.punctuation+"«»“”‘’…–—≠×"}))
    return re.sub(r"\s+"," ",text).strip().casefold()
def _contains_anchor(markdown,anchor):return bool(anchor) and _strip_markup(anchor) in _strip_markup(markdown)
def _marker_block(markdown,marker):
    lines=markdown.splitlines();idx=next((i for i,x in enumerate(lines) if marker in x),None)
    if idx is None:return ""
    buf=[]
    for line in lines[idx:idx+60]:
        if buf and "[SIDE-STORY:" in line:break
        if buf and re.match(r"^##\s+",line):break
        buf.append(line)
    return "\n".join(buf)
def _lineage_nonempty(lineage):return any(lineage.get(k) for k in ("claim_ids","source_ids","bridge_ids","drift_paths","origin_paths"))
def _evidence_lineage(lineage):return bool((lineage.get("claim_ids") or []) or (lineage.get("source_ids") or []))
def _takeaway_echoes_title(item):
    takeaway=_strip_markup((item.get("content") or {}).get("takeaway",''));title=_strip_markup(item.get("title",''))
    return bool(takeaway and title and takeaway==title)
def _materialized_existing_fragment(item,canonical):
    if item.get("materialization_mode")!="existing_fragment":return False
    anchor=(item.get("placement") or {}).get("section_anchor") or item.get("title")
    return _contains_anchor(canonical,anchor)

def _analytical_focus_errors(prefix,item):
    errors=[]
    if item.get("schema_version")!="1.2":errors.append(f"side story {prefix}: analytical_focus requires schema 1.2")
    analysis=item.get("analysis") or {};visual=item.get("visual") or {};content=item.get("content") or {}
    for field in ("core_question","thesis"):
        if not analysis.get(field):errors.append(f"side story {prefix}: analysis.{field} required")
    contrast=analysis.get("contrast")
    if not isinstance(contrast,list) or len(contrast)<2:errors.append(f"side story {prefix}: analysis.contrast requires at least two positions")
    else:
        for i,row in enumerate(contrast):
            if not isinstance(row,dict) or not row.get("label") or not row.get("position") or not row.get("caveat"):
                errors.append(f"side story {prefix}: analysis.contrast[{i}] requires label/position/caveat")
    mechanisms=analysis.get("mechanisms")
    if not isinstance(mechanisms,list) or not mechanisms:errors.append(f"side story {prefix}: analysis.mechanisms requires at least one mechanism")
    else:
        for i,row in enumerate(mechanisms):
            if not isinstance(row,dict) or not row.get("name") or not row.get("explanation"):
                errors.append(f"side story {prefix}: analysis.mechanisms[{i}] requires name/explanation")
            if isinstance(row,dict) and row.get("evidence_status") not in EVIDENCE_STATUSES:
                errors.append(f"side story {prefix}: analysis.mechanisms[{i}].evidence_status invalid")
    callbacks=analysis.get("callbacks")
    if not isinstance(callbacks,list) or not callbacks:errors.append(f"side story {prefix}: analysis.callbacks requires at least one callback")
    else:
        for i,row in enumerate(callbacks):
            if not isinstance(row,dict) or not row.get("target") or not row.get("relation"):
                errors.append(f"side story {prefix}: analysis.callbacks[{i}] requires target/relation")
    if visual.get("format")!="one_or_two_pager":errors.append(f"side story {prefix}: visual.format must be one_or_two_pager")
    if visual.get("orientation")!="A4_landscape":errors.append(f"side story {prefix}: visual.orientation must be A4_landscape")
    if visual.get("layout")!="historical_focus":errors.append(f"side story {prefix}: visual.layout must be historical_focus")
    if (visual.get("evidence_palette") or {})!={"verified":"green","inference":"orange","unknown":"red"}:
        errors.append(f"side story {prefix}: visual.evidence_palette must preserve verified/inference/unknown semantics")
    composition=set(visual.get("composition") or []);required={"hero_question","contrast_cards","mechanism_band","callback_strip"}
    if not required.issubset(composition):errors.append(f"side story {prefix}: visual.composition missing {sorted(required-composition)}")
    if not content.get("takeaway"):errors.append(f"side story {prefix}: content.takeaway required")
    return errors

def validate_side_story_item(item,known=None,canonical="",strict=False):
    errors=[];sid=item.get("id");prefix=sid or "<unknown>";klass=item.get("class")
    if item.get("schema_version") not in SUPPORTED_SCHEMA_VERSIONS:errors.append(f"side story {prefix}: invalid schema_version")
    if klass not in VALID_CLASSES:errors.append(f"side story {prefix}: invalid class")
    if klass==APPARATUS_CLASS:
        if item.get("scope")!="book":errors.append(f"side story {prefix}: apparatus requires scope=book")
        if item.get("arc") not in (None,""):errors.append(f"side story {prefix}: apparatus must not have arc")
        if (item.get("placement") or {}).get("return_to") not in (None,""):errors.append(f"side story {prefix}: apparatus must not have return_to")
    kind=item.get("kind");status=item.get("status")
    if kind not in KINDS:errors.append(f"side story {prefix}: invalid kind {kind!r}")
    if status not in STATUSES:errors.append(f"side story {prefix}: invalid status {status!r}")
    if item.get("lineage_quality")=="legacy_fragment" and status=="promoted":errors.append(f"side story {prefix}: legacy_fragment cannot be promoted")
    if not isinstance(item.get("map_eligible"),bool):errors.append(f"side story {prefix}: map_eligible must be boolean")
    if not item.get("title") or not item.get("purpose"):errors.append(f"side story {prefix}: missing title/purpose")
    lineage=item.get("lineage") or {};render=item.get("render") or {}
    for key in ("claim_ids","source_ids","bridge_ids","hil_ids","drift_paths","origin_paths"):
        if not isinstance(lineage.get(key,[]),list):errors.append(f"side story {prefix}: lineage.{key} must be list")
    if sid and render.get("marker")!=canonical_marker(str(sid)):errors.append(f"side story {prefix}: invalid render marker")
    if kind in RENDER_LABELS and render.get("label")!=RENDER_LABELS[kind]:errors.append(f"side story {prefix}: label/kind mismatch")
    if not isinstance(render.get("required_in_reader"),bool):errors.append(f"side story {prefix}: required_in_reader must be boolean")
    if render.get("required_in_reader") and not _evidence_lineage(lineage):
        exempt=item.get("lineage_quality")=="legacy_fragment" and bool(item.get("legacy_retention_reason"))
        if not exempt:errors.append(f"side story {prefix}: required_in_reader without evidence lineage or legacy_retention_reason")
    if status in {"validated","promoted"}:
        takeaway=(item.get("content") or {}).get("takeaway")
        if not takeaway:errors.append(f"side story {prefix}: takeaway required outside candidate")
        elif _takeaway_echoes_title(item):errors.append(f"side story {prefix}: takeaway merely repeats title")
    if kind==ANALYTICAL_FOCUS_KIND:errors+=_analytical_focus_errors(prefix,item)
    return errors

def discover_side_story_fragments(markdown):
    found=[]
    html=re.compile(r"<p><strong>(POINT DE MÉTHODE|PETIT DÉTOUR|MAIS AUSSI|FAUSSE PISTE|FOCUS ANALYTIQUE)(?:\s*[—:-]\s*([^<]+))?</strong></p>(?:\s*<p><strong>([^<]+)</strong></p>)?",re.I)
    for m in html.finditer(markdown):
        label=m.group(1);title=(m.group(2) or m.group(3) or "").strip()
        if not title:
            after=markdown[m.end():m.end()+350];body=re.search(r"<p>([^<]+)</p>",after);title=(body.group(1).split(".")[0] if body else "untitled method").strip()
        found.append({"label":label,"title":title})
    md=re.compile(r"(?mi)^(?:#{1,6}\s*)?(?:\*\*)?(Mais aussi|Petit détour|Point de méthode|Fausse piste|Dézoom|Personnage|Objet / terrain|Comparaison|Fil rouge|Focus analytique)\s*[—:-]\s*([^\n*]+)")
    for m in md.finditer(markdown):found.append({"label":m.group(1),"title":m.group(2).strip()})
    return list({(_strip_markup(x["label"]),_strip_markup(x["title"])):x for x in found}.values())

def _record_aliases(item):return [item.get("title","")]+list((item.get("content") or {}).get("legacy_titles") or [])
def _matches_fragment(item,frag):
    title=_strip_markup(frag["title"])
    for alias in _record_aliases(item):
        a=_strip_markup(alias)
        if a and (title==a or (len(title)>12 and (title in a or a in title))):return True
    return False

def side_story_coverage(project):
    canonical=canonical_markdown_path(project).read_text(encoding="utf-8");discovered=discover_side_story_fragments(canonical);stories=[item for _,item in load_side_stories(project)]
    required=[item for item in stories if (item.get("render") or {}).get("required_in_reader")]
    traced=[item for item in required if _evidence_lineage(item.get("lineage") or {})]
    declared=[item for item in required if not _evidence_lineage(item.get("lineage") or {})]
    legacy_required_exemptions=sum(1 for item in declared if item.get("lineage_quality")=="legacy_fragment" and item.get("legacy_retention_reason"))
    untracked=[]
    for frag in discovered:
        if not any(_matches_fragment(item,frag) for item in stories):untracked.append(frag)
    return {"discovered":len(discovered),"traced":len(traced),"declared":len(declared),"untracked":len(untracked),"legacy_required_exemptions":legacy_required_exemptions,"untracked_fragments":untracked}

def validate_side_stories(project,*,check_render=True):
    errors=[];warnings=[]
    empty={"discovered":0,"traced":0,"declared":0,"untracked":0,"legacy_required_exemptions":0,"untracked_fragments":[]}
    try:
        stories=load_side_stories(project)
        if not stories and not (project/"00_method/output_state.json").exists():return [],[],0,empty
        canonical=canonical_markdown_path(project).read_text(encoding="utf-8");claims=_ids(project,"01_arcs/*/claims/*.json");bridges=_ids(project,"06_bridges/*.json");sources=_sources(project);arcs={p.name for p in (project/"01_arcs").iterdir() if p.is_dir()} if (project/"01_arcs").exists() else set()
    except Exception as exc:return [f"invalid side-story registry/state: {exc}"],[],0,empty
    seen=set()
    for path,item in stories:
        sid=item.get("id");prefix=sid or path.name;errors+=validate_side_story_item(item,canonical=canonical)
        if not sid:errors.append(f"side story {path.name}: missing id")
        elif sid in seen:errors.append(f"duplicate side story id: {sid}")
        else:seen.add(sid)
        klass=item.get("class");kind=item.get("kind");status=item.get("status");lineage=item.get("lineage") or {};placement=item.get("placement") or {};render=item.get("render") or {}
        anchor=placement.get("section_anchor")
        if klass!=APPARATUS_CLASS and status in {"validated","promoted"} and not anchor:errors.append(f"side story {prefix}: missing section_anchor")
        if anchor and status in {"validated","promoted"} and not _contains_anchor(canonical,anchor):errors.append(f"side story {prefix}: section_anchor does not resolve in canonical state")
        ret=placement.get("return_to")
        if kind=="method" and ret not in (None,""):errors.append(f"side story {prefix}: method must not invent a return_to")
        if klass!=APPARATUS_CLASS and kind in RETURN_REQUIRED and status in {"validated","promoted"}:
            if not ret:errors.append(f"side story {prefix}: missing return_to")
            elif ret in claims or ret in bridges or ret in arcs:pass
            elif isinstance(ret,str) and ret.startswith("anchor:") and _contains_anchor(canonical,ret.split(":",1)[1]):pass
            else:errors.append(f"side story {prefix}: return_to does not resolve")
        strict=status in {"validated","promoted"};legacy=item.get("lineage_quality")=="legacy_fragment"
        if strict:
            if not _lineage_nonempty(lineage):errors.append(f"side story {prefix}: no lineage")
            if klass!=APPARATUS_CLASS and not legacy and item.get("arc") not in arcs:errors.append(f"side story {prefix}: unknown arc {item.get('arc')!r}")
            for vals,known,label in ((lineage.get("claim_ids") or [],claims,"claims"),(lineage.get("source_ids") or [],sources,"sources"),(lineage.get("bridge_ids") or [],bridges,"bridges")):
                bad=set(vals)-known
                if bad:errors.append(f"side story {prefix}: unknown {label} {sorted(bad)}")
            bad_h=set(lineage.get("hil_ids") or [])-HILS
            if bad_h:errors.append(f"side story {prefix}: unknown HILs {sorted(bad_h)}")
            for rel in (lineage.get("drift_paths") or [])+(lineage.get("origin_paths") or []):
                if not (project/rel).exists():errors.append(f"side story {prefix}: missing lineage path {rel}")
        if kind=="dezoom":
            z=item.get("zoom_excursion") or {}
            for field in ("from","to","return_to","mechanism","local_payoff"):
                if not z.get(field):errors.append(f"side story {prefix}: dezoom missing {field}")
            for field in ("from","to","return_to"):
                if z.get(field) and z[field] not in ZOOMS:errors.append(f"side story {prefix}: invalid dezoom {field}")
        marker=render.get("marker")
        if status=="retired" and marker and marker in canonical:errors.append(f"side story {prefix}: retired marker still present in canonical")
        if check_render and status=="promoted":
            if marker in canonical:
                if _strip_markup(render.get("label","")) not in _strip_markup(_marker_block(canonical,marker)):errors.append(f"side story {prefix}: normalized label not in marker block")
            elif not _materialized_existing_fragment(item,canonical):errors.append(f"side story {prefix}: promoted marker missing from canonical state")
    coverage=side_story_coverage(project)
    try:require_complete=bool(load_output_state(project).get("composition",{}).get("side_story_coverage_required"))
    except Exception:require_complete=False
    if require_complete and coverage["untracked"]:errors.append(f"side-story coverage incomplete: traced {coverage['traced']} / declared {coverage['declared']} / discovered {coverage['discovered']}; {coverage['untracked']} untracked: {coverage['untracked_fragments']}")
    if coverage["declared"]:warnings.append(f"side-story evidence debt: {coverage['declared']} required records without claim/source lineage")
    if coverage["legacy_required_exemptions"]:warnings.append(f"side-story legacy retention exemptions: {coverage['legacy_required_exemptions']}")
    return errors,warnings,len(stories),coverage

def assert_rendered_side_stories(project,markdown):
    missing=[]
    for _,item in load_side_stories(project):
        if item.get("status")!="promoted":continue
        render=item.get("render") or {}
        if not render.get("required_in_reader"):continue
        if render.get("marker") in markdown:continue
        if item.get("materialization_mode")=="existing_fragment":continue
        missing.append(str(item.get("id")))
    if missing:raise RuntimeError("side-story retention gate failed: missing "+", ".join(sorted(missing)))
def validate_or_raise(project,*,check_render=True):
    errors,warnings,count,_=validate_side_stories(project,check_render=check_render)
    if errors:raise ValueError('; '.join(errors))
    return count
