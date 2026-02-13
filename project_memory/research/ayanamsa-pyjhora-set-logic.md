# Ayanamsa Set/Apply Logic In PyJHora
Date: 2026-02-13
Source repo scanned: `D:\lab\Pyjhora\src\jhora\`

## 1) Runtime control points (where ayanamsa is set)

### 1.1 Primary runtime setter (active path)
- Function: `set_ayanamsa_mode(ayanamsa_mode, ayanamsa_value=None, jd=None)`
- Ref: `D:\lab\Pyjhora\src\jhora\panchanga\drik.py:117`
- Branches:
  - `SIDM_USER`: stores `_ayanamsa_value` and calls `swe.set_sid_mode(swe.SIDM_USER, ayanamsa_value)`
    - Refs: `drik.py:133-135`
  - `SENTHIL`: computes `_ayanamsa_value = _calculate_ayanamsa_senthil_from_jd(jd)`
    - Refs: `drik.py:136`, `drik.py:86-98`
  - `SUNDAR_SS`: computes `_ayanamsa_value = _ayanamsa_surya_siddhantha_model(jd)`
    - Refs: `drik.py:138`, `drik.py:65-84`
  - Otherwise: calls `swe.set_sid_mode(const.available_ayanamsa_modes[key])`
    - Ref: `drik.py:141`
  - Unsupported key fallback: warning then default mode setup
    - Refs: `drik.py:143-145`
- Side effect: updates global default mode `const._DEFAULT_AYANAMSA_MODE = _ayanamsa_mode`
  - Ref: `drik.py:147`

### 1.2 Reset behavior
- `reset_ayanamsa_mode` lambda:
  - If default mode is not in `['SIDM_USER','SENTHIL','SUNDAR_SS','KP-SENTHIL']`, reset to mapped default mode.
  - Else reset to `swe.SIDM_LAHIRI`.
- Refs: `D:\lab\Pyjhora\src\jhora\panchanga\drik.py:148-150`

### 1.3 Legacy/experimental parallel implementation
- File carries explicit warning: `DO NOT USE THIS YET - EXPERIMENTAL WORK`
  - Ref: `D:\lab\Pyjhora\src\jhora\panchanga\drik1.py:23`
- Has parallel setter/getter/sidereal paths:
  - `drik1.py:222`, `drik1.py:236`, `drik1.py:319`, `drik1.py:994-1003`

## 2) Where ayanamsa is applied to planetary and house outputs

## 2.1 Planetary longitude path (`sidereal_longitude`)
- Function: `sidereal_longitude(jd_utc, planet)`
- Refs: `D:\lab\Pyjhora\src\jhora\panchanga\drik.py:203-229`

Order of operations in this function:
1. Decide flags:
- Tropical: `flags = swe.FLG_SWIEPH` (`drik.py:221`)
- Non-tropical: `flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | _rise_flags` (`drik.py:223`)
2. Non-tropical branch sets ayanamsa mode again using current default mode:
- `set_ayanamsa_mode(const._DEFAULT_AYANAMSA_MODE, _ayanamsa_value, jd_utc)` (`drik.py:225`)
3. Planet computed with `swe.calc_ut`:
- `swe.calc_ut(jd_utc, planet, flags=flags)` (`drik.py:228`)
4. Mode reset:
- `reset_ayanamsa_mode()` (`drik.py:229`)

Interpretation:
- Primary behavior is Swiss sidereal-flag path (mode applied in Swiss via `set_sid_mode` when the mode branch does that): **model (a)**.

## 2.2 House/ascendant path (`houses_ex`)
- House cusps (`bhaava_madhya_swe`): `drik.py:1410-1441`
- KP cusps (`bhaava_madhya_kp`): `drik.py:1442-1455`
- Ascendant (`ascendant`): `drik.py:1474-1493`

Order of operations in each houses path:
1. Convert local JD -> `jd_utc` via timezone (`drik.py:1435`, `1449`, `1483`).
2. Set flags:
- Tropical: `swe.FLG_SWIEPH` (`drik.py:1437`, `1451`, `1485`)
- Sidereal: `swe.FLG_SIDEREAL` (`drik.py:1439`, `1453`, `1487`)
3. In sidereal mode call `set_ayanamsa_mode(...)` before `swe.houses_ex(...)` (`drik.py:1440`, `1454`, `1488`).
4. Compute houses/asc (`drik.py:1441`, `1455`, `1489`).
5. In ascendant path, explicit reset after read (`drik.py:1493`).

Interpretation:
- Houses path also relies on Swiss sidereal mode + `FLG_SIDEREAL`: **model (a)**.

## 2.3 Chart orchestration call chain (where setter is triggered from higher layers)
- `charts.rasi_chart(...)` sets ayanamsa first, then calls ascendant and dhasavarga:
  - Refs: `D:\lab\Pyjhora\src\jhora\horoscope\chart\charts.py:65`, `:97`, `:99`, `:106`
- `charts.bhava_chart(...)` sets ayanamsa before house logic:
  - Refs: `charts.py:114`, `:119`
- `horoscope.main.Horoscope.__init__` only forces mode for `ss` calculation type:
  - Refs: `D:\lab\Pyjhora\src\jhora\horoscope\main.py:98`
  - Then reads mode/value from global state:
    - `self.ayanamsa_mode = const._DEFAULT_AYANAMSA_MODE` (`horoscope/main.py:99`)
    - `self.ayanamsa_value = drik.get_ayanamsa_value(self.julian_day)` (`horoscope/main.py:100`)

## 2.4 UT vs TT and topocentric handling
- Planet calls use `swe.calc_ut(...)` (UT API), not `calc` TT call:
  - Ref: `drik.py:228`
- House calls use `swe.houses_ex(...)` with `jd_utc` computed from local timezone.
  - Refs: `drik.py:1435`, `1441`, `1449`, `1455`, `1483`, `1489`
- No explicit `swe.set_topo(...)` call found in scanned scope.
  - Search ref: `set_topo` repo scan (no matches).
- House system code supports `'T'` (topocentric house system code), but this is house-system selection, not `set_topo` observer state.
  - Refs: `drik.py:1348`, `drik.py:1422`, `charts.py:134`

## 3) Custom/computed ayanamsa models (formula + execution)

### 3.1 SENTHIL model
- Formula function: `_calculate_ayanamsa_senthil_from_jd(jd)`
  - Refs: `drik.py:86-98`
- Inputs and steps:
  - Reference JD: J2000 `swe.julday(2000,1,1,12)` (`drik.py:88`)
  - `t = (jd-reference_jd)/sidereal_year` (`drik.py:95-96`)
  - `ayanamsa_arcsec = a0 + p0*t + q*t*t`, convert to degrees by `/3600` (`drik.py:97-98`)
- Consumption path:
  - Assigned in setter SENTHIL branch (`drik.py:136`)
  - Getter returns cached value for custom modes (`drik.py:109-112`)

### 3.2 SUNDAR_SS model
- Formula function: `_ayanamsa_surya_siddhantha_model(jd)`
  - Refs: `drik.py:65-84`
- Inputs and steps:
  - Kali epoch JD via `swe.julday(-3101,1,23,12, cal=swe.JUL_CAL)` (`drik.py:77`)
  - Cyclic fractions over sidereal year and equinox cycles (`drik.py:79-82`)
  - Final value from sinusoidal precession model (`drik.py:83-84`)
- Consumption path:
  - Assigned in setter SUNDAR_SS branch (`drik.py:138`)
  - Getter returns cached custom value (`drik.py:109-112`)

### 3.3 SIDM_USER model
- Branch stores user value and calls Swiss user mode directly:
  - Refs: `drik.py:133-135`
- User input contract mention:
  - `drik.py:124`

## 4) Which application model is used? (a/b/c)
- (a) Set Swiss sidereal mode + `FLG_SIDEREAL`: **Yes**, primary implementation (`drik.py:117-141`, `203-229`, `1410-1493`).
- (b) Compute tropical then subtract ayanamsa for core longitudes/houses: **No direct core path found** in main longitude/house functions.
- (c) Mixed/special: **Yes** for selected derived computations.
  - Example: `declination_of_planets` reconstructs tropical-like longitude by adding ayanamsa to sidereal longitudes (`p_long = h*30 + long + _ayanamsa`).
  - Ref: `drik.py:1561-1576`.

## 5) Deterministic findings from code
- `set_sid_mode` call-sites in scanned scope are concentrated in:
  - `drik.py`, `drik1.py`, `utils.py`.
- Active charting path (`horoscope/chart/charts.py`) routes into `drik.py`, not `drik1.py`.
- `drik1.py` keeps alternative behaviors (including fixed `SIDM_USER` lambdas and reset to `FAGAN`) but is marked experimental.

## 6) Open technical ambiguities discovered directly from code
- In `drik.py`, `SENTHIL` and `SUNDAR_SS` branches compute `_ayanamsa_value` but do not call `swe.set_sid_mode(...)` in those branches (`drik.py:136-139`), while sidereal planet/house APIs rely on `FLG_SIDEREAL` Swiss calls.
- `reset_ayanamsa_mode` forces LAHIRI when default is `SIDM_USER`, `SENTHIL`, `SUNDAR_SS`, or `KP-SENTHIL` (`drik.py:148-150`), so effective mode after each call depends on re-application at next entry.
- `drik1.py` fallback warning says `KP Assumed` but code sets LAHIRI (`drik1.py:258-259`), which is an explicit message/behavior mismatch.

## 7) Strict Recheck Addendum (missed call-sites patched)

### 7.1 Additional runtime apply call-sites inside `drik.py`
- `planets_in_retrograde`:
  - sets once before loop: `D:\lab\Pyjhora\src\jhora\panchanga\drik.py:245`
  - resets inside loop: `D:\lab\Pyjhora\src\jhora\panchanga\drik.py:251`
- `planets_speed_info`:
  - sets once before loop: `D:\lab\Pyjhora\src\jhora\panchanga\drik.py:278`
  - resets inside loop: `D:\lab\Pyjhora\src\jhora\panchanga\drik.py:286`
- `next_planet_retrograde_change_date` inner helper:
  - calls `set_ayanamsa_mode` before `calc_ut`: `D:\lab\Pyjhora\src\jhora\panchanga\drik.py:2713`
- Sidereal eclipse flag usage (without local set call in function body):
  - `D:\lab\Pyjhora\src\jhora\panchanga\drik.py:2300`

### 7.2 Additional external call-sites for `set_ayanamsa_mode(...)`
- UI:
  - `D:\lab\Pyjhora\src\jhora\ui\panchangam.py:450`, `:595` (passes `jd` for `SUNDAR_SS`)
  - `D:\lab\Pyjhora\src\jhora\ui\horo_chart_tabs.py:2753`
  - `D:\lab\Pyjhora\src\jhora\ui\horo_chart.py:67` (SS mode only)
- Test/demo callers:
  - `D:\lab\Pyjhora\src\jhora\tests\pvr_tests.py:5524`
  - `D:\lab\Pyjhora\src\jhora\panchanga\vratha.py:791` (`__main__` script path)
  - `D:\lab\Pyjhora\src\jhora\horoscope\chart\strength.py:1053` (`__main__` demo path)

### 7.3 UI wiring mismatch affecting effective mode application
- `horo_chart.py` reads selected mode (`currentText`) but does not pass mode into `main.Horoscope(...)` constructor calls:
  - mode read: `D:\lab\Pyjhora\src\jhora\ui\horo_chart.py:376`
  - constructor calls: `D:\lab\Pyjhora\src\jhora\ui\horo_chart.py:392`, `:396`
  - implication: non-SS selection here depends on previously set global mode rather than explicit constructor argument.
