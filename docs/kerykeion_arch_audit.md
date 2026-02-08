# Kerykeion Vedic-Only Migration Plan (Audit + Refactor Map)

Date: 2026-02-05
Scope: Remove Western astrology; keep SwissEphemeris; Vedic-only canonical pipeline; JHora as QA/diff only.

## A) Public API + Entry Points (current)

**Primary entrypoint now:**
- `kerykeion/astrological_subject_factory.py::AstrologicalSubjectFactory.from_birth_data` (and `.from_current_time`, `.from_iso_utc_time`).

**Other public factories built on Western:**
- `kerykeion/chart_data_factory.py::ChartDataFactory`
- `kerykeion/aspects/aspects_factory.py::AspectsFactory`
- `kerykeion/composite_subject_factory.py::CompositeSubjectFactory`
- `kerykeion/planetary_return_factory.py::PlanetaryReturnFactory`
- `kerykeion/transits_time_range_factory.py::TransitsTimeRangeFactory`
- `kerykeion/ephemeris_data_factory.py::EphemerisDataFactory`

**Recommendation (Vedic-only):**
- New public entrypoint: `VedicSubjectFactory.from_birth_data` (new file under `kerykeion/vedic/subject_factory.py`) OR rename the existing factory to `VedicSubjectFactory` and provide a thin compatibility wrapper if you want a transition period.
- If breaking changes are acceptable, remove Western factories from `kerykeion/__init__.py` and expose only Vedic.

## B) Keep / Refactor / Delete Map

| Keep | Refactor | Delete |
| --- | --- | --- |
| `kerykeion/vedic/*` (builder, vargas, houses, rasi_d1) | `kerykeion/astrological_subject_factory.py` → replace with Vedic-only factory; drop aspects/houses/Western calc | `kerykeion/aspects/*` |
| `kerykeion/ayanamsa.py` (sidereal mode + ayan) | `kerykeion/ephemeris_data_factory.py` → rename/redo as Vedic ephemeris series | `kerykeion/chart_data_factory.py` |
| `kerykeion/ephemeris.py` | `kerykeion/context_serializer.py` → Vedic-only context view | `kerykeion/composite_subject_factory.py` |
| `kerykeion/schemas/kr_models.py` (but prune Western models) | `kerykeion/__init__.py` → export Vedic-only API | `kerykeion/planetary_return_factory.py` |
| `kerykeion/utilities.py` (time + geo helpers) | `kerykeion/report.py` → Vedic-only report | `kerykeion/transits_time_range_factory.py` |
| `kerykeion/fetch_geonames.py` | `kerykeion/llms.txt` → update docs/examples to Vedic | `kerykeion/charts/*` (SVG/visualization for Western)
| `kerykeion/settings/*` (only Vedic relevant constants) | `kerykeion/backword.py` → remove (Western legacy) | `kerykeion/house_comparison/*`
| `kerykeion/schemas/kr_literals.py` (keep shared enums; remove western-only aspects) | `kerykeion/schemas/kr_models.py` → split Vedic models into their own module | `kerykeion/relationship_score_factory.py`

Notes:
- Anything aspect-related or synastry-specific is Western; remove entirely unless you want Vedic equivalents later.
- Western houses, aspects, composite/synastry, returns, transits are all Western-specific and should be deleted.

## C) Shared data to keep (Vedic-only minimal set)

- Time conversions: JD UTC, local time, tz handling (from `astrological_subject_factory.py::_calculate_time_conversions`).
- Geo location: lat/lon/alt and tz (from `LocationData`).
- Ephemeris context: `set_ephe_path`, `set_sid_mode` (wrapped safely).
- Ayanamsa: `kerykeion/ayanamsa.py`.

## D) Vedic canonical pipeline (recommended)

**Current Vedic uses Western `calc_data` as input**
- `build_vedic_payload(calc_data, ...)` in `kerykeion/vedic/builder.py`.

**Target Vedic-only pipeline (canonical):**
1) Build a `VedicCalculationContext` from birth data:
   - JD UTC, tz, lat/lon/alt, ephe_path
2) Compute **sidereal abs positions directly** (planets + nodes) via SwissEph with sidereal mode set.
3) Compute Asc/MC from SwissEph using sidereal flags *or* tropical-ayan (only if compat requires).
4) Construct D1, houses, vargas from sidereal core.
5) Return `VedicSubjectModel` (new Vedic-only Pydantic model).

**Rationale:** This removes dependency on Western `calc_data`, makes Vedic canonical, and isolates SwissEph global state.

## E) QA/JHora usage

- JHora is **oracle only**, not a runtime feature.
- Keep parity and diff tests only in `tests/test_vedic_vargas_parity_jhora.py` + fixtures.
- Keep PyJHora parity tests as golden truth for varga engine.
- Remove JHora parity from runtime (no compat flags in public API, or keep only in test-only harness).

## F) Docs + packaging

- Update `docs/README.md` to explicitly state Vedic-only.
- Move Western-specific docs to archive or delete.
- Update `kerykeion/__init__.py` exports to Vedic-only.
- Update `kerykeion/_cli` commands to use Vedic factory and remove Western commands.

---

# Plan (Phased)

## Phase 0: Baseline + snapshot
- Save current test status (already in `docs/kerykeion_arch_audit.md`).
- Run: `pytest -k "vedic_vargas" -q` and `pytest -k "pyjhora_" -q`.

**Files touched**: none
**Risks**: none
**Acceptance**: tests pass

## Phase 1: Introduce Vedic-only factory/context
- Create `kerykeion/vedic/subject_factory.py`.
- Move time/geo normalization into Vedic context (reuse `LocationData` + `_calculate_time_conversions`).
- Compute sidereal abs directly; do not rely on Western `calc_data`.

**Files**:
- Add: `kerykeion/vedic/subject_factory.py`
- Refactor: `kerykeion/vedic/builder.py` to accept `VedicCalculationContext` instead of Western `calc_data`.

**Risks**:
- SwissEph global state management.
- Backward compatibility break.

**Tests**:
- Add new `tests/test_vedic_subject_factory.py` (basic D1/asc/planet positions sanity).

## Phase 2: Delete Western modules + refactor imports
- Remove Western factories and aspects pipeline:
  - `kerykeion/astrological_subject_factory.py`
  - `kerykeion/aspects/*`
  - `kerykeion/chart_data_factory.py`
  - `kerykeion/composite_subject_factory.py`
  - `kerykeion/planetary_return_factory.py`
  - `kerykeion/transits_time_range_factory.py`
  - `kerykeion/relationship_score_factory.py`
  - `kerykeion/house_comparison/*`
  - `kerykeion/charts/*`
- Update imports in `kerykeion/__init__.py` and CLI.

**Risks**:
- Breaks all Western tests; must delete or rewrite.

**Tests**:
- Remove Western test suites (aspects, chart data, synastry, returns).

## Phase 3: Tests migration + QA harness
- Keep Vedic tests:
  - `test_vedic_vargas.py`
  - `test_vedic_vargas_parity_jhora.py`
  - `test_vedic_vargas_pyjhora_*.py`
- Update fixtures for Vedic-only suite.
- Keep `docs/jhora_*` parity docs, but mark as QA only.

**Risks**:
- Missing coverage for time/geo conversions.

**Tests**:
- Add `test_vedic_context_time_geo.py` for JD/geo/tz conversions.

## Phase 4: Docs + packaging cleanup
- Rewrite `docs/README.md` to Vedic-only.
- Archive/remove Western docs.
- Update `kerykeion/llms.txt` to Vedic-only API examples.
- Ensure `pyproject.toml` metadata updated to Vedic-only.

---

# Keep/Refactor/Delete Detail (with reasons)

**Keep (shared utilities):**
- `kerykeion/ayanamsa.py` (sidereal mode + ayanamsa) — Vedic core.
- `kerykeion/ephemeris.py` (ephe path helpers) — Vedic core.
- `kerykeion/fetch_geonames.py` + `LocationData` (geo + timezone) — Vedic core.
- `kerykeion/utilities.py` (time conversions + normalization).
- `kerykeion/vedic/*` (all Vedic logic).

**Refactor:**
- `kerykeion/astrological_subject_factory.py` → remove Western features; replace with Vedic subject factory.
- `kerykeion/schemas/kr_models.py` → remove Western models (aspects, composite, return models), keep Vedic models only (or split into `vedic_models.py`).
- `kerykeion/__init__.py` → export only Vedic API.
- `kerykeion/_cli/commands/vedic_d1.py` → point to VedicSubjectFactory (no Western subject).

**Delete:**
- `kerykeion/aspects/*`, `kerykeion/chart_data_factory.py`, `kerykeion/composite_subject_factory.py`, `kerykeion/planetary_return_factory.py`, `kerykeion/transits_time_range_factory.py`, `kerykeion/relationship_score_factory.py`, `kerykeion/house_comparison/*`, `kerykeion/charts/*`, `kerykeion/backword.py`.

---

# QA + JHora

- Keep JHora parity tests as QA only.
- Keep PyJHora parity tests as golden truth for varga engine.
- Remove compat flags from public API (or keep them under test-only harness if needed).

---

# Open Questions

1) Breaking change OK? If yes, we can delete Western factories outright. If not, provide a small compatibility wrapper.
2) Do you want to keep any Western artifacts (e.g., charts SVG) in an archive folder for reference?

