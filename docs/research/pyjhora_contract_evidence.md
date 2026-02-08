# PyJHora Contract Evidence (Repo-Local)

Scope: Evidence is only from the PyJHora code bundled in this repo under `docs/jhora/`.

**1) PyJHora Code Location (Repo)**
- Root: `docs/jhora/` (files in this subtree declare they are part of the PyJHora library and were downloaded from the PyJHora repo). Sources: `docs/jhora/const.py:5`, `docs/jhora/const.py:7`, `docs/jhora/horoscope/chart/charts.py:5`, `docs/jhora/horoscope/chart/charts.py:7`, `docs/jhora/panchanga/drik.py:26`.
- Key files used in this research: `docs/jhora/const.py`, `docs/jhora/panchanga/drik.py`, `docs/jhora/horoscope/chart/charts.py`, `docs/jhora/horoscope/chart/house.py`.

**2) House System Evidence (Each Rasi Is a House / Whole Sign)**
- PyJHora labels house system method 5 as “Each Rasi is the house” in `indian_house_systems`. Source: `docs/jhora/const.py:630`, `docs/jhora/const.py:631`.
- `_bhaava_madhya_new` documents method 5 as: “Each Rasi is the house (rasi is the house, 0 is start and 30 is end, asc is asc+rasi*30)”. Source: `docs/jhora/horoscope/chart/charts.py:121`, `docs/jhora/horoscope/chart/charts.py:131`.
- Method 5 implementation sets: `h1 = (h + ascendant_constellation) % 12`; `_bhava_start = h1 * 30`; `_bhava_mid = _bhava_start + ascendant_longitude`; `_bhava_end = ((h1 + 1) % 12) * 30`. Sources: `docs/jhora/horoscope/chart/charts.py:175`, `docs/jhora/horoscope/chart/charts.py:176`, `docs/jhora/horoscope/chart/charts.py:177`, `docs/jhora/horoscope/chart/charts.py:178`, `docs/jhora/horoscope/chart/charts.py:179`.
- The `planet_positions` format indicates the Ascendant longitude is expressed as degrees within its sign (e.g., “Lagnam in Aries 13.4 degrees”). Source: `docs/jhora/horoscope/chart/charts.py:77`, `docs/jhora/horoscope/chart/charts.py:78`, `docs/jhora/horoscope/chart/charts.py:79`.

**Cusp Rule (from code):**
- In method 5, the cusp (bhava mid) is computed as `sign_start + ascendant_longitude` for every house, which implies the cusp degree is the same as the Ascendant degree in each sign. Sources: `docs/jhora/horoscope/chart/charts.py:175`, `docs/jhora/horoscope/chart/charts.py:177`, `docs/jhora/horoscope/chart/charts.py:178`.
- This matches “cusp = Asc degree in each sign” and does not match “cusp at sign start (0°)” or “cusp fixed at 15° mid-sign.” (Inference from the above code path.)

**3) Node Mode Evidence (Mean vs True)**
- PyJHora defines Rahu/Ketu using Swiss Ephemeris MEAN node constants: `_RAHU = swe.MEAN_NODE`, `_KETU = -swe.MEAN_NODE`. Source: `docs/jhora/const.py:53`, `docs/jhora/const.py:54`.
- The panchanga planet lists include Rahu/Ketu and explicitly comment “Rahu = MEAN_NODE.” Source: `docs/jhora/panchanga/drik.py:42`, `docs/jhora/panchanga/drik.py:43`, `docs/jhora/panchanga/drik.py:44`, `docs/jhora/panchanga/drik.py:45`.
- Ketu is always computed as Rahu + 180°. Source: `docs/jhora/panchanga/drik.py:153`, `docs/jhora/panchanga/drik.py:155`.

**Conclusion (Node mode):**
- PyJHora uses mean nodes by default via `swe.MEAN_NODE` and derives Ketu as the opposite point. No true-node constant appears in these definitions (inference based on the above evidence).

**4) Ayanamsa Evidence (Lahiri / Chitra Paksha / True Citra)**
- `available_ayanamsa_modes` maps `LAHIRI` → `swe.SIDM_LAHIRI`, `SS_CITRA` → `swe.SIDM_SS_CITRA`, `TRUE_CITRA` → `swe.SIDM_TRUE_CITRA`, and `TRUE_LAHIRI` → `swe.SIDM_TRUE_CITRA`. Sources: `docs/jhora/const.py:190`, `docs/jhora/const.py:194`, `docs/jhora/const.py:195`, `docs/jhora/const.py:196`.
- Default ayanamsa mode is `LAHIRI`. Source: `docs/jhora/const.py:202`.
- `set_ayanamsa_mode` applies the selected mode via `swe.set_sid_mode(const.available_ayanamsa_modes[key])`, otherwise falls back to the default. Sources: `docs/jhora/panchanga/drik.py:117`, `docs/jhora/panchanga/drik.py:132`, `docs/jhora/panchanga/drik.py:141`, `docs/jhora/panchanga/drik.py:142`, `docs/jhora/panchanga/drik.py:143`, `docs/jhora/panchanga/drik.py:144`, `docs/jhora/panchanga/drik.py:145`.

**Preset/Profile Trace:**
- No PyJHora profile/preset mechanism is referenced in these ayanamsa selection paths; the selection is direct through `set_ayanamsa_mode` and `const._DEFAULT_AYANAMSA_MODE` (inference from the sources above).
