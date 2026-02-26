# D01 DST fold gap policy

## Scope

- NON_BINDING: This pack covers handling of ambiguous and nonexistent local civil times (DST fold/gap) at the TIME boundary and downstream consumers.

## Facts

- FACT: `drik.sidereal_longitude` defines UTC basis expectations via `jd_utc` relation to local `jd` and timezone. [E01]
- FACT: Multiple callsites derive `jd_utc` from `jd - timezone/24`. [E02]
- FACT: `sunrise` computes date-based `jd_utc`, calls `swe.rise_trans`, and recomputes local rise value. [E03]
- FACT: `utils.local_time_to_jdut1` uses `swe.utc_time_zone` and `swe.utc_to_jd(..., 0, ...)`. [E04]
- FACT: Sweep2 explicitly marks DST fold/gap behavior as unresolved by static evidence and requiring probes. [E01,E02,E03,E04]
- FACT: Missing date/time defaults are present in validation flows, which can change effective civil-time interpretation. [E17]

## Options

- Option A (NON_BINDING): Reject ambiguous/nonexistent local times at ingestion and require explicit correction input.
- Option B (NON_BINDING): Accept local time plus explicit disambiguation marker (fold/gap handling field) in time payload.
- Option C (NON_BINDING): Evaluate both fold candidates in ambiguous windows and carry both forward until deterministic boundary selection.
  - OPEN_QUESTION: Where and when do we collapse the two-candidate fan-out?

## Pros and cons

- Option A
  - Pros: deterministic entry behavior; minimal hidden conversion.
  - Cons: stricter UX; additional caller burden.
- Option B
  - Pros: single-path execution with explicit provenance; easier replay.
  - Cons: requires all producers to populate disambiguation field.
- Option C
  - Pros: preserves information under ambiguity; no forced early collapse.
  - Cons: larger state fan-out; extra compute and comparison logic.

## Impact map

- TIME boundary contract (`jd`, `jd_utc`, timezone) [E01,E02,E03,E04]
- `utils.local_time_to_jdut1` adapter behavior [E04]
- Input validation/defaulting behavior [E17]
- Panchanga coupling paths that depend on sunrise anchor [E03,E21]

## Validation plan

- Use a fixed corpus of tzids + local timestamps (to be defined/linked in parity corpus).
- Probe 1: Re-run conversions across known DST fold timestamps and compare resulting `jd_utc` values by option path. [E01,E04]
- Probe 2: Re-run conversions across known DST gap timestamps and capture error/surrogate outcomes by option path. [E01,E04]
- Probe 3: Compare sunrise/tithi downstream outputs for adjacent timestamps around fold/gap boundaries. [E03,E21]

## Open questions

- OPEN_QUESTION: Which boundary should own civil-time ambiguity resolution before `jd_utc` is materialized?
- OPEN_QUESTION: Should ambiguity metadata remain in payloads after conversion to `jd_utc`?
- OPEN_QUESTION: Which parity tests are required around DST transitions to keep reproducibility claims stable?
