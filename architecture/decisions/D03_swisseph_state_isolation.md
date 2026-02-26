# D03 swisseph state isolation

## Scope

- NON_BINDING: This pack covers isolation of mutable SwissEph sidereal/ephemeris state across contracts and call paths.

## Facts

- FACT: `set_ayanamsa_mode` invokes `swe.set_sid_mode` and mutates global default mode state. [E08]
- FACT: Callsite audit shows multiple invocation patterns with mixed third-argument basis (`jd` and `jd_utc`). [E26,E27,E28,E29,E30,E31,E32,E34,E36]
- FACT: Some functions include in-function `reset_ayanamsa_mode`, while others return without reset in the same function body. [E27,E29,E30,E31,E24,E25]
- FACT: House functions `bhaava_madhya_kp` and `bhaava_madhya_swe` set sidereal mode and return house cusps without local reset call in the same body. [E24,E25]
- FACT: Ephemeris path is also configured via global SwissEph call at import scope. [E07]
- FACT: Existing test baseline references Lahiri default-mode assumptions. [E09]

## Options

- Option A (NON_BINDING): Scoped state wrapper around each SwissEph call sequence with explicit set/reset ownership.
- Option B (NON_BINDING): Single serialized execution lane for stateful SwissEph operations with deterministic state ledger.
  - Isolation unit: per-request serialized execution context.
- Option C (NON_BINDING): Process-level isolation for SwissEph workers and immutable request/response boundaries.
  - Isolation unit: per-run worker process boundary.
- Option D (NON_BINDING): Pre/post state assertion hooks around current callsites, preserving current signatures and behavior.

## Pros and cons

- Option A
  - Pros: direct mapping to existing callsites; localized migration.
  - Cons: relies on strict wrapper coverage and no bypass paths.
- Option B
  - Pros: deterministic state progression in one lane.
  - Cons: throughput constraints for parallel workloads.
- Option C
  - Pros: strongest state isolation across requests.
  - Cons: higher operational complexity and IPC overhead.
- Option D
  - Pros: low disruption to existing code paths; faster evidence gathering.
  - Cons: assertions detect drift but do not inherently isolate shared state.

## Impact map

- SIDEREAL state contract and callsite wrappers [E08,E26-E36]
- HOUSES contract paths with set-without-reset risk [E24,E25,E29]
- Graha/retrograde/speed paths that use sidereal mode mutation [E28,E31]
- Import-time ephemeris configuration and test reproducibility assumptions [E07,E09]

## Validation plan

- Probe 1: Repeat-run determinism checks for mixed call sequences spanning `sidereal_longitude`, `planets_in_retrograde`, `bhaava_madhya_*`, `ascendant`, and sunrise/`rise_trans` paths. [E03,E27,E28,E29,E30,E31,E24,E25]
- Probe 2: Concurrency probes to detect cross-call contamination of sidereal mode or defaults. [E08,E26-E36]
- Probe 3: Regression checks against Lahiri-default assumptions in current test baseline. [E09]
- Probe 4: State-ledger instrumentation checks for set/reset balance per function path. [E26-E36]

## Open questions

- OPEN_QUESTION: Which boundary owns final reset responsibility when nested helpers mutate sidereal state?
- OPEN_QUESTION: Should import-time ephemeris path and sidereal defaults be frozen per run context?
- OPEN_QUESTION: What level of isolation is required for parallel execution targets in the current architecture scope?
