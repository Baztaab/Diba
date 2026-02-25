# PyJHora-only

## E28 — Loop-local reset pattern

- provenance: `src/jhora/panchanga/drik.py:L243-L252`

```python
    jd_utc = jd - place.timezone / 24.
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | _rise_flags
    set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd)
    retro_planets = []
    _planet_list = [p for p in _sideral_planet_list if p not in [const._RAHU, const._KETU]]
    for planet in _planet_list:
        p_id = _sideral_planet_list.index(planet)
        longi,_ = swe.calc_ut(jd_utc, planet, flags = flags)
        reset_ayanamsa_mode()
```

- provenance: `src/jhora/panchanga/drik.py:L276-L287`

```python
    jd_utc = jd - place.timezone / 24.
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | _rise_flags
    set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd)
    _planets_speed_info = {}
    for planet in planet_list:
        planet_index = planet_list.index(planet)
        if planet == const._KETU:
            _planets_speed_info[planet_index] = _planets_speed_info[planet_list.index(const._RAHU)]
            continue
```

## E29 — House functions return without local reset

- provenance: `src/jhora/panchanga/drik.py:L1435-L1437`

```python
        flags = swe.FLG_SIDEREAL
        set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd) # needed for swe.houses_ex()
    return list(swe.houses_ex(jd_utc, lat, lon,hsys, flags = flags)[0])
```

- provenance: `src/jhora/panchanga/drik.py:L1449-L1451`

```python
        flags = swe.FLG_SIDEREAL
        set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd) # needed for swe.houses_ex()
    return list(swe.houses_ex(jd_utc, lat, lon, flags = flags)[0])
```

## E30 — ascendant path resets before return

- provenance: `src/jhora/panchanga/drik.py:L1483-L1490`

```python
    else:
        flags = swe.FLG_SIDEREAL
        set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd) # needed for swe.houses_ex()
    nirayana_lagna = swe.houses_ex(jd_utc, lat, lon, flags = flags)[1][0]
    nak_no,paadha_no,_ = nakshatra_pada(nirayana_lagna)
    constellation = int(nirayana_lagna / 30)
    coordinates = nirayana_lagna-constellation*30
    reset_ayanamsa_mode()
```

## E31 — Nested helper call without local reset

- provenance: `src/jhora/panchanga/drik.py:L2711-L2717`

```python
def _get_planet_longitude_sign(planet,jd):
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | _rise_flags
    set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd)
    longi,_ = swe.calc_ut(jd, pl, flags = flags)
    sl_sign = 1
    if longi[3] < 0: sl_sign = -1
    return sl_sign
```
