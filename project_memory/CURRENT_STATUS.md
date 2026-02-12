# Current Status

Last updated: 2026-02-13

## Snapshot

- Repo cleaned aggressively to Vedic-focused scope.
- Legacy/kerykeion-heavy folders removed: `docs/`, `examples/`, `release_notes/`, `scripts/`.
- Legacy files removed: `CHANGELOG.md`, `DEVELOPMENT.md`, `MIGRATION_V4_TO_V5.md`, `TODO.md`.
- SwissEph guardrails are in place (Ruff banned import + AST test).
- Test/lint baseline is green:
  - `ruff check diba tests` -> pass
  - `pytest -q` -> 68 passed

## Important Note

- Working tree is intentionally dirty right now because cleanup changes are not committed yet.

