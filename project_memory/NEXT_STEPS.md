# Next Steps

Last updated: 2026-02-13

## Completed in this iteration

1. Enforced ephemeris runtime contract (Action-1):
- deterministic precedence + fail-fast + runtime re-init conflict + expectations validation.
- tests: `tests/test_ephemeris_runtime_contract.py`
2. Wired ephemeris runtime initialization into canonical engine orchestration path:
- `diba/engine/state.py` now calls `initialize_ephemeris_runtime(...)` before compute path.
- tests: `tests/test_engine_ephemeris_wiring.py`
3. Implemented Action-2 benchmark harness:
- command: `diba bench state-base --n <N>`
- tests: `tests/test_cli_bench.py`
4. Maintained SwissEph containment allowlist unchanged.
5. CI remains green after wiring + Action-2: `ruff` + `pytest`.

## Near-term backlog

1. Lock P0 meta contract in serializer/API path.
- Ensure `meta.schema_version` and required reproducibility fields are asserted in tests.
2. Extend benchmark surface from `state-base` to `d1` once D1 output path is fully stabilized for throughput tracking.
3. Gradually remove temporary `D` per-file ignores from older modules after incremental docstring migration.

## Exit Criteria Status

1. Ephemeris runtime contract implementation + tests: complete.
2. Runtime wiring in canonical orchestration path: complete.
3. Benchmark harness baseline (`state-base`) implementation: complete.
4. SwissEph containment integrity after wiring and bench changes: complete.
5. Lint/tests green after latest changes: complete.
