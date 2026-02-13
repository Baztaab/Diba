# Runtime Contracts (Schema, Tolerance, Benchmark, Session Ownership)

Last updated: 2026-02-13

## 1) Session Ownership (Single Source of Truth)

- Owner of session lifecycle is `DibaEngine`.
- `VedicCalculationContext` is calculation runtime and may manage its own session only for backward-compatible direct usage.
- Engine path must call context with `manage_session=False` under an active engine session.
- Session lifecycle rules govern SwissEph global state calls only through existing session boundary modules.

Enforcement:
- `tests/test_session_ownership_contract.py`
- `tests/test_engine_thread_session_isolation.py`

## 2) schema_version vs serializer versions

- `meta.schema_version` is the canonical consumer-facing version and must follow strict SemVer (`MAJOR.MINOR.PATCH`).
- Serializer module names (`api_v1`, `static_chart_v0_1`) are implementation channels and are not the authoritative schema version by themselves.
- Mapping rule:
  - serializer channel declares supported schema major(s)
  - payload must carry explicit `meta.schema_version`

Breaking policy:
- MAJOR bump for any breaking schema change.
- MINOR for additive non-breaking fields/subtrees.
- PATCH for non-breaking fixes and non-required metadata additions.

## 3) Tolerance profile selection mechanism

- Mechanism: environment variable `DIBA_TOL_PROFILE`.
- Values:
  - `ci` => looser tolerances for platform variability
  - `golden` => strict tolerances for pinned deterministic runs
- Implementation source: `diba/core/contracts.py`.

## 4) Benchmark governance

- Benchmarks are valid only via defined harness (`benchmarks/` suite or dedicated CLI bench command).
- Output must include:
  - machine/CPU identifier
  - tolerance profile
  - cold/warm cache flag
  - ephemeris I/O mode (included/excluded)
  - sample size, median, p95

Execution policy:
- CI runs benchmark smoke only (non-blocking performance signal).
- Full throughput acceptance runs are local/release-gate with declared environment and threshold.

## 5) Research artifact gate

- Any capability implementation requires research artifact existence in `project_memory/research/`.
- CI enforces mandatory artifact presence and minimum document sections.

Enforcement:
- `tests/test_policy_research_gate.py`

## 6) Ephemeris policy precedence and re-init scope

- Ephemeris asset/runtime policy precedence is:
  - `DIBA_EPHE_PATH` (environment override)
  - configured path in runtime settings
  - packaged ephemeris path
  - validated fallback/default policy
- Re-init conflict applies to ephemeris policy/path/expectations changes inside the same process.
- Re-init conflict does not redefine SwissEph session flag lifecycle; sidereal/topo/path state calls remain session-bound by containment rules.

Enforcement:
- `tests/test_ephemeris_runtime_contract.py`

## 7) Ayanamsa resolver and fallback policy

- Resolver contract:
  - `resolve_ayanamsa(mode, on_unsupported, default_id) -> (spec, report)`
  - resolver does not log
  - structured `report` carries:
    - `reason_code` (`none|invalid|disabled|recognized_not_implemented`)
    - `input_id`
    - `effective_id`
    - `was_fallback`
- Fallback behavior:
  - `on_unsupported="raise"`: fail-fast for invalid/disabled/recognized-not-implemented
  - `on_unsupported="fallback_default"`: fallback for all three reason classes
  - if `default_id` cannot resolve, resolver must raise (internal misconfiguration)
- Logging scope:
  - fallback warnings are allowed only at entrypoints (`build_vedic_state` and CLI parse path)
  - no downstream logging in registry resolver

## 8) Ayanamsa canonicalization and listing

- Canonicalization rule is fixed:
  - `strip` + `casefold` + replace `-`/space with `_`
- Alias acceptance is supported at input edges, but canonical IDs are emitted in runtime.
- Deterministic listing:
  - `list_ayanamsa_ids(selectable_only=True, include_aliases=False)` returns sorted canonical selectable IDs only.
  - aliases are exposed only when `include_aliases=True`.

## 9) Single-resolve rule

- Runtime ayanamsa resolution is performed only at entrypoints:
  - `build_vedic_state` (engine canonical path)
  - CLI parse path
- Downstream runtime layers must carry `AyanamsaSpec` and must not call `resolve_ayanamsa` again.
