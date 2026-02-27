from __future__ import annotations

import csv
import datetime as dt
import hashlib
import os
import re
import shutil
from pathlib import Path

SOURCE_ROOT = Path(r"D:/lab/Pyjhora")
REPO_ROOT = Path(r"d:/Diba")
OUT_ROOT = REPO_ROOT / "research" / "graha_longitudes_and_states"
CODEPACK_ROOT = OUT_ROOT / "_codepack"

ENGINE_FILES = [
    "src/jhora/horoscope/chart/strength.py",
    "src/jhora/horoscope/chart/charts.py",
    "src/jhora/panchanga/drik.py",
    "src/jhora/utils.py",
    "src/jhora/const.py",
]
CONSUMER_FILES = [
    "src/jhora/horoscope/main.py",
    "src/jhora/horoscope/chart/house.py",
    "src/jhora/horoscope/chart/dosha.py",
    "src/jhora/horoscope/prediction/longevity.py",
    "src/jhora/horoscope/dhasa/graha/aayu.py",
    "src/jhora/horoscope/transit/tajaka.py",
    "src/jhora/horoscope/transit/tajaka_yoga.py",
    "src/jhora/horoscope/dhasa/sudharsana_chakra.py",
]
IN_SCOPE = ENGINE_FILES + CONSUMER_FILES
ENGINE_SET = set(ENGINE_FILES)
CONSUMER_SET = set(CONSUMER_FILES)

PATTERNS = [
    "shadbala", "shad_bala", "bhava_bala", "sthana_bala", "dik_bala", "kala_bala", "cheshta_bala", "naisargika_bala", "drik_bala",
    "vimsopaka", "vaiseshikamsa", "house_strengths_of_planets", "moola_trikona",
    "combust", "combustion", "planets_in_combustion",
    "retrograde", "planets_in_retrograde", "vakra",
    "exalt", "debilit", "is_planet_in_exalation", "is_planet_in_debilitation",
    "deeptaamsa", "ayanamsa",
    "avastha", "jagrad", "baladi", "bala", "kumar", "yuva", "vriddha", "mrita",
    "\\b30\\b",
]

SHADBALA_COLUMNS = [
    "file", "function", "component", "formula_signature", "constants_used", "input_dependencies",
    "normalization_unit", "output_slot", "evidence_lines", "anchor_id"
]
STATE_COLUMNS = [
    "file", "function", "state_type", "decision_rule", "threshold_source", "depends_on",
    "branches", "producer_consumer_path", "evidence_lines", "anchor_id"
]
OUTIDX_COLUMNS = [
    "producer_function", "producer_shape", "consumer_function", "consumer_index_use", "match_status", "evidence_lines", "anchor_id"
]
CALLSITE_COLUMNS = ["file", "line", "pattern", "function_context", "anchor_id", "scope_class"]


def norm_rel(p: Path) -> str:
    return str(p.as_posix())


def read_lines(rel: str) -> list[str]:
    return (SOURCE_ROOT / rel).read_text(encoding="utf-8", errors="replace").splitlines()


def sha256_and_size(abs_path: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    with abs_path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest(), abs_path.stat().st_size


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
    block = lines[s - 1:e][:12]
    return "\n".join(block)

def collect_scan_files() -> list[str]:
    root = SOURCE_ROOT / "src" / "jhora"
    rels = []
    for p in root.rglob("*.py"):
        rel = norm_rel(p.relative_to(SOURCE_ROOT))
        if "/ui/" in rel or "/tests/" in rel or rel.endswith("/drik1.py"):
            continue
        rels.append(rel)
    return sorted(set(rels) | set(IN_SCOPE))


def find_matches(lines: list[str], pattern: str, flags=re.IGNORECASE):
    if pattern == r"\b30\b":
        rgx = re.compile(r"\b30\b")
    else:
        rgx = re.compile(re.escape(pattern), flags)
    for i, ln in enumerate(lines, 1):
        if rgx.search(ln):
            yield i


def build_callsites() -> tuple[list[dict], bool]:
    rows: list[dict] = []
    scan_files = collect_scan_files()
    avastha_direct_found = False
    for rel in scan_files:
        lines = read_lines(rel)
        ctx = function_context_map(lines)
        matched_here = 0
        for pat in PATTERNS:
            for line_no in find_matches(lines, pat):
                matched_here += 1
                if pat in {"avastha", "jagrad", "baladi"} and rel in set(IN_SCOPE):
                    avastha_direct_found = True
                rows.append({
                    "file": rel,
                    "line": str(line_no),
                    "pattern": pat,
                    "function_context": ctx[line_no - 1],
                    "anchor_id": "GS900",
                    "scope_class": scope_class(rel),
                })
        if rel in set(IN_SCOPE) and matched_here == 0:
            rows.append({
                "file": rel,
                "line": "0",
                "pattern": "not_found_in_file",
                "function_context": "<module>",
                "anchor_id": "GS900",
                "scope_class": scope_class(rel),
            })
    if not avastha_direct_found:
        rows.append({
            "file": f"InScope-{len(IN_SCOPE)}",
            "line": "0",
            "pattern": "avastha",
            "function_context": "not_found_in_scope",
            "anchor_id": "ABSENCE-OF-AVASTHA",
            "scope_class": "engine_core",
        })
    return rows, avastha_direct_found


def build_shadbala_matrix() -> list[dict]:
    return [
        {"file":"src/jhora/horoscope/chart/strength.py","function":"_sthana_bala","component":"sthana_bala","formula_signature":"sum(uchcha,sapthavargaja,ojayugama,kendra,dreshkona)","constants_used":"sapthavargaja_factors,house_strengths_of_planets,moola_trikona_of_planets","input_dependencies":"divisional_chart(1,2,3,7,9,12,30)","normalization_unit":"shastiamsa","output_slot":"shad_bala[0]","evidence_lines":"src/jhora/horoscope/chart/strength.py:L214-L233","anchor_id":"GS06"},
        {"file":"src/jhora/horoscope/chart/strength.py","function":"_dig_bala","component":"dik_bala","formula_signature":"directional strength from kendras/opposites","constants_used":"_EXALTED_UCCHAM,_FRIEND","input_dependencies":"rasi_chart,planet_positions","normalization_unit":"shastiamsa","output_slot":"shad_bala[2]","evidence_lines":"src/jhora/horoscope/chart/strength.py:L419-L444","anchor_id":"GS07"},
        {"file":"src/jhora/horoscope/chart/strength.py","function":"_kaala_bala","component":"kala_bala","formula_signature":"sum(nathonnatha,paksha,tribhaga,abda,masa,vaara,hora,ayana,yuddha)","constants_used":"planet_disc_diameters","input_dependencies":"jd,place,tithi,weekday,hora","normalization_unit":"shastiamsa","output_slot":"shad_bala[1]","evidence_lines":"src/jhora/horoscope/chart/strength.py:L643-L670","anchor_id":"GS08"},
        {"file":"src/jhora/horoscope/chart/strength.py","function":"_cheshta_bala_new","component":"cheshta_bala","formula_signature":"motional strength from orbital speed/state","constants_used":"none","input_dependencies":"planet_mean_true_motion","normalization_unit":"shastiamsa","output_slot":"shad_bala[3]","evidence_lines":"src/jhora/horoscope/chart/strength.py:L1028-L1066","anchor_id":"GS09"},
        {"file":"src/jhora/horoscope/chart/strength.py","function":"_naisargika_bala","component":"naisargika_bala","formula_signature":"constant lookup slice","constants_used":"const.naisargika_bala","input_dependencies":"none","normalization_unit":"shastiamsa","output_slot":"shad_bala[4]","evidence_lines":"src/jhora/horoscope/chart/strength.py:L718-L719","anchor_id":"GS10"},
        {"file":"src/jhora/horoscope/chart/strength.py","function":"_drik_bala","component":"drik_bala","formula_signature":"benefic minus malefic aspect aggregation","constants_used":"benefics_and_malefics,aspect ratios","input_dependencies":"planetary aspects matrix","normalization_unit":"shastiamsa","output_slot":"shad_bala[5]","evidence_lines":"src/jhora/horoscope/chart/strength.py:L803-L829","anchor_id":"GS11"},
        {"file":"src/jhora/horoscope/chart/strength.py","function":"shad_bala","component":"shad_bala_total","formula_signature":"stack(6 components)->sum->rupa->strength_ratio","constants_used":"shad_bala_factors","input_dependencies":"_sthana,_kaala,_dig,_cheshta,_naisargika,_drik","normalization_unit":"rupa(=/60)","output_slot":"[6],[7],[8]","evidence_lines":"src/jhora/horoscope/chart/strength.py:L830-L854","anchor_id":"GS12"},
        {"file":"src/jhora/horoscope/chart/strength.py","function":"bhava_bala","component":"bhava_bala","formula_signature":"sum(bhava_adhipati,bhava_dig,bhava_drik)","constants_used":"minimum_bhava_bala_rupa","input_dependencies":"shad_bala_sum,bhava_midpoints,aspects","normalization_unit":"rupa(=/60)","output_slot":"[0],[1],[2]","evidence_lines":"src/jhora/horoscope/chart/strength.py:L956-L968","anchor_id":"GS13"},
    ]


def build_state_matrix(avastha_absent: bool) -> list[dict]:
    rows = [
        {"file":"src/jhora/horoscope/chart/charts.py","function":"planets_in_retrograde","state_type":"retrograde","decision_rule":"planet_long within sun-relative retrograde window","threshold_source":"const.planets_retrograde_limits_from_sun","depends_on":"sun_longitude,planet_longitude","branches":"method=old vs method=sun-window","producer_consumer_path":"charts.planets_in_retrograde -> dosha/aayu/tajaka_yoga","evidence_lines":"src/jhora/horoscope/chart/charts.py:L1160-L1179","anchor_id":"GS14"},
        {"file":"src/jhora/panchanga/drik.py","function":"planets_in_retrograde","state_type":"retrograde","decision_rule":"if swe longitude_speed < 0 then retrograde","threshold_source":"swe.calc_ut longi[3]","depends_on":"jd_utc,ayanamsa_mode,planet_speed","branches":"sidereal swisseph branch","producer_consumer_path":"drik.planets_in_retrograde -> main/sudharsana_chakra","evidence_lines":"src/jhora/panchanga/drik.py:L233-L253","anchor_id":"GS15"},
        {"file":"src/jhora/horoscope/chart/charts.py","function":"planets_in_combustion","state_type":"combustion","decision_rule":"abs(planet_long-sun_long) <= combustion_range[p]","threshold_source":"const.combustion_range_of_planets_from_sun(_while_in_retrogade)","depends_on":"retrograde_planets,sun_longitude,planet_longitude","branches":"if planet in retrograde -> use retro combustion range","producer_consumer_path":"charts.planets_in_combustion -> dosha/aayu/tajaka_yoga","evidence_lines":"src/jhora/horoscope/chart/charts.py:L1181-L1198","anchor_id":"GS16"},
        {"file":"src/jhora/utils.py","function":"is_planet_in_exalation","state_type":"dignity_exaltation","decision_rule":"deep exaltation tolerance OR matrix exalted state","threshold_source":"planet_deep_exaltation_longitudes,tolerance,house_strengths_of_planets","depends_on":"planet_positions(optional),planet_house","branches":"deep-longitude branch vs matrix branch","producer_consumer_path":"utils.is_planet_in_exalation -> multiple chart evaluations","evidence_lines":"src/jhora/utils.py:L1259-L1270","anchor_id":"GS17"},
        {"file":"src/jhora/utils.py","function":"is_planet_in_debilitation","state_type":"dignity_debilitation","decision_rule":"deep debilitation tolerance OR matrix debilitated state","threshold_source":"planet_deep_debilitation_longitudes,tolerance,house_strengths_of_planets","depends_on":"planet_positions(optional),planet_house","branches":"deep-longitude branch vs matrix branch","producer_consumer_path":"utils.is_planet_in_debilitation -> weak/strength paths","evidence_lines":"src/jhora/utils.py:L1279-L1291","anchor_id":"GS18"},
        {"file":"src/jhora/utils.py","function":"is_planet_weak","state_type":"weakness_classifier","decision_rule":"debilitation/affliction/dusthana/combustion checks","threshold_source":"house_strengths_of_planets + combustion result","depends_on":"planet_positions,asc_house,combust_set","branches":"feature flags per criterion","producer_consumer_path":"utils.is_planet_weak -> predictive scoring","evidence_lines":"src/jhora/utils.py:L1305-L1370","anchor_id":"GS19"},
        {"file":"src/jhora/const.py","function":"house_strengths_of_planets","state_type":"dignity_matrix","decision_rule":"sign-specific dignity lookup table","threshold_source":"const.house_strengths_of_planets","depends_on":"planet_id,sign_house","branches":"none","producer_consumer_path":"const matrix -> house/strength/longevity/aayu","evidence_lines":"src/jhora/const.py:L286-L307","anchor_id":"GS20"},
    ]
    if avastha_absent:
        rows.append({"file":"InScope-13","function":"n/a","state_type":"avastha","decision_rule":"no direct avastha implementation found in in-scope engine+consumers","threshold_source":"pattern scan: avastha,jagrad,baladi","depends_on":"none","branches":"absence","producer_consumer_path":"n/a","evidence_lines":"research/graha_longitudes_and_states/_coverage_graha_states_callsites_engine_plus_consumers.tsv","anchor_id":"ABSENCE-OF-AVASTHA"})
    return rows

def build_output_matrix() -> list[dict]:
    return [
        {"producer_function":"strength.shad_bala","producer_shape":"[sthana,kala,dig,cheshta,naisargika,drik,sum,rupa,strength]","consumer_function":"main._get_shad_bala","consumer_index_use":"passes full list unchanged","match_status":"match","evidence_lines":"src/jhora/horoscope/main.py:L902-L905","anchor_id":"GS21"},
        {"producer_function":"strength.bhava_bala","producer_shape":"[bb,bb_rupas,bb_strength]","consumer_function":"main._get_bhava_bala","consumer_index_use":"transpose np.array(bb).T","match_status":"transform","evidence_lines":"src/jhora/horoscope/main.py:L906-L914","anchor_id":"GS22"},
        {"producer_function":"charts._vimsopaka_bala_of_planets","producer_shape":"dict[p]=[count,divisional_tags,score]","consumer_function":"main._get_vimsopaka_bala","consumer_index_use":"sv[p][0], sv[p][1], sv[p][2]","match_status":"match","evidence_lines":"src/jhora/horoscope/main.py:L926-L943","anchor_id":"GS23"},
        {"producer_function":"charts.planets_in_combustion","producer_shape":"list[planet_id]","consumer_function":"aayu._pindayu_full_longevity_of_planets","consumer_index_use":"membership & weights per planet","match_status":"match","evidence_lines":"src/jhora/horoscope/dhasa/graha/aayu.py:L46-L58","anchor_id":"GS24"},
        {"producer_function":"charts.planets_in_retrograde","producer_shape":"list[planet_id]","consumer_function":"dosha.manglik","consumer_index_use":"2 in retrograde list","match_status":"match","evidence_lines":"src/jhora/horoscope/chart/dosha.py:L110-L111","anchor_id":"GS25"},
    ]


def anchor_specs(avastha_absent: bool) -> list[dict]:
    anchors = [
        {"id":"GS01","behavior":"Vimsopaka/Vaiseshikamsa weight tables are constant-defined.","src":"src/jhora/const.py","start":141,"end":153,"obs":"Weight dictionaries and score ladders are hardcoded in const."},
        {"id":"GS02","behavior":"Dignity matrix and moola-trikona lookup are constant-defined.","src":"src/jhora/const.py","start":286,"end":311,"obs":"Sign-level dignity and moola-trikona mapping are centralized."},
        {"id":"GS03","behavior":"Combustion ranges include retrograde-specific variant.","src":"src/jhora/const.py","start":494,"end":495,"obs":"Combustion threshold is branchable by retrograde state."},
        {"id":"GS04","behavior":"Retrograde sun-relative windows and method switch are constants.","src":"src/jhora/const.py","start":573,"end":574,"obs":"Chart-based retrograde uses configured limits and mode."},
        {"id":"GS05","behavior":"Shadbala factor requirements and naisargika values are constant-based.","src":"src/jhora/const.py","start":571,"end":571,"obs":"Naisargika baseline values exist in const."},
        {"id":"GS06","behavior":"Sthana bala aggregates uchcha/sapthavargaja/ojayugama/kendra/dreshkona.","src":"src/jhora/horoscope/chart/strength.py","start":214,"end":233,"obs":"Sthana sub-components are summed into one bala vector."},
        {"id":"GS07","behavior":"Dig bala has dedicated directional computation path.","src":"src/jhora/horoscope/chart/strength.py","start":419,"end":438,"obs":"Directional strength is computed separately from other bala parts."},
        {"id":"GS08","behavior":"Kala bala is composite of nine temporal contributors.","src":"src/jhora/horoscope/chart/strength.py","start":643,"end":670,"obs":"Kala bala sums nathonnatha/paksha/tribhaga/abda/masa/vaara/hora/ayana/yuddha."},
        {"id":"GS09","behavior":"Cheshta bala has motion-oriented computation branch.","src":"src/jhora/horoscope/chart/strength.py","start":699,"end":717,"obs":"Cheshta derives from mean/true motion relationships."},
        {"id":"GS10","behavior":"Naisargika bala is direct constant projection.","src":"src/jhora/horoscope/chart/strength.py","start":718,"end":719,"obs":"Naisargika output slices from const values."},
        {"id":"GS11","behavior":"Drik bala computes benefic-minus-malefic aspect contributions.","src":"src/jhora/horoscope/chart/strength.py","start":803,"end":829,"obs":"Aspect matrix is reduced into per-planet drik bala."},
        {"id":"GS12","behavior":"Shad bala assembly returns 9-slot composite payload.","src":"src/jhora/horoscope/chart/strength.py","start":830,"end":854,"obs":"Return includes six components + sum + rupa + strength ratio."},
        {"id":"GS13","behavior":"Bhava bala returns [raw,rupas,strength] triple.","src":"src/jhora/horoscope/chart/strength.py","start":956,"end":968,"obs":"Bhava aggregation is normalized and returned as three arrays."},
        {"id":"GS14","behavior":"Chart retrograde can use old method or sun-window method.","src":"src/jhora/horoscope/chart/charts.py","start":1160,"end":1179,"obs":"Retrograde logic diverges by configured method."},
        {"id":"GS15","behavior":"Drik retrograde uses Swiss Ephemeris speed sign.","src":"src/jhora/panchanga/drik.py","start":233,"end":253,"obs":"Negative longitudinal speed marks retrograde."},
        {"id":"GS16","behavior":"Combustion depends on retrograde branch-specific threshold.","src":"src/jhora/horoscope/chart/charts.py","start":1181,"end":1198,"obs":"Combustion range switches when planet is retrograde."},
        {"id":"GS17","behavior":"Exaltation supports deep-longitude and matrix fallback.","src":"src/jhora/utils.py","start":1259,"end":1270,"obs":"Deep exaltation tolerance can override sign-only checks."},
        {"id":"GS18","behavior":"Debilitation supports deep-longitude and matrix fallback.","src":"src/jhora/utils.py","start":1279,"end":1291,"obs":"Deep debilitation tolerance can override sign-only checks."},
        {"id":"GS19","behavior":"Weakness classifier includes combustion and multiple optional criteria.","src":"src/jhora/utils.py","start":1305,"end":1370,"obs":"Weakness is multi-criterion with feature toggles."},
        {"id":"GS20","behavior":"Main wrapper exposes shadbala and bhava bala from strength module.","src":"src/jhora/horoscope/main.py","start":902,"end":914,"obs":"Main passes shadbala and reshapes bhava bala payload."},
        {"id":"GS21","behavior":"Main wrapper consumes vimsopaka output slots by fixed indices.","src":"src/jhora/horoscope/main.py","start":926,"end":943,"obs":"Consumer expects [count,tags,score] row shape."},
        {"id":"GS22","behavior":"Aayu consumer composes combustion and retrograde state for longevity adjustments.","src":"src/jhora/horoscope/dhasa/graha/aayu.py","start":46,"end":58,"obs":"State lists feed fractional longevity penalties."},
        {"id":"GS23","behavior":"Dosha consumer uses retrograde and combustion booleans in rule chain.","src":"src/jhora/horoscope/chart/dosha.py","start":110,"end":116,"obs":"Consumer uses state presence checks directly in dosha logic."},
        {"id":"GS24","behavior":"Tajaka yoga consumer gates yoga outcomes on combustion/retrograde.","src":"src/jhora/horoscope/transit/tajaka_yoga.py","start":318,"end":320,"obs":"Transit yoga conditions combine combustion and retrograde constraints."},
    ]
    if avastha_absent:
        anchors.append({"id":"ABSENCE-OF-AVASTHA","behavior":"No direct Avastha implementation found in in-scope files.","src":"research/graha_longitudes_and_states/_coverage_graha_states_callsites_engine_plus_consumers.tsv","start":1,"end":1,"obs":"Pattern scan found no explicit avastha/jagrad/baladi implementation in locked scope."})
    anchors.append({"id":"GS900","behavior":"Residual matched rows are retained for completeness.","src":"research/graha_longitudes_and_states/_coverage_graha_states_callsites_engine_plus_consumers.tsv","start":1,"end":1,"obs":"Non-focused matches remain visible via GS900 rows."})
    return anchors


def write_tsv(path: Path, columns: list[str], rows: list[dict]):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=columns, delimiter="\t")
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in columns})

def build_map_md(digests: list[tuple[str, str, int]], anchors: list[dict], call_rows: list[dict], avastha_absent: bool):
    t = dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    out = []
    out.append("# graha_states_behavior_contract_map.engine_plus_consumers.md")
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
    out.append("## Evidence anchors (GS01..GSNN, ABSENCE-OF-AVASTHA, GS900)")
    out.append("")
    for a in anchors:
        out.append(f"### {a['id']}")
        out.append("")
        out.append(f"- Behavior: {a['behavior']}")
        if a['src'].startswith("src/"):
            out.append(f"- Source: `{a['src']}:L{a['start']}-L{a['end']}`")
            out.append("- Excerpt:")
            out.append("```python")
            out.append(excerpt(a['src'], a['start'], a['end']))
            out.append("```")
        else:
            out.append(f"- Source: `{a['src']}`")
            out.append("- Excerpt:")
            out.append("```text")
            out.append("Evidence row is present in generated callsite inventory.")
            out.append("```")
        out.append(f"- Observed behavior: {a['obs']}")
        out.append("")
    out.append("## Conflict / ambiguity register")
    out.append("")
    out.append("- UNCERTAIN-GS-SHADBALA-01: formula and normalization vary across bala sub-components.")
    out.append("- UNCERTAIN-GS-STATE-01: retrograde differs between drik speed-sign and chart sun-window methods.")
    out.append("- UNCERTAIN-GS-COMBUST-RETRO-01: combustion logic branches on retrograde state.")
    out.append("- UNCERTAIN-GS-DIGNITY-01: matrix dignity and deep-longitude dignity can diverge.")
    out.append("- UNCERTAIN-GS-OUTIDX-01: producer payloads are heterogeneous across bala/state APIs.")
    out.append("- UNCERTAIN-GS-AVASTHA-ABSENCE-01: " + ("absence confirmed in locked scope." if avastha_absent else "partial presence detected; needs deeper mapping."))
    out.append("")
    out.append("## Coverage ledger")
    out.append("")
    out.append("- Inventory file: `research/graha_longitudes_and_states/_coverage_graha_states_callsites_engine_plus_consumers.tsv`")
    out.append(f"- Inventory row count: `{len(call_rows)}`")
    out.append("- Shadbala component matrix: `research/graha_longitudes_and_states/_coverage_graha_states_shadbala_component_matrix.tsv`")
    out.append("- State logic matrix: `research/graha_longitudes_and_states/_coverage_graha_states_state_logic_matrix.tsv`")
    out.append("- Output contract matrix: `research/graha_longitudes_and_states/_coverage_graha_states_output_contract_matrix.tsv`")
    (OUT_ROOT / "graha_states_behavior_contract_map.engine_plus_consumers.md").write_text("\n".join(out) + "\n", encoding="utf-8")


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
        rows.append({"original_path": rel, "codepack_path": norm_rel(cp.relative_to(CODEPACK_ROOT)), "sha256": h, "bytes": str(sz), "copied_sha256": ch, "copied_bytes": str(csz)})
    with (CODEPACK_ROOT / "MANIFEST.tsv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["original_path","codepack_path","sha256","bytes","copied_sha256","copied_bytes"], delimiter="\t")
        w.writeheader(); w.writerows(rows)


def main():
    OUT_ROOT.mkdir(parents=True, exist_ok=True)
    CODEPACK_ROOT.mkdir(parents=True, exist_ok=True)

    digests = []
    for rel in IN_SCOPE:
        h, sz = sha256_and_size(SOURCE_ROOT / rel)
        digests.append((rel, h, sz))

    call_rows, avastha_direct_found = build_callsites()
    shadbala_rows = build_shadbala_matrix()
    state_rows = build_state_matrix(avastha_absent=(not avastha_direct_found))
    outidx_rows = build_output_matrix()

    write_tsv(OUT_ROOT / "_coverage_graha_states_callsites_engine_plus_consumers.tsv", CALLSITE_COLUMNS, call_rows)
    write_tsv(OUT_ROOT / "_coverage_graha_states_shadbala_component_matrix.tsv", SHADBALA_COLUMNS, shadbala_rows)
    write_tsv(OUT_ROOT / "_coverage_graha_states_state_logic_matrix.tsv", STATE_COLUMNS, state_rows)
    write_tsv(OUT_ROOT / "_coverage_graha_states_output_contract_matrix.tsv", OUTIDX_COLUMNS, outidx_rows)

    anchors = anchor_specs(avastha_absent=(not avastha_direct_found))
    build_map_md(digests, anchors, call_rows, avastha_absent=(not avastha_direct_found))
    copy_codepack_and_manifest(digests)

    report = []
    report.append("# graha_longitudes_and_states")
    report.append("")
    report.append("## artifacts")
    report.append("- `graha_states_behavior_contract_map.engine_plus_consumers.md`")
    report.append("- `_coverage_graha_states_callsites_engine_plus_consumers.tsv`")
    report.append("- `_coverage_graha_states_shadbala_component_matrix.tsv`")
    report.append("- `_coverage_graha_states_state_logic_matrix.tsv`")
    report.append("- `_coverage_graha_states_output_contract_matrix.tsv`")
    report.append("- `_codepack/MANIFEST.tsv`")
    report.append("")
    report.append("## notes")
    report.append(f"- in-scope files: {len(IN_SCOPE)}")
    report.append(f"- callsite rows: {len(call_rows)}")
    report.append(f"- absence-of-avastha: {str((not avastha_direct_found)).lower()}")
    report.append("- canonical path: research/graha_longitudes_and_states")
    (OUT_ROOT / "report.md").write_text("\n".join(report) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
