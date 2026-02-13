# Diba Execution Roadmap (Priority-Driven)

Last updated: 2026-02-13

This roadmap is aligned with project policies and architecture constraints:
- PyJHora-first research is mandatory before every capability implementation.
- Docstring policy is enforced in CI via Ruff (`pydocstyle`, `google`).
- SwissEph containment remains strict (session/adapter boundary only).
- Engine/State orchestration is the canonical execution path.

## Canonical Path Rules

1. Canonical research/artifact root is `D:\Diba\project_memory\...`.
2. Repo-relative mirror (`project_memory/...`) is maintained for review and CI traceability.
3. No capability implementation starts before its research artifact exists in canonical path.

## 1) Priority Ranking (P0/P1/P2)

### P0: Reliable JSON Core Outputs

Scope:
- astronomy base correctness
- D1 chart stability
- serializer contract stability
- meta contract completeness

Why P0:
- All downstream capability work depends on stable core primitives.
- Early JSON contract stability prevents repeated breaking changes.
- This layer has the highest blast-radius for integration consumers.

### P1: Highest Downstream Dependency Capabilities

Scope:
- Panchanga baseline (instantaneous mode)
- Vimshottari baseline timeline

Why P1:
- Panchanga and Vimshottari are high-demand surfaces for UI/report layers.
- Both directly depend on P0 contracts and unlock many P2 capabilities.

### P2: Extended/Advanced Surfaces

Scope:
- transit ranges and windowing
- compatibility expansions
- advanced yogas and analytics
- plugin evolution

Why P2:
- Valuable but not blocking for the first stable production surface.
- Higher combinatorial complexity and broader validation matrix.

## 2) Phase Plan

## Phase A (P0): Core JSON Reliability

Outcome:
- Stable, reproducible JSON for base astronomy + D1 + serializer path.

Scope (modules/files):
- `diba/engine/state.py`
- `diba/chart/service.py`
- `diba/serializers/static_chart_v0_1.py`
- `diba/serializers/api_v1.py`
- `diba/domain/models/common.py`

Mandatory PyJHora research artifacts (before code):
- `project_memory/research/phase-a-astronomy-base-pyjhora-extract.md`
- `project_memory/research/phase-a-d1-chart-pyjhora-extract.md`
- `project_memory/research/phase-a-serializer-contract-pyjhora-extract.md`

Tests and tolerances:
- Boundary: longitudes near `0/30/.../360-eps`, index conversions `0<->1`.
- Regression/Golden: canonical subjects for D1 JSON shape.
- Tolerances:
  - angle: `1e-5` (golden), `1e-2` (ci profile)
  - time boundaries: `30s` (golden), `60s` (ci profile)

Exit criteria (non-negotiable):
- Stable JSON subtree for base + D1 + serializer with documented schema.
- `meta.schema_version` is present and valid SemVer.
- Meta includes all required keys:
  - `engine_version`
  - `swisseph_version`
  - `config_digest`
  - `timezone_policy`
  - `ephe_expectations`
- No SwissEph containment violations.
- `ruff check diba tests` and `pytest -q` green.

Risks and guardrails:
- Risk: serializer drift from core indexing policy.
  - Guardrail: explicit boundary tests + `api_v1` index serialization tests.
- Risk: direct ephemeris usage leak.
  - Guardrail: AST containment tests + banned import rule.

## Phase B (P1): Panchanga Baseline (Instantaneous)

Outcome:
- Stable Panchanga baseline API output at a single input datetime (`instantaneous`).

Scope (modules/files):
- `diba/panchanga/service.py`
- `diba/panchanga/calculators/tithi.py`
- `diba/panchanga/calculators/nakshatra.py`
- `diba/panchanga/calculators/vara.py`
- `diba/panchanga/calculators/yoga.py`
- `diba/panchanga/calculators/karana.py`

Explicit mode lock:
- Phase B baseline is **instantaneous only**.
- Daily almanac (`sunrise/sunset`-anchored day windows) is deferred to Phase B2 / Phase D.
- Optional in Phase B: event window for tithi change only, tolerance-profile bounded.

Mandatory PyJHora research artifacts:
- `project_memory/research/phase-b-panchanga-baseline-pyjhora-extract.md`
- `project_memory/research/phase-b-tithi-boundaries-pyjhora-extract.md`

Tests and tolerances:
- Boundary: transitions at element boundaries (especially tithi change edges).
- Regression/Golden: curated datetime-location golden set.
- Tolerances:
  - event boundary: `<=60s` (ci), `<=30s` (golden)
  - angular comparisons by profile

Exit criteria:
- Panchanga baseline fields available in stable JSON subtree.
- Instantaneous mode explicitly documented in API contract.
- Golden set reproducibility under fixed env.
- No containment/docstring policy regressions.

Risks and guardrails:
- Risk: off-by-one classification mismatch on boundaries.
  - Guardrail: explicit transition-window tests.
- Risk: accidental coupling to non-state path.
  - Guardrail: require `VedicState` input path in services.

## Phase C (P1): Vimshottari Baseline

Outcome:
- Stable Vimshottari baseline timeline with explicit depth and JSON contract.

Scope (modules/files):
- `diba/dasha/service.py`
- `diba/dasha/graha/vimsottari.py`
- `diba/domain/models/dasha.py`

Baseline lock:
- Phase C baseline includes **Mahadasha + Antardasha**.
- Pratyantar and deeper levels are deferred to Phase C2 / P2.

Mandatory PyJHora research artifacts:
- `project_memory/research/phase-c-vimshottari-baseline-pyjhora-extract.md`
- `project_memory/research/phase-c-dasha-time-contract-pyjhora-extract.md`

Tests and tolerances:
- Boundary: period/sub-period boundaries and ordering.
- Regression/Golden: known baseline charts with expected timeline snippets.
- Tolerances: boundary timing per configured profile.

JSON shape baseline:
```json
"data": {
  "dasha": {
    "vimshottari": {
      "level": "mahadasha_antardasha",
      "entries": [
        {
          "mahadasha_lord": "...",
          "start_jd_ut": 0.0,
          "end_jd_ut": 0.0,
          "antardasha": [
            {"lord": "...", "start_jd_ut": 0.0, "end_jd_ut": 0.0}
          ]
        }
      ]
    }
  }
}
```

Exit criteria:
- Dasha JSON subtree stable for baseline use.
- Golden timelines reproducible in pinned environment.
- CLI/API surface documented and versioned.

Risks and guardrails:
- Risk: timeline boundary drift due to time conversion.
  - Guardrail: UTC/JD contract tests and profile-based tolerance checks.

## Phase D (P2): Extended Surfaces (Split to avoid scope explosion)

### Phase D1: Transit Windowing

Scope:
- `diba/transit/service.py`
- `diba/transit/tajaka.py`
- `diba/transit/saham.py`

Research artifact:
- `project_memory/research/phase-d1-transit-ranges-pyjhora-extract.md`

### Phase D2: Compatibility

Scope:
- `diba/compatibility/service.py`
- `diba/compatibility/ashtakoota.py`

Research artifact:
- `project_memory/research/phase-d2-compatibility-pyjhora-extract.md`

### Phase D3: Advanced Analytics and Plugins

Scope:
- `diba/chart/analytics/*.py`
- plugin compatibility surfaces

Research artifacts:
- `project_memory/research/phase-d3-advanced-yogas-pyjhora-extract.md`
- `project_memory/research/phase-d3-plugin-policy-pyjhora-extract.md`

Shared D-exit criteria:
- No breaking regressions on P0/P1 surfaces.
- Stable contracts with explicit status flags.

## 3) Measurable Milestones

## Benchmark harness definition (mandatory for throughput metrics)

Throughput numbers are valid only when measured with a fixed harness.

Harness target:
- Add benchmark entrypoint (`benchmarks/` suite or CLI command such as `diba bench d1 --n 1000`).

Benchmark protocol:
- machine/CPU model documented in benchmark output
- tolerance profile explicitly set (`ci` or `golden`)
- run mode stated: cold-cache vs warm-cache
- ephemeris I/O mode stated: included or excluded
- sample size reported (`n`), median and p95 latency reported

### Milestone M1 (end of Phase A)
- Golden coverage: 5 core cases.
- Throughput target: >=25 charts/sec on **warm-cache**, profile `ci`, benchmark harness protocol compliant.
- Stable endpoints/subtrees: 2 (`chart.d1`, `serializer.v1`).

### Milestone M2 (end of Phase B)
- Golden coverage: 25 mixed cases (core + panchanga baseline).
- Throughput target: >=18 charts/sec (same harness protocol).
- Stable endpoints/subtrees: 3 (`chart.d1`, `serializer.v1`, `panchanga.baseline`).

### Milestone M3 (end of Phase C)
- Golden coverage: 60 cases (add vimshottari baseline).
- Throughput target: >=12 charts/sec (same harness protocol).
- Stable endpoints/subtrees: 4 (`chart.d1`, `serializer.v1`, `panchanga.baseline`, `dasha.vimshottari`).

### Milestone M4 (end of Phase D)
- Golden coverage: 100 cases (all priority capabilities).
- Throughput target: >=10 charts/sec (same harness protocol).
- Stable endpoints/subtrees: >=6 including transit/compatibility slices.

## Golden matrix dimensions (for 5 -> 25 -> 60 -> 100 growth)

Mandatory dimensions:
- timezone class: UTC, fixed-offset local, DST-observing local
- DST edges: ambiguous/non-existent local times
- latitude bands: equatorial, mid-latitude, high-latitude near operational limit
- longitude spread: west/east hemispheres
- ayanamsa modes: minimum `lahiri`, `true_citra`, plus one additional implemented mode
- date spread: historical + modern + near-boundary seasonal samples

## 4) JSON Output and Versioning Plan

## Capability subtree additions

### P0 additions
- `data.base`: core planets/houses/flags/time model from `VedicState`.
- `data.chart.d1`: normalized D1 chart payload.
- `data.serializer.v1`: boundary-safe serialized values (1-based public indexing).

### P1 additions
- `data.panchanga.baseline`: instantaneous tithi/nakshatra/vara/yoga/karana stable fields.
- `data.dasha.vimshottari`: Mahadasha + Antardasha baseline timeline entries.

### P2 additions
- `data.transit.ranges`
- `data.compatibility.ashtakoota`
- `data.analytics.*` (selected stable slices)

## schema_version rules (strict SemVer)

- `meta.schema_version` is mandatory and formatted exactly as `MAJOR.MINOR.PATCH`.
- SemVer mapping:
  - PATCH: non-breaking fixes and additive metadata that do not change required contract
  - MINOR: additive backward-compatible fields/subtrees/endpoints
  - MAJOR: removed/renamed fields, semantic/type changes, indexing contract changes

Breaking-change policy:
- Any MAJOR bump requires migration notes and explicit regression suite updates.

## 5) Next 7 Actions (Executable Order)

1. Create research artifact for Phase A astronomy base.
- File: `project_memory/research/phase-a-astronomy-base-pyjhora-extract.md`
- Verifiable output: committed research document with extracted formulas/contracts.

2. Create research artifact for Phase A D1 chart mapping.
- File: `project_memory/research/phase-a-d1-chart-pyjhora-extract.md`
- Verifiable output: committed research document with boundary/indexing notes.

3. Create research artifact for Phase A serializer/meta contract.
- File: `project_memory/research/phase-a-serializer-contract-pyjhora-extract.md`
- Verifiable output: committed research doc including SemVer and required meta keys.

4. Implement benchmark harness spec (command + output schema), then add benchmark smoke.
- Files: `benchmarks/...` or CLI bench command files + tests
- Verifiable output: reproducible benchmark run log with machine/profile/cache/io annotations.

5. Implement and lock `meta.schema_version` + required meta keys in P0 output.
- Files: `diba/serializers/static_chart_v0_1.py`, `diba/serializers/api_v1.py`, tests
- Verifiable output: regression tests proving schema version and required meta key presence.

6. Create research artifact for Phase B Panchanga instantaneous baseline.
- File: `project_memory/research/phase-b-panchanga-baseline-pyjhora-extract.md`
- Verifiable output: committed research + explicit instantaneous scope + boundary map.

7. Create research artifact for Phase C Vimshottari baseline depth, then implement baseline.
- Files:
  - `project_memory/research/phase-c-vimshottari-baseline-pyjhora-extract.md`
  - `diba/dasha/graha/vimsottari.py`, `diba/dasha/service.py`, tests
- Verifiable output: baseline Mahadasha+Antardasha JSON subtree + golden regression slice.

## Non-Negotiable Constraints (Carried Through All Phases)

- No capability implementation before its research file exists.
- No mock/monkeypatch in tests.
- SwissEph usage only through existing session/adapter boundary.
- Docstring lint remains green under enforced policy.
