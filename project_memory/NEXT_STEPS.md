# Next Steps

Last updated: 2026-02-13

## Pre-commit hardening items for Phase-1

1. Add ADR Addendum-B for Engine + VedicState and store it in docs + project memory.
2. Upgrade SwissEph guardrail tests to block bypass paths:
- alias import
- from-import
- `importlib.import_module("swisseph")`
- `__import__("swisseph")`
- enforce `set_*` usage only in `diba/infra/swisseph/session.py`

## After Phase-1 commit (Phase-2)

1. Implement `DibaEngine` and `VedicState` in code.
2. Wire `chart/dasha/panchanga/transit/compatibility` services to consume shared state outputs.
3. Keep compute path centralized through engine/session boundaries for high-throughput batch flows.
