# PyJHora-only

## E13 — Rahu/Ketu SwissEph mapping

- provenance: `src/jhora/const.py:L53-L54`

```python
_KETU = -swe.MEAN_NODE; KETU_ID = 8
_RAHU = swe.MEAN_NODE; RAHU_ID = 7
```

## E16 — _planet_speed_info calc_ut and rounding

- provenance: `src/jhora/panchanga/drik.py:L260-L264`

```python
    round_factors = [3,3,4,3,3,6]
    jd_utc = jd - place.timezone / 24.
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | _rise_flags
    longi,_ = swe.calc_ut(jd_utc, planet, flags = flags)
    return [round(l,round_factors[i]) for i,l in enumerate(longi)]
```

## E28 — calc_ut retrograde pattern

- provenance: `src/jhora/panchanga/drik.py:L248-L252`

```python
    for planet in _planet_list:
        p_id = _sideral_planet_list.index(planet)
        longi,_ = swe.calc_ut(jd_utc, planet, flags = flags)
        reset_ayanamsa_mode()
        if longi[3]<0 : retro_planets.append(p_id)
```

## E31 — calc_ut sign helper pattern

- provenance: `src/jhora/panchanga/drik.py:L2712-L2717`

```python
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | _rise_flags
    set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd)
    longi,_ = swe.calc_ut(jd, pl, flags = flags)
    sl_sign = 1
    if longi[3] < 0: sl_sign = -1
    return sl_sign
```
