# D02 time bundle canonicalization

## Scope

- NON_BINDING: This pack covers canonical time payload shape across TIME, GRAHA, HOUSES, PANCHANGA_COUPLING, and TRANSIT_COUPLING boundaries.

## Facts

- FACT: Functions in scope consume both local `jd` and UTC-basis `jd_utc` forms. [E01,E02,E03,E24,E25]
- FACT: `jd_utc` derivation pattern (`jd - timezone/24`) appears in multiple operational paths. [E02,E24,E25]
- FACT: `local_time_to_jdut1` converts civil-time input through SwissEph conversion calls. [E04]
- FACT: Sunrise/tithi coupling depends on sunrise anchor output from time conversion flow. [E03,E21]
- FACT: Validation defaults may inject current date/time or fallback selections, affecting canonical payload provenance. [E17,E18,E19]
- FACT: Callsite audit shows mixed `set_ayanamsa_mode` third-argument basis (`jd` and `jd_utc`) across paths. [E26,E27,E28,E29,E30,E31,E32,E33,E34,E35,E36]

## Options

- Option A (NON_BINDING): Canonical bundle carries both `jd` and `jd_utc` plus timezone and civil-time origin fields.
- Option B (NON_BINDING): Canonical bundle carries civil-time + timezone only; `jd` and `jd_utc` are derived lazily per boundary.
- Option C (NON_BINDING): Canonical bundle is UTC-first (`jd_utc`) with optional local projections added for downstream consumers.
- Option D (NON_BINDING): Boundary-specific adapters keep current signatures and emit standardized provenance envelope only.

## Pros and cons

- Option A
  - Pros: explicit parity-ready payload; fewer hidden conversions.
  - Cons: risk of divergence if dual values drift without checks.
- Option B
  - Pros: single source of truth at input edge.
  - Cons: repeated conversion paths can diverge across modules.
- Option C
  - Pros: strong UTC normalization for ephemeris calls.
  - Cons: local-time-dependent consumers may require repeated reverse projections.
- Option D
  - Pros: lower migration cost from existing call signatures.
  - Cons: Does not enforce canonicalization; only reports provenance.

## Impact map

- TIME contract and helper adapters [E01,E02,E03,E04]
- HOUSES contract (`bhaava_madhya_*` bases on `jd` and derived `jd_utc`) [E24,E25]
- Panchanga sunrise-anchor consumers [E03,E21]
- Cross-cutting defaults/provenance pathways [E17,E18,E19]

## Validation plan

- Probe 1: Round-trip checks between civil input and `jd_utc` for representative timezones, including edge timestamps. [E01,E04]
- Probe 2: Differential checks of house outputs under same payload across canonicalization options. Hold constant the house method/house_code across runs. [E24,E25]
- Probe 3: Differential checks of sunrise/tithi outputs for same payload across canonicalization options. [E03,E21]
- Probe 4: Provenance assertions to verify defaults are explicitly stamped when fallback behavior is exercised. [E17,E18,E19]

## Open questions

- OPEN_QUESTION: Which fields are mandatory in the canonical time payload for reproducibility claims?
- OPEN_QUESTION: Should `jd` and `jd_utc` coexist in one payload or be boundary-derived only?
- OPEN_QUESTION: Where should defaulting behavior be attached so provenance remains explicit and testable?
