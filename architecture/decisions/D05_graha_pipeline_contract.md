# D05 graha pipeline contract

## Scope

- NON_BINDING: This pack covers contract shape and coupling boundaries for Graha longitude/state payloads consumed by downstream modules.

## Facts

- FACT: Graha pipeline callsites use SwissEph `calc_ut` and consume the raw vector as `longi` before local transformations. [E05,E16,E28,E31]
- FACT: `sidereal_longitude` normalizes longitude with `utils.norm360(longi[0])` at the callsite boundary. [E05; Source: `research/ephemeris_engine_contracts/core_ephemeris_engine_contract/guru.md`]
- FACT: Speed payload extraction rounds the raw `calc_ut` vector with fixed round factors `[3,3,4,3,3,6]`. [E16; Source: `research/graha_longitudes_and_states/core_graha_longitudes_and_states_contract/guru.md`]
- FACT: Retrograde state is derived from the sign of `longi[3]` in observed callsites. [E28,E31; Source: `research/graha_longitudes_and_states/core_graha_longitudes_and_states_contract/guru.md`]
- FACT: Node identifiers map to SwissEph node constants as `RAHU = swe.MEAN_NODE` and `KETU = -swe.MEAN_NODE`. [E13; Source: `research/graha_longitudes_and_states/core_graha_longitudes_and_states_contract/guru.md`]
- FACT: Planet ordering and included planet set are mutable in module globals (`planet_list`, `_sideral_planet_list`) and can be changed by tropical toggle paths. [E10,E11]
- FACT: Observed Graha report scope includes longitude/speed/retrograde behavior and does not list combust extraction excerpts in the current captured artifacts. [Source: `research/graha_longitudes_and_states/report.md`; Source: `research/graha_longitudes_and_states/core_graha_longitudes_and_states_contract/guru.md`]
- FACT: `calc_ut` callsites around Graha/state paths show mixed sidereal setup basis patterns tied to `jd` and `jd_utc` in the broader set/reset audit. [E26,E27,E28,E31,E34,E36; Source: `research/kala_time/core_kala_time_contract/guru.md`]

## Options

- Option A (NON_BINDING): Raw-only Graha payload (`calc_ut` vector + ids), with all derived states computed downstream.
- Option B (NON_BINDING): Raw+derived Graha payload in one envelope (longitude, speed, retrograde, node-normalized ids).
- Option C (NON_BINDING): Strict canonical Graha fields plus optional debug payload containing raw SwissEph vector and call provenance.
- Option D (NON_BINDING): Dual-lane envelope: parity lane mirrors PyJHora callsite semantics; strict lane exposes canonicalized fields.

## Pros and cons

- Option A
  - Pros: closest to source engine output; minimal contract assumptions.
  - Cons: duplicated derivation logic across consuming modules.
- Option B
  - Pros: fewer repeated derivations; simpler consumers.
  - Cons: contract couples raw acquisition with policy-level derivations.
- Option C
  - Pros: stable consumer surface with traceable debug fallback.
  - Cons: canonical field set definition becomes a separate contract burden.
- Option D
  - Pros: explicit separation of parity replay and strict consumption.
  - Cons: higher payload and maintenance complexity across two lanes.

## Impact map

- HOUSES coupling: house assignment consumes Lagna/planet payload ordering assumptions that depend on Graha contract shape. [E14,E23]
- VARGA coupling: divisional pipelines consume packaged planet positions from upstream chart orchestration. [E14; Source: `research/varga_divisional_charts/report.md`]
- PANCHANGA coupling: sunrise/tithi and related computations consume planetary longitudes and shared time-state setup paths. [E03,E21]
- TRANSIT coupling: transit modules import and consume core Graha/house/time primitives from chart/panchanga layers. [E22]

## Validation plan

- Probe 1: Parity probes for Graha callsite outputs against observed PyJHora expectations (`sidereal_longitude`, retrograde, speed vector paths). [E05,E16,E28,E31]
- Probe 2: Normalization and rounding regression probes on `norm360(longi[0])` and fixed round-factor speed vectors. [E05,E16]
- Probe 3: Node mapping probes for Rahu/Ketu id and constant mapping behavior in payload generation. [E10,E13]
- Probe 4: Ordering probes for mutable planet-list scenarios (sidereal and tropical modes) and downstream payload consumers. [E10,E11]

## Open questions

- OPEN_QUESTION: Which Graha fields are mandatory across all consuming contracts versus optional/debug-only?
- OPEN_QUESTION: How should payload provenance stamps link to the time bundle canonicalization boundary in [D02_time_bundle_canonicalization.md](D02_time_bundle_canonicalization.md)?
- OPEN_QUESTION: How should Graha payload provenance encode sidereal-state ownership/isolation boundaries from [D03_swisseph_state_isolation.md](D03_swisseph_state_isolation.md)?
- OPEN_QUESTION: Where should combust-state computation live in contract boundaries when moving from evidence capture to implementation planning?
