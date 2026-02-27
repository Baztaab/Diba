from __future__ import annotations

import csv
import datetime as dt
import hashlib
import re
import shutil
from pathlib import Path

SOURCE_ROOT = Path(r"D:/lab/Pyjhora")
REPO_ROOT = Path(r"d:/Diba")
OUT_ROOT = REPO_ROOT / "research" / "ashtakavarga_system"
CODEPACK_ROOT = OUT_ROOT / "_codepack"

ENGINE_FILES = [
    "src/jhora/horoscope/chart/ashtakavarga.py",
    "src/jhora/const.py",
    "src/jhora/utils.py",
]
CONSUMER_FILES = [
    "src/jhora/horoscope/main.py",
    "src/jhora/horoscope/chart/charts.py",
    "src/jhora/horoscope/chart/house.py",
    "src/jhora/horoscope/chart/strength.py",
    "src/jhora/horoscope/prediction/__init__.py",
    "src/jhora/horoscope/prediction/general.py",
    "src/jhora/horoscope/prediction/longevity.py",
    "src/jhora/horoscope/transit/__init__.py",
    "src/jhora/horoscope/transit/saham.py",
    "src/jhora/horoscope/transit/tajaka.py",
    "src/jhora/horoscope/transit/tajaka_yoga.py",
    "src/jhora/horoscope/dhasa/__init__.py",
    "src/jhora/horoscope/dhasa/sudharsana_chakra.py",
    "src/jhora/horoscope/dhasa/annual/mudda.py",
    "src/jhora/horoscope/dhasa/annual/patyayini.py",
    "src/jhora/horoscope/dhasa/graha/aayu.py",
    "src/jhora/horoscope/dhasa/graha/applicability.py",
    "src/jhora/horoscope/dhasa/graha/ashtottari.py",
    "src/jhora/horoscope/dhasa/graha/buddhi_gathi.py",
    "src/jhora/horoscope/dhasa/graha/chathuraaseethi_sama.py",
    "src/jhora/horoscope/dhasa/graha/dwadasottari.py",
    "src/jhora/horoscope/dhasa/graha/dwisatpathi.py",
    "src/jhora/horoscope/dhasa/graha/kaala.py",
    "src/jhora/horoscope/dhasa/graha/karaka.py",
    "src/jhora/horoscope/dhasa/graha/karana_chathuraaseethi_sama.py",
    "src/jhora/horoscope/dhasa/graha/naisargika.py",
    "src/jhora/horoscope/dhasa/graha/panchottari.py",
    "src/jhora/horoscope/dhasa/graha/saptharishi_nakshathra.py",
    "src/jhora/horoscope/dhasa/graha/sataatbika.py",
    "src/jhora/horoscope/dhasa/graha/shastihayani.py",
    "src/jhora/horoscope/dhasa/graha/shattrimsa_sama.py",
    "src/jhora/horoscope/dhasa/graha/shodasottari.py",
    "src/jhora/horoscope/dhasa/graha/tara.py",
    "src/jhora/horoscope/dhasa/graha/tithi_ashtottari.py",
    "src/jhora/horoscope/dhasa/graha/tithi_yogini.py",
    "src/jhora/horoscope/dhasa/graha/vimsottari.py",
    "src/jhora/horoscope/dhasa/graha/yoga_vimsottari.py",
    "src/jhora/horoscope/dhasa/graha/yogini.py",
    "src/jhora/horoscope/dhasa/raasi/brahma.py",
    "src/jhora/horoscope/dhasa/raasi/chakra.py",
    "src/jhora/horoscope/dhasa/raasi/chara.py",
    "src/jhora/horoscope/dhasa/raasi/drig.py",
    "src/jhora/horoscope/dhasa/raasi/kalachakra.py",
    "src/jhora/horoscope/dhasa/raasi/kendradhi_rasi.py",
    "src/jhora/horoscope/dhasa/raasi/lagnamsaka.py",
    "src/jhora/horoscope/dhasa/raasi/mandooka.py",
    "src/jhora/horoscope/dhasa/raasi/moola.py",
    "src/jhora/horoscope/dhasa/raasi/narayana.py",
    "src/jhora/horoscope/dhasa/raasi/navamsa.py",
    "src/jhora/horoscope/dhasa/raasi/nirayana.py",
    "src/jhora/horoscope/dhasa/raasi/padhanadhamsa.py",
    "src/jhora/horoscope/dhasa/raasi/paryaaya.py",
    "src/jhora/horoscope/dhasa/raasi/sandhya.py",
    "src/jhora/horoscope/dhasa/raasi/shoola.py",
    "src/jhora/horoscope/dhasa/raasi/sthira.py",
    "src/jhora/horoscope/dhasa/raasi/sudasa.py",
    "src/jhora/horoscope/dhasa/raasi/tara_lagna.py",
    "src/jhora/horoscope/dhasa/raasi/trikona.py",
    "src/jhora/horoscope/dhasa/raasi/varnada.py",
    "src/jhora/horoscope/dhasa/raasi/yogardha.py",
]
IN_SCOPE = ENGINE_FILES + CONSUMER_FILES
ENGINE_SET = set(ENGINE_FILES)
CONSUMER_SET = set(CONSUMER_FILES)

PATTERNS = [
    "ashtakavarga", "ashtaka_varga", "get_ashtaka_varga",
    "bhinna", "binna", "sav", "samudhaya", "sarvashtakavarga", "pav", "prastara", "prasthara",
    "trikona_sodhana", "trikona_shodhana", "ekadhipatya_sodhana", "ekadhipatya_shodhana",
    "sodhaya_pindas", "sodhya_pindas", "shodhya_pinda",
    "ashtaka_varga_dict", "ashtakavarga_rasi_owners", "ashtakavarga_rasimana_multipliers", "ashtakavarga_grahamana_multipliers",
    "[:]", "min(", "sum(",
]

CALLSITE_COLUMNS = ["file", "line", "pattern", "function_context", "anchor_id", "scope_class"]
BAV_COLUMNS = [
    "file", "function", "source_planet", "contributor", "target_mode", "offset_rule", "target_house", "point_delta", "output_tensor_slot", "evidence_lines", "anchor_id"
]
SHODHANA_COLUMNS = [
    "file", "function", "sequence_index", "rule_group", "condition", "operation", "operand_source", "branch_outcome", "in_place_mutation", "implementation_status", "evidence_lines", "anchor_id"
]
PINDA_COLUMNS = [
    "file", "function", "weight_type", "weight_vector", "input_vector", "formula_signature", "normalization_unit", "output_slot", "evidence_lines", "anchor_id"
]
OUTIDX_COLUMNS = ["producer_function", "producer_shape", "consumer_function", "consumer_index_use", "match_status", "evidence_lines", "anchor_id"]
DEP_COLUMNS = ["file", "function", "depends_on_module", "depends_on_symbol", "coupling_type", "impact_area", "notes", "evidence_lines", "anchor_id"]


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
        if "/ui/" in rel or "/tests/" in rel or "/docs/" in rel or "/data/" in rel or "/lang/" in rel:
            continue
        if rel.endswith("/drik1.py"):
            continue
        rels.append(rel)
    return sorted(set(rels) | set(IN_SCOPE))


def find_matches(lines: list[str], pattern: str):
    if pattern in ("sav", "bav", "pav"):
        rgx = re.compile(rf"(?<![A-Za-z0-9_]){pattern}(?![A-Za-z0-9_])", re.IGNORECASE)
    elif pattern == "[:]":
        rgx = re.compile(r"\[:\]")
    elif pattern == "min(":
        rgx = re.compile(r"min\s*\(")
    elif pattern == "sum(":
        rgx = re.compile(r"sum\s*\(")
    else:
        rgx = re.compile(re.escape(pattern), re.IGNORECASE)
    for i, ln in enumerate(lines, 1):
        if rgx.search(ln):
            yield i


def detect_non_ui_consumers() -> list[dict]:
    rows: list[dict] = []
    checks = [
        re.compile(r"from\s+jhora\.horoscope\.chart\s+import\s+ashtakavarga"),
        re.compile(r"import\s+ashtakavarga"),
        re.compile(r"get_ashtaka_varga\s*\("),
        re.compile(r"sodhaya_pindas\s*\("),
    ]
    for rel in collect_scan_files():
        if rel in ENGINE_SET:
            continue
        lines = read_lines(rel)
        ctx = function_context_map(lines)
        for i, ln in enumerate(lines, 1):
            if any(r.search(ln) for r in checks):
                rows.append({
                    "file": rel,
                    "line": str(i),
                    "pattern": "non_ui_ashtakavarga_consumer",
                    "function_context": ctx[i - 1],
                    "anchor_id": "AV900",
                    "scope_class": scope_class(rel),
                })
    return rows


def build_callsites() -> tuple[list[dict], list[dict]]:
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
                    "anchor_id": "AV900",
                    "scope_class": scope_class(rel),
                })
        if rel in set(IN_SCOPE) and hit == 0:
            rows.append({
                "file": rel,
                "line": "0",
                "pattern": "not_found_in_file",
                "function_context": "<module>",
                "anchor_id": "AV900",
                "scope_class": scope_class(rel),
            })
    non_ui = detect_non_ui_consumers()
    if not non_ui:
        rows.append({
            "file": "Scope-ConsumerAudit",
            "line": "0",
            "pattern": "non_ui_ashtakavarga_consumer",
            "function_context": "not_found_in_non_ui_scope",
            "anchor_id": "ABSENCE-OF-NONUI-CONSUMER",
            "scope_class": "consumer_core",
        })
    return rows, non_ui


def build_bav_matrix() -> list[dict]:
    return [
        {
            "file": "src/jhora/const.py",
            "function": "ashtaka_varga_dict",
            "source_planet": "0..7 (Sun..Lagna)",
            "contributor": "nested contributor offset lists",
            "target_mode": "BAV+PAV seed table",
            "offset_rule": "1-based relative offset from contributor house",
            "target_house": "computed in get_ashtaka_varga",
            "point_delta": "+1",
            "output_tensor_slot": "ashtaka_varga_dict[key][contributor][offset]",
            "evidence_lines": "src/jhora/const.py:L239-L248",
            "anchor_id": "AV01",
        },
        {
            "file": "src/jhora/horoscope/chart/ashtakavarga.py",
            "function": "get_ashtaka_varga",
            "source_planet": "p=int(key)",
            "contributor": "op=0..7 (7=lagna)",
            "target_mode": "BAV",
            "offset_rule": "r=(raasi-1+pr)%12",
            "target_house": "r",
            "point_delta": "raasi_ashtaka[p][r]+=1",
            "output_tensor_slot": "binna_ashtaka_varga[p][r]",
            "evidence_lines": "src/jhora/horoscope/chart/ashtakavarga.py:L42-L55",
            "anchor_id": "AV03",
        },
        {
            "file": "src/jhora/horoscope/chart/ashtakavarga.py",
            "function": "get_ashtaka_varga",
            "source_planet": "p=int(key)",
            "contributor": "op=0..7 plus accumulator axis",
            "target_mode": "PAV",
            "offset_rule": "same r as BAV",
            "target_house": "r",
            "point_delta": "set contributor slot and increment accumulator slot",
            "output_tensor_slot": "prastara_ashtaka_varga[p][op][r] & prastara_ashtaka_varga[p][-1][r]",
            "evidence_lines": "src/jhora/horoscope/chart/ashtakavarga.py:L41-L56",
            "anchor_id": "AV03",
        },
        {
            "file": "src/jhora/horoscope/chart/ashtakavarga.py",
            "function": "get_ashtaka_varga",
            "source_planet": "BAV rows 0..6",
            "contributor": "sum across Sun..Saturn rows",
            "target_mode": "SAV",
            "offset_rule": "exclude lagna via bav[:-1]",
            "target_house": "0..11",
            "point_delta": "sum(axis=0)",
            "output_tensor_slot": "samudhaya_ashtaka_varga[h]",
            "evidence_lines": "src/jhora/horoscope/chart/ashtakavarga.py:L57-L58",
            "anchor_id": "AV04",
        },
    ]


def build_shodhana_matrix() -> list[dict]:
    return [
        {
            "file": "src/jhora/horoscope/chart/ashtakavarga.py",
            "function": "_trikona_sodhana",
            "sequence_index": "1",
            "rule_group": "trikona_rule_1",
            "condition": "any member of triad has zero",
            "operation": "skip",
            "operand_source": "bav[p][r+HOUSE_1|5|9]",
            "branch_outcome": "no reduction",
            "in_place_mutation": "yes",
            "implementation_status": "Active",
            "evidence_lines": "src/jhora/horoscope/chart/ashtakavarga.py:L63-L65",
            "anchor_id": "AV05",
        },
        {
            "file": "src/jhora/horoscope/chart/ashtakavarga.py",
            "function": "_trikona_sodhana",
            "sequence_index": "2",
            "rule_group": "trikona_rule_2",
            "condition": "triad values equal and non-zero",
            "operation": "zero-out",
            "operand_source": "bav[p][r+HOUSE_1|5|9]",
            "branch_outcome": "all three become 0",
            "in_place_mutation": "yes",
            "implementation_status": "Active",
            "evidence_lines": "src/jhora/horoscope/chart/ashtakavarga.py:L66-L70",
            "anchor_id": "AV05",
        },
        {
            "file": "src/jhora/horoscope/chart/ashtakavarga.py",
            "function": "_trikona_sodhana",
            "sequence_index": "3",
            "rule_group": "trikona_rule_3",
            "condition": "non-zero and not all equal",
            "operation": "min-subtract",
            "operand_source": "min(triad)",
            "branch_outcome": "subtract min from all three",
            "in_place_mutation": "yes",
            "implementation_status": "Active",
            "evidence_lines": "src/jhora/horoscope/chart/ashtakavarga.py:L72-L77",
            "anchor_id": "AV05",
        },
        {
            "file": "src/jhora/horoscope/chart/ashtakavarga.py",
            "function": "_ekadhipatya_sodhana",
            "sequence_index": "4",
            "rule_group": "ekadhipatya_rule_1_2",
            "condition": "either value zero OR both signs occupied",
            "operation": "skip",
            "operand_source": "bav[p][r1], bav[p][r2], occupancy flags",
            "branch_outcome": "no reduction",
            "in_place_mutation": "yes",
            "implementation_status": "Active",
            "evidence_lines": "src/jhora/horoscope/chart/ashtakavarga.py:L87-L89",
            "anchor_id": "AV06",
        },
        {
            "file": "src/jhora/horoscope/chart/ashtakavarga.py",
            "function": "_ekadhipatya_sodhana",
            "sequence_index": "5",
            "rule_group": "ekadhipatya_rule_4",
            "condition": "both signs empty",
            "operation": "equalize-min OR zero-out",
            "operand_source": "bav[p][r1], bav[p][r2]",
            "branch_outcome": "different->set both to min; equal->set both 0",
            "in_place_mutation": "yes",
            "implementation_status": "Active",
            "evidence_lines": "src/jhora/horoscope/chart/ashtakavarga.py:L90-L99",
            "anchor_id": "AV06",
        },
        {
            "file": "src/jhora/horoscope/chart/ashtakavarga.py",
            "function": "_ekadhipatya_sodhana",
            "sequence_index": "6",
            "rule_group": "ekadhipatya_rule_3",
            "condition": "one occupied, one empty",
            "operation": "zero-out OR copy",
            "operand_source": "occupied/empty pair comparison",
            "branch_outcome": "lower empty->0; higher empty->occupied value",
            "in_place_mutation": "yes",
            "implementation_status": "Active",
            "evidence_lines": "src/jhora/horoscope/chart/ashtakavarga.py:L100-L115",
            "anchor_id": "AV06",
        },
    ]


def build_pinda_matrix() -> list[dict]:
    return [
        {
            "file": "src/jhora/horoscope/chart/ashtakavarga.py",
            "function": "_sodhya_pindas",
            "weight_type": "rasimana",
            "weight_vector": "const.ashtakavarga_rasimana_multipliers",
            "input_vector": "bav[p][0..11]",
            "formula_signature": "sum(np.multiply(bav[p], rasimana_multipliers))",
            "normalization_unit": "none",
            "output_slot": "raasi_pindas[p]",
            "evidence_lines": "src/jhora/horoscope/chart/ashtakavarga.py:L126-L134",
            "anchor_id": "AV07",
        },
        {
            "file": "src/jhora/horoscope/chart/ashtakavarga.py",
            "function": "_sodhya_pindas",
            "weight_type": "grahamana",
            "weight_vector": "const.ashtakavarga_grahamana_multipliers",
            "input_vector": "bav[p][planet_houses[i]]",
            "formula_signature": "sum(grahamana[i]*bav[p][pr] for i,pr in enumerate(planet_houses))",
            "normalization_unit": "none",
            "output_slot": "graha_pindas[p]",
            "evidence_lines": "src/jhora/horoscope/chart/ashtakavarga.py:L135-L138",
            "anchor_id": "AV07",
        },
        {
            "file": "src/jhora/horoscope/chart/ashtakavarga.py",
            "function": "_sodhya_pindas",
            "weight_type": "sodhya_total",
            "weight_vector": "raasi_pinda + graha_pinda",
            "input_vector": "raasi_pindas[p], graha_pindas[p]",
            "formula_signature": "sodhya_pindas[p]=raasi_pindas[p]+graha_pindas[p]",
            "normalization_unit": "none",
            "output_slot": "sodhya_pindas[p]",
            "evidence_lines": "src/jhora/horoscope/chart/ashtakavarga.py:L138-L139",
            "anchor_id": "AV07",
        },
    ]


def build_output_matrix(non_ui_consumers: list[dict]) -> list[dict]:
    if non_ui_consumers:
        sample = non_ui_consumers[0]
        cref = f"{sample['file']}:{sample['line']}"
        return [
            {
                "producer_function": "ashtakavarga.get_ashtaka_varga",
                "producer_shape": "(bav[8][12], sav[12], pav[8][9][12])",
                "consumer_function": cref,
                "consumer_index_use": "detected non-ui callsite",
                "match_status": "presence",
                "evidence_lines": cref,
                "anchor_id": "AV08",
            }
        ]
    return [
        {
            "producer_function": "ashtakavarga.get_ashtaka_varga",
            "producer_shape": "(bav[8][12], sav[12], pav[8][9][12])",
            "consumer_function": "ABSENCE-OF-NONUI-CONSUMER",
            "consumer_index_use": "not_found_in_non_ui_scope",
            "match_status": "absence_fact",
            "evidence_lines": "research/ashtakavarga_system/_coverage_ashtakavarga_callsites_engine_plus_consumers.tsv:L2",
            "anchor_id": "ABSENCE-OF-NONUI-CONSUMER",
        },
        {
            "producer_function": "ashtakavarga.sodhaya_pindas",
            "producer_shape": "(raasi_pindas[7], graha_pindas[7], sodhya_pindas[7])",
            "consumer_function": "ABSENCE-OF-NONUI-CONSUMER",
            "consumer_index_use": "not_found_in_non_ui_scope",
            "match_status": "absence_fact",
            "evidence_lines": "research/ashtakavarga_system/_coverage_ashtakavarga_callsites_engine_plus_consumers.tsv:L2",
            "anchor_id": "ABSENCE-OF-NONUI-CONSUMER",
        },
    ]


def build_dependency_matrix(non_ui_consumers: list[dict]) -> list[dict]:
    rows = [
        {
            "file": "src/jhora/horoscope/chart/ashtakavarga.py",
            "function": "get_ashtaka_varga",
            "depends_on_module": "jhora.utils",
            "depends_on_symbol": "get_planet_to_house_dict_from_chart",
            "coupling_type": "chart_mapping",
            "impact_area": "base contributor placement",
            "notes": "maps contributor planets to houses for offset shifts",
            "evidence_lines": "src/jhora/horoscope/chart/ashtakavarga.py:L38-L39",
            "anchor_id": "AV08",
        },
        {
            "file": "src/jhora/horoscope/chart/ashtakavarga.py",
            "function": "get_ashtaka_varga",
            "depends_on_module": "jhora.const",
            "depends_on_symbol": "ashtaka_varga_dict",
            "coupling_type": "lookup_table",
            "impact_area": "BAV/PAV seeding",
            "notes": "rule table drives contributor offsets",
            "evidence_lines": "src/jhora/horoscope/chart/ashtakavarga.py:L42-L46",
            "anchor_id": "AV01",
        },
        {
            "file": "src/jhora/horoscope/chart/ashtakavarga.py",
            "function": "_ekadhipatya_sodhana",
            "depends_on_module": "jhora.const",
            "depends_on_symbol": "ashtakavarga_rasi_owners",
            "coupling_type": "ownership_rule_table",
            "impact_area": "ekadhipatya routing",
            "notes": "owner-pair mapping selects r1/r2 comparisons",
            "evidence_lines": "src/jhora/horoscope/chart/ashtakavarga.py:L82-L84",
            "anchor_id": "AV06",
        },
        {
            "file": "src/jhora/horoscope/chart/ashtakavarga.py",
            "function": "_sodhya_pindas",
            "depends_on_module": "jhora.const",
            "depends_on_symbol": "ashtakavarga_rasimana_multipliers|ashtakavarga_grahamana_multipliers",
            "coupling_type": "weight_vector",
            "impact_area": "sodhya pinda outputs",
            "notes": "both vectors directly scale BAV values",
            "evidence_lines": "src/jhora/horoscope/chart/ashtakavarga.py:L126-L127",
            "anchor_id": "AV02",
        },
        {
            "file": "src/jhora/horoscope/chart/ashtakavarga.py",
            "function": "_trikona_sodhana|_ekadhipatya_sodhana|_sodhya_pindas",
            "depends_on_module": "python_list_copy",
            "depends_on_symbol": "[:]",
            "coupling_type": "mutation_risk",
            "impact_area": "in-place reductions on nested arrays",
            "notes": "shallow copy on 2D list can leak mutation",
            "evidence_lines": "src/jhora/horoscope/chart/ashtakavarga.py:L60-L60",
            "anchor_id": "AV09",
        },
    ]
    if not non_ui_consumers:
        rows.append({
            "file": "Scope-ConsumerAudit",
            "function": "non_ui_consumer_scan",
            "depends_on_module": "consumer_audit_scope",
            "depends_on_symbol": "main/prediction/dhasa/transit/chart(charts,house,strength)",
            "coupling_type": "absence",
            "impact_area": "output contract consumers",
            "notes": "no direct non-ui invocation detected",
            "evidence_lines": "research/ashtakavarga_system/_coverage_ashtakavarga_callsites_engine_plus_consumers.tsv:L2",
            "anchor_id": "ABSENCE-OF-NONUI-CONSUMER",
        })
    return rows

def anchor_specs(non_ui_consumers: list[dict]) -> list[dict]:
    anchors = [
        {"id": "AV01", "behavior": "BAV/PAV seed lookup table is defined as a constant dictionary.", "src": "src/jhora/const.py", "start": 239, "end": 248, "obs": "Ashtakavarga core contributor-offset rules are hardcoded."},
        {"id": "AV02", "behavior": "Ekadhipatya owners and pinda multipliers are constant vectors.", "src": "src/jhora/const.py", "start": 1209, "end": 1211, "obs": "Ownership and weight vectors are centralized in const."},
        {"id": "AV03", "behavior": "get_ashtaka_varga computes BAV and PAV from contributor offsets.", "src": "src/jhora/horoscope/chart/ashtakavarga.py", "start": 27, "end": 56, "obs": "Offset-shifted contributor points populate BAV/PAV tensors."},
        {"id": "AV04", "behavior": "SAV is computed as axis-sum of BAV excluding Lagna row.", "src": "src/jhora/horoscope/chart/ashtakavarga.py", "start": 57, "end": 58, "obs": "samudhaya_ashtaka_varga = sum(bav[:-1], axis=0)."},
        {"id": "AV05", "behavior": "Trikona shodhana is implemented with explicit three-branch rule set.", "src": "src/jhora/horoscope/chart/ashtakavarga.py", "start": 59, "end": 79, "obs": "skip, zero-out, and min-subtract branches are explicit."},
        {"id": "AV06", "behavior": "Ekadhipatya shodhana is implemented as explicit occupancy/value branches.", "src": "src/jhora/horoscope/chart/ashtakavarga.py", "start": 80, "end": 116, "obs": "Rules for occupied/empty/equal cases are directly coded."},
        {"id": "AV07", "behavior": "Sodhya pinda uses rasimana + grahamana weighted sums.", "src": "src/jhora/horoscope/chart/ashtakavarga.py", "start": 125, "end": 139, "obs": "raasi_pindas, graha_pindas, sodhya_pindas are computed sequentially."},
        {"id": "AV08", "behavior": "Engine depends directly on utils chart-mapping helper.", "src": "src/jhora/horoscope/chart/ashtakavarga.py", "start": 38, "end": 39, "obs": "Contributor alignment relies on planet-to-house mapping."},
        {"id": "AV09", "behavior": "Shallow-copy pattern is used before mutating nested BAV arrays.", "src": "src/jhora/horoscope/chart/ashtakavarga.py", "start": 59, "end": 82, "obs": "Use of [:] with 2D structures introduces mutation-risk ambiguity."},
    ]
    if not non_ui_consumers:
        anchors.append({"id": "ABSENCE-OF-NONUI-CONSUMER", "behavior": "No direct non-UI consumer callsite was found for ashtakavarga producers.", "src": "research/ashtakavarga_system/_coverage_ashtakavarga_callsites_engine_plus_consumers.tsv", "start": 2, "end": 2, "obs": "Consumer audit scope has an explicit negative fact row."})
    anchors.append({"id": "AV900", "behavior": "Residual matched rows are retained in callsite inventory.", "src": "research/ashtakavarga_system/_coverage_ashtakavarga_callsites_engine_plus_consumers.tsv", "start": 1, "end": 1, "obs": "Non-focused matches remain visible as residual evidence."})
    return anchors


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
    out.append("# ashtakavarga_behavior_contract_map.engine_plus_consumers.md")
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
    out.append("  - docs/data/lang folders")
    out.append("  - deep redesign decisions")
    out.append("")
    out.append("## Pattern inventory (FACTS)")
    out.append("")
    for p in PATTERNS:
        out.append(f"- `{p}`")
    out.append("")
    out.append("## Behavior taxonomy (FACTS)")
    out.append("")
    out.append("- seed tables and constants: `AV01`, `AV02`")
    out.append("- BAV/SAV/PAV production: `AV03`, `AV04`")
    out.append("- Shodhana algorithms: `AV05`, `AV06`")
    out.append("- Sodhya pinda weighting: `AV07`")
    out.append("- dependency and mutation touchpoints: `AV08`, `AV09`")
    if any(a["id"] == "ABSENCE-OF-NONUI-CONSUMER" for a in anchors):
        out.append("- consumer audit negative fact: `ABSENCE-OF-NONUI-CONSUMER`")
    out.append("- residual inventory: `AV900`")
    out.append("")
    out.append("## Evidence anchors (AV01..AVNN, AV900)")
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
            out.append(f"- Source: `{a['src']}:L{a['start']}`")
            out.append("- Excerpt:")
            out.append("```text")
            if a["id"] == "ABSENCE-OF-NONUI-CONSUMER":
                out.append("Scope-ConsumerAudit\t0\tnon_ui_ashtakavarga_consumer\tnot_found_in_non_ui_scope\tABSENCE-OF-NONUI-CONSUMER\tconsumer_core")
            else:
                out.append("Rows with anchor_id=AV900 remain in inventory as residual evidence.")
            out.append("```")
        out.append(f"- Observed behavior: {a['obs']}")
        out.append("")
    out.append("## Conflict / ambiguity register")
    out.append("")
    out.append("- UNCERTAIN-AV-NAMING-01: naming variants exist (`sodhana/shodhana`, `sodhaya/sodhya`).")
    out.append("- UNCERTAIN-AV-SHAPE-01: PAV documented shape vs runtime slicing may diverge by axis semantics.")
    out.append("- UNCERTAIN-AV-MUTATION-01: shallow copies (`[:]`) are used with nested arrays before mutation.")
    out.append("- UNCERTAIN-AV-CONSUMER-01: non-UI direct consumer may be absent in audited scope.")
    out.append("- UNCERTAIN-AV-SAV-EXCLUSION-01: SAV explicitly excludes Lagna row (`bav[:-1]`).")
    out.append("")
    out.append("## Coverage ledger")
    out.append("")
    out.append("- Inventory file: `research/ashtakavarga_system/_coverage_ashtakavarga_callsites_engine_plus_consumers.tsv`")
    out.append("- Inventory columns: `file`, `line`, `pattern`, `function_context`, `anchor_id`, `scope_class`")
    out.append(f"- Inventory row count: `{len(call_rows)}`")
    ufs = len({(r['file'], r['function_context']) for r in call_rows})
    out.append(f"- Unique `(file,function_context)` count: `{ufs}`")
    ec = sum(1 for r in call_rows if r["scope_class"] == "engine_core")
    cc = sum(1 for r in call_rows if r["scope_class"] == "consumer_core")
    rc = sum(1 for r in call_rows if r["scope_class"] == "residual")
    out.append(f"- Rows by scope_class: `engine_core={ec}`, `consumer_core={cc}`, `residual={rc}`")
    av900 = sum(1 for r in call_rows if r["anchor_id"] == "AV900")
    out.append(f"- Residual rows (`AV900`): `{av900}`")
    abs_rows = sum(1 for r in call_rows if r["anchor_id"] == "ABSENCE-OF-NONUI-CONSUMER")
    out.append(f"- Absence rows (`ABSENCE-OF-NONUI-CONSUMER`): `{abs_rows}`")
    out.append("- BAV seed matrix: `research/ashtakavarga_system/_coverage_ashtakavarga_bav_seed_rule_matrix.tsv`")
    out.append("- Shodhana matrix: `research/ashtakavarga_system/_coverage_ashtakavarga_shodhana_reduction_rules_matrix.tsv`")
    out.append("- Pinda matrix: `research/ashtakavarga_system/_coverage_ashtakavarga_pinda_weight_matrix.tsv`")
    out.append("- Output-contract matrix: `research/ashtakavarga_system/_coverage_ashtakavarga_output_contract_matrix.tsv`")
    out.append("- Dependency matrix: `research/ashtakavarga_system/_coverage_ashtakavarga_dependency_touchpoints_matrix.tsv`")
    out.append("")
    out.append("## Sanity checks")
    out.append("")
    out.append("- command: `rg -n \"^### AV[0-9]+|^### AV900|^### ABSENCE-OF-NONUI-CONSUMER\" research/ashtakavarga_system/ashtakavarga_behavior_contract_map.engine_plus_consumers.md -S`")
    out.append("- command: `rg -n \"UNCERTAIN-AV-\" research/ashtakavarga_system/ashtakavarga_behavior_contract_map.engine_plus_consumers.md -S`")
    out.append("- command: `rg -n \"Source:\" research/ashtakavarga_system/ashtakavarga_behavior_contract_map.engine_plus_consumers.md -S`")
    out.append("- command: `Get-Content research/ashtakavarga_system/_coverage_ashtakavarga_callsites_engine_plus_consumers.tsv | Measure-Object -Line`")
    out.append("- command: `Get-Content research/ashtakavarga_system/_coverage_ashtakavarga_bav_seed_rule_matrix.tsv | Measure-Object -Line`")
    out.append("- command: `Get-Content research/ashtakavarga_system/_coverage_ashtakavarga_shodhana_reduction_rules_matrix.tsv | Measure-Object -Line`")
    out.append("- command: `Get-Content research/ashtakavarga_system/_coverage_ashtakavarga_pinda_weight_matrix.tsv | Measure-Object -Line`")
    out.append("- command: `Get-Content research/ashtakavarga_system/_coverage_ashtakavarga_output_contract_matrix.tsv | Measure-Object -Line`")
    out.append("- command: `Get-Content research/ashtakavarga_system/_coverage_ashtakavarga_dependency_touchpoints_matrix.tsv | Measure-Object -Line`")
    (OUT_ROOT / "ashtakavarga_behavior_contract_map.engine_plus_consumers.md").write_text("\n".join(out) + "\n", encoding="utf-8")


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


def patch_index():
    idx = REPO_ROOT / "research" / "INDEX.md"
    if not idx.exists():
        return
    content = idx.read_text(encoding="utf-8", errors="replace")
    marker = "- `ashtakavarga_system` — ACTIVE"
    block = (
        "\n- `ashtakavarga_system` — ACTIVE\n"
        "  - `report`: `D:\\Diba\\research\\ashtakavarga_system\\report.md`\n"
    )
    if marker not in content:
        content = content.rstrip() + "\n" + block
        idx.write_text(content, encoding="utf-8")


def main():
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    CODEPACK_ROOT.mkdir(parents=True, exist_ok=True)

    digests = []
    for rel in IN_SCOPE:
        h, sz = sha256_and_size(SOURCE_ROOT / rel)
        digests.append((rel, h, sz))

    call_rows, non_ui_consumers = build_callsites()
    bav_rows = build_bav_matrix()
    shodhana_rows = build_shodhana_matrix()
    pinda_rows = build_pinda_matrix()
    out_rows = build_output_matrix(non_ui_consumers)
    dep_rows = build_dependency_matrix(non_ui_consumers)

    write_tsv(OUT_ROOT / "_coverage_ashtakavarga_callsites_engine_plus_consumers.tsv", CALLSITE_COLUMNS, call_rows)
    write_tsv(OUT_ROOT / "_coverage_ashtakavarga_bav_seed_rule_matrix.tsv", BAV_COLUMNS, bav_rows)
    write_tsv(OUT_ROOT / "_coverage_ashtakavarga_shodhana_reduction_rules_matrix.tsv", SHODHANA_COLUMNS, shodhana_rows)
    write_tsv(OUT_ROOT / "_coverage_ashtakavarga_pinda_weight_matrix.tsv", PINDA_COLUMNS, pinda_rows)
    write_tsv(OUT_ROOT / "_coverage_ashtakavarga_output_contract_matrix.tsv", OUTIDX_COLUMNS, out_rows)
    write_tsv(OUT_ROOT / "_coverage_ashtakavarga_dependency_touchpoints_matrix.tsv", DEP_COLUMNS, dep_rows)

    anchors = anchor_specs(non_ui_consumers)
    build_map_md(digests, call_rows, anchors)
    copy_codepack_and_manifest(digests)
    patch_index()

    report = []
    report.append("# ashtakavarga_system")
    report.append("")
    report.append("## artifacts")
    report.append("- `ashtakavarga_behavior_contract_map.engine_plus_consumers.md`")
    report.append("- `_coverage_ashtakavarga_callsites_engine_plus_consumers.tsv`")
    report.append("- `_coverage_ashtakavarga_bav_seed_rule_matrix.tsv`")
    report.append("- `_coverage_ashtakavarga_shodhana_reduction_rules_matrix.tsv`")
    report.append("- `_coverage_ashtakavarga_pinda_weight_matrix.tsv`")
    report.append("- `_coverage_ashtakavarga_output_contract_matrix.tsv`")
    report.append("- `_coverage_ashtakavarga_dependency_touchpoints_matrix.tsv`")
    report.append("- `_codepack/MANIFEST.tsv`")
    report.append("")
    report.append("## notes")
    report.append(f"- in-scope files: {len(IN_SCOPE)}")
    report.append(f"- callsite rows: {len(call_rows)}")
    report.append(f"- consumer-audit files: {len(CONSUMER_FILES)}")
    report.append(f"- non-ui consumer callsites found: {len(non_ui_consumers)}")
    report.append("- canonical path: research/ashtakavarga_system")
    (OUT_ROOT / "report.md").write_text("\n".join(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
