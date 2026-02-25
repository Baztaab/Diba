# PyJHora-only

## E01 — JD_UTC relation in sidereal_longitude

- provenance: `src/jhora/panchanga/drik.py:L214-L216`

```python
              All other functions of this PyJHora library will require JD and not JD_UTC
              JD_UTC = JD - Place.TimeZoneInFloatHours
              For example for India JD_UTC = JD - 5.5. For wester time zone -5.0 it JD_UTC = JD - (-5.0)
```

## E02 — Local JD to jd_utc conversion

- provenance: `src/jhora/panchanga/drik.py:L243-L245`

```python
    jd_utc = jd - place.timezone / 24.
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | _rise_flags
    set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd)
```

## E03 — sunrise jd_utc path and rise_trans call

- provenance: `src/jhora/panchanga/drik.py:L353-L359`

```python
    y, m, d,_  = jd_to_gregorian(jd)
    jd_utc = utils.gregorian_to_jd(Date(y, m, d))

    _,lat, lon, tz = place
    result = swe.rise_trans(jd_utc - tz/24, swe.SUN, geopos=(lon, lat,0.0), rsmi = _rise_flags + swe.CALC_RISE)
    rise_jd = result[1][0]  # julian-day number
    rise_local_time = (rise_jd - jd_utc) * 24 + tz
```

- provenance: `src/jhora/panchanga/drik.py:L361-L363`

```python
    dob = (y,m,d)
    tob = tuple(utils.to_dms(rise_local_time, as_string=False))
    rise_jd = utils.julian_day_number(dob, tob)
```

## E04 — local_time_to_jdut1

- provenance: `src/jhora/utils.py:L715-L720`

```python
def local_time_to_jdut1(year, month, day, hour = 0, minutes = 0, seconds = 0, timezone = 0.0):
  """Converts local time to JD(UT1)"""
  y, m, d, h, mnt, s = swe.utc_time_zone(year, month, day, hour, minutes, seconds, timezone)
  # BUG in pyswisseph: replace 0 by s
  jd_et, jd_ut1 = swe.utc_to_jd(y, m, d, h, mnt, 0, flag = swe.GREG_CAL)
  return jd_ut1
```

## E21 — tithi anchor at sunrise jd

- provenance: `src/jhora/panchanga/drik.py:L479-L483`

```python
    y, m, d,bt = jd_to_gregorian(jd)
    jd_utc = utils.gregorian_to_jd(Date(y, m, d))
    # 1. Find time of sunrise
    rise = sunrise(jd, place)[2] # V2.2.8
```
