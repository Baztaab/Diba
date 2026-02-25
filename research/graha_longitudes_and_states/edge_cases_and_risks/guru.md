# PyJHora-only

## E28 — Ketu speed assignment from Rahu entry

- provenance: `src/jhora/panchanga/drik.py:L280-L287`

```python
    for planet in planet_list:
        planet_index = planet_list.index(planet)
        if planet == const._KETU:
            _planets_speed_info[planet_index] = _planets_speed_info[planet_list.index(const._RAHU)]
            continue
        longi,_ = swe.calc_ut(jd_utc, planet, flags = flags)
        reset_ayanamsa_mode()
```
