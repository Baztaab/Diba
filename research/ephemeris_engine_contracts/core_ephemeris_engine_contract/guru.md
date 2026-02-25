# PyJHora-only

## E05 — sidereal_longitude SwissEph calc contract

- provenance: `src/jhora/panchanga/drik.py:L222-L232`

```python
    if const._TROPICAL_MODE:
        flags = swe.FLG_SWIEPH
    else:
        flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | _rise_flags
        #set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd)
        set_ayanamsa_mode(_ayanamsa_default,_ayanamsa_value,jd_utc); _ayanamsa_mode = const._DEFAULT_AYANAMSA_MODE
        #print('drik sidereal long ayanamsa',_ayanamsa_mode, const._DEFAULT_AYANAMSA_MODE)
```

- provenance: `src/jhora/panchanga/drik.py:L230-L232`

```python
    longi,_ = swe.calc_ut(jd_utc, planet, flags = flags)
    reset_ayanamsa_mode()
    return utils.norm360(longi[0]) # degrees
```

## E06 — rise/set flag bundle

- provenance: `src/jhora/panchanga/drik.py:L52-L52`

```python
_rise_flags = swe.BIT_HINDU_RISING | swe.FLG_TRUEPOS | swe.FLG_SPEED # V3.2.3 # Speed flag added for retrogression
```

## E07 — Ephemeris path set at import

- provenance: `src/jhora/const.py:L174-L175`

```python
_ephe_path = os.path.abspath(_EPHIMERIDE_DATA_PATH)
swe.set_ephe_path(_ephe_path)
```

## E03 — rise_trans call contract

- provenance: `src/jhora/panchanga/drik.py:L356-L358`

```python
    _,lat, lon, tz = place
    result = swe.rise_trans(jd_utc - tz/24, swe.SUN, geopos=(lon, lat,0.0), rsmi = _rise_flags + swe.CALC_RISE)
    rise_jd = result[1][0]  # julian-day number
```
