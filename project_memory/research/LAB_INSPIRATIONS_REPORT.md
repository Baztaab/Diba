# Lab Inspirations Report (D:\lab)
Date: 2026-02-13

## Executive Summary
- [High] Adopt a strict ephemeris asset/runtime initialization contract like Phoenix Engine: deterministic path precedence, fail-fast, and re-init conflict detection scoped to ephemeris policy/path/expectations (not SwissEph session flag lifecycle) (`D:\lab\phoenix_engine\core\ephemeris_manager.py`).
- [High] Add benchmark protocol that is machine-readable and CI-visible, following Astropy + Hifitime patterns (`D:\lab\astropy\.github\workflows\ci_benchmark.yml`, `D:\lab\hifitime\.github\workflows\benchmarks.yml`).
- [High] Expand golden and boundary tests for time/sky edges using the style seen in PyEphem and Kosmorro (`D:\lab\pyephem\ephem\tests\test_rise_set.py`, `D:\lab\kosmorro\tests\output.py`).
- [High] Keep output contracts explicit and strongly typed at API boundary (Pydantic-style request/response models) as in vedicpanchanga backend (`D:\lab\vedicpanchanga.com\backend\api.py`).
- [High] Keep capability modules vertically split and immutable data-first like Stellium and Jyotishganit (`D:\lab\stellium\docs\ARCHITECTURE.md`, `D:\lab\jyotishganit\tests\test_birth_charts.py`).
- [Med] Add external-reference verification docs with reproducible URLs for manual sanity checks (Panchang verification docs) (`D:\lab\panchang\VERIFICATION_GUIDE.md`).
- [Med] Add compatibility-shim tests for API migration windows (Kerykeion style) (`D:\lab\kerykeion\tests\test_backward_compatibility.py`).
- [Med] Add deterministic timezone and DST contract tests modeled after Kosmorro and vedicpanchanga (`D:\lab\kosmorro\tests\timezone.py`, `D:\lab\vedicpanchanga.com\tests\test_timezones.py`).
- [Low] Add precomputed caches for heavy repeated ranges (Morinus and panchangam-2 style), behind explicit cache policy (`D:\lab\morinus-console\ephemcalc.py`, `D:\lab\panchangam-2\precomputed`).
- [Low] Add optional SDK/CLI wrappers that are contract-first and discoverable (Panchang CLI + VedAstro wrapper patterns) (`D:\lab\panchang\src\cli.js`, `D:\lab\VedAstro.Python\vedastro\calculate.py`).

## Per-Project Findings
### astro-sweph
- Strong Patterns:
  - Single deployable artifact bundling computation engine + ephemeris payload for offline usage.
  - Explicit memory lifecycle controls (`preload`, `destroy`, cleanup) exposed to consumers.
- Files/Refs:
  - `D:\lab\astro-sweph\README.md`
  - `D:\lab\astro-sweph\js\calculate.js`
  - `D:\lab\astro-sweph\lib\src\astro.c`
- How to adopt in Diba:
  - Add an optional `diba/infra/io/ephemeris_manifest.py` that records bundled assets and checksum list.
  - Add an optional prewarm API in CLI (`diba/_cli/commands/bench.py`) to measure cold vs warm runs.
- Risks/Tradeoffs:
  - Larger distribution artifacts and stricter release process for ephemeris updates.

### Astrolog
- Strong Patterns:
  - Preserved upstream snapshot with minimal wrapper metadata for traceable provenance.
- Files/Refs:
  - `D:\lab\Astrolog\README.md`
  - `D:\lab\Astrolog\Makefile`
- How to adopt in Diba:
  - Keep a `docs/research/reference_sources.md` table linking each external baseline and exact version/date used for validation.
- Risks/Tradeoffs:
  - Extra maintenance overhead for provenance docs.

### astropy
- Strong Patterns:
  - Benchmark workflow executed on demand via PR label to control CI cost.
  - Automated dependency pin refresh through scheduled workflow + bot PR.
  - Schema version tests with explicit expected compatibility outcomes.
- Files/Refs:
  - `D:\lab\astropy\.github\workflows\ci_benchmark.yml`
  - `D:\lab\astropy\.github\workflows\update_astropy_iers_data_pin.yml`
  - `D:\lab\astropy\astropy\io\votable\tests\test_schema_versions.py`
- How to adopt in Diba:
  - Add a workflow `benchmark-on-label` for `diba bench d1 --n 1000`.
  - Add scheduled workflow to refresh ephemeris expectations metadata, creating PRs.
  - Add explicit schema compatibility tests around `meta.schema_version` transitions.
- Risks/Tradeoffs:
  - More CI configuration complexity; needs maintainers to review automation PRs.

### celerity
- Strong Patterns:
  - Type-safe API that avoids implicit string parsing for critical numerical inputs.
  - Tight lint/type/test stack in `pyproject` + `mypy` + `ruff`.
- Files/Refs:
  - `D:\lab\celerity\README.md`
  - `D:\lab\celerity\pyproject.toml`
- How to adopt in Diba:
  - Keep strict typed input models for public API (`diba/domain/models/common.py`) and avoid permissive ad-hoc parsing in core modules.
- Risks/Tradeoffs:
  - Slightly higher friction for API users; mitigated by serializer helpers.

### drik-panchanga
- Strong Patterns:
  - Clear computational decomposition of tithi/nakshatra/yoga with interpolation and skipped-event handling.
  - Sunrise-anchored Panchanga logic documented in implementation.
- Files/Refs:
  - `D:\lab\drik-panchanga\panchanga.py`
- How to adopt in Diba:
  - Mirror this decomposition in `diba/panchanga/calculators/*` with explicit boundary tests for skipped transitions.
- Risks/Tradeoffs:
  - Direct porting is unsafe if indexing/contracts are not normalized to Diba ADR rules.

### financial-astrology-machine-learning
- Strong Patterns:
  - Explicit model benchmarking scripts and persisted performance ledger CSVs.
  - Scripted experiment variants with reproducible naming.
- Files/Refs:
  - `D:\lab\financial-astrology-machine-learning\modelsBenchmark.R`
  - `D:\lab\financial-astrology-machine-learning\models-predict-retrain-performance.csv`
- How to adopt in Diba:
  - Keep benchmark outputs as append-only artifacts in `project_memory/research/benchmarks/` for trend tracking across phases.
- Risks/Tradeoffs:
  - Benchmark artifacts can become noisy without strict run protocol.

### financial-astrology-stats
- Strong Patterns:
  - No analyzable source files at top-level clone (git metadata only).
- Files/Refs:
  - `D:\lab\financial-astrology-stats`
- How to adopt in Diba:
  - None from this root.
- Risks/Tradeoffs:
  - N/A.

### hifitime
- Strong Patterns:
  - Dedicated benchmark workflows with parsed summaries in CI.
  - Feature-matrix testing (default/no-default/feature variants, multi-platform).
  - Formal verification workflow (Kani) on schedule.
- Files/Refs:
  - `D:\lab\hifitime\.github\workflows\benchmarks.yml`
  - `D:\lab\hifitime\.github\workflows\tests.yml`
  - `D:\lab\hifitime\.github\workflows\weekly-kani-checker.yaml`
- How to adopt in Diba:
  - Keep separate quick CI vs deep verification jobs.
  - Add benchmark parser producing machine-readable summary in CI artifacts.
- Risks/Tradeoffs:
  - More CI runtime and maintenance burden.

### Hindu-Panchangam
- Strong Patterns:
  - Validation script comparing computed output against an external authority source.
  - Explicit post-fix validation report documenting issue, root cause, and measured result.
- Files/Refs:
  - `D:\lab\Hindu-Panchangam\src\scripts\validate-comparison.ts`
  - `D:\lab\Hindu-Panchangam\VALIDATION_REPORT.md`
- How to adopt in Diba:
  - Keep `docs/research/verification_reports/` per capability with root-cause + fix + metric.
- Risks/Tradeoffs:
  - External site scraping can be brittle; keep as optional/manual verification.

### immanuel-python
- Strong Patterns:
  - Rich fixture-based tests anchored to known references with tolerances.
  - Config object reset and cache clear between tests for isolation.
  - Serializer-focused output shape tests.
- Files/Refs:
  - `D:\lab\immanuel-python\tests\test_ephemeris.py`
  - `D:\lab\immanuel-python\tests\test_setup.py`
  - `D:\lab\immanuel-python\README.md`
- How to adopt in Diba:
  - Add deterministic fixture packs and explicit cache reset utilities for test runs in `tests/conftest.py`.
- Risks/Tradeoffs:
  - Requires disciplined fixture lifecycle management.

### jyotishganit
- Strong Patterns:
  - Capability-wide tests across geography/timezone/extreme latitude dimensions.
  - JSON-LD output path with stable structure checks.
  - Dasha tests with structural invariants and timeline consistency checks.
- Files/Refs:
  - `D:\lab\jyotishganit\tests\test_birth_charts.py`
  - `D:\lab\jyotishganit\tests\test_dashas.py`
  - `D:\lab\jyotishganit\jyotishganit\output\jsonld_formatter.py`
- How to adopt in Diba:
  - Expand Diba golden matrix dimensions exactly as roadmap says, plus explicit structural asserts for output subtree contracts.
- Risks/Tradeoffs:
  - Test matrix growth can slow CI unless tiered.

### kerykeion
- Strong Patterns:
  - Factory-centered public API and explicit migration tests for compatibility layers.
  - Context manager around ephemeris configuration and cleanup.
  - High-coverage complete tests per feature module.
- Files/Refs:
  - `D:\lab\kerykeion\kerykeion\astrological_subject_factory.py`
  - `D:\lab\kerykeion\tests\test_backward_compatibility.py`
  - `D:\lab\kerykeion\tests\test_transits_time_range_factory_complete.py`
- How to adopt in Diba:
  - Keep facade-first API imports (`diba/api/*`) and test deprecation windows for future renames.
  - Keep cleanup-oriented session boundary in Diba session layer only.
- Risks/Tradeoffs:
  - Compatibility shims add temporary complexity; require sunset plan.

### kosmorro
- Strong Patterns:
  - Exact CLI golden output tests for JSON/text/latex.
  - Robust timezone precedence tests for CLI arg vs environment variable.
- Files/Refs:
  - `D:\lab\kosmorro\tests\output.py`
  - `D:\lab\kosmorro\tests\timezone.py`
  - `D:\lab\kosmorro\tests\events.py`
- How to adopt in Diba:
  - Start with golden output tests for Diba JSON subtrees only (`meta.*`, `data.base`, `data.chart.d1`); defer text-format goldens to a later hardening pass.
  - Add precedence contract tests for timezone configuration path.
- Risks/Tradeoffs:
  - Golden text fixtures need controlled formatting stability.

### morinus-console
- Strong Patterns:
  - Domain-split modules (houses, doshas, aspects, etc.) and command-line extraction scripts.
  - Precomputed daily planetary arrays for yearly runs to improve speed.
- Files/Refs:
  - `D:\lab\morinus-console\ephemcalc.py`
  - `D:\lab\morinus-console\console\chart_dump.py`
- How to adopt in Diba:
  - Add optional precomputed cache for repetitive daily scans in `diba/transit` and `diba/panchanga/events` paths.
- Risks/Tradeoffs:
  - Cache invalidation and memory usage need explicit policy.

### New folder
- Strong Patterns:
  - `pyhora2`: explicit package capability map and broad module split useful as coverage checklist.
  - `financial-astrology-stats`: pipeline script that codifies data preparation order.
  - `immanuel-js`: separation of rendering tracks/boundaries from computation data.
  - `jyotishyamitra`: explicit API invocation sequence with validation gates.
- Files/Refs:
  - `D:\lab\New folder\pyhora2\README_Package_Structure.md`
  - `D:\lab\New folder\financial-astrology-stats\dataPipelineRun.R`
  - `D:\lab\New folder\immanuel-js\README.md`
  - `D:\lab\New folder\jyotishyamitra\README.md`
- How to adopt in Diba:
  - Keep capability inventory checklist in roadmap and enforce sequence gates in CI (already aligned with research gate).
- Risks/Tradeoffs:
  - Mixed-quality sandbox folder; copy only specific patterns, not full architecture.

### NodaTime_console
- Strong Patterns:
  - Clear separation of instant/offset/zoned/local time types and JSON serialization examples.
- Files/Refs:
  - `D:\lab\NodaTime_console\NodaTime_console\Program.cs`
- How to adopt in Diba:
  - Keep explicit time model boundaries in `diba/core/time.py` and serializer-level timezone formatting tests.
- Risks/Tradeoffs:
  - More type surfaces to maintain.

### openastro2
- Strong Patterns:
  - Rich configuration schema documentation for house systems, zodiac, perspective, and UI options.
  - Snapshot sanitization helper to stabilize regression outputs.
- Files/Refs:
  - `D:\lab\openastro2\docs\configuration.md`
  - `D:\lab\openastro2\openastro2\openastro2.py`
- How to adopt in Diba:
  - Keep a machine-readable runtime options registry and snapshot sanitizers for deterministic tests.
- Risks/Tradeoffs:
  - Option surface can grow quickly; requires strict ownership.

### panchang
- Strong Patterns:
  - Transition finder with bounded search and precision control.
  - Verification guide + verification results as first-class docs.
  - CLI with predefined locations and explicit timezone formatting options.
- Files/Refs:
  - `D:\lab\panchang\src\panchanga\transitions.ts`
  - `D:\lab\panchang\VERIFICATION_GUIDE.md`
  - `D:\lab\panchang\VERIFICATION_RESULTS.md`
  - `D:\lab\panchang\src\cli.js`
- How to adopt in Diba:
  - Implement bounded transition search utilities in `diba/panchanga/events.py` with profile-based tolerances.
  - Keep verification docs adjacent to capability code.
- Risks/Tradeoffs:
  - External-verification metrics can drift as data sources update.

### panchangam-2
- Strong Patterns:
  - Multi-channel outputs (PDF, ICS, monthly/daily) from a shared computation base.
  - Precomputed data directory for repeatable calendar generation.
- Files/Refs:
  - `D:\lab\panchangam-2\README.md`
  - `D:\lab\panchangam-2\precomputed`
- How to adopt in Diba:
  - Add export adapters (`serializers/` + CLI commands) that reuse core results rather than recompute.
- Risks/Tradeoffs:
  - Output channels can expand maintenance scope quickly.

### phoenix_engine
- Strong Patterns:
  - Strong ephemeris loader contract: precedence, validation, one-time init, and conflict error on re-init for asset/runtime policy changes.
  - Bootstrap context object used as a single initialization entrypoint.
  - Deterministic tests for precedence and error semantics.
- Files/Refs:
  - `D:\lab\phoenix_engine\core\ephemeris_manager.py`
  - `D:\lab\phoenix_engine\core\bootstrap.py`
  - `D:\lab\phoenix_engine\tests\test_ephemeris_loader.py`
- How to adopt in Diba:
  - Reuse this strict policy style in Diba ephemeris/runtime contracts for asset policy only; keep SwissEph state/session lifecycle strictly in existing session boundary.
- Risks/Tradeoffs:
  - Requires strict startup discipline and clear operational docs.

### pyephem
- Strong Patterns:
  - Rich edge-case regression tests (never-up/always-up, NaN input, infinite-loop prevention).
  - Validation against external authority datasets with explicit tolerance checks.
  - Cross-platform wheel build + test pipeline.
- Files/Refs:
  - `D:\lab\pyephem\ephem\tests\test_rise_set.py`
  - `D:\lab\pyephem\ephem\tests\test_usno.py`
  - `D:\lab\pyephem\.github\workflows\build-and-test.yml`
- How to adopt in Diba:
  - Add edge-case suites for rise/set, DST, and polar latitudes in `tests/panchanga/`, using semantic assertions resilient to tzdata version drift.
- Risks/Tradeoffs:
  - Large reference fixture datasets can be heavy in repo.

### Pyjhora
- Strong Patterns:
  - Very broad capability catalog useful as parity checklist.
  - Large test claim and explicit ayanamsa assumption note.
  - Detailed package structure that maps capability families.
- Files/Refs:
  - `D:\lab\Pyjhora\README.md`
  - `D:\lab\Pyjhora\src\jhora\horoscope\README.md`
- How to adopt in Diba:
  - Use as capability inventory source for phased parity targets only; keep Diba contracts and containment as-is.
- Risks/Tradeoffs:
  - Direct implementation style is monolithic; selective extraction is required.

### python-skyfield
- Strong Patterns:
  - High-quality docs on accuracy, time scales, and performance behavior.
  - Precision-focused tests with strict numerical thresholds.
  - Clear operational guidance for thread-related BLAS settings.
- Files/Refs:
  - `D:\lab\python-skyfield\documentation\accuracy-efficiency.rst`
  - `D:\lab\python-skyfield\skyfield\tests\test_topos.py`
- How to adopt in Diba:
  - Add operations notes for numeric-thread environment variables in benchmark profile docs, with deterministic benchmark profile declaration.
  - Add stricter numerical threshold tests for selected geometry paths.
- Risks/Tradeoffs:
  - Very strict tolerances can increase platform-specific flakiness if not tiered.

### scripts
- Strong Patterns:
  - Simple default test entrypoint script with optional coverage path.
- Files/Refs:
  - `D:\lab\scripts\run_tests.ps1`
- How to adopt in Diba:
  - Keep one standard script entry for local developer validation mirroring CI commands.
- Risks/Tradeoffs:
  - Minimal; mostly DX improvement.

### stellium
- Strong Patterns:
  - Protocol-driven architecture + immutable models + capability layering documented clearly.
  - Built-in benchmark script with charts/sec assertion.
  - Strict lint/type/test configuration in pyproject.
- Files/Refs:
  - `D:\lab\stellium\docs\ARCHITECTURE.md`
  - `D:\lab\stellium\tests\benchmark_performance.py`
  - `D:\lab\stellium\pyproject.toml`
- How to adopt in Diba:
  - Preserve capability-first module boundaries and immutable domain models in Diba.
  - Add benchmark assertions with explicit limits for core scenarios.
- Risks/Tradeoffs:
  - Strong abstraction may increase initial implementation overhead.

### VedAstro
- Strong Patterns:
  - No analyzable source files at this root clone.
- Files/Refs:
  - `D:\lab\VedAstro`
- How to adopt in Diba:
  - None from this root.
- Risks/Tradeoffs:
  - N/A.

### VedAstro.Python
- Strong Patterns:
  - Auto-generated Python client surface for a large API, indicating contract-driven SDK generation.
  - Demo-first onboarding with many narrow examples.
- Files/Refs:
  - `D:\lab\VedAstro.Python\vedastro\calculate.py`
  - `D:\lab\VedAstro.Python\README.md`
- How to adopt in Diba:
  - For future remote APIs, generate clients from a contract spec rather than hand-writing repetitive wrappers.
- Risks/Tradeoffs:
  - Generated clients can hide weak server contracts unless schema is strict.

### vedicpanchanga.com
- Strong Patterns:
  - Clear backend/frontend split with typed request/response contracts.
  - Strong test tooling for API behavior, timezone validation, and stress/rate-limit checks.
  - Practical operations docs and API docs side by side.
- Files/Refs:
  - `D:\lab\vedicpanchanga.com\backend\api.py`
  - `D:\lab\vedicpanchanga.com\tests\test_api.py`
  - `D:\lab\vedicpanchanga.com\tests\test_timezones.py`
  - `D:\lab\vedicpanchanga.com\README.md`
- How to adopt in Diba:
  - Keep typed IO contracts in API layer and dedicated timezone + load tests before exposing new endpoints.
- Risks/Tradeoffs:
  - Broader test scope increases CI runtime unless tiered into fast/slow lanes.

## Cross-cutting Patterns
- Testing patterns (golden/boundary/property-based):
  - Golden JSON subtree contracts for API/serializer; add textual report goldens only when output formatting is explicitly frozen.
  - Boundary/edge behavior for astronomical edge cases (`pyephem/ephem/tests/test_rise_set.py`).
  - Capability matrix tests for timezone/latitude/date spread (`jyotishganit/tests/test_birth_charts.py`).
- Indexing conventions and adapters:
  - Keep explicit numeric index contracts in API docs/tests; pair index with human-readable name in outputs (`panchang` and `vedicpanchanga.com` structures).
  - Diba should continue internal 0-based and boundary-only 1-based serialization.
- Ephemeris asset management:
  - Deterministic path precedence + explicit fallback rules (`phoenix_engine/core/ephemeris_manager.py`).
  - Bundle/manifest awareness for packaged assets (`astro-sweph`, `pyjhora` README notes).
- Session/state handling:
  - Context-managed ephemeris state setup/cleanup (`kerykeion` context manager).
  - One-time process-global initialization with conflict detection (`phoenix_engine`).
- JSON schema/versioning strategies:
  - Explicit typed API models (`vedicpanchanga.com/backend/api.py`).
  - Schema compatibility tests and version expectations (`astropy` schema tests).
  - Stable JSON fixtures as golden contracts (`kosmorro`).
- Performance/benchmark harness patterns:
  - Label-triggered benchmark CI (`astropy`).
  - Bench parser to CI summary (`hifitime`).
  - Local benchmark script with threshold assertion (`stellium`).

## Concrete Action List for Diba (next)
1. Add strict ephemeris initialization contract tests.
- Files to touch:
  - `diba/infra/io/ephemeris.py`
  - `tests/test_ephemeris_runtime_contract.py`
  - `docs/contracts/RUNTIME_CONTRACTS.md`
- Tests to add:
  - precedence rules defined in `docs/contracts/RUNTIME_CONTRACTS.md` (single source of truth)
  - fail-fast on missing configured path
  - conflict on re-init when ephemeris policy/path/expectations change in-process
- Contract/policy impact:
  - Strengthens runtime contracts and reproducibility policy without changing SwissEph session containment.

2. Add benchmark command with machine-readable output schema.
- Files to touch:
  - `diba/_cli/commands/bench.py`
  - `docs/contracts/RUNTIME_CONTRACTS.md`
- Tests to add:
  - smoke benchmark output includes cpu/profile/cache/io/median/p95/n
- Contract/policy impact:
  - Makes roadmap throughput milestones auditable.

3. Add API/serializer golden output fixtures for P0 payload.
- Files to touch:
  - `tests/golden/test_api_v1_golden.py`
  - `tests/golden/fixtures/*.json`
- Tests to add:
  - exact JSON subtree checks for `meta.*`, `data.base`, `data.chart.d1`
- Contract/policy impact:
  - Locks serializer and schema contract behavior while avoiding fragile text-output goldens.

4. Add explicit timezone precedence and DST edge test suite.
- Files to touch:
  - `tests/test_timezone_contract.py`
  - `diba/core/time.py`
- Tests to add:
  - ambiguous/non-existent local times, UTC and fixed-offset paths
  - semantic assertions robust to tzdata-version variation
- Contract/policy impact:
  - Hardens timezone policy and deterministic replay.

5. Add transition boundary search utilities for Panchanga events.
- Files to touch:
  - `diba/panchanga/events.py`
  - `diba/panchanga/calculators/tithi.py`
- Tests to add:
  - bounded binary search precision by profile (`ci`/`golden`)
  - transition edge windows around tithi boundary
- Contract/policy impact:
  - Aligns with instantaneous baseline and tolerance profile contract.

6. Add reference-verification notes per capability with traceable source paths.
- Files to touch:
  - `project_memory/research/verification_reports/*.md`
  - `docs/research/verification_reports/*.md`
- Tests to add:
  - `tests/test_memory_sync_contract.py` include verification report mirror check
- Contract/policy impact:
  - Reinforces research gate and canonical/mirror sync gate.

7. Add compatibility-window test pattern for future API renames (after public API freeze).
- Files to touch:
  - `tests/test_api_compatibility_contract.py`
  - `docs/contracts/RUNTIME_CONTRACTS.md`
- Tests to add:
  - deprecation warning behavior and removal schedule assertions
- Contract/policy impact:
  - Prevents accidental breaking changes after external contract freeze.
