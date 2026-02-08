# Repo Vedic Equivalency Map (Baztab) — Vedic‑Only Canonical

Date: 2026-02-06  
Scope: Remove Western runtime; Vedic is canonical; JHora only for QA/diff (non‑gating)

## 0) Executive Summary

Runtime still routes through Western factories and Western schemas. The primary public API (`kerykeion/__init__.py`) exports Western factories and legacy wrappers; CLI routes through `AstrologicalSubjectFactory` and a legacy D1 helper. That means Western code remains in the executable call graph even when requesting Vedic output. To reach Vedic‑only, we must introduce a Vedic‑only factory/context entrypoint and rewire **all** entrypoints to it, then archive/remove Western factories/modules.

Evidence:
- Library exports Western factories and legacy wrappers: `kerykeion/__init__.py:45–127`
- CLI dispatch calls Western factory via `AstrologicalSubjectFactory.from_birth_data`: `kerykeion/_cli/commands/vedic_d1.py:86–106`
- Vedic builder currently consumes Western `calc_data`: `kerykeion/vedic/builder.py:111–230`

---

## 1) EntryPoints Map (runtime paths)

| Entrypoint | File:Line | Current call graph | Vedic equivalent | Action |
| --- | --- | --- | --- | --- |
| Library public API (imports) | `kerykeion/__init__.py:45–127` | Exports Western factories (AstrologicalSubjectFactory, ChartDrawer, AspectsFactory, etc.) | Export **VedicSubjectFactory** only | REWRITE |
| CLI wrapper | `kerykeion/cli.py:5–7` | `kerykeion._cli.app.dispatch` and `run_vedic_d1` + legacy `build_d1_whole_sign` | `baztab/_cli/app.py` should call VedicSubjectFactory | REWRITE |
| CLI dispatch | `kerykeion/_cli/app.py:10–21` | Only “vedic d1” but still uses Western factory via command module | Use VedicSubjectFactory directly (no Western) | REWRITE |
| CLI command: vedic d1 | `kerykeion/_cli/commands/vedic_d1.py:86–123` | Uses `AstrologicalSubjectFactory` + `build_d1_whole_sign` | Directly call VedicSubjectFactory + context | REWRITE |
| Legacy API class | `kerykeion/backword.py:1–900` | Wraps Western subject factory | Remove/Archive | REMOVE |
| Examples | `examples/*.py` | Western factories + charts | Replace with Vedic‑only examples or archive | REWRITE/ARCHIVE |

Goal: **all entrypoints call VedicSubjectFactory** and never instantiate Western factories.

---

## 2) Domain Modules: Keep / Replace / Archive

### 2A) Canonical Vedic Core (KEEP)

| Module | Why keep | Required refactor (if any) |
| --- | --- | --- |
| `kerykeion/vedic/context.py` | Canonical SwissEph compute path | Make this the only `swe.*` call site |
| `kerykeion/vedic/registry.py` | Ayanamsa + house spec registry | No change; enforce in Vedic factory |
| `kerykeion/vedic/vargas.py` | Varga engine & registry | Ensure defaults embedded, remove compat‑only rules |
| `kerykeion/vedic/rasi_d1.py` | Pure D1 point builder | Keep; ensure it consumes context output |
| `kerykeion/vedic/houses.py` | Whole‑sign house mapping | Keep; no `swe.*` calls |
| `kerykeion/ayanamsa.py` | Shared sidereal utilities | Keep if Vedic pipeline still needs (only for non‑context calls) |
| `kerykeion/time_contract.py` | JD/time conversion | Keep; used by Vedic factory |

Evidence:
- `VedicCalculationContext` is already canonical compute: `kerykeion/vedic/context.py:54–130`
- `rasi_d1` and `houses` are pure functions: `kerykeion/vedic/rasi_d1.py:24–39`, `kerykeion/vedic/houses.py:15–31`

### 2B) Mixed / Transitional (REWRITE to Vedic equivalents)

| Module | Current role | Vedic equivalent | Migration |
| --- | --- | --- | --- |
| `kerykeion/astrological_subject_factory.py` | Western subject builder + optional Vedic payload | **VedicSubjectFactory** that uses `VedicCalculationContext` and builds `VedicModel` directly | Replace usage in CLI + public API; deprecate file |
| `kerykeion/vedic/builder.py` | Vedic payload built from Western `calc_data` | VedicSubjectFactory should bypass calc_data entirely | Move mapping into new factory and delete builder or limit to transitional adapter |
| `kerykeion/vedic/d1.py` | Direct SwissEph calls for Vedic D1 | Replace with context output + `rasi_d1` | Archive/delete (Western‑style path) |
| `kerykeion/_cli/commands/vedic_d1.py` | CLI uses Western factory + build_d1_whole_sign | Use VedicSubjectFactory + context | Rewrite |

Evidence of mixed path:
- Builder uses Western `calc_data` (sun/moon/asc): `kerykeion/vedic/builder.py:146–197`
- CLI command uses `AstrologicalSubjectFactory`: `kerykeion/_cli/commands/vedic_d1.py:86–106`

### 2C) Western‑only (ARCHIVE/DELETE)

| Module/Folder | Why remove | Extract? |
| --- | --- | --- |
| `kerykeion/aspects/*` | Western‑only aspects | None (Vedic has different drishti rules) |
| `kerykeion/charts/*` | Western SVG rendering | None (Vedic UI separate) |
| `kerykeion/house_comparison/*` | Western synastry | None |
| `kerykeion/report.py` | Western report + ASCII tables | None |
| `kerykeion/chart_data_factory.py` | Western chart data | None |
| `kerykeion/composite_subject_factory.py` | Western composites | None |
| `kerykeion/planetary_return_factory.py` | Western returns | None |
| `kerykeion/relationship_score_factory.py` | Western compatibility | None |
| `kerykeion/transits_time_range_factory.py` | Western transits | None |
| `kerykeion/context_serializer.py` | Western narrative | None |
| `kerykeion/ephemeris_data_factory.py` | Western multi‑subject factory | None |
| `kerykeion/backword.py` | Legacy Western API | None |

Evidence (examples):
- Report uses `simple_ascii_tables` (Western): `kerykeion/report.py:6`
- Charts render SVG: `kerykeion/charts/chart_drawer.py:1+` (Western only)

---

## 3) Data & Configuration Map (Ephemeris/Geonames/Cache)

| Data path | Current usage | Keep in repo? | Action |
| --- | --- | --- | --- |
| `data/*.se1` | SwissEph binaries | **No** | Move to external ephe path; add to `.gitignore` |
| `data/*.txt` (e.g. `ast_list.txt`, `sefstars.txt`) | Text catalogs | Optional | Keep if used by SwissEph or charts |
| `kerykeion/sweph/*.se1` | Local ephemeris | **No** | Ignore binaries only; keep README | 
| `kerykeion/sweph/README.md` | Ephe instructions | Yes | Keep |
| `cache/` + `geonames*.sqlite` | GeoNames runtime cache | **No** | Ignore |

Evidence:
- GeoNames cache default: `kerykeion/fetch_geonames.py:21–22`
- Cache storage uses sqlite backend: `kerykeion/fetch_geonames.py:53–57`

---

## 4) Schemas & Output Contract (Pydantic v2)

Current models are mixed Western + Vedic in `kerykeion/schemas/kr_models.py`. Vedic models are defined here:
- `VedicSettingsModel`: `kerykeion/schemas/kr_models.py:132–142`
- `VedicCoreModel`: `:152–159`
- `VedicRasiD1Model`: `:182–189`
- `VedicVargasModel`: `:225–232`
- `VedicModel`: `:234–243`

Western models dominate file (`AstrologicalSubjectModel`, `PlanetReturnModel`, etc.)—should be **split** for Vedic‑only:
- KEEP: Vedic models (move to `kerykeion/schemas/vedic_models.py` or keep in same file if you avoid Western exports)
- REMOVE/ARCHIVE: Western models after Vedic‑only transition

Decision: Baztab canonical output = `VedicModel` only. If you need “dynamic payloads”, keep a separate `BaztabPayloadModel` with explicit optional sections.

---

## 5) Tests Map (Keep/Rewrite/Archive)

### KEEP (Vedic core)
- `tests/test_vedic_context.py` (context gate)
- `tests/test_vedic_contract.py` (registry gate)
- `tests/test_vedic_vargas.py` (varga logic)
- `tests/test_vedic_vargas_pyjhora_d7.py`, `tests/test_vedic_vargas_pyjhora_d81.py` (PyJHora parity)

### REWRITE (QA diff, not gating)
- `tests/test_vedic_vargas_parity_jhora.py` → move into QA harness (non‑blocking) or `tools/jhora_diff.py`

### ARCHIVE/DELETE
- `tests/aspects/*`, `tests/charts/*`, `tests/compatibility/*`, `tests/reports/*`, `tests/factories/*` (Western only)

Evidence:
- Vedic tests list: `tests/test_vedic_*`
- Western test directories: `tests/aspects`, `tests/charts`, `tests/reports` (see `tests/` tree)

---

## 6) Dependency Map (pyproject.toml)

Dependencies currently:
- **Keep**: `pyswisseph`, `pydantic`, `pytz`, `typing-extensions`
- **Maybe keep**: `requests`, `requests-cache` (if you still want GeoNames lookup)
- **Remove**: `scour` (SVG charts), `simple-ascii-tables` (Western report)

Evidence:
- `pyproject.toml:dependencies` includes `scour`, `simple-ascii-tables`, `requests-cache`.
- Western report uses `simple_ascii_tables`: `kerykeion/report.py:6`

Suggested removal timing:
- Phase C3 (after archiving Western modules), remove unused deps.

---

## 7) Action Plan (phase‑based, non‑hacky)

### Phase C0 — Research lock‑in (this report)
- ✅ Identify entrypoints and Western paths
- ✅ Identify Vedic core and mixed modules

### Phase C1 — Introduce VedicSubjectFactory + canonical time/place
- Create `kerykeion/vedic/factory.py`
- Inputs: birth data (date/time/tz/lat/lon/alt)
- Use `VedicCalculationContext.compute_core()` and build `VedicModel`
- Stop using `calc_data` from Western pipeline

Tests:
- New factory tests (basic output + deterministic) + reuse `test_vedic_context` and `test_vedic_vargas`

### Phase C2 — Rewire entrypoints
- Update `kerykeion/__init__.py` to export VedicSubjectFactory only
- Update CLI to call VedicSubjectFactory and remove `AstrologicalSubjectFactory` dependency
- Remove `build_d1_whole_sign` usage (deprecated)

Tests:
- CLI smoke + Vedic tests

### Phase C3 — Archive Western modules + deps
- Move Western modules to `_archive/` or remove
- Remove Western tests
- Prune dependencies (`scour`, `simple-ascii-tables`, possibly `requests-cache` if GeoNames removed)

### Phase C4 — QA harness (non‑blocking)
- Convert JHora parity into `tools/jhora_diff.py`
- Store snapshots under `tests/fixtures/jhora_oracle/` and keep as QA only

---

# Bottom line

After executing this map, **no runtime path** will instantiate Western factories or Western schemas; Vedic will be canonical and deterministic; JHora remains QA‑only.
