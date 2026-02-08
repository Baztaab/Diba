# Natal Full Data Roadmap (Kerykeion Architecture, Evidence-Based)

## 1) Scope & Non-Negotiables
- Scope: `Natal only` (non-GUI).
- Out of scope (explicit): `dasha`, `transit`, `prediction`, `match`.
- No new dependencies.
- `swe.set_*` only in `kerykeion/vedic/context.py`.
- `policy` only in `kerykeion/vedic/registry.py`.
- `orchestration` only in `kerykeion/vedic/factory.py` + `kerykeion/vedic/services/*`.
- CLI only parse/validate/dispatch in `_cli/*`.
- `recognized-but-not-implemented` must fail fast.
- Roadmap model: `Derived D0..D7` (data-tier first, not domain-first).

## 2) Evidence Inventory

### 2.1 Must-Read (12 files)
- `kerykeion/vedic/registry.py`
- `kerykeion/vedic/context.py`
- `kerykeion/vedic/factory.py`
- `kerykeion/_cli/options.py`
- `kerykeion/_cli/app.py`
- `kerykeion/_cli/commands/vedic_d1.py`
- `docs/jhora/const.py`
- `docs/jhora/panchanga/drik.py`
- `docs/jhora/horoscope/chart/charts.py`
- `docs/jhora/horoscope/chart/house.py`
- `docs/jhora/horoscope/chart/arudhas.py`
- `docs/research/pyjhora_runtime_recipe.md`

Why these are mandatory:
- معماری فعلی و guardrailهای runtime/CLI را مستقیم پوشش می‌دهند.
- سطح واقعی داده‌های ناتال PyJHora را مشخص می‌کنند (ayanamsa/house/panchanga/chart/arudha/karaka).

### 2.2 Optional (focused)
- `_archive/legacy_bridge/vedic_d1.py`
- `_archive/legacy_western/kerykeion/chart_data_factory.py`
- `_archive/legacy_western/kerykeion/ephemeris_data_factory.py`
- `_archive/legacy_western/tests/core/test_json_dump.py`
- `schemas/static_chart.v0.1.json`
- `kerykeion/vedic/static_chart.py`
- `docs/research/jhora_config_mapping.md`
- `docs/research/pyjhora_coverage.md`
- `docs/research/pyjhora_contract_evidence.md`

Why optional:
- برای refinement الگوی contract/test/migration مفید هستند اما برای تصمیم‌های D0..D7 حیاتی نیستند.

### 2.3 Evidence Findings (No Guess)
- CLI فعلی فقط `vedic d1` را dispatch می‌کند: `kerykeion/_cli/app.py` و `kerykeion/_cli/options.py`.
- الگوی parse/validate/dispatch در CLI شفاف است: `kerykeion/_cli/options.py`, `kerykeion/_cli/commands/vedic_d1.py`.
- policy resolution در factory انجام می‌شود: `kerykeion/vedic/factory.py`.
- `swe.set_*` در runtime فعلی فقط در context است و guard test هم دارد: `kerykeion/vedic/context.py`, `tests/test_vedic_no_swe_outside_context.py`.
- fail-fast برای modeهای recognized-not-implemented موجود است: `kerykeion/vedic/registry.py`, `tests/test_config_surface_pyjhora_parity.py`.
- PyJHora ayanamsa surface در `docs/jhora/const.py` تعریف شده است.
- house systems (1..5 + western) در `docs/jhora/const.py` و منطق آن در `docs/jhora/panchanga/drik.py`/`docs/jhora/horoscope/chart/charts.py` آمده است.
- arudha و karaka صریحاً در `docs/jhora/horoscope/chart/arudhas.py` و `docs/jhora/horoscope/chart/house.py` وجود دارند.
- panchanga runtime وابستگی شدید به JD/timezone conversion دارد: `docs/research/pyjhora_runtime_recipe.md`, `docs/jhora/panchanga/drik.py`.
- legacy pattern بیشتر model-first + validation-heavy است، نه schema explosion: `_archive/legacy_western/tests/core/test_json_dump.py`, `schemas/static_chart.v0.1.json`.

## 3) Contracts (Minimal, Versioned)

### 3.1 Contract Set (only 2 schemas in v1)
- `schemas/vedic_natal_core.v1.json`
  - Covers D0..D5.
  - `core` mandatory.
  - `advanced` sections optional with feature flags.
- `schemas/vedic_natal_full.v1.json`
  - Envelope contract.
  - Wraps `core` + optional `panchanga` (D6) + provenance/diagnostics fields.

### 3.2 Versioning Rules
- Any breaking field change => version bump.
- New optional fields => same version.
- `schema_version` required in payload root (like `static_chart.v0.1` pattern).

## 4) CLI Surface (Minimal)
- `kerykeion vedic natal core [--diagnose-runtime]`
- `kerykeion vedic natal full [--include-panchanga]`

Notes:
- No separate CLI for dasha/transit/prediction.
- CLI handlers remain thin wrappers to services.

## 5) Data-Tier Roadmap (Derived D0..D7)

## D0: Runtime Canonicalization Lock
- Owner modules:
`kerykeion/vedic/registry.py`
`kerykeion/vedic/context.py`
- Deliverables:
  - Freeze ayanamsa/house/node policy surface with explicit status.
  - Enforce deterministic context call-order and reset behavior.
  - Runtime diagnostics branch under `--diagnose-runtime`.
- Tests:
`tests/test_natal_d0_registry_surface.py`
`tests/test_natal_d0_context_call_order.py`
`tests/test_natal_d0_no_swe_outside_context.py`

## D1: Core Natal Typed Model
- Owner modules:
`kerykeion/vedic/factory.py`
`kerykeion/vedic/services/natal_core_service.py`
`kerykeion/vedic/contracts/natal_core_contract.py`
- Deliverables:
  - Typed input/output for natal core.
  - Serialize to `vedic_natal_core.v1`.
  - Data-tier tagging (`core`, `advanced` placeholders).
- Tests:
`tests/test_natal_d1_contract_core.py`
`tests/test_natal_d1_factory_validation.py`

## D2: Varga Tier
- Owner modules:
`kerykeion/vedic/vargas.py`
`kerykeion/vedic/services/natal_core_service.py`
- Deliverables:
  - Batch varga outputs integrated into core contract `advanced.varga`.
  - Method/profile registry references only (no policy in service).
- Tests:
`tests/test_natal_d2_varga_parity.py`
`tests/test_natal_d2_varga_boundaries.py`

## D3: House/Arudha/Karaka Tier
- Owner modules:
`kerykeion/vedic/services/natal_house_service.py`
- Deliverables:
  - bhava triplets
  - drishti/argala diagnostics
  - chara karakas
  - bhava/graha arudhas
- Tests:
`tests/test_natal_d3_house_arudha_karaka.py`

## D4: Analytics Foundation Tier
- Owner modules:
`kerykeion/vedic/services/natal_analytics_service.py`
- Deliverables:
  - Strength baseline fields (deterministic subset).
  - Contract integration under `advanced.analytics.strength`.
- Tests:
`tests/test_natal_d4_strength_smoke.py`

## D5: Analytics Extended Tier
- Owner modules:
`kerykeion/vedic/services/natal_analytics_service.py`
- Deliverables:
  - Yoga/dosha/sphuta subsets behind explicit feature flags.
  - `recognized_not_implemented` for unsupported IDs.
- Tests:
`tests/test_natal_d5_yoga_dosha_sphuta.py`
`tests/test_natal_d5_fail_fast_status.py`

## D6: Panchanga Tier (Deferred-Until-Green)
- Status:
`In scope but deferred`
- Start gate:
  - D0..D4 all green.
  - Context/time-policy drift report zero critical mismatch.
- Owner modules:
`kerykeion/vedic/services/natal_panchanga_service.py`
- Deliverables:
  - sunrise/sunset/moonrise/moonset
  - tithi/vara/nakshatra/yoga/karana
  - rahu/gulika/yamaghanta/hora
- Tests:
`tests/test_natal_d6_panchanga_parity.py`
`tests/test_natal_d6_timezone_dst_edges.py`

## D7: Productization Tier
- Owner modules:
`kerykeion/_cli/options.py`
`kerykeion/_cli/app.py`
`kerykeion/_cli/commands/vedic_natal.py`
`kerykeion/vedic/services/natal_full_data_service.py`
- Deliverables:
  - `natal core` and `natal full` commands.
  - `vedic_natal_full.v1` envelope output.
- Tests:
`tests/test_natal_d7_cli_core.py`
`tests/test_natal_d7_cli_full.py`
`tests/test_natal_d7_contract_full.py`

## 6) DoD Template (Strict, Measurable)
- Dataset:
  - fixed fixtures with explicit provenance.
  - minimum case count per tier required.
- Tolerance:
  - numeric tolerance defined per field (arcsec/seconds).
- Test file:
  - exact pytest file(s) listed.
- Pass condition:
  - binary threshold (e.g., `N/N pass`, `max delta <= X`).

### 6.1 DoD Matrix
- D0:
  - Cases: 12
  - Tolerance: planets/nodes/asc `<= 1.0 arcsec`
  - Pass: `12/12`, and `0` SwissEph offenders outside context.
- D1:
  - Cases: 20
  - Tolerance: contract validation strict (`0` schema errors)
  - Pass: `20/20` + deterministic replay hash equality.
- D2:
  - Cases: 20 (core vargas) + 6 (D81/108/144)
  - Tolerance: sign exact match, longitude `<= 1.0 arcsec`
  - Pass: core `>= 99%`, extended `>= 95%`.
- D3:
  - Cases: 12
  - Tolerance: house cusp `<= 5.0 arcsec`; arudha/karaka exact index
  - Pass: `12/12`.
- D4:
  - Cases: 10
  - Tolerance: deterministic exact (discrete outputs), numeric `<= 1e-9` where applicable
  - Pass: `10/10`.
- D5:
  - Cases: 10
  - Tolerance: boolean/index exact; sphuta `<= 30 arcsec`
  - Pass: `10/10` + fail-fast tests all pass.
- D6:
  - Cases: 12 (timezone + DST heavy)
  - Tolerance: rise/set `<= 60s`; phase boundaries `<= 60s`
  - Pass: `>= 95%`, no critical timezone regression.
- D7:
  - Cases: 14 CLI e2e
  - Tolerance: `0` parse/dispatch regressions; `0` contract failures
  - Pass: `14/14`.

## 7) Guardrails -> Concrete Tests
- No scripts import in runtime tests:
`tests/test_natal_guard_no_scripts_runtime_import.py`
- No self-fulfilling golden fallback:
`tests/test_natal_guard_no_expected_as_fallback.py`
- No SwissEph outside context:
`tests/test_natal_guard_no_swe_outside_context.py`
- Recognized-not-implemented fail-fast:
`tests/test_natal_guard_fail_fast_modes.py`
- CLI thin-layer enforcement:
`tests/test_natal_guard_cli_no_astro_logic.py`

## 8) Explicit Out-of-Scope
- No dasha files/services/contracts/CLI in this roadmap phase.
- No transit/tajaka/saham.
- No prediction APIs.
- No compatibility/match.

## 9) Next Sprint = D0 Only

Allowed files to change in this sprint (max 5):
- `kerykeion/vedic/registry.py`
- `kerykeion/vedic/context.py`
- `kerykeion/vedic/factory.py`
- `kerykeion/_cli/commands/vedic_d1.py`
- `tests/test_natal_d0_context_call_order.py`

Exact tests for D0:
- `tests/test_natal_d0_registry_surface.py`
- `tests/test_natal_d0_context_call_order.py`
- `tests/test_natal_d0_no_swe_outside_context.py`

D0 measurable DoD:
- `docs/jhora/const.py` ayanamsa IDs covered in registry with explicit status: `100%`.
- House methods `1..5` present in registry and validated by tests: `100%`.
- Context call-order test passes with deterministic `set_ephe_path -> set_sid_mode -> calc_ut/houses_ex -> reset sid mode`.
- SwissEph offender scan reports `0` uses of `swe.set_*` outside `kerykeion/vedic/context.py`.
- D0 test set pass condition: `3/3` test files green.
