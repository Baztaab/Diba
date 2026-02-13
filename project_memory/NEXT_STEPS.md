# Next Steps

Last updated: 2026-02-13

## Completed in this iteration

1. Enforced ephemeris runtime contract (Action-1):
- deterministic precedence + fail-fast + runtime re-init conflict + expectations validation.
- tests: `tests/test_ephemeris_runtime_contract.py`
2. Maintained SwissEph containment allowlist unchanged.
3. CI remains green after Action-1: `ruff` + `pytest`.

## Near-term backlog

1. Wire ephemeris runtime init into Engine entry path.
- Target: call `initialize_ephemeris_runtime(...)` from canonical orchestration path (`diba/engine/state.py`) with deterministic `config_digest` and expectations source.
- Why first: current contract is implemented but not yet enforced in end-to-end runtime path.
2. Action-2 benchmark harness implementation.
- Add `diba bench d1 --n 1000` (or equivalent) with machine-readable output fields required by `RUNTIME_CONTRACTS`.
- Add smoke test and CI non-blocking benchmark signal.
3. Lock P0 meta contract in serializer/API path.
- Ensure `meta.schema_version` and required reproducibility fields are asserted in tests.
4. Gradually remove temporary `D` per-file ignores from older modules after incremental docstring migration.

## Exit Criteria Status

1. Ephemeris runtime contract implementation + tests: complete.
2. SwissEph containment integrity after Action-1: complete.
3. Lint/tests green after Action-1: complete.
4. Runtime wiring of ephemeris init in orchestration path: pending.
