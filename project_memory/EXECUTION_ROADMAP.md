# Diba Execution Roadmap (Priority-Driven)

Last updated: 2026-02-13

This roadmap is aligned with active project policies and architecture constraints:
- PyJHora-first research is mandatory before every capability implementation.
- Docstring policy is enforced in CI via Ruff (`pydocstyle`, `google`).
- SwissEph containment remains strict (session/adapter boundary only).
- Engine/State orchestration is the canonical execution path.

## 1) Priority Ranking (P0/P1/P2)

### P0: Reliable JSON Core Outputs

Scope:
- astronomy base correctness
- D1 chart stability
- serializer contract stability

Why P0:
- All downstream capability work depends on stable core primitives.
- Early JSON contract stability prevents repeated breaking changes.
- This layer is the highest blast-radius surface for integration consumers.

### P1: Highest Downstream Dependency Capabilities

Scope:
- Panchanga baseline (tithi/nakshatra/vara/yoga/karana minimal stable slice)
- Vimshottari baseline timeline

Why P1:
- Panchanga and Vimshottari are heavily consumed by UI, reports, and interpretation layers.
- Both reuse P0 primitives and unlock many P2 capabilities.

### P2: Extended/Advanced Surfaces

Scope:
- transit ranges and windowing
- compatibility expansions
- advanced yogas and analytics
- plugin evolution

Why P2:
- Valuable but not blocking for stable first production surface.
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

Mandatory PyJHora research artifacts (before code in each sub-scope):
- `project_memory/research/phase-a-astronomy-base-pyjhora-extract.md`
- `project_memory/research/phase-a-d1-chart-pyjhora-extract.md`
- `project_memory/research/phase-a-serializer-contract-pyjhora-extract.md`

Tests and tolerances:
- Boundary: longitudes near `0/30/.../360-eps`, index conversions `0<->1`.
- Regression/Golden: canonical subjects for D1 JSON shape.
- Tolerances:
  - angle: `1e-5` (golden), `1e-2` (ci profile)
  - time boundaries: `30s` (golden), `60s` (ci profile)

Exit criteria:
- Stable JSON subtree for base + D1 + serializer with documented schema.
- No SwissEph containment violations.
- `ruff check diba tests` and `pytest -q` green.

Risks and guardrails:
- Risk: serializer drift from core indexing policy.
  - Guardrail: explicit boundary tests + `api_v1` index serialization tests.
- Risk: direct ephemeris usage leak.
  - Guardrail: AST containment tests + banned import rule.

## Phase B (P1): Panchanga Baseline

Outcome:
- Stable Panchanga baseline API output for key daily elements.

Scope (modules/files):
- `diba/panchanga/service.py`
- `diba/panchanga/calculators/tithi.py`
- `diba/panchanga/calculators/nakshatra.py`
- `diba/panchanga/calculators/vara.py`
- `diba/panchanga/calculators/yoga.py`
- `diba/panchanga/calculators/karana.py`

Mandatory PyJHora research artifacts:
- `project_memory/research/phase-b-panchanga-baseline-pyjhora-extract.md`
- `project_memory/research/phase-b-tithi-boundaries-pyjhora-extract.md`

Tests and tolerances:
- Boundary: transitions at element boundaries (e.g. tithi change edges).
- Regression/Golden: curated date-time-location golden set.
- Tolerances:
  - event boundary: `<=60s` in ci, `<=30s` in golden
  - angular comparisons by profile

Exit criteria:
- Panchanga baseline fields available in stable JSON subtree.
- Golden set reproducibility under fixed env.
- No containment/docstring policy regressions.

Risks and guardrails:
- Risk: off-by-one or classification mismatch on boundaries.
  - Guardrail: explicit transition-window tests.
- Risk: accidental coupling to non-state path.
  - Guardrail: require `VedicState` input path in services.

## Phase C (P1): Vimshottari Baseline

Outcome:
- Stable baseline Vimshottari timeline output with documented assumptions.

Scope (modules/files):
- `diba/dasha/service.py`
- `diba/dasha/graha/vimsottari.py`
- `diba/domain/models/dasha.py`

Mandatory PyJHora research artifacts:
- `project_memory/research/phase-c-vimshottari-baseline-pyjhora-extract.md`
- `project_memory/research/phase-c-dasha-time-contract-pyjhora-extract.md`

Tests and tolerances:
- Boundary: period/sub-period boundaries and ordering.
- Regression/Golden: known baseline charts with expected timeline snippets.
- Tolerances:
  - boundary event timing per configured profile

Exit criteria:
- Dasha JSON subtree stable for baseline use.
- Golden timelines reproducible in pinned environment.
- CLI/API surface documented and versioned.

Risks and guardrails:
- Risk: timeline boundary drift due to time conversion.
  - Guardrail: UTC/JD contract tests and profile-based tolerance checks.

## Phase D (P2): Transit/Compatibility/Advanced Analytics

Outcome:
- Extended capability coverage with guarded rollout.

Scope (modules/files):
- `diba/transit/service.py`, `diba/transit/tajaka.py`, `diba/transit/saham.py`
- `diba/compatibility/service.py`, `diba/compatibility/ashtakoota.py`
- `diba/chart/analytics/*.py`
- plugin compatibility surfaces as needed

Mandatory PyJHora research artifacts:
- `project_memory/research/phase-d-transit-ranges-pyjhora-extract.md`
- `project_memory/research/phase-d-compatibility-pyjhora-extract.md`
- `project_memory/research/phase-d-advanced-yogas-pyjhora-extract.md`

Tests and tolerances:
- Boundary/event windows for transit ranges.
- Regression sets for compatibility score invariants.
- Golden cases for selected analytics outputs.

Exit criteria:
- P2 capabilities behind stable contracts with clear status flags.
- No breaking regressions on P0/P1 surfaces.

Risks and guardrails:
- Risk: combinatorial test explosion.
  - Guardrail: prioritized golden matrix + deterministic replay metadata.

## 3) Measurable Milestones

### Milestone M1 (end of Phase A)
- Golden coverage: 5 core cases.
- Throughput target: >=25 charts/sec (D1 baseline benchmark on one machine/profile).
- Stable endpoints/subtrees: 2 (`chart.d1`, `serializer.v1`).

### Milestone M2 (end of Phase B)
- Golden coverage: 25 mixed cases (core + panchanga baseline).
- Throughput target: >=18 charts/sec (core + panchanga baseline).
- Stable endpoints/subtrees: 3 (`chart.d1`, `serializer.v1`, `panchanga.baseline`).

### Milestone M3 (end of Phase C)
- Golden coverage: 60 cases (add vimshottari baseline).
- Throughput target: >=12 charts/sec (core + panchanga + dasha baseline).
- Stable endpoints/subtrees: 4 (`chart.d1`, `serializer.v1`, `panchanga.baseline`, `dasha.vimshottari`).

### Milestone M4 (end of Phase D)
- Golden coverage: 100 cases (all priority capabilities).
- Throughput target: >=10 charts/sec (expanded bundle).
- Stable endpoints/subtrees: >=6 including transit/compatibility slices.

## 4) JSON Output and Versioning Plan

## Capability subtree additions

### P0 additions
- `data.base`: core planets/houses/flags/time model from `VedicState`.
- `data.chart.d1`: normalized D1 chart payload.
- `data.serializer.v1`: boundary-safe serialized values (1-based public indexing).

### P1 additions
- `data.panchanga.baseline`: tithi/nakshatra/vara/yoga/karana minimal stable fields.
- `data.dasha.vimshottari`: baseline timeline entries with metadata.

### P2 additions
- `data.transit.ranges`
- `data.compatibility.ashtakoota`
- `data.analytics.*` (selected stable slices)

## schema_version bump rules

- `meta.schema_version` is mandatory in public payload root.
- Patch bump (`x.y.z` -> `x.y.z+1` equivalent policy):
  - internal non-breaking refactor
  - additive metadata fields not consumed as required
- Minor bump (`x.y` -> `x.(y+1)`):
  - additive optional JSON subtrees/fields
  - backward-compatible endpoint additions
- Major bump (`x` -> `x+1`):
  - removed or renamed field
  - changed field type/semantics
  - indexing contract change at public boundary

Breaking-change policy:
- Any major bump must include migration notes and explicit regression suite updates.

## 5) Next 7 Actions (Executable Order)

1. Create research artifact for Phase A astronomy base.
- File: `project_memory/research/phase-a-astronomy-base-pyjhora-extract.md`
- Verifiable output: committed research document with extracted formulas/contracts.

2. Create research artifact for Phase A D1 chart mapping.
- File: `project_memory/research/phase-a-d1-chart-pyjhora-extract.md`
- Verifiable output: committed research document with boundary/indexing notes.

3. Implement and lock `meta.schema_version` in P0 serializer output.
- Files: `diba/serializers/static_chart_v0_1.py`, `diba/serializers/api_v1.py`
- Verifiable output: regression test proving schema version presence and stability.

4. Add/expand P0 golden baseline set (5 cases).
- Files: `tests/...` golden suite + fixture assets
- Verifiable output: golden tests green in CI profile and deterministic replay metadata.

5. Create research artifact for Phase B Panchanga baseline.
- File: `project_memory/research/phase-b-panchanga-baseline-pyjhora-extract.md`
- Verifiable output: committed research + boundary map for transitions.

6. Implement Panchanga baseline subtree and boundary tests.
- Files: `diba/panchanga/service.py`, `diba/panchanga/calculators/*.py`, tests
- Verifiable output: stable `data.panchanga.baseline` subtree + boundary/regression tests green.

7. Create research artifact for Phase C Vimshottari baseline, then baseline implementation PR.
- Files:
  - `project_memory/research/phase-c-vimshottari-baseline-pyjhora-extract.md`
  - `diba/dasha/graha/vimsottari.py`, `diba/dasha/service.py`, tests
- Verifiable output: baseline timeline JSON subtree + golden regression slice.

## Non-Negotiable Constraints (Carried Through All Phases)

- No capability implementation before its research file exists.
- No mock/monkeypatch in tests.
- SwissEph usage only through existing session/adapter boundary.
- Docstring lint remains green under enforced policy.
