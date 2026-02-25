# PyJHora-only

## E25/E30 — ascmc output index and local reset in ascendant

- provenance: `src/jhora/panchanga/drik.py:L1484-L1489`

```python
        set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd) # needed for swe.houses_ex()
    nirayana_lagna = swe.houses_ex(jd_utc, lat, lon, flags = flags)[1][0]
    nak_no,paadha_no,_ = nakshatra_pada(nirayana_lagna)
    constellation = int(nirayana_lagna / 30)
    coordinates = nirayana_lagna-constellation*30
    reset_ayanamsa_mode()
```

## E29 — direct return in house paths

- provenance: `src/jhora/panchanga/drik.py:L1435-L1437`

```python
        flags = swe.FLG_SIDEREAL
        set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd) # needed for swe.houses_ex()
    return list(swe.houses_ex(jd_utc, lat, lon,hsys, flags = flags)[0])
```
