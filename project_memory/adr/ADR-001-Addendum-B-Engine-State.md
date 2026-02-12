# ADR-001 Addendum-B: Engine and Shared VedicState

- Status: Accepted
- Date: 2026-02-13
- Parent: ADR-001 Core Foundations

## Context

Phase-1 modular foundation is in place and guardrails exist for SwissEph usage. To keep data flow deterministic and avoid orchestration sprawl across capability modules, we need one explicit execution path for shared astronomical primitives.

## Decision

1. Introduce a shared `VedicState` (or `SkyContext`) as the canonical data bag for:
- base positions
- house outputs
- runtime flags
- request context metadata

2. `VedicState` includes runtime cache slots for repeated reads during one request or batch unit.
- Cache is request-scoped.
- Cache keys include policy inputs that affect results.

3. Introduce `DibaEngine` as context-aware orchestrator:
- if a SwissEph session is already active, reuse it.
- if no active session exists, create a short session for a single call.
- for high-throughput batches, expose context-manager usage such as `with engine.session():` to keep one session open across many computations.

4. Module boundary rule:
- `diba.chart`, `diba.dasha`, `diba.panchanga`, `diba.transit`, `diba.compatibility` must consume computed data via `DibaEngine` and `VedicState`.
- Those modules must not call ephemeris primitives or `swisseph` directly.

## Consequences

- Reduced repeated SwissEph work in chained capability calls.
- Predictable orchestration path and lower coupling between capability modules and infra code.
- Easier enforcement in CI with import/setter containment tests and future engine-path checks.

## Implementation Notes

- Keep current Phase-1 facades.
- Add engine/state wiring in Phase-2 and route service modules to consume shared state outputs.
- Keep serializer boundary policy unchanged: core remains zero-based, public payload remains one-based where required.
