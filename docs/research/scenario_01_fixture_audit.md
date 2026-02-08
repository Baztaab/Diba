# Scenario 01 Fixture Audit (No Code Changes)

Scope: fixture-level فقط برای `scenario_01` (input/output JSON) + sanity checks عددی.

## 1) Source Files
- `tests/golden_inputs/scenario_01.tehran_2001-07-30T10-30+0430.json`
- `tests/golden_outputs/scenario_01.static_chart.expected.json`

## 2) Field Extraction Table (Input vs Expected Meta)

| Field | Input (`golden_inputs`) | Expected (`golden_outputs.meta`) | Note |
| --- | --- | --- | --- |
| `id` | `scenario_01` | `scenario_01` | Match |
| `datetime_local` | `2001-07-30T10:30:00` | `2001-07-30T10:30:00` | Match |
| `datetime_utc` | `2001-07-30T06:00:00Z` (inside `timezone`) | `2001-07-30T06:00:00Z` | Match |
| `utc_offset` | `+04:30` | `+04:30` | Match |
| `utc_offset_minutes` | `270` (derived from `+04:30`) | `270` (derived) | Match (derived) |
| `dst` / `dst_minutes` | `dst_expected=true` / `dst_minutes` ندارد | `dst=true` / `dst_minutes` ندارد | Semantic match |
| `place.lat` | `32.7` | `32.7` | Match |
| `place.lon` | `51.15` | `51.15` | Match |
| `place.alt_m` | `0.0` | `0.0` | Match |
| `ayanamsa_id` | `lahiri` | `lahiri` | Match |
| `node_policy` | **Not present** | **Not present** | Missing in fixture/meta |
| `house_system` | `whole_sign` (`house_system_id`) | `whole_sign` (`house_system_id`) | Match |
| `compat_mode` | **Not present** | **Not present** | Missing in fixture/meta |

## 3) Consistency Checks

### A) Time arithmetic check
- Given:
  - `datetime_local = 2001-07-30T10:30:00`
  - `utc_offset = +04:30` => `offset_minutes = 270`
  - `dst_minutes` field does not exist (assumed `0` because offset already includes local effective offset)
- Derived:
  - `datetime_utc_derived = datetime_local - offset = 2001-07-30T06:00:00Z`
- Compare with fixture `datetime_utc`:
  - fixture UTC = `2001-07-30T06:00:00Z`
  - mismatch = `0` minutes

### B) Date/time sanity
- `datetime_local` is exactly `2001-07-30 10:30:00`: **Yes**.
- Historical timezone sanity for Tehran on this date:
  - `Asia/Tehran` effective offset = `+04:30` (DST season)
  - Fixture offset is `+04:30`
  - mismatch = `0` minutes
- No weird value (like `18:04`) exists in scenario_01 fixture time fields.

### C) Location sanity
- Fixture says `name = Tehran, Iran` with `lat=32.7`, `lon=51.15`.
- Tehran common reference is roughly `35.68N, 51.39E`.
- Latitude anomaly vs common Tehran latitude:
  - `35.68 - 32.70 = 2.98°` (~`331 km` north-south equivalent using ~111 km/deg)
- این anomaly در fixture وجود دارد (بدون اصلاح).

## 4) Evidence Conclusion

### Which field most likely drives the large mismatch?
From fixture-only evidence + numeric diagnose output for scenario_01:
- Large deltas observed (actual vs expected) are:
  - `sun`: `+258,088.090"` (`+71.691°`)
  - `moon`: `-300,421.300"` (`-83.450°`)
  - `asc`: `+200,826.880"` (`+55.785°`)
  - `rahu/ketu`: `-14,299.060"` (`-3.972°`)
- Yet input and expected meta time fields are internally consistent (`0` min mismatch), and offset/DST are also consistent.

Therefore, the largest likely fixture-level driver is:
1. **Missing parity-driving fields in input fixture** (`compat_mode`, `node_policy`, `ayanamsa_override_deg`) while expected points appear to reflect a stricter parity profile than plain `lahiri/whole_sign`.
2. Secondary anomaly: **`location.lat=32.7` labeled as Tehran** (geographic inconsistency).

### Suggested correction (proposal only, no change now)
- First candidate to correct in `golden_input`:
  - add explicit settings fields:
    - `compat_mode` (e.g. `jhora_us` if expected is JHora-compat based),
    - `node_policy` (explicit `mean`),
    - `ayanamsa_override_deg` (if expected is tied to printed JHora ayanamsa).
- Also review location identity consistency:
  - either adjust `location.name` to match `lat=32.7`, or adjust latitude to actual Tehran range.

## Bonus: Runtime raw values used by pipeline (scenario_01)
Observed via direct factory call using scenario_01 fixture inputs:
- `pipeline_local_datetime`: `2001-07-30T10:30:00`
- `pipeline_timezone`: `Asia/Tehran`
- `pipeline_jd_utc`: `2452120.75`
- `pipeline_ayanamsa_deg`: `23.862028182672844`

These values confirm the pipeline is consuming local datetime + timezone and deriving a concrete JD UTC from those fixture fields.
