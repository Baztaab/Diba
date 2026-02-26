# time_behavior_contract_map.core.md

## Snapshot identity (FACTS)

- pyjhora_root: `D:\lab\Pyjhora`
- extraction_timestamp_local: `2026-02-26 22:18:33 +03:30`
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
  - experiements
  - `src/jhora/panchanga/drik1.py`

## Behavior taxonomy (FACTS)

- timezone source and fallback: `T01`, `T02`, `T901`
- JD/JD_UTC basis and conversion helpers: `T03`, `T04`, `T05`, `T06`, `T08`, `T09`, `T10`, `T11`
- sunrise-anchored panchanga behavior: `T12`, `T19`, `T20`, `T21`
- calendar base-time and use_utc branching: `T16`, `T17`, `T24`
- sidereal state coupling with time basis: `T05`, `T06`, `T13`, `T14`, `T15`, `T18`, `T23`, `T32`
- transit coupling that consumes sunrise/sunset windows: `T27`, `T28`, `T29`
- time constants and thresholds: `T30`, `T31`

## Evidence anchors (T01..T32)

### T01

- Behavior: `utils.get_place_timezone_offset` uses `TimezoneFinder` + `datetime.now()` and returns fallback `+5.0` on exception.
- Source: `src/jhora/utils.py:L306-L327`
- Excerpt:
```python
def get_place_timezone_offset(latitude, longitude):
    try:
        tf = TimezoneFinder()
        today = datetime.datetime.now()
        tz_target = timezone(tf.timezone_at(lng=longitude, lat=latitude))
        today_target = tz_target.localize(today)
        today_utc = utc.localize(today)
        tz_offset = (today_utc - today_target).total_seconds() / 3600.0
        return tz_offset
    except Exception as err:
        print('WARNING: Time Zone returned as default +5.0. Need to change it')
        return 5.0
```
- Observed behavior: offset path is runtime-now based; failure path returns fixed numeric fallback.

### T02

- Behavior: missing DOB/TOB in `_validate_data` are auto-filled with current date/time; invalid divisional factor defaults to `1`.
- Source: `src/jhora/utils.py:L135-L148`
- Excerpt:
```python
if dob is None:
    today = datetime.datetime.today()
    dob = (today.year,today.month,today.day)
    print("Today's Date:",dob,'assumed')
if tob is None:
    tob = tuple(str(datetime.datetime.now()).split()[1].split(':'))
    print('Current time:',tob,'assumed')
if division_chart_factor not in const.division_chart_factors:
    warnings.warn(w_msg)
    divisional_chart_factor = 1
```
- Observed behavior: defaults mutate civil-time input assumptions before downstream JD conversion.

### T03

- Behavior: canonical helper relations include `julian_day_utc`, `gregorian_to_jd`, and `jd_to_gregorian`.
- Source: `src/jhora/utils.py:L675-L703`
- Excerpt:
```python
def julian_day_utc(julian_day,place):
     return julian_day - (place.timezone / 24.)
# Julian Day number as on (year, month, day) at 00:00 UTC
gregorian_to_jd = lambda date: swe.julday(date.year, date.month, date.day, 0.0)
jd_to_gregorian = lambda jd: swe.revjul(jd, swe.GREG_CAL)
def jd_to_local(jd,place):
    y, m, d,_  = jd_to_gregorian(jd)
    jd_utc = gregorian_to_jd(drik.Date(y, m, d))
    fhl = (jd - jd_utc) * 24 + place.timezone
```
- Observed behavior: conversion helpers encode local/UTC projection formulas explicitly.

### T04

- Behavior: local civil-time to UT1 uses `utc_time_zone` and calls `utc_to_jd` with seconds argument `0`.
- Source: `src/jhora/utils.py:L715-L720`
- Excerpt:
```python
def local_time_to_jdut1(year, month, day, hour = 0, minutes = 0, seconds = 0, timezone = 0.0):
  y, m, d, h, mnt, s = swe.utc_time_zone(year, month, day, hour, minutes, seconds, timezone)
  jd_et, jd_ut1 = swe.utc_to_jd(y, m, d, h, mnt, 0, flag = swe.GREG_CAL)
  return jd_ut1
```
- Observed behavior: function signature accepts `seconds`, but call passes `0` to SwissEph conversion.

### T05

- Behavior: `sidereal_longitude` requires UTC JD input, sets sidereal mode with `jd_utc`, calls `calc_ut`, resets mode, returns normalized longitude.
- Source: `src/jhora/panchanga/drik.py:L204-L232`
- Excerpt:
```python
def sidereal_longitude(jd_utc, planet):
    """
          JD_UTC = JD - Place.TimeZoneInFloatHours
    """
    if const._TROPICAL_MODE:
        flags = swe.FLG_SWIEPH
    else:
        flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | _rise_flags
        set_ayanamsa_mode(_ayanamsa_default,_ayanamsa_value,jd_utc)
    longi,_ = swe.calc_ut(jd_utc, planet, flags = flags)
    reset_ayanamsa_mode()
    return utils.norm360(longi[0])
```
- Observed behavior: callsite basis is `jd_utc` and normalization occurs after raw vector read.

### T06

- Behavior: `planets_in_retrograde` derives `jd_utc = jd - timezone/24`, but sets ayanamsa with `jd`; retrograde state uses sign of `longi[3]`.
- Source: `src/jhora/panchanga/drik.py:L233-L253`
- Excerpt:
```python
def planets_in_retrograde(jd,place):
    jd_utc = jd - place.timezone / 24.
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | _rise_flags
    set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd)
    for planet in _planet_list:
        longi,_ = swe.calc_ut(jd_utc, planet, flags = flags)
        reset_ayanamsa_mode()
        if longi[3]<0 : retro_planets.append(p_id)
```
- Observed behavior: mixed basis appears in same function (`jd_utc` for `calc_ut`, `jd` for set-mode).

### T07

- Behavior: speed info path rounds raw SwissEph vector with fixed factors; multi-planet path copies Ketu speed from Rahu slot.
- Source: `src/jhora/panchanga/drik.py:L254-L288`
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
    _planets_speed_info[planet_index] = [round(l,round_factors[i]) for i,l in enumerate(longi)]
```
- Observed behavior: output rounding contract is fixed and node speed linkage is explicit.

### T08

- Behavior: sunrise converts local JD to date-based `jd_utc`, calls `rise_trans(CALC_RISE)`, then recomputes local rise JD.
- Source: `src/jhora/panchanga/drik.py:L344-L365`
- Excerpt:
```python
y, m, d,_  = jd_to_gregorian(jd)
jd_utc = utils.gregorian_to_jd(Date(y, m, d))
_,lat, lon, tz = place
result = swe.rise_trans(jd_utc - tz/24, swe.SUN, geopos=(lon, lat,0.0), rsmi = _rise_flags + swe.CALC_RISE)
rise_jd = result[1][0]
rise_local_time = (rise_jd - jd_utc) * 24 + tz
tob = tuple(utils.to_dms(rise_local_time, as_string=False))
rise_jd = utils.julian_day_number(dob, tob)
```
- Observed behavior: function returns local-time-form rise and recalculated local JD value.

### T09

- Behavior: sunset uses the same date-based `jd_utc` pattern with `rise_trans(CALC_SET)`.
- Source: `src/jhora/panchanga/drik.py:L414-L435`
- Excerpt:
```python
y, m, d,_  = jd_to_gregorian(jd)
jd_utc = utils.gregorian_to_jd(Date(y, m, d))
_,lat, lon, tz = place
result = swe.rise_trans(jd_utc - tz/24, swe.SUN, geopos=(lon, lat,0.0), rsmi = _rise_flags + swe.CALC_SET)
set_jd = result[1][0]
set_local_time = (set_jd - jd_utc) * 24 + tz
```
- Observed behavior: solar set path is parallel to sunrise but with `CALC_SET`.

### T10

- Behavior: moonrise uses date-based `jd_utc` and `rise_trans(CALC_RISE)` for moon.
- Source: `src/jhora/panchanga/drik.py:L436-L452`
- Excerpt:
```python
y, m, d, h = jd_to_gregorian(jd)
jd_utc = utils.gregorian_to_jd(Date(y, m, d))
city, lat, lon, tz = place
result = swe.rise_trans(jd_utc - tz/24, swe.MOON, geopos=(lon, lat,0.0), rsmi = _rise_flags + swe.CALC_RISE)
rise = result[1][0]
local_time = (rise - jd_utc) * 24 + tz
```
- Observed behavior: moonrise output uses same local-time projection formula as sunrise/sunset.

### T11

- Behavior: moonset uses date-based `jd_utc` and `rise_trans(CALC_SET)` for moon.
- Source: `src/jhora/panchanga/drik.py:L454-L470`
- Excerpt:
```python
y, m, d, h = jd_to_gregorian(jd)
jd_utc = utils.gregorian_to_jd(Date(y, m, d))
city, lat, lon, tz = place
result = swe.rise_trans(jd_utc - tz/24, swe.MOON, geopos=(lon, lat,0.0), rsmi = _rise_flags + swe.CALC_SET)
setting = result[1][0]
local_time = (setting - jd_utc) * 24 + tz
```
- Observed behavior: moonset mirrors moonrise with `CALC_SET` selector.

### T12

- Behavior: `_get_tithi` anchors phase computation to sunrise JD.
- Source: `src/jhora/panchanga/drik.py:L477-L488`
- Excerpt:
```python
tz = place.timezone
y, m, d,bt = jd_to_gregorian(jd)
jd_utc = utils.gregorian_to_jd(Date(y, m, d))
rise = sunrise(jd, place)[2]
moon_phase = _special_tithi_phase(rise, planet1, planet2, tithi_index, cycle)
today = ceil(moon_phase / 12)
if const.increase_tithi_by_one_before_kali_yuga and jd < const.mahabharatha_tithi_julian_day:
```
- Observed behavior: tithi phase basis is sunrise-derived, not direct input `jd`.

### T13

- Behavior: `bhaava_madhya_swe` validates house code, converts to `hsys`, derives `jd_utc`, sets ayanamsa with `jd`, returns `houses_ex(...)[0]`.
- Source: `src/jhora/panchanga/drik.py:L1424-L1437`
- Excerpt:
```python
if house_code not in const.western_house_systems.keys():
    warnings.warn(warn_msg)
    house_code = 'P'
hsys = bytes(house_code,encoding='ascii')
_, lat, lon, tz = place
jd_utc = jd - (tz / 24.)
flags = swe.FLG_SIDEREAL
set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd)
return list(swe.houses_ex(jd_utc, lat, lon,hsys, flags = flags)[0])
```
- Observed behavior: set basis is `jd`; output index is cusps list `[0]`.

### T14

- Behavior: `bhaava_madhya_kp` derives `jd_utc`, sets ayanamsa with `jd`, returns `houses_ex(...)[0]`.
- Source: `src/jhora/panchanga/drik.py:L1438-L1451`
- Excerpt:
```python
def bhaava_madhya_kp(jd,place):
    _, lat, lon, tz = place
    jd_utc = jd - (tz / 24.)
    if const._TROPICAL_MODE:
        flags = swe.FLG_SWIEPH
    else:
        flags = swe.FLG_SIDEREAL
        set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd)
    return list(swe.houses_ex(jd_utc, lat, lon, flags = flags)[0])
```
- Observed behavior: house cusp path also uses `jd` for set-mode and `jd_utc` for `houses_ex`.

### T15

- Behavior: `ascendant` uses `houses_ex(...)[1][0]` and calls `reset_ayanamsa_mode()` before return.
- Source: `src/jhora/panchanga/drik.py:L1477-L1490`
- Excerpt:
```python
_, lat, lon, tz = place
jd_utc = jd - (tz / 24.)
flags = swe.FLG_SIDEREAL
set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd)
nirayana_lagna = swe.houses_ex(jd_utc, lat, lon, flags = flags)[1][0]
coordinates = nirayana_lagna-constellation*30
reset_ayanamsa_mode()
return [constellation, coordinates, nak_no, paadha_no]
```
- Observed behavior: ascmc index path and in-function reset are explicit.

### T16

- Behavior: `tamil_solar_month_and_date` dispatches method variants and forwards `base_time/use_utc` to new method branch.
- Source: `src/jhora/panchanga/drik.py:L2055-L2074`
- Excerpt:
```python
def tamil_solar_month_and_date(panchanga_date,place,tamil_month_method=const.tamil_month_method,base_time=0,use_utc=True):
    if tamil_month_method==0:
        return tamil_solar_month_and_date_RaviAnnnaswamy(panchanga_date, place)
    elif tamil_month_method==1:
        return tamil_solar_month_and_date_V4_3_5(panchanga_date, place)
    elif tamil_month_method==2:
        return tamil_solar_month_and_date_V4_3_8(panchanga_date, place)
    else:
        return tamil_solar_month_and_date_new(panchanga_date, place, base_time, use_utc)
```
- Observed behavior: method routing controls whether `base_time/use_utc` are used.

### T17

- Behavior: `tamil_solar_month_and_date_new` derives `jd_base` from sunset/sunrise/midday and optionally converts to `jd_utc` by `use_utc`.
- Source: `src/jhora/panchanga/drik.py:L2075-L2092`
- Excerpt:
```python
def tamil_solar_month_and_date_new(panchanga_date,place,base_time=0,use_utc=True):
    jd = utils.julian_day_number(panchanga_date, (10,0,0))
    jd_base = sunset(jd, place)[2] if base_time==0 else (sunrise(jd,place)[2] if base_time==1 else midday(jd, place)[1])
    jd_utc = jd_base - place.timezone/24 if use_utc else jd_base
    sr = solar_longitude(jd_utc)
    while True:
        jd -= 1
        jd_base = sunset(jd, place)[2] if base_time==0 else (sunrise(jd,place)[2] if base_time==1 else midday(jd, place)[1])
        jd_utc = jd_base - place.timezone/24 if use_utc else jd_base
```
- Observed behavior: both `base_time` and `use_utc` directly affect longitude search timeline.

### T18

- Behavior: `next_planet_retrograde_change_date` nested helper sets ayanamsa with `jd` argument, while caller iterates on `jd_utc` timeline and converts back to local basis at return.
- Source: `src/jhora/panchanga/drik.py:L2711-L2730`
- Excerpt:
```python
def _get_planet_longitude_sign(planet,jd):
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | _rise_flags
    set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd)
    longi,_ = swe.calc_ut(jd, pl, flags = flags)
    if longi[3] < 0: sl_sign = -1
jd = utils.gregorian_to_jd(panchanga_date)
jd_utc = jd - place.timezone/24.0
while sl_sign == sl_sign_next:
    jd_utc += increment_days*direction
jd_utc += place.timezone/24.0
```
- Observed behavior: helper call signature is generic `jd`; caller passes `jd_utc` values.

### T19

- Behavior: `vratha.pradosham_dates` uses `gregorian_to_jd` date basis and sunset to produce local pradosham window.
- Source: `src/jhora/panchanga/vratha.py:L154-L166`
- Excerpt:
```python
def pradosham_dates(panchanga_place,panchanga_start_date,panchanga_end_date=None):
    _tz = panchanga_place.timezone
    for pdate,_,_ ,tag_t in pdates:
        panch_date = panchanga.Date(pdate[0],pdate[1],pdate[2])
        cur_jd = utils.gregorian_to_jd(panch_date); jd_utc=cur_jd
        sunset = panchanga.sunset(cur_jd, panchanga_place)[2]
        pradosham_start = (sunset - jd_utc) * 24 + _tz+pradosham_sunset_offset[0]
        pradosham_end = (sunset - jd_utc) * 24 + _tz+pradosham_sunset_offset[1]
```
- Observed behavior: local pradosham interval is computed from date-based JD and sunset anchor.

### T20

- Behavior: `vratha._get_conjunction_time` keeps date-based `jd_utc` and contains explicit comment rejecting direct `jd - tz/24` in this function.
- Source: `src/jhora/panchanga/vratha.py:L324-L353`
- Excerpt:
```python
def _get_conjunction_time(jd,place,p1,p2):
    tz = place.timezone
    yjd, mjd, djd, _ = utils.jd_to_gregorian(jd)
    jd_utc = utils.gregorian_to_jd(panchanga.Date(yjd, mjd, djd))
    #jd_utc = jd - tz/24. ### It appears this way calculating jd_utc is incorrect
    rise = panchanga.sunrise(jd, place)[2]
```
- Observed behavior: function documents an in-code disagreement against the direct offset formula.

### T21

- Behavior: vratha crescent-date helpers consume sunset/moonset outputs from drik time functions.
- Source: `src/jhora/panchanga/vratha.py:L552-L568`
- Excerpt:
```python
jd = utils.gregorian_to_jd(panchanga.Date(c_date[0],c_date[1],c_date[2]))
sunset = panchanga.sunset(jd, panchanga_place)[0]
moonset = panchanga.moonset(jd, panchanga_place)[0]
results.append((c_date,sunset,moonset,tag))
```
- Observed behavior: vratha output tags include moonset/sunset-dependent windows.

### T22

- Behavior: Surya Siddhantha path reads sunrise and date-based `jd_utc` in the same computation block.
- Source: `src/jhora/panchanga/surya_sidhantha.py:L124-L131`
- Excerpt:
```python
sun_rise = drik.sunrise(jd, place)
jd_sunrise = sun_rise[-1]
y, m, d,_  = utils.jd_to_gregorian(jd)
jd_utc = utils.gregorian_to_jd(drik.Date(y, m, d))
time_from_sunrise_vinadi = (jd-jd_sunrise)*24/2.5*60
```
- Observed behavior: function consumes both sunrise-derived and date-derived time bases.

### T23

- Behavior: Surya Siddhantha ascendant branch sets ayanamsa with `jd` when sidereal mode is active.
- Source: `src/jhora/panchanga/surya_sidhantha.py:L174-L180`
- Excerpt:
```python
if const._TROPICAL_MODE:
    flags = swe.FLG_SWIEPH
else:
    flags = swe.FLG_SIDEREAL
    drik.set_ayanamsa_mode(drik._ayanamsa_mode,drik._ayanamsa_value,jd)
```
- Observed behavior: sidereal setup callsite here is `jd`-based.

### T24

- Behavior: `surya_sidhantha.solar_month_and_date` signature includes `base_time/use_utc`, but current body uses direct planet longitude path while old `jd_base/jd_utc` logic is commented.
- Source: `src/jhora/panchanga/surya_sidhantha.py:L446-L470`
- Excerpt:
```python
def solar_month_and_date(panchanga_date,place,base_time=0,use_utc=True):
    jd = utils.julian_day_number(panchanga_date, (10,0,0))
    #jd_base = sunset(jd, place)[2] if base_time==0 else ...
    #jd_utc = jd_base - place.timezone/24 if use_utc else jd_base
    solar_mean_long = _planet_mean_longitude(jd, place, const._SUN)
    sr = _planet_true_longitude(jd, place, const._SUN, solar_mean_long)
    while True:
        jd -= 1
        #jd_utc = jd_base - place.timezone/24 if use_utc else jd_base
```
- Observed behavior: runtime branch ignores `use_utc` and `base_time` in active lines.

### T25

- Behavior: `charts.rasi_chart` obtains ascendant and dhasavarga from the same `jd_years/place` input and prepends lagna row.
- Source: `src/jhora/horoscope/chart/charts.py:L95-L107`
- Excerpt:
```python
ascendant_constellation, ascendant_longitude, _, _ = drik.ascendant(jd_years,place_as_tuple)
planet_positions = drik.dhasavarga(jd_years,place_as_tuple,divisional_chart_factor=1)
planet_positions = [[ascendant_index,(ascendant_constellation, ascendant_longitude)]] + planet_positions
```
- Observed behavior: time basis is shared between lagna and planet payload packaging.

### T26

- Behavior: `_bhaava_madhya_new` defaults invalid house method to `1` and routes method `4` / western codes to drik house backends.
- Source: `src/jhora/horoscope/chart/charts.py:L136-L166`
- Excerpt:
```python
if bhava_madhya_method not in const.available_house_systems.keys():
    warnings.warn(warn_msg)
    bhava_madhya_method = 1
ascendant_full_longitude = (ascendant_constellation*30+ascendant_longitude)%360
elif bhava_madhya_method ==4 or bhava_madhya_method in const.western_house_systems.keys():
    bm = drik.bhaava_madhya_kp(jd, place) if bhava_madhya_method ==4 else drik.bhaava_madhya_swe(jd, place, house_code=bhava_madhya_method)
```
- Observed behavior: house-time semantics are delegated to drik backend by method routing.

### T27

- Behavior: Tajaka module binds year stepping to `const.sidereal_year`.
- Source: `src/jhora/horoscope/transit/tajaka.py:L22-L25`
- Excerpt:
```python
from jhora import const,utils
from jhora.panchanga import drik
year_value = const.sidereal_year
```
- Observed behavior: annual timeline base is sidereal-year constant.

### T28

- Behavior: Tajaka yearly lord path determines night/day birth by comparing `tob_hrs` with sunrise/sunset at progressed JD.
- Source: `src/jhora/horoscope/transit/tajaka.py:L520-L534`
- Excerpt:
```python
jd_at_years = jd_at_dob + years_from_dob*year_value
tob_hrs = drik.jd_to_gregorian(jd_at_years)[3]
sunrise = utils.from_dms_str_to_dms(drik.sunrise(jd_at_years, place)[1])
sunset = utils.from_dms_str_to_dms(drik.sunset(jd_at_years, place)[1])
night_time_birth = tob_hrs > sunset_hrs or tob_hrs < sunrise_hrs
```
- Observed behavior: annual transit logic consumes drik sunrise/sunset outputs as thresholds.

### T29

- Behavior: Tajaka monthly lord path repeats sunrise/sunset threshold logic on month-shifted JD.
- Source: `src/jhora/horoscope/transit/tajaka.py:L552-L560`
- Excerpt:
```python
jd_at_years = jd_at_dob + (years_from_dob+months_from_dob/12.0)*year_value
tob_hrs = drik.jd_to_gregorian(jd_at_years)[3]
sunrise = utils.from_dms_str_to_dms(drik.sunrise(jd_at_years, place)[1])
sunset = utils.from_dms_str_to_dms(drik.sunset(jd_at_years, place)[1])
night_time_birth = tob_hrs > sunset_hrs or tob_hrs < sunrise_hrs
```
- Observed behavior: same threshold contract is reused for month-level progression.

### T30

- Behavior: const time constants include `sidereal_year`, `tropical_year`, and related year-length constants.
- Source: `src/jhora/const.py:L174-L180`
- Excerpt:
```python
_ephe_path = os.path.abspath(_EPHIMERIDE_DATA_PATH)
swe.set_ephe_path(_ephe_path)
sidereal_year = 365.256364
tropical_year = 365.242190
```
- Observed behavior: time progression constants are globally defined at import scope.

### T31

- Behavior: tithi-skip threshold uses fixed Julian-day constant.
- Source: `src/jhora/const.py:L599-L603`
- Excerpt:
```python
increase_tithi_by_one_before_kali_yuga = True
mahabharatha_tithi_julian_day = 588465.5
```
- Observed behavior: historical threshold is numeric constant consumed in tithi logic.

### T32

- Behavior: `set_ayanamsa_mode` mutates default mode and supports `jd`-dependent mode branches (`SENTHIL`, `SUNDAR_SS`).
- Source: `src/jhora/panchanga/drik.py:L117-L149`
- Excerpt:
```python
def set_ayanamsa_mode(ayanamsa_mode = None,ayanamsa_value=None,jd=None):
    if key == "SENTHIL":
        _ayanamsa_value = _calculate_ayanamsa_senthil_from_jd(jd)
    elif key == "SUNDAR_SS":
        _ayanamsa_value = _ayanamsa_surya_siddhantha_model(jd)
    _ayanamsa_mode = ayanamsa_mode
    const._DEFAULT_AYANAMSA_MODE = _ayanamsa_mode
```
- Observed behavior: set-mode mutates module/global default and may depend on supplied `jd`.

### T901

- Behavior: residual temporal callsites in `utils.py` not captured by focused anchors T01..T04.
- Source: `src/jhora/utils.py:L1-L1448`
- Excerpt:
```python
from pytz import timezone, utc
from timezonefinder import TimezoneFinder
```
- Observed behavior: full per-line evidence is listed in `_coverage_time_callsites_core.tsv` with `anchor_id=T901`.

### T902

- Behavior: residual temporal callsites in `drik.py` not captured by focused anchors T05..T18 and T32.
- Source: `src/jhora/panchanga/drik.py:L1-L3455`
- Excerpt:
```python
Place = struct('Place', ['Place','latitude', 'longitude', 'timezone'])
```
- Observed behavior: full per-line evidence is listed in `_coverage_time_callsites_core.tsv` with `anchor_id=T902`.

### T903

- Behavior: residual temporal callsites in `vratha.py` not captured by focused anchors T19..T21.
- Source: `src/jhora/panchanga/vratha.py:L1-L851`
- Excerpt:
```python
import swisseph as swe
```
- Observed behavior: full per-line evidence is listed in `_coverage_time_callsites_core.tsv` with `anchor_id=T903`.

### T904

- Behavior: residual temporal callsites in `surya_sidhantha.py` not captured by focused anchors T22..T24.
- Source: `src/jhora/panchanga/surya_sidhantha.py:L1-L549`
- Excerpt:
```python
from jhora.panchanga import drik
```
- Observed behavior: full per-line evidence is listed in `_coverage_time_callsites_core.tsv` with `anchor_id=T904`.

### T905

- Behavior: residual temporal callsites in `charts.py` not captured by focused anchors T25..T26.
- Source: `src/jhora/horoscope/chart/charts.py:L1-L2343`
- Excerpt:
```python
from jhora.panchanga import drik
```
- Observed behavior: full per-line evidence is listed in `_coverage_time_callsites_core.tsv` with `anchor_id=T905`.

### T906

- Behavior: residual temporal callsites in `tajaka.py` not captured by focused anchors T27..T29.
- Source: `src/jhora/horoscope/transit/tajaka.py:L1-L660`
- Excerpt:
```python
from jhora.panchanga import drik
```
- Observed behavior: full per-line evidence is listed in `_coverage_time_callsites_core.tsv` with `anchor_id=T906`.

### T907

- Behavior: residual temporal callsites in `const.py` outside focused anchors T30..T31.
- Source: `src/jhora/const.py:L1-L1235`
- Excerpt:
```python
_other_upagraha_list = ['kaala','mrityu','artha_prabhakara','yama','gulika','maandi']
```
- Observed behavior: full per-line evidence is listed in `_coverage_time_callsites_core.tsv` with `anchor_id=T907`.

## Conflict / ambiguity register

- UNCERTAIN-U01: `jd_utc` derivation is not uniform across all paths.
  - Evidence A: direct-offset pattern appears in multiple callsites (`jd_utc = jd - timezone/24`). [T03, T06, T17]
  - Evidence B: `vratha._get_conjunction_time` comment explicitly marks direct-offset variant as incorrect in that function. [T20]

- UNCERTAIN-U02: sidereal state reset discipline is inconsistent across time-coupled callsites.
  - Evidence A: `sidereal_longitude` and `ascendant` include in-function reset. [T05, T15]
  - Evidence B: `bhaava_madhya_swe`, `bhaava_madhya_kp`, and nested helper in retrograde-change path set sidereal mode without local reset in the shown function body. [T13, T14, T18]

- UNCERTAIN-U03: `use_utc/base_time` parameters are active in `drik` month-date flow but currently inactive in `surya_sidhantha` active lines.
  - Evidence A: `drik.tamil_solar_month_and_date_new` uses `base_time` and `use_utc` in executed code. [T17]
  - Evidence B: `surya_sidhantha.solar_month_and_date` keeps `base_time/use_utc` in signature/docstring but the `jd_base/jd_utc` lines are commented in active body. [T24]

- UNCERTAIN-U04: timezone offset path uses runtime current datetime, while computational paths may target arbitrary historical/future JDs.
  - Evidence A: timezone offset uses `datetime.datetime.now()` in `get_place_timezone_offset`. [T01]
  - Evidence B: calculation paths consume arbitrary input JDs and progressed dates across panchanga/transit flows. [T08, T17, T28, T29]

## Coverage ledger

- Inventory file: `research/kala_time/_coverage_time_callsites_core.tsv`
- Inventory columns: `file`, `line`, `pattern`, `function_context`, `anchor_id`
- Inventory row count: `682`
- Unique `(file,function_context)` count: `191`
- Function-context to anchor mapping (complete):

```text
src/jhora/const.py::<module> -> T31
src/jhora/horoscope/chart/charts.py::_amsa -> T905
src/jhora/horoscope/chart/charts.py::_bhaava_madhya_new -> T905
src/jhora/horoscope/chart/charts.py::_varnada_lagna_bv_raman -> T905
src/jhora/horoscope/chart/charts.py::_varnada_lagna_bv_raman_mixed_chart -> T905
src/jhora/horoscope/chart/charts.py::_varnada_lagna_jha_pandey -> T905
src/jhora/horoscope/chart/charts.py::_varnada_lagna_jha_pandey_mixed_chart -> T905
src/jhora/horoscope/chart/charts.py::_varnada_lagna_sanjay_rath -> T905
src/jhora/horoscope/chart/charts.py::_varnada_lagna_sanjay_rath_mixed_chart -> T905
src/jhora/horoscope/chart/charts.py::_varnada_lagna_santhanam -> T905
src/jhora/horoscope/chart/charts.py::_varnada_lagna_sharma -> T905
src/jhora/horoscope/chart/charts.py::_varnada_lagna_sharma_mixed_chart -> T905
src/jhora/horoscope/chart/charts.py::bhava_chart_houses -> T905
src/jhora/horoscope/chart/charts.py::divisional_chart -> T905
src/jhora/horoscope/chart/charts.py::get_22nd_drekkana -> T905
src/jhora/horoscope/chart/charts.py::next_conjunction_of_planet_pair_divisional_chart -> T905
src/jhora/horoscope/chart/charts.py::next_planet_entry_date_divisional_chart -> T905
src/jhora/horoscope/chart/charts.py::next_planet_entry_date_mixed_chart -> T905
src/jhora/horoscope/chart/charts.py::rasi_chart -> T905
src/jhora/horoscope/chart/charts.py::special_lagna_longitudes -> T905
src/jhora/horoscope/chart/charts.py::special_planet_longitudes -> T905
src/jhora/horoscope/chart/charts.py::vaiseshikamsa_dhasavarga_of_planets -> T905
src/jhora/horoscope/chart/charts.py::vaiseshikamsa_sapthavarga_of_planets -> T905
src/jhora/horoscope/chart/charts.py::vaiseshikamsa_shadvarga_of_planets -> T905
src/jhora/horoscope/chart/charts.py::vaiseshikamsa_shodhasavarga_of_planets -> T905
src/jhora/horoscope/chart/charts.py::varnada_lagna -> T905
src/jhora/horoscope/chart/charts.py::varnada_lagna_mixed_chart -> T905
src/jhora/horoscope/chart/charts.py::vimsamsavarga_of_planets -> T905
src/jhora/horoscope/chart/charts.py::vimsopaka_dhasavarga_of_planets -> T905
src/jhora/horoscope/chart/charts.py::vimsopaka_sapthavarga_of_planets -> T905
src/jhora/horoscope/chart/charts.py::vimsopaka_shadvarga_of_planets -> T905
src/jhora/horoscope/chart/charts.py::vimsopaka_shodhasavarga_of_planets -> T905
src/jhora/horoscope/transit/tajaka.py::annual_chart -> T906
src/jhora/horoscope/transit/tajaka.py::annual_chart_approximate -> T906
src/jhora/horoscope/transit/tajaka.py::lord_of_the_month -> T29,T906
src/jhora/horoscope/transit/tajaka.py::lord_of_the_year -> T28,T906
src/jhora/horoscope/transit/tajaka.py::monthly_chart -> T906
src/jhora/horoscope/transit/tajaka.py::sixty_hour_chart -> T906
src/jhora/panchanga/drik.py::__next_conjunction_of_planet_pair -> T902
src/jhora/panchanga/drik.py::__next_solar_jd -> T902
src/jhora/panchanga/drik.py::_bhaava_madhya_new -> T902
src/jhora/panchanga/drik.py::_birthtime_rectification_lagna_suddhi -> T902
src/jhora/panchanga/drik.py::_get_estimated_nakshatra -> T902
src/jhora/panchanga/drik.py::_get_nakshathra -> T902
src/jhora/panchanga/drik.py::_get_nakshathra_new -> T902
src/jhora/panchanga/drik.py::_get_nakshathra_old -> T902
src/jhora/panchanga/drik.py::_get_planet_longitude_sign -> T18
src/jhora/panchanga/drik.py::_get_tithi -> T12,T902
src/jhora/panchanga/drik.py::_get_tithi_using_planet_speed -> T902
src/jhora/panchanga/drik.py::_get_yogam -> T902
src/jhora/panchanga/drik.py::_get_yogam_new -> T902
src/jhora/panchanga/drik.py::_nisheka_time -> T902
src/jhora/panchanga/drik.py::_nisheka_time_1 -> T902
src/jhora/panchanga/drik.py::_planet_speed_info -> T07
src/jhora/panchanga/drik.py::_previous_sankranti_date_new -> T902
src/jhora/panchanga/drik.py::<module> -> T902
src/jhora/panchanga/drik.py::aadal_yoga -> T902
src/jhora/panchanga/drik.py::abhijit_muhurta -> T902
src/jhora/panchanga/drik.py::ascendant -> T15,T902
src/jhora/panchanga/drik.py::bhaava_madhya -> T902
src/jhora/panchanga/drik.py::bhaava_madhya_kp -> T14
src/jhora/panchanga/drik.py::bhaava_madhya_swe -> T13
src/jhora/panchanga/drik.py::brahma_muhurtha -> T902
src/jhora/panchanga/drik.py::chandrabalam -> T902
src/jhora/panchanga/drik.py::chandrashtama -> T902
src/jhora/panchanga/drik.py::day_length -> T902
src/jhora/panchanga/drik.py::days_in_tamil_month -> T902
src/jhora/panchanga/drik.py::declination_of_planets -> T902
src/jhora/panchanga/drik.py::dhasavarga -> T902
src/jhora/panchanga/drik.py::durmuhurtam -> T902
src/jhora/panchanga/drik.py::elapsed_year -> T902
src/jhora/panchanga/drik.py::float_hours_to_vedic_time -> T902
src/jhora/panchanga/drik.py::float_hours_to_vedic_time_equal_day_night_ghati -> T902
src/jhora/panchanga/drik.py::fraction_moon_yet_to_traverse -> T902
src/jhora/panchanga/drik.py::gauri_choghadiya -> T902
src/jhora/panchanga/drik.py::get_ayanamsa_value -> T902
src/jhora/panchanga/drik.py::godhuli_muhurtha -> T902
src/jhora/panchanga/drik.py::is_night_birth -> T902
src/jhora/panchanga/drik.py::is_solar_eclipse -> T902
src/jhora/panchanga/drik.py::karaka_yogam -> T902
src/jhora/panchanga/drik.py::karana -> T902
src/jhora/panchanga/drik.py::lat_distance -> T902
src/jhora/panchanga/drik.py::lunar_month -> T902
src/jhora/panchanga/drik.py::lunar_month_date -> T902
src/jhora/panchanga/drik.py::lunar_year_index -> T902
src/jhora/panchanga/drik.py::midday -> T902
src/jhora/panchanga/drik.py::midnight -> T902
src/jhora/panchanga/drik.py::moonrise -> T10
src/jhora/panchanga/drik.py::moonset -> T11
src/jhora/panchanga/drik.py::muhurthas -> T902
src/jhora/panchanga/drik.py::nakshatra -> T902
src/jhora/panchanga/drik.py::nakshatra_new -> T902
src/jhora/panchanga/drik.py::next_annual_solar_date_approximate -> T902
src/jhora/panchanga/drik.py::next_ascendant_entry_date -> T902
src/jhora/panchanga/drik.py::next_conjunction_of_planet_pair -> T902
src/jhora/panchanga/drik.py::next_lunar_eclipse -> T902
src/jhora/panchanga/drik.py::next_lunar_month -> T902
src/jhora/panchanga/drik.py::next_lunar_year -> T902
src/jhora/panchanga/drik.py::next_planet_entry_date -> T902
src/jhora/panchanga/drik.py::next_planet_retrograde_change_date -> T902
src/jhora/panchanga/drik.py::next_sankranti_date -> T902
src/jhora/panchanga/drik.py::next_solar_date -> T902
src/jhora/panchanga/drik.py::next_solar_eclipse -> T902
src/jhora/panchanga/drik.py::next_tithi -> T902
src/jhora/panchanga/drik.py::night_length -> T902
src/jhora/panchanga/drik.py::nishita_kaala -> T902
src/jhora/panchanga/drik.py::nishita_muhurtha -> T902
src/jhora/panchanga/drik.py::planetary_positions -> T902
src/jhora/panchanga/drik.py::planets_in_retrograde -> T06
src/jhora/panchanga/drik.py::planets_speed_info -> T07
src/jhora/panchanga/drik.py::pranapada_lagna -> T902
src/jhora/panchanga/drik.py::pranapada_lagna_mixed_chart -> T902
src/jhora/panchanga/drik.py::previous_lunar_month -> T902
src/jhora/panchanga/drik.py::previous_lunar_year -> T902
src/jhora/panchanga/drik.py::previous_sankranti_date -> T902
src/jhora/panchanga/drik.py::pushkara_yoga -> T902
src/jhora/panchanga/drik.py::raasi -> T902
src/jhora/panchanga/drik.py::sahasra_chandrodayam -> T902
src/jhora/panchanga/drik.py::sahasra_chandrodayam_old -> T902
src/jhora/panchanga/drik.py::samvatsara -> T902
src/jhora/panchanga/drik.py::sandhya_periods -> T902
src/jhora/panchanga/drik.py::set_ayanamsa_mode -> T32,T902
src/jhora/panchanga/drik.py::shubha_hora -> T902
src/jhora/panchanga/drik.py::sidereal_longitude -> T05
src/jhora/panchanga/drik.py::special_ascendant -> T902
src/jhora/panchanga/drik.py::special_ascendant_mixed_chart -> T902
src/jhora/panchanga/drik.py::sunrise -> T08
src/jhora/panchanga/drik.py::sunset -> T09
src/jhora/panchanga/drik.py::tamil_jaamam -> T902
src/jhora/panchanga/drik.py::tamil_solar_month_and_date -> T16
src/jhora/panchanga/drik.py::tamil_solar_month_and_date_from_jd -> T902
src/jhora/panchanga/drik.py::tamil_solar_month_and_date_new -> T17
src/jhora/panchanga/drik.py::tamil_solar_month_and_date_RaviAnnnaswamy -> T902
src/jhora/panchanga/drik.py::tamil_solar_month_and_date_V4_3_5 -> T902
src/jhora/panchanga/drik.py::tamil_solar_month_and_date_V4_3_8 -> T902
src/jhora/panchanga/drik.py::tithi -> T902
src/jhora/panchanga/drik.py::tithi_using_inverse_lagrange -> T902
src/jhora/panchanga/drik.py::tithi_using_planet_speed -> T902
src/jhora/panchanga/drik.py::triguna -> T902
src/jhora/panchanga/drik.py::trikalam -> T902
src/jhora/panchanga/drik.py::udhaya_lagna_muhurtha -> T902
src/jhora/panchanga/drik.py::upagraha_longitude -> T902
src/jhora/panchanga/drik.py::vedic_date -> T902
src/jhora/panchanga/drik.py::vidaal_yoga -> T902
src/jhora/panchanga/drik.py::vijaya_muhurtha -> T902
src/jhora/panchanga/drik.py::vivaha_chakra_palan -> T902
src/jhora/panchanga/drik.py::yogam -> T902
src/jhora/panchanga/drik.py::yogam_old -> T902
src/jhora/panchanga/surya_sidhantha.py::_balachandra_rao_basic_program -> T904
src/jhora/panchanga/surya_sidhantha.py::_declination_of_sun -> T904
src/jhora/panchanga/surya_sidhantha.py::_delination -> T22,T23,T904
src/jhora/panchanga/surya_sidhantha.py::kali_ahargana -> T904
src/jhora/panchanga/surya_sidhantha.py::nakshatra -> T904
src/jhora/panchanga/surya_sidhantha.py::planet_positions -> T904
src/jhora/panchanga/surya_sidhantha.py::solar_month_and_date -> T24
src/jhora/panchanga/surya_sidhantha.py::tithi -> T904
src/jhora/panchanga/vratha.py::_get_conjunction_time -> T20,T903
src/jhora/panchanga/vratha.py::_get_conjunction_time_1 -> T20
src/jhora/panchanga/vratha.py::_get_criteria_for_the_day -> T903
src/jhora/panchanga/vratha.py::chandra_dharshan_dates -> T21
src/jhora/panchanga/vratha.py::conjunctions -> T903
src/jhora/panchanga/vratha.py::get_festival -> T903
src/jhora/panchanga/vratha.py::get_festivals_between_the_dates -> T903
src/jhora/panchanga/vratha.py::get_festivals_of_the_day -> T903
src/jhora/panchanga/vratha.py::mahalaya_paksha_dates -> T903
src/jhora/panchanga/vratha.py::moondraam_pirai_dates -> T21
src/jhora/panchanga/vratha.py::nakshathra_dates -> T903
src/jhora/panchanga/vratha.py::pradosham_dates -> T19
src/jhora/panchanga/vratha.py::sankranti_dates -> T903
src/jhora/panchanga/vratha.py::search -> T903
src/jhora/panchanga/vratha.py::tithi_dates -> T903
src/jhora/panchanga/vratha.py::tithi_pravesha -> T903
src/jhora/panchanga/vratha.py::yoga_dates -> T903
src/jhora/utils.py::_convert_to_tamil_date_and_time -> T901
src/jhora/utils.py::_get_place_from_ipinfo -> T901
src/jhora/utils.py::_get_timezone_from_pytz -> T01
src/jhora/utils.py::_scrap_google_map_for_latlongtz_from_city_with_country -> T901
src/jhora/utils.py::<module> -> T901
src/jhora/utils.py::get_dob_years_months_60hrs_from_today -> T901
src/jhora/utils.py::get_location -> T901
src/jhora/utils.py::get_location_using_nominatim -> T901
src/jhora/utils.py::get_place_from_user_ip_address -> T901
src/jhora/utils.py::get_place_timezone_offset -> T01
src/jhora/utils.py::jd_to_local -> T03
src/jhora/utils.py::julian_day_number -> T03
src/jhora/utils.py::julian_day_number_new -> T03
src/jhora/utils.py::julian_day_to_date_time_string -> T901
src/jhora/utils.py::julian_day_utc -> T03
src/jhora/utils.py::local_time_to_jdut1 -> T04
src/jhora/utils.py::scrap_google_map_for_latlongtz_from_city_with_country -> T901
src/jhora/utils.py::udhayadhi_nazhikai -> T901

```

## Sanity checks

- command: `rg -n "^### T[0-9]+|^### T9[0-9]{2}" research/kala_time/time_behavior_contract_map.core.md -S`
  - result: `39`
- command: `rg -n "UNCERTAIN" research/kala_time/time_behavior_contract_map.core.md -S`
  - result: `5`
- command: `rg -n "Source:" research/kala_time/time_behavior_contract_map.core.md -S`
  - result: `40`
- command: `Get-Content research/kala_time/_coverage_time_callsites_core.tsv | Measure-Object -Line`
  - result: `683`
