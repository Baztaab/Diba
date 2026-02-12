# Next Steps

Last updated: 2026-02-13

1. Review deleted/kept files once more and confirm no extra removals are needed.
2. Commit cleanup in atomic commits (recommended split):
   - Commit A: repo cleanup/removals.
   - Commit B: config/readme realignment.
   - Commit C: varga fallback fix.
3. Add CI checks for architectural guardrails (if not already in pipeline job files):
   - serializer 1-based vs core 0-based contract test.
   - import boundary enforcement for `swisseph`.
4. Expand ADR set after ADR-001:
   - ADR-002: API boundary/indexing policy.
   - ADR-003: CI guardrails and enforcement policy.

