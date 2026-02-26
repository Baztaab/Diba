# ephemeris_behavior_contract_map.core.md

## Snapshot identity (FACTS)

- pyjhora_root: `D:\lab\Pyjhora`
- extraction_timestamp_local: `2026-02-27 01:55:35 +03:30`
- in-scope file digests (SHA256):
  - `src/jhora/utils.py` -> `861062b3abba1655b9d4e5608333f8aaa1d391b3d38ecdacbac565bf930f3875` (bytes: `70076`)
  - `src/jhora/panchanga/drik.py` -> `9790dcdf442910b1eaa260b16c346c6696438eb6955c0a520c1be220ba3497bc` (bytes: `186944`)
  - `src/jhora/panchanga/vratha.py` -> `88e2eb31edeb521779bdf91f818797ae391418e37dd3da67ba492b250ea785e4` (bytes: `48575`)
  - `src/jhora/panchanga/surya_sidhantha.py` -> `cb5190f94884e4e79d5ed0f98988fa510567bb8e8a02942d3a0a600c4ed808b9` (bytes: `29995`)
  - `src/jhora/horoscope/chart/charts.py` -> `34c49af9fb3359fdb243f2a467404b7a849e35b9def9e2961a45a4027c8619b2` (bytes: `141395`)
  - `src/jhora/horoscope/transit/tajaka.py` -> `8f1d7c369363c953ff21405cf4a7243c488cc6d155315b80e279a861f58bce17` (bytes: `40858`)
  - `src/jhora/const.py` -> `2dacc910fce9babc69582491b52cde9fd23ab9dde835d41efb65fc0f79e00ba8` (bytes: `79727`)

## Scope (FACTS)

- In-scope files:
  - `src/jhora/utils.py`
  - `src/jhora/panchanga/drik.py`
  - `src/jhora/panchanga/vratha.py`
  - `src/jhora/panchanga/surya_sidhantha.py`
  - `src/jhora/horoscope/chart/charts.py`
  - `src/jhora/horoscope/transit/tajaka.py`
  - `src/jhora/const.py`
- Out-of-scope:
  - UI modules
  - tests
  - experiments
  - `src/jhora/panchanga/drik1.py`

## Pattern inventory (FACTS)

- `swe.calc_ut`
- `swe.rise_trans`
- `swe.houses_ex`
- `swe.fixstar_ut`
- `swe.julday`
- `swe.revjul`
- `swe.utc_time_zone`
- `swe.utc_to_jd`
- `swe.set_sid_mode`
- `swe.get_ayanamsa`
- `swe.set_ephe_path`
- `swe.sol_eclipse_how`
- `swe.sol_eclipse_when_loc`
- `swe.lun_eclipse_when_loc`
- `swe.version`

## Must-anchor set (FACTS)

- For every ephemeris anchor that uses `flags` or `rsmi`, the excerpt includes the exact flag expression with operator and order when combination is present.
- `_rise_flags` definition and `rise_trans(..., rsmi=...)` usage are anchored separately.
- If a pattern has no match in Core-7, absence is recorded in coverage ledger.

## Evidence anchors (EP01..EP18)

### EP01

- Behavior: ephemeris path is configured at module import in `const.py`.
- Source: `src/jhora/const.py:L174-L176`
- Excerpt:
```python
_ephe_path = os.path.abspath(_EPHIMERIDE_DATA_PATH)
swe.set_ephe_path(_ephe_path)
sidereal_year = 365.256364   # From JHora
```
- Observed behavior: global ephemeris path setup occurs during module load.

### EP02

- Behavior: utility API exposes runtime ephemeris path override.
- Source: `src/jhora/utils.py:L374-L376`
- Excerpt:
```python
def set_ephemeris_data_path(data_path=const._ephe_path):
    swe.set_ephe_path(data_path)
def set_language(language=const._DEFAULT_LANGUAGE):
```
- Observed behavior: caller can mutate SwissEph path after import.

### EP03

- Behavior: ayanamsa read/set/reset paths call SwissEph sidereal state APIs.
- Source A: `src/jhora/panchanga/drik.py:L115-L116`
- Excerpt A:
```python
_ayanamsa_value = swe.get_ayanamsa(jd)
return _ayanamsa_value
```
- Source B: `src/jhora/panchanga/drik.py:L133-L142`
- Excerpt B:
```python
if key in [am.upper() for am in const.available_ayanamsa_modes.keys()]:
    if key == "SIDM_USER":
        _ayanamsa_value = ayanamsa_value
        swe.set_sid_mode(swe.SIDM_USER,ayanamsa_value)
    elif key == "SENTHIL":
        _ayanamsa_value = _calculate_ayanamsa_senthil_from_jd(jd)
    elif key == "SUNDAR_SS":
        _ayanamsa_value = _ayanamsa_surya_siddhantha_model(jd)
    else:
        swe.set_sid_mode(const.available_ayanamsa_modes[key])
```
- Source C: `src/jhora/panchanga/drik.py:L149-L151`
- Excerpt C:
```python
reset_ayanamsa_mode = lambda: swe.set_sid_mode(const.available_ayanamsa_modes[const._DEFAULT_AYANAMSA_MODE]) \
                  if const._DEFAULT_AYANAMSA_MODE not in ['SIDM_USER','SENTHIL','SUNDAR_SS','KP-SENTHIL'] else \
                  swe.set_sid_mode(swe.SIDM_LAHIRI)
```
- Observed behavior: sidereal state is global and mutable via set/reset callsites.

### EP04

- Behavior: `sidereal_longitude` composes `flags` with `|`, calls `calc_ut`, then resets state.
- Source: `src/jhora/panchanga/drik.py:L225-L231`
- Excerpt:
```python
flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | _rise_flags
set_ayanamsa_mode(_ayanamsa_default,_ayanamsa_value,jd_utc); _ayanamsa_mode = const._DEFAULT_AYANAMSA_MODE
longi,_ = swe.calc_ut(jd_utc, planet, flags = flags)
reset_ayanamsa_mode()
```
- Observed behavior: combined flag expression is explicit and reset is in-function.

### EP05

- Behavior: retrograde path composes flags with `|`, uses `calc_ut`, and resets inside loop.
- Source: `src/jhora/panchanga/drik.py:L243-L252`
- Excerpt:
```python
jd_utc = jd - place.timezone / 24.
flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | _rise_flags
set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd)
for planet in _planet_list:
    p_id = _sideral_planet_list.index(planet)
    longi,_ = swe.calc_ut(jd_utc, planet, flags = flags)
    reset_ayanamsa_mode()
    if longi[3]<0 : retro_planets.append(p_id)
```
- Observed behavior: `set_ayanamsa_mode` basis is `jd`; `calc_ut` basis is `jd_utc`.

### EP06

- Behavior: speed path composes flags with `|`, resets, and rounds raw vector fields.
- Source: `src/jhora/panchanga/drik.py:L275-L287`
- Excerpt:
```python
round_factors = [3,3,4,3,3,6]
jd_utc = jd - place.timezone / 24.
flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | _rise_flags
set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd)
for planet in planet_list:
    if planet == const._KETU:
        _planets_speed_info[planet_index] = _planets_speed_info[planet_list.index(const._RAHU)]
        continue
    longi,_ = swe.calc_ut(jd_utc, planet, flags = flags)
    reset_ayanamsa_mode()
```
- Observed behavior: combined flags are explicit and reset executes per-planet branch.

### EP07

- Behavior: `_rise_flags` is a combined bitmask defined with `|`.
- Source: `src/jhora/panchanga/drik.py:L52-L52`
- Excerpt:
```python
_rise_flags = swe.BIT_HINDU_RISING | swe.FLG_TRUEPOS | swe.FLG_SPEED # V3.2.3 # Speed flag added for retrogression
```
- Observed behavior: rise/set shared flag bundle is pre-composed once at module scope.

### EP08

- Behavior: rise/set callsites compose `rsmi` with `+` against `_rise_flags`.
- Source A: `src/jhora/panchanga/drik.py:L357-L357`
- Excerpt A:
```python
result = swe.rise_trans(jd_utc - tz/24, swe.SUN, geopos=(lon, lat,0.0), rsmi = _rise_flags + swe.CALC_RISE)
```
- Source B: `src/jhora/panchanga/drik.py:L426-L426`
- Excerpt B:
```python
result = swe.rise_trans(jd_utc - tz/24, swe.SUN, geopos=(lon, lat,0.0), rsmi = _rise_flags + swe.CALC_SET)
```
- Source C: `src/jhora/panchanga/drik.py:L448-L448`
- Excerpt C:
```python
result = swe.rise_trans(jd_utc - tz/24, swe.MOON, geopos=(lon, lat,0.0), rsmi = _rise_flags + swe.CALC_RISE)
```
- Source D: `src/jhora/panchanga/drik.py:L466-L466`
- Excerpt D:
```python
result = swe.rise_trans(jd_utc - tz/24, swe.MOON, geopos=(lon, lat,0.0), rsmi = _rise_flags + swe.CALC_SET)
```
- Observed behavior: operator in `rsmi` composition is `+` at all shown callsites.

### EP09

- Behavior: `bhaava_madhya_swe` calls `houses_ex(...)[0]` after sidereal set; no local reset appears.
- Source: `src/jhora/panchanga/drik.py:L1431-L1437`
- Excerpt:
```python
jd_utc = jd - (tz / 24.)
if const._TROPICAL_MODE:
    flags = swe.FLG_SWIEPH
else:
    flags = swe.FLG_SIDEREAL
    set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd) # needed for swe.houses_ex()
return list(swe.houses_ex(jd_utc, lat, lon,hsys, flags = flags)[0])
```
- Observed behavior: function returns cusps `[0]`; reset call is absent in shown body.

### EP10

- Behavior: `bhaava_madhya_kp` calls `houses_ex(...)[0]` after sidereal set; no local reset appears.
- Source: `src/jhora/panchanga/drik.py:L1445-L1451`
- Excerpt:
```python
jd_utc = jd - (tz / 24.)
if const._TROPICAL_MODE:
    flags = swe.FLG_SWIEPH
else:
    flags = swe.FLG_SIDEREAL
    set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd) # needed for swe.houses_ex()
return list(swe.houses_ex(jd_utc, lat, lon, flags = flags)[0])
```
- Observed behavior: function returns cusps `[0]`; reset call is absent in shown body.

### EP11

- Behavior: `ascendant` reads `houses_ex(...)[1][0]` and performs reset before return.
- Source: `src/jhora/panchanga/drik.py:L1483-L1490`
- Excerpt:
```python
flags = swe.FLG_SIDEREAL
set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd) # needed for swe.houses_ex()
nirayana_lagna = swe.houses_ex(jd_utc, lat, lon, flags = flags)[1][0]
nak_no,paadha_no,_ = nakshatra_pada(nirayana_lagna)
constellation = int(nirayana_lagna / 30)
coordinates = nirayana_lagna-constellation*30
reset_ayanamsa_mode()
return [constellation, coordinates, nak_no, paadha_no]
```
- Observed behavior: ascmc index path is `[1][0]` and state reset is in-function.

### EP12

- Behavior: local civil-time conversion calls `utc_time_zone` then `utc_to_jd(..., 0, ...)`.
- Source: `src/jhora/utils.py:L717-L720`
- Excerpt:
```python
y, m, d, h, mnt, s = swe.utc_time_zone(year, month, day, hour, minutes, seconds, timezone)
# BUG in pyswisseph: replace 0 by s
jd_et, jd_ut1 = swe.utc_to_jd(y, m, d, h, mnt, 0, flag = swe.GREG_CAL)
return jd_ut1
```
- Observed behavior: `seconds` parameter exists but SwissEph call passes `0` in shown line.

### EP13

- Behavior: helper `_function` sets sidereal mode and calls `fixstar_ut` with combined flag expression.
- Source: `src/jhora/utils.py:L601-L608`
- Excerpt:
```python
swe.set_sid_mode(swe.SIDM_USER, point, 0.0)
#swe.set_sid_mode(swe.SIDM_LAHIRI)
# Place Revati at 359°50'
#fval = norm180(swe.fixstar_ut("Revati", point, flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0]) - ((359 + 49/60 + 59/3600) - 360)
# Place Revati at 0°0'0"
#fval = norm180(swe.fixstar_ut("Revati", point, flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0])
# Place Citra at 180°
fval = swe.fixstar_ut("Citra", point, flag = swe.FLG_SWIEPH | swe.FLG_SIDEREAL)[0] - (180)
```
- Observed behavior: shown active line uses `fixstar_ut` with `FLG_SWIEPH | FLG_SIDEREAL`.

### EP14

- Behavior: eclipse paths use SwissEph eclipse APIs with flags on `sol_eclipse_how` path.
- Source A: `src/jhora/panchanga/drik.py:L2297-L2300`
- Excerpt A:
```python
flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | _rise_flags
ret,_ = swe.sol_eclipse_how(jd_utc,geopos=(lon, lat,0.0),flags=flags)
```
- Source B: `src/jhora/panchanga/drik.py:L2338-L2339`
- Excerpt B:
```python
geopos = (place.latitude, place.longitude,0.0)
retflag,tret,attrs = swe.sol_eclipse_when_loc(jd,geopos)
```
- Source C: `src/jhora/panchanga/drik.py:L2377-L2378`
- Excerpt C:
```python
geopos = (place.latitude, place.longitude,0.0)
retflag,tret,attrs = swe.lun_eclipse_when_loc(jd,geopos)
```
- Observed behavior: one branch shows explicit combined flags, and location-based finders are called directly.

### EP15

- Behavior: JD helper conversions use `julday`/`revjul` in utility definitions.
- Source: `src/jhora/utils.py:L694-L698`
- Excerpt:
```python
jd = swe.julday(date_of_birth_as_tuple[0],date_of_birth_as_tuple[1],date_of_birth_as_tuple[2],tob_in_hours)
return jd
# Julian Day number as on (year, month, day) at 00:00 UTC
gregorian_to_jd = lambda date: swe.julday(date.year, date.month, date.day, 0.0)
jd_to_gregorian = lambda jd: swe.revjul(jd, swe.GREG_CAL)   # returns (y, m, d, fh
```
- Observed behavior: core conversion helpers bind SwissEph JD APIs into module-level contracts.

### EP16

- Behavior: vratha paths compute search ranges from repeated `swe.julday(...)` bases.
- Source A: `src/jhora/panchanga/vratha.py:L183-L184`
- Excerpt A:
```python
cur_jd = swe.julday(panchanga_start_date.year,panchanga_start_date.month,panchanga_start_date.day,sunrise_hours)
end_jd = swe.julday(_end_date.year,_end_date.month,_end_date.day,sunrise_hours)
```
- Source B: `src/jhora/panchanga/vratha.py:L478-L483`
- Excerpt B:
```python
jd_start = swe.julday(start_date.year,start_date.month,start_date.day,9.0)# get around cur_sunrise
if end_date is None :
    _end_date = utils.next_panchanga_day(start_date, 365)
else:
    _end_date = panchanga.Date(end_date.year,end_date.month,end_date.day)
jd_end = swe.julday(_end_date.year,_end_date.month,_end_date.day,9.0)
```
- Observed behavior: same SwissEph day-number builder is reused with differing hour anchors.

### EP17

- Behavior: Tajaka docstrings include `swe.julday(...)` as caller guidance text.
- Source: `src/jhora/horoscope/transit/tajaka.py:L397-L397`
- Excerpt:
```python
Note: You can use swe.julday(dob_year,dob_month,dob_day,tob_hour+tob_minutes/60.0+tob_seconds/3600.0) to get
```
- Observed behavior: this is a non-executable mention inside docstring text.

### EP18

- Behavior: `swe.version` has no executable match in Core-7 scan output.
- Source: `research/ephemeris_engine_contracts/_coverage_ephemeris_callsites_core.tsv:L2-L2`
- Excerpt:
```text
Core-7	0	version	not_found	EP18
```
- Observed behavior: absence is recorded as ledger evidence.

### EP900

- Behavior: residual ephemeris callsites not expanded into dedicated anchors EP01..EP18.
- Source: `research/ephemeris_engine_contracts/_coverage_ephemeris_callsites_core.tsv`
- Excerpt:
```text
Rows with anchor_id=EP900 are retained as residual inventory entries for Core-7.
```
- Observed behavior: coverage ledger keeps unmapped callsites explicit instead of dropping them.

## Conflict / ambiguity register

- UNCERTAIN-EP-STATE-01: asymmetry between `set_ayanamsa_mode` and `reset_ayanamsa_mode` exists across ephemeris callsites.
  - Evidence A (reset present in same function): `sidereal_longitude` calls `reset_ayanamsa_mode()` after `calc_ut`. [EP04]
  - Evidence B (reset absent in same function): `bhaava_madhya_swe` and `bhaava_madhya_kp` call `set_ayanamsa_mode(...)` and return without local reset. [EP09, EP10]
  - Cross-impact (fact): all cited paths invoke SwissEph sidereal-dependent calls (`calc_ut` or `houses_ex`).

## Coverage ledger

- Inventory file: `research/ephemeris_engine_contracts/_coverage_ephemeris_callsites_core.tsv`
- Inventory columns: `file`, `line`, `pattern`, `function_context`, `anchor_id`
- Inventory row count: `66`
- Unique `(file,function_context)` count: `41`
- `swe.version` status: `not_found` in Core-7 (`EP18` row present)
- Residual rows with `EP900`: `25`

## Acceptance / DoD reinforcement

- Flag/rsmi anchors include explicit operator form where combination exists.
  - `flags = ... | ...` is shown in EP04/EP05/EP06/EP07/EP13/EP14.
  - `rsmi = _rise_flags + swe.CALC_*` is shown in EP08.
- `UNCERTAIN-EP-STATE-01` includes in-function reset and no-reset evidence.
- `swe.version` absence is logged in ledger as evidence-of-absence row.

## Sanity checks

- command: `rg -n "^### EP[0-9]+|^### EP900" research/ephemeris_engine_contracts/ephemeris_behavior_contract_map.core.md -S`
- command: `rg -n "UNCERTAIN-EP-STATE-01" research/ephemeris_engine_contracts/ephemeris_behavior_contract_map.core.md -S`
- command: `rg -n "swe\.version|version\tnot_found" research/ephemeris_engine_contracts/ephemeris_behavior_contract_map.core.md research/ephemeris_engine_contracts/_coverage_ephemeris_callsites_core.tsv -S`
- command: `Get-Content research/ephemeris_engine_contracts/_coverage_ephemeris_callsites_core.tsv | Measure-Object -Line`
