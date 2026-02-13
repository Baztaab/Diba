# Worklog

## 2026-02-13

- Created `project_memory/` as persistent cross-chat tracking space.
- Added status files:
  - `project_memory/CURRENT_STATUS.md`
  - `project_memory/NEXT_STEPS.md`
  - `project_memory/WORKLOG.md`
  - `project_memory/README.md`
- Added ADR folder and stored ADR-001.

## 2026-02-13 02:47:48

- Completed Phase-1 modular foundation validation (`ruff` and `pytest` baseline green).
- Added ADR addendum for Engine + VedicState in:
  - `docs/architecture/ADR-001-Addendum-B-Engine-State.md`
  - `project_memory/adr/ADR-001-Addendum-B-Engine-State.md`
- Hardened SwissEph containment policy:
  - upgraded AST guardrail test to block alias/from-import/dynamic import bypasses
  - enforced state-setter containment to `diba/infra/swisseph/session.py`
- Moved SwissEph state setters to session boundary and updated call sites.
- Prepared working tree for final Phase-1 commit.

## 2026-02-13 02:49:30

- Committed Phase-1 as 035c11c.
- Updated CURRENT_STATUS and NEXT_STEPS for Phase-2 engine/state wiring.


## 2026-02-13 06:41:45

- Started Phase-2 implementation (Engine/State + state-based capability wiring + ephemeris SRE hardening).
- Locked key constraint: SwissEph containment allowlist remains unchanged; no new swisseph imports outside existing boundary.
- Planned scope includes contextvar-based stateless engine session control and strict base-only VedicState.


## 2026-02-13 06:45:19

- Completed Phase-2 implementation: stateless Engine/State, state-based service wiring, ephemeris fail-fast policy.
- Added tests for engine re-entrant session semantics and ephemeris env policy.
- Validation complete: ruff pass, pytest pass (82 tests).
- Commit recorded: 7ea238f.


## 2026-02-13 06:59:50

- Enabled Ruff docstring enforcement (pydocstyle/google) in CI configuration.
- Added concurrency hard-check: tests/test_engine_thread_session_isolation.py to verify no cross-thread session leakage.
- Added/updated docstrings in active Phase-2 modules to satisfy enforcement without wide refactor.
- Validation complete: ruff pass, pytest pass (83 tests).


## 2026-02-13 15:44:02

- Added execution roadmap document with priority ranking, phased plan, measurable milestones, JSON versioning policy, and next seven actions.
- Stored roadmap in both repo docs and project memory.
- Verified CI gate remains green: ruff + pytest.


## 2026-02-13 15:50:28

- Post-commit check after docs roadmap refine commit (694ff02).
- uff check diba tests: pass.
- pytest -q: pass (83 tests).


## 2026-02-13 15:50:52

- Post-commit check after project memory roadmap commit (151e084).
- uff check diba tests: pass.
- pytest -q: pass (83 tests).


## 2026-02-13 15:56:52

- Added enforceable governance locks for roadmap/policy gaps.
- Added CI tests for research gate, canonical/mirror sync, session ownership contract, and tolerance profile selection.
- Added runtime contract document and mirrored it in project memory.
- Added phase research artifact templates for P0/P1/P2 tracks under project_memory/research/.
- Updated ADR Addendum-B with explicit session single-owner rule.
- Validation complete: ruff pass, pytest pass (89 tests).


## 2026-02-13 16:01:15

- Pre-commit checks for Commit 1 (docs/contracts/policies/roadmap/ADR scope).
- uff check diba tests: pass.
- pytest -q: pass (89 tests).


## 2026-02-13 16:01:44

- Post-commit checks for Commit 1 (464bd6c).
- uff check diba tests: pass.
- pytest -q: pass (89 tests).


## 2026-02-13 16:02:02

- Pre-commit checks for Commit 2 (enforcement tests scope).
- uff check diba tests: pass.
- pytest -q: pass (89 tests).


## 2026-02-13 16:02:31

- Post-commit checks for Commit 2 (4928be0).
- uff check diba tests: pass.
- pytest -q: pass (89 tests).


## 2026-02-13 16:02:53

- Pre-commit checks for Commit 3 (research artifacts + memory status updates).
- uff check diba tests: pass.
- pytest -q: pass (89 tests).


## 2026-02-13 16:25:13

- Finalize lab inspirations alignment + runtime contracts sync (pre-commit validation ok)
- ruff check diba tests: pass.
- pytest -q: pass (89 tests).


## 2026-02-13 16:26:26

- Post-commit checks for docs/contracts alignment commit (b061106).
- ruff check diba tests: pass.
- pytest -q: pass (89 tests).


## 2026-02-13 18:23:09

- Action 1: ephemeris runtime contract enforced + tests added (T1/T2/T3), validation ok.
- ruff check diba tests: pass.
- pytest -q: pass (92 tests).


## 2026-02-13 18:30:43

- Performed deep repository analysis after Action-1 completion.
- Confirmed Action-1 commits are present and tests remain green (92).
- Identified highest-priority gap: ephemeris runtime contract exists but is not yet wired into the canonical engine orchestration path.
- Recommended next step: wire initialize_ephemeris_runtime(...) in diba/engine/state.py, then implement Action-2 benchmark harness (diba bench d1 --n 1000).


## 2026-02-13 19:28:07

- Wire ephemeris runtime init into canonical engine path; validated.
- Added canonical-path wiring tests: tests/test_engine_ephemeris_wiring.py.
- Implemented benchmark harness command: diba bench state-base --n <N>.
- Added benchmark CLI tests: tests/test_cli_bench.py.
- ruff check diba tests: pass.
- pytest -q: pass (97 tests).


## 2026-02-13 19:55:41

- Ayanamsa extraction research completed against D:\lab\Pyjhora\src\jhora with line-level references.
- Total mapped/supported ayanamsa keys in const mapping: 21 (const.py:182-192).
- Custom/computed ayanamsa modes are present: SENTHIL and SUNDAR_SS; SIDM_USER is runtime-user-defined.
- Order-of-ops finding #1: sidereal planet path uses set_ayanamsa_mode -> FLG_SIDEREAL calc_ut -> reset_ayanamsa_mode (drik.py:223-229).
- Order-of-ops finding #2: houses/asc paths use set_ayanamsa_mode before swe.houses_ex with FLG_SIDEREAL (drik.py:1439-1441,1453-1455,1487-1489).
- Order-of-ops finding #3: charts orchestration sets ayanamsa first, then ascendant+dhasavarga (charts.py:97,99,106).
- Remaining ambiguity/risk #1: SENTHIL/SUNDAR_SS branches compute value but do not call swe.set_sid_mode in branch body (drik.py:136-139).
- Remaining ambiguity/risk #2: reset_ayanamsa_mode forces LAHIRI for SIDM_USER/SENTHIL/SUNDAR_SS/KP-SENTHIL after calls (drik.py:148-150).
- Remaining ambiguity/risk #3: drik1 experimental fallback warning text and actual fallback mode are inconsistent (drik1.py:258-259).
- Coverage proof: required pattern scans completed; union of 75 matched files categorized with no uncovered file.

## 2026-02-14 00:40:55

- Strict recheck patch applied for PyJHora ayanamsa research docs.
- Added missed coverage: panchanga/info.py get_ayanamsa consumer and extra set_ayanamsa_mode call-site reconciliation.
- Updated logic doc with corrected Horoscope wiring semantics and UI-mode propagation gaps.
- Synced canonical and mirror research files for inventory/set-logic/coverage.
## 2026-02-14 01:54:22

- Implemented locked Ayanamsa plan delta: resolver now returns (spec, report) with reason-code taxonomy and fallback policy.
- Added canonicalization contract (strip/casefold/hyphen-space normalization), alias acceptance, deterministic selectable listing, and non-selectable SIDM_USER quarantine.
- Added entrypoint-only fallback logging in engine state and CLI parse paths; resolver remains side-effect free.
- Introduced generated canonical enum flow: tools/gen_ayanamsa_enum.py + diba/domain/enums/generated_ayanamsa_enum.py.
- Updated schema surfaces to canonicalize aliases before enum validation (BeforeValidator + AyanamsaIdEnum).
- Baseline sidereal restore now derives from default ayanamsa contract, not hardcoded literal.
- Added new test suites: registry contract, disabled modes, runtime wiring, restore contract, codegen sync, PyJHora coverage exception table.
- Synced runtime contract docs mirror and added PyJHora inventory exception table.
- ruff check diba tests: pass.
- pytest -q: pass (110 tests).
## 2026-02-14 02:03:12

- Final review checklist enforced for Ayanamsa hardening.
- Confirmed ResolveReport semantics use `effective_id` as post-fallback effective mode.
- Enforced single-resolve runtime rule: `resolve_ayanamsa` call sites in diba are now limited to CLI parse and engine state entrypoint (plus registry internals).
- Added guard tests: `tests/test_ayanamsa_single_resolve_rule.py` and `tests/test_research_mirror_pointer_headers.py`.
- Added explicit Mirror/Pointer headers for docs/research ayanamsa files.
- Updated runtime contracts with single-resolve rule.
- ruff check diba tests tools: pass.
- pytest -q: pass (112 tests).
