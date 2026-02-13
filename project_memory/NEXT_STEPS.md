# Next Steps

Last updated: 2026-02-13

## Completed in this iteration

1. Enforced docstring checks in Ruff using `pydocstyle` with `google` convention.
2. Added thread isolation test for engine session context:
- `tests/test_engine_thread_session_isolation.py`
3. Kept SwissEph containment allowlist unchanged.

## Near-term backlog

1. Gradually remove temporary `D` per-file ignores from older modules (`diba/vedic`, `diba/schemas`, `diba/settings`, utility modules) after incremental docstring migration.
2. Replace placeholder metadata (`swisseph_version`, `config_digest`) with deterministic runtime values.
3. Extend `ChartAnalysis` orchestration flow in API facades.

## Exit Criteria Status

1. Docstring policy enforce in CI: complete.
2. Concurrency session leak test added: complete.
3. Lint/tests green: complete.
