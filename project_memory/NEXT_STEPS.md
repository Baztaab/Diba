# Next Steps

Last updated: 2026-02-13

## Phase-2 Execution Plan

1. Implement concrete `DibaEngine` API with explicit session lifecycle options:
- `compute_once(...)` with internal short session
- `with engine.session():` for batch throughput
- state reuse when session is already active

2. Implement `VedicState` as canonical shared output container:
- positions
- houses
- flags
- context metadata
- request-scoped cache keys bound to runtime policy

3. Wire capability services to consume shared engine/state outputs:
- `diba/chart/service.py`
- `diba/dasha/service.py`
- `diba/panchanga/service.py`
- `diba/transit/service.py`
- `diba/compatibility/service.py`

4. Add focused acceptance tests for engine/state wiring:
- repeated capability calls reuse cached primitives
- no direct ephemeris path in capability modules
- deterministic meta digest propagation through service outputs
