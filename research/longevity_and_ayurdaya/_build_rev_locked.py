from __future__ import annotations

import csv
import datetime as dt
import hashlib
import re
import shutil
from pathlib import Path

SOURCE_ROOT = Path(r"D:/lab/Pyjhora")
REPO_ROOT = Path(r"d:/Diba")
OUT_ROOT = REPO_ROOT / "research" / "longevity_and_ayurdaya"
CODEPACK_ROOT = OUT_ROOT / "_codepack"

ENGINE_FILES = [
    "src/jhora/horoscope/dhasa/graha/aayu.py",
    "src/jhora/horoscope/prediction/longevity.py",
    "src/jhora/horoscope/chart/house.py",
    "src/jhora/horoscope/dhasa/raasi/sandhya.py",
    "src/jhora/const.py",
]
CONSUMER_FILES = [
    "src/jhora/horoscope/main.py",
]
IN_SCOPE = ENGINE_FILES + CONSUMER_FILES
ENGINE_SET = set(ENGINE_FILES)
CONSUMER_SET = set(CONSUMER_FILES)

PATTERNS = [
    "harana", "bharana", "_apply_harana", "chakrapata", "astangata", "shatru_kshetra", "krurodaya",
    "aayu", "ayur", "longevity", "life_span",
    "pindayu", "nisargayu", "amsayu", "sandhya",
    "alpaayu", "madhyaayu", "poornaayu", "alpa", "madhya", "poorna",
    "is_amsayu", "min(", "method=", "NOT FULLY IMPLEMENTED", "return _pindayu_santhanam", "return _nisargayu_santhanam", "TODO",
]

CALLSITE_COLUMNS = ["file", "line", "pattern", "function_context", "anchor_id", "scope_class"]
BASE_COLUMNS = [
    "file", "function", "ayur_family", "formula_signature", "inputs", "constants", "pre_harana_output",
    "implementation_status", "evidence_lines", "anchor_id"
]
HARANA_COLUMNS = [
    "file", "function", "sequence_index", "rule_name", "applies_to_family", "condition", "raw_factor_formula",
    "combine_operator", "conflict_resolution", "depends_on_state", "skip_flags", "implementation_status", "evidence_lines", "anchor_id"
]
BHARANA_COLUMNS = [
    "file", "function", "rule_name", "trigger", "scale_factor", "priority_resolution", "output_factor", "evidence_lines", "anchor_id"
]
CLASS_COLUMNS = [
    "file", "function", "class_scheme", "method_variant", "decision_inputs", "threshold_map", "output_labels", "consumer_path", "evidence_lines", "anchor_id"
]
OUTIDX_COLUMNS = ["producer_function", "producer_shape", "consumer_function", "consumer_index_use", "match_status", "evidence_lines", "anchor_id"]


def norm_rel(p: Path) -> str:
    return str(p.as_posix())


def read_lines(rel: str) -> list[str]:
    return (SOURCE_ROOT / rel).read_text(encoding="utf-8", errors="replace").splitlines()


def sha256_and_size(path: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest(), path.stat().st_size


def scope_class(rel: str) -> str:
    if rel in ENGINE_SET:
        return "engine_core"
    if rel in CONSUMER_SET:
        return "consumer_core"
    return "residual"


def function_context_map(lines: list[str]) -> list[str]:
    ctx = "<module>"
    out = []
    for ln in lines:
        m = re.match(r"^\s*def\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(", ln)
        if m:
            ctx = m.group(1)
        out.append(ctx)
    return out


def excerpt(rel: str, start: int, end: int) -> str:
    lines = read_lines(rel)
    s = max(1, start)
    e = min(len(lines), end)
    block = lines[s - 1:e]
    kept = []
    for ln in block:
        if "http://" in ln or "https://" in ln:
            continue
        kept.append(ln)
        if len(kept) >= 12:
            break
    return "\n".join(kept)

def collect_scan_files() -> list[str]:
    root = SOURCE_ROOT / "src" / "jhora"
    rels = []
    for p in root.rglob("*.py"):
        rel = norm_rel(p.relative_to(SOURCE_ROOT))
        if "/ui/" in rel or "/tests/" in rel or rel.endswith("/drik1.py"):
            continue
        rels.append(rel)
    return sorted(set(rels) | set(IN_SCOPE))


def find_matches(lines: list[str], pattern: str):
    if pattern == "min(":
        rgx = re.compile(r"min\(")
    elif pattern == "method=":
        rgx = re.compile(r"method\s*=")
    else:
        rgx = re.compile(re.escape(pattern), re.IGNORECASE)
    for i, ln in enumerate(lines, 1):
        if rgx.search(ln):
            yield i


def build_callsites() -> list[dict]:
    rows: list[dict] = []
    scan_files = collect_scan_files()
    for rel in scan_files:
        lines = read_lines(rel)
        ctx = function_context_map(lines)
        hit = 0
        for pat in PATTERNS:
            for line_no in find_matches(lines, pat):
                hit += 1
                rows.append({
                    "file": rel,
                    "line": str(line_no),
                    "pattern": pat,
                    "function_context": ctx[line_no - 1],
                    "anchor_id": "AY900",
                    "scope_class": scope_class(rel),
                })
        if rel in set(IN_SCOPE) and hit == 0:
            rows.append({
                "file": rel,
                "line": "0",
                "pattern": "not_found_in_file",
                "function_context": "<module>",
                "anchor_id": "AY900",
                "scope_class": scope_class(rel),
            })
    return rows


def build_base_matrix() -> list[dict]:
    return [
        {
            "file": "src/jhora/horoscope/dhasa/graha/aayu.py",
            "function": "_pindayu_santhanam",
            "ayur_family": "pindayu",
            "formula_signature": "arc_from_deep_exaltation -> piecewise(full - full*arc/360)",
            "inputs": "planet_positions,planet_deep_exaltation_longitudes",
            "constants": "pindayu_full_longevity_of_planets",
            "pre_harana_output": "planet_base_longevity dict",
            "implementation_status": "Active",
            "evidence_lines": "src/jhora/horoscope/dhasa/graha/aayu.py:L282-L297",
            "anchor_id": "AY06",
        },
        {
            "file": "src/jhora/horoscope/dhasa/graha/aayu.py",
            "function": "_pindayu",
            "ayur_family": "pindayu",
            "formula_signature": "early return to _pindayu_santhanam then unreachable alternate branch",
            "inputs": "planet_positions,apply_haranas,method",
            "constants": "pindayu_full_longevity_of_planets",
            "pre_harana_output": "delegated",
            "implementation_status": "Dead_Branch",
            "evidence_lines": "src/jhora/horoscope/dhasa/graha/aayu.py:L299-L310",
            "anchor_id": "AY07",
        },
        {
            "file": "src/jhora/horoscope/dhasa/graha/aayu.py",
            "function": "_nisargayu_santhanam",
            "ayur_family": "nisargayu",
            "formula_signature": "arc_from_deep_exaltation -> piecewise(full - full*arc/360)",
            "inputs": "planet_positions,planet_deep_exaltation_longitudes",
            "constants": "nisargayu_full_longevity_of_planets",
            "pre_harana_output": "planet_base_longevity dict",
            "implementation_status": "Active",
            "evidence_lines": "src/jhora/horoscope/dhasa/graha/aayu.py:L312-L327",
            "anchor_id": "AY08",
        },
        {
            "file": "src/jhora/horoscope/dhasa/graha/aayu.py",
            "function": "_nisargayu",
            "ayur_family": "nisargayu",
            "formula_signature": "early return to _nisargayu_santhanam then unreachable alternate branch",
            "inputs": "planet_positions,apply_haranas,method",
            "constants": "nisargayu_full_longevity_of_planets",
            "pre_harana_output": "delegated",
            "implementation_status": "Dead_Branch",
            "evidence_lines": "src/jhora/horoscope/dhasa/graha/aayu.py:L329-L345",
            "anchor_id": "AY09",
        },
        {
            "file": "src/jhora/horoscope/dhasa/graha/aayu.py",
            "function": "_amsayu",
            "ayur_family": "amsayu",
            "formula_signature": "base=(planet_long*108)%12 (or *60/200 varahamihira)",
            "inputs": "planet_positions,method",
            "constants": "none",
            "pre_harana_output": "planet_base_longevity dict",
            "implementation_status": "Active",
            "evidence_lines": "src/jhora/horoscope/dhasa/graha/aayu.py:L348-L360",
            "anchor_id": "AY10",
        },
        {
            "file": "src/jhora/horoscope/dhasa/graha/aayu.py",
            "function": "_apply_harana",
            "ayur_family": "all",
            "formula_signature": "sequential min aggregation over harana factors",
            "inputs": "base_aayu,is_amsayu,method",
            "constants": "none",
            "pre_harana_output": "final_harana dict",
            "implementation_status": "Active",
            "evidence_lines": "src/jhora/horoscope/dhasa/graha/aayu.py:L246-L280",
            "anchor_id": "AY11",
        },
        {
            "file": "src/jhora/horoscope/dhasa/graha/aayu.py",
            "function": "module_docstring",
            "ayur_family": "all",
            "formula_signature": "status disclaimer",
            "inputs": "N/A",
            "constants": "N/A",
            "pre_harana_output": "N/A",
            "implementation_status": "WIP",
            "evidence_lines": "src/jhora/horoscope/dhasa/graha/aayu.py:L22-L25",
            "anchor_id": "AY05",
        },
    ]

def build_harana_matrix() -> list[dict]:
    return [
        {
            "file": "src/jhora/horoscope/dhasa/graha/aayu.py",
            "function": "_apply_harana",
            "sequence_index": "1",
            "rule_name": "astangata_harana",
            "applies_to_family": "pindayu,nisargayu,amsayu",
            "condition": "planet in combustion/retrograde set with ignore rules",
            "raw_factor_formula": "0.5 for selected planets else 1.0",
            "combine_operator": "seed",
            "conflict_resolution": "initial factor map",
            "depends_on_state": "combustion,retrograde",
            "skip_flags": "none",
            "implementation_status": "Active",
            "evidence_lines": "src/jhora/horoscope/dhasa/graha/aayu.py:L262-L266",
            "anchor_id": "AY12",
        },
        {
            "file": "src/jhora/horoscope/dhasa/graha/aayu.py",
            "function": "_apply_harana",
            "sequence_index": "2",
            "rule_name": "shatru_kshetra_harana",
            "applies_to_family": "pindayu,nisargayu,amsayu",
            "condition": "enemy sign and not exempt retrograde",
            "raw_factor_formula": "2/3 for eligible planets",
            "combine_operator": "min",
            "conflict_resolution": "final_harana[p]=min(prev,skh[p])",
            "depends_on_state": "enemy_sign,retrograde",
            "skip_flags": "none",
            "implementation_status": "Active",
            "evidence_lines": "src/jhora/horoscope/dhasa/graha/aayu.py:L265-L267",
            "anchor_id": "AY13",
        },
        {
            "file": "src/jhora/horoscope/dhasa/graha/aayu.py",
            "function": "_apply_harana",
            "sequence_index": "3",
            "rule_name": "chakrapata_harana",
            "applies_to_family": "pindayu,nisargayu,amsayu",
            "condition": "visible hemisphere and benefic/malefic weighting",
            "raw_factor_formula": "lookup from subha_asubha_factors_dict",
            "combine_operator": "min",
            "conflict_resolution": "final_harana[p]=min(prev,ch[p])",
            "depends_on_state": "relative_house,benefic_malefic_class",
            "skip_flags": "method_variant chooses santhanam vs varahamihira path",
            "implementation_status": "Active",
            "evidence_lines": "src/jhora/horoscope/dhasa/graha/aayu.py:L269-L271",
            "anchor_id": "AY14",
        },
        {
            "file": "src/jhora/horoscope/dhasa/graha/aayu.py",
            "function": "_apply_harana",
            "sequence_index": "4",
            "rule_name": "krurodaya_harana",
            "applies_to_family": "pindayu,nisargayu",
            "condition": "not is_amsayu",
            "raw_factor_formula": "lagna-fraction based reduction",
            "combine_operator": "min",
            "conflict_resolution": "final_harana[p]=min(prev,kh[p])",
            "depends_on_state": "lagna_proximity,benefic_aspect",
            "skip_flags": "bypass when is_amsayu=True",
            "implementation_status": "Active",
            "evidence_lines": "src/jhora/horoscope/dhasa/graha/aayu.py:L272-L276",
            "anchor_id": "AY15",
        },
        {
            "file": "src/jhora/horoscope/dhasa/graha/aayu.py",
            "function": "_apply_harana",
            "sequence_index": "5",
            "rule_name": "final_application",
            "applies_to_family": "all",
            "condition": "apply final_harana factor to base",
            "raw_factor_formula": "graha_aayu=base_aayu*final_harana",
            "combine_operator": "multiply_after_harana",
            "conflict_resolution": "single reduced factor used",
            "depends_on_state": "final_harana",
            "skip_flags": "none",
            "implementation_status": "Active",
            "evidence_lines": "src/jhora/horoscope/dhasa/graha/aayu.py:L279-L280",
            "anchor_id": "AY16",
        },
        {
            "file": "src/jhora/horoscope/dhasa/graha/aayu.py",
            "function": "_krurodaya_harana",
            "sequence_index": "6",
            "rule_name": "krurodaya_todo_gap",
            "applies_to_family": "pindayu,nisargayu",
            "condition": "method=2 documentation vs actual partial implementation",
            "raw_factor_formula": "partial lagna-based logic",
            "combine_operator": "bypass/partial",
            "conflict_resolution": "TODO unresolved bullets",
            "depends_on_state": "malefic_with_lagna,benefic_aspect",
            "skip_flags": "none",
            "implementation_status": "WIP",
            "evidence_lines": "src/jhora/horoscope/dhasa/graha/aayu.py:L188-L201",
            "anchor_id": "AY17",
        },
    ]


def build_bharana_matrix() -> list[dict]:
    return [
        {
            "file": "src/jhora/horoscope/dhasa/graha/aayu.py",
            "function": "_bharana",
            "rule_name": "triple_factor",
            "trigger": "retrograde OR exalted OR owner_ruler",
            "scale_factor": "3.0",
            "priority_resolution": "applied before 2x update",
            "output_factor": "bharana_factors[p]=3",
            "evidence_lines": "src/jhora/horoscope/dhasa/graha/aayu.py:L234-L239",
            "anchor_id": "AY18",
        },
        {
            "file": "src/jhora/horoscope/dhasa/graha/aayu.py",
            "function": "_bharana",
            "rule_name": "double_factor",
            "trigger": "sva-navamsa OR sva-drekkana OR vargottama-navamsa",
            "scale_factor": "2.0",
            "priority_resolution": "if both 3x and 2x apply, higher factor intended by comment",
            "output_factor": "bharana_factors[p]=2/3 per update",
            "evidence_lines": "src/jhora/horoscope/dhasa/graha/aayu.py:L240-L245",
            "anchor_id": "AY19",
        },
    ]


def build_classification_matrix() -> list[dict]:
    return [
        {
            "file": "src/jhora/horoscope/prediction/longevity.py",
            "function": "life_span_range",
            "class_scheme": "alpa/madhya/poorna index",
            "method_variant": "none",
            "decision_inputs": "lagna_lord_house,eighth_lord_house,asc_house,moon_house,hora_lagna",
            "threshold_map": "fixed/movable/dual pairing logic",
            "output_labels": "0=alpa,1=madhya,2=poorna (via const.aayu_types)",
            "consumer_path": "prediction module standalone",
            "evidence_lines": "src/jhora/horoscope/prediction/longevity.py:L152-L194",
            "anchor_id": "AY20",
        },
        {
            "file": "src/jhora/horoscope/chart/house.py",
            "function": "longevity",
            "class_scheme": "pair-based longevity_years lookup",
            "method_variant": "none",
            "decision_inputs": "(lagna_lord,eighth_lord),(moon,saturn),(lagna,hora_lagna)",
            "threshold_map": "const.longevity + const.longevity_years",
            "output_labels": "years bucket from matrix",
            "consumer_path": "chart.house direct utility",
            "evidence_lines": "src/jhora/horoscope/chart/house.py:L1098-L1149",
            "anchor_id": "AY21",
        },
        {
            "file": "src/jhora/horoscope/dhasa/graha/aayu.py",
            "function": "get_dhasa_antardhasa",
            "class_scheme": "aayur type routing",
            "method_variant": "santhanam_m1|varahamihira_m2",
            "decision_inputs": "sp in {sun,moon,lagna}, dhasa_method, apply_haranas",
            "threshold_map": "sp->pindayu/nisargayu/amsayu",
            "output_labels": "_dhasa_type 0/1/2",
            "consumer_path": "main._get_aayu_dhasa_bhukthi",
            "evidence_lines": "src/jhora/horoscope/dhasa/graha/aayu.py:L409-L460",
            "anchor_id": "AY22",
        },
    ]


def build_output_matrix() -> list[dict]:
    return [
        {
            "producer_function": "aayu.get_dhasa_antardhasa",
            "producer_shape": "(_dhasa_type, list[(dhasa_lord,bhukthi_lord,start,duration)])",
            "consumer_function": "main._get_aayu_dhasa_bhukthi",
            "consumer_index_use": "self._aayu_dhasa_type, then unpack 4-field tuples",
            "match_status": "match",
            "evidence_lines": "src/jhora/horoscope/main.py:L1152-L1158",
            "anchor_id": "AY23",
        },
        {
            "producer_function": "aayu.longevity",
            "producer_shape": "(total_longevity,_aayu_type)",
            "consumer_function": "direct module consumer (none in main)",
            "consumer_index_use": "N/A",
            "match_status": "orphan_producer",
            "evidence_lines": "src/jhora/horoscope/dhasa/graha/aayu.py:L494-L497",
            "anchor_id": "AY24",
        },
    ]

def anchor_specs() -> list[dict]:
    return [
        {"id":"AY01","behavior":"Longevity category and year matrices are defined in constants.","src":"src/jhora/const.py","start":398,"end":399,"obs":"Fixed/movable/dual mapping and year buckets are hardcoded."},
        {"id":"AY02","behavior":"Pindayu/Nisargayu baseline constants and labels are module-level constants.","src":"src/jhora/const.py","start":623,"end":629,"obs":"Base and full values plus aayu labels are centralized."},
        {"id":"AY03","behavior":"Main consumer routes aayu dhasa via get_dhasa_antardhasa.","src":"src/jhora/horoscope/main.py","start":1149,"end":1158,"obs":"Consumer captures _aayu_dhasa_type and unpacks 4-field rows."},
        {"id":"AY04","behavior":"Aayu engine entrypoint publishes aayu-type and dhasa rows.","src":"src/jhora/horoscope/dhasa/graha/aayu.py","start":409,"end":460,"obs":"Dispatches among pindayu/nisargayu/amsayu using seed selector."},
        {"id":"AY05","behavior":"Aayu module self-labels implementation incompleteness.","src":"src/jhora/horoscope/dhasa/graha/aayu.py","start":22,"end":25,"obs":"WIP disclaimer exists directly in module header."},
        {"id":"AY06","behavior":"Pindayu base formula is implemented in santhanam path.","src":"src/jhora/horoscope/dhasa/graha/aayu.py","start":282,"end":297,"obs":"Arc-based base years are computed before harana."},
        {"id":"AY07","behavior":"Pindayu wrapper contains dead branch after early return.","src":"src/jhora/horoscope/dhasa/graha/aayu.py","start":299,"end":310,"obs":"Code after immediate return is unreachable."},
        {"id":"AY08","behavior":"Nisargayu base formula is implemented in santhanam path.","src":"src/jhora/horoscope/dhasa/graha/aayu.py","start":312,"end":327,"obs":"Arc-based base years are computed before harana."},
        {"id":"AY09","behavior":"Nisargayu wrapper contains dead branch after early return.","src":"src/jhora/horoscope/dhasa/graha/aayu.py","start":329,"end":345,"obs":"Alternate method block is unreachable as written."},
        {"id":"AY10","behavior":"Amsayu computes base then applies Bharana and Harana.","src":"src/jhora/horoscope/dhasa/graha/aayu.py","start":348,"end":360,"obs":"Amsayu path multiplies bharana and harana results."},
        {"id":"AY11","behavior":"_apply_harana composes reductions in sequential chain.","src":"src/jhora/horoscope/dhasa/graha/aayu.py","start":246,"end":280,"obs":"Reduction chain is explicit and ordered."},
        {"id":"AY12","behavior":"Astangata and shatru_kshetra are combined with min().","src":"src/jhora/horoscope/dhasa/graha/aayu.py","start":262,"end":267,"obs":"Combine operator is min, not multiplicative."},
        {"id":"AY13","behavior":"Chakrapata is merged through another min() pass.","src":"src/jhora/horoscope/dhasa/graha/aayu.py","start":269,"end":271,"obs":"Sequential min aggregation continues."},
        {"id":"AY14","behavior":"Krurodaya is bypassed for Amsayu.","src":"src/jhora/horoscope/dhasa/graha/aayu.py","start":272,"end":276,"obs":"is_amsayu flag disables krurodaya application."},
        {"id":"AY15","behavior":"Krurodaya method-2 block includes explicit TODO for missing bullets.","src":"src/jhora/horoscope/dhasa/graha/aayu.py","start":188,"end":201,"obs":"Specification and implementation are partially diverged."},
        {"id":"AY16","behavior":"Bharana factors (3x/2x) are computed in dedicated function.","src":"src/jhora/horoscope/dhasa/graha/aayu.py","start":226,"end":245,"obs":"Bharana increase rules are separated from Harana."},
        {"id":"AY17","behavior":"Prediction module computes alpa/madhya/poorna class by pairing logic.","src":"src/jhora/horoscope/prediction/longevity.py","start":152,"end":194,"obs":"Standalone life_span_range classification path exists."},
        {"id":"AY18","behavior":"House module exposes second independent longevity classification path.","src":"src/jhora/horoscope/chart/house.py","start":1098,"end":1149,"obs":"Parallel classification path uses const.longevity_years matrix."},
        {"id":"AY19","behavior":"Sandhya is parallel ayurdasa path with fixed duration spread.","src":"src/jhora/horoscope/dhasa/raasi/sandhya.py","start":22,"end":64,"obs":"Ayurdaya-related but distinct from pinda/nisarga/amsa."},
        {"id":"AY900","behavior":"Residual matched rows are retained in callsite inventory.","src":"research/longevity_and_ayurdaya/_coverage_longevity_callsites_engine_plus_consumers.tsv","start":1,"end":1,"obs":"Non-focused matches remain visible as residual evidence."},
    ]


def write_tsv(path: Path, columns: list[str], rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columns, delimiter="\t")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in columns})


def build_map_md(digests: list[tuple[str, str, int]], call_rows: list[dict], anchors: list[dict]):
    t = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    out = []
    out.append("# longevity_behavior_contract_map.engine_plus_consumers.md")
    out.append("")
    out.append("## Snapshot identity (FACTS)")
    out.append("")
    out.append(f"- pyjhora_root: `{SOURCE_ROOT}`")
    out.append(f"- extraction_timestamp_local: `{t}`")
    out.append(f"- in-scope files: `{len(IN_SCOPE)}`")
    out.append("- in-scope file digests (SHA256):")
    for rel, h, sz in digests:
        out.append(f"  - `{rel}` -> `{h}` (bytes: `{sz}`)")
    out.append("")
    out.append("## Scope (FACTS)")
    out.append("")
    out.append("- In-scope engine files:")
    for r in ENGINE_FILES: out.append(f"  - `{r}`")
    out.append("- In-scope consumers/config:")
    for r in CONSUMER_FILES: out.append(f"  - `{r}`")
    out.append("- Out-of-scope:")
    out.append("  - UI modules")
    out.append("  - tests")
    out.append("  - `src/jhora/panchanga/drik1.py`")
    out.append("  - deep consumers outside one-hop list")
    out.append("")
    out.append("## Pattern inventory (FACTS)")
    out.append("")
    for p in PATTERNS:
        out.append(f"- `{p}`")
    out.append("")
    out.append("## Behavior taxonomy (FACTS)")
    out.append("")
    out.append("- constants and year buckets: `AY01`, `AY02`")
    out.append("- aayu engine routing and output contracts: `AY03`, `AY04`")
    out.append("- base formula paths and dead branches: `AY05`, `AY06`, `AY07`, `AY08`, `AY09`, `AY10`")
    out.append("- harana/bharana sequencing and operators: `AY11`, `AY12`, `AY13`, `AY14`, `AY15`, `AY16`")
    out.append("- parallel classification systems: `AY17`, `AY18`")
    out.append("- parallel ayurdasa path: `AY19`")
    out.append("- residual inventory: `AY900`")
    out.append("")
    out.append("## Evidence anchors (AY01..AYNN, AY900)")
    out.append("")
    for a in anchors:
        out.append(f"### {a['id']}")
        out.append("")
        out.append(f"- Behavior: {a['behavior']}")
        if a["src"].startswith("src/"):
            out.append(f"- Source: `{a['src']}:L{a['start']}-L{a['end']}`")
            out.append("- Excerpt:")
            out.append("```python")
            out.append(excerpt(a["src"], a["start"], a["end"]))
            out.append("```")
        else:
            out.append(f"- Source: `{a['src']}`")
            out.append("- Excerpt:")
            out.append("```text")
            out.append("Rows with anchor_id=AY900 remain in inventory as residual evidence.")
            out.append("```")
        out.append(f"- Observed behavior: {a['obs']}")
        out.append("")
    out.append("## Conflict / ambiguity register")
    out.append("")
    out.append("- UNCERTAIN-AY-HARANA-COMBINE: Harana aggregation uses `min` operator instead of multiplicative composition.")
    out.append("- UNCERTAIN-AY-DEAD-CODE: `_pindayu` and `_nisargayu` include unreachable branches after early return.")
    out.append("- UNCERTAIN-AY-DUPLICATE-CLASS: longevity class logic appears in both prediction and house modules.")
    out.append("- UNCERTAIN-AY-METHOD-PROPAGATION: method 1/2 behavior is partially divergent and partially bypassed.")
    out.append("")
    out.append("## Coverage ledger")
    out.append("")
    out.append("- Inventory file: `research/longevity_and_ayurdaya/_coverage_longevity_callsites_engine_plus_consumers.tsv`")
    out.append("- Inventory columns: `file`, `line`, `pattern`, `function_context`, `anchor_id`, `scope_class`")
    out.append(f"- Inventory row count: `{len(call_rows)}`")
    ufs = len({(r['file'], r['function_context']) for r in call_rows})
    out.append(f"- Unique `(file,function_context)` count: `{ufs}`")
    ec = sum(1 for r in call_rows if r["scope_class"] == "engine_core")
    cc = sum(1 for r in call_rows if r["scope_class"] == "consumer_core")
    rc = sum(1 for r in call_rows if r["scope_class"] == "residual")
    out.append(f"- Rows by scope_class: `engine_core={ec}`, `consumer_core={cc}`, `residual={rc}`")
    ay900 = sum(1 for r in call_rows if r["anchor_id"] == "AY900")
    out.append(f"- Residual rows (`AY900`): `{ay900}`")
    out.append("- Base matrix: `research/longevity_and_ayurdaya/_coverage_longevity_base_ayur_formula_matrix.tsv`")
    out.append("- Harana matrix: `research/longevity_and_ayurdaya/_coverage_longevity_harana_reduction_matrix.tsv`")
    out.append("- Bharana matrix: `research/longevity_and_ayurdaya/_coverage_longevity_bharana_increase_matrix.tsv`")
    out.append("- Classification matrix: `research/longevity_and_ayurdaya/_coverage_longevity_classification_matrix.tsv`")
    out.append("- Output-contract matrix: `research/longevity_and_ayurdaya/_coverage_longevity_output_contract_matrix.tsv`")
    out.append("")
    out.append("## Sanity checks")
    out.append("")
    out.append("- command: `rg -n \"^### AY[0-9]+|^### AY900\" research/longevity_and_ayurdaya/longevity_behavior_contract_map.engine_plus_consumers.md -S`")
    out.append("- command: `rg -n \"UNCERTAIN-AY-\" research/longevity_and_ayurdaya/longevity_behavior_contract_map.engine_plus_consumers.md -S`")
    out.append("- command: `rg -n \"Source:\" research/longevity_and_ayurdaya/longevity_behavior_contract_map.engine_plus_consumers.md -S`")
    out.append("- command: `Get-Content research/longevity_and_ayurdaya/_coverage_longevity_callsites_engine_plus_consumers.tsv | Measure-Object -Line`")
    out.append("- command: `Get-Content research/longevity_and_ayurdaya/_coverage_longevity_base_ayur_formula_matrix.tsv | Measure-Object -Line`")
    out.append("- command: `Get-Content research/longevity_and_ayurdaya/_coverage_longevity_harana_reduction_matrix.tsv | Measure-Object -Line`")
    out.append("- command: `Get-Content research/longevity_and_ayurdaya/_coverage_longevity_bharana_increase_matrix.tsv | Measure-Object -Line`")
    out.append("- command: `Get-Content research/longevity_and_ayurdaya/_coverage_longevity_classification_matrix.tsv | Measure-Object -Line`")
    out.append("- command: `Get-Content research/longevity_and_ayurdaya/_coverage_longevity_output_contract_matrix.tsv | Measure-Object -Line`")
    (OUT_ROOT / "longevity_behavior_contract_map.engine_plus_consumers.md").write_text("\n".join(out) + "\n", encoding="utf-8")


def copy_codepack_and_manifest(digests: list[tuple[str, str, int]]):
    for rel, _, _ in digests:
        src = SOURCE_ROOT / rel
        dst = CODEPACK_ROOT / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
    rows = []
    for rel, h, sz in sorted(digests, key=lambda x: x[0]):
        cp = CODEPACK_ROOT / rel
        ch, csz = sha256_and_size(cp)
        rows.append({
            "original_path": rel,
            "codepack_path": norm_rel(cp.relative_to(CODEPACK_ROOT)),
            "sha256": h,
            "bytes": str(sz),
            "copied_sha256": ch,
            "copied_bytes": str(csz),
        })
    with (CODEPACK_ROOT / "MANIFEST.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["original_path", "codepack_path", "sha256", "bytes", "copied_sha256", "copied_bytes"], delimiter="\t")
        w.writeheader()
        w.writerows(rows)


def main():
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    CODEPACK_ROOT.mkdir(parents=True, exist_ok=True)

    digests = []
    for rel in IN_SCOPE:
        h, sz = sha256_and_size(SOURCE_ROOT / rel)
        digests.append((rel, h, sz))

    call_rows = build_callsites()
    base_rows = build_base_matrix()
    harana_rows = build_harana_matrix()
    bharana_rows = build_bharana_matrix()
    class_rows = build_classification_matrix()
    out_rows = build_output_matrix()

    write_tsv(OUT_ROOT / "_coverage_longevity_callsites_engine_plus_consumers.tsv", CALLSITE_COLUMNS, call_rows)
    write_tsv(OUT_ROOT / "_coverage_longevity_base_ayur_formula_matrix.tsv", BASE_COLUMNS, base_rows)
    write_tsv(OUT_ROOT / "_coverage_longevity_harana_reduction_matrix.tsv", HARANA_COLUMNS, harana_rows)
    write_tsv(OUT_ROOT / "_coverage_longevity_bharana_increase_matrix.tsv", BHARANA_COLUMNS, bharana_rows)
    write_tsv(OUT_ROOT / "_coverage_longevity_classification_matrix.tsv", CLASS_COLUMNS, class_rows)
    write_tsv(OUT_ROOT / "_coverage_longevity_output_contract_matrix.tsv", OUTIDX_COLUMNS, out_rows)

    anchors = anchor_specs()
    build_map_md(digests, call_rows, anchors)
    copy_codepack_and_manifest(digests)

    report = []
    report.append("# longevity_and_ayurdaya")
    report.append("")
    report.append("## artifacts")
    report.append("- `longevity_behavior_contract_map.engine_plus_consumers.md`")
    report.append("- `_coverage_longevity_callsites_engine_plus_consumers.tsv`")
    report.append("- `_coverage_longevity_base_ayur_formula_matrix.tsv`")
    report.append("- `_coverage_longevity_harana_reduction_matrix.tsv`")
    report.append("- `_coverage_longevity_bharana_increase_matrix.tsv`")
    report.append("- `_coverage_longevity_classification_matrix.tsv`")
    report.append("- `_coverage_longevity_output_contract_matrix.tsv`")
    report.append("- `_codepack/MANIFEST.tsv`")
    report.append("")
    report.append("## notes")
    report.append(f"- in-scope files: {len(IN_SCOPE)}")
    report.append(f"- callsite rows: {len(call_rows)}")
    report.append("- dead-branch capture: enabled via implementation_status")
    report.append("- combine_operator capture: explicit in harana matrix")
    report.append("- canonical path: research/longevity_and_ayurdaya")
    (OUT_ROOT / "report.md").write_text("\n".join(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
