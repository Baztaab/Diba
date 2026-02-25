# PyJHora-only

## E14 — rasi_chart Lagna + dhasavarga packaging

- provenance: `src/jhora/horoscope/chart/charts.py:L95-L107`

```python
    ascendant_index = const._ascendant_symbol
    " Get Ascendant information"
    ascendant_constellation, ascendant_longitude, _, _ = drik.ascendant(jd_years,place_as_tuple)
    """ FIXED in V2.3.1 - asc long re-calculated to get full longitude value """
    " Get planet information "
    " planet_positions lost: [planet_id, planet_constellation, planet_longitude] "
    planet_positions = drik.dhasavarga(jd_years,place_as_tuple,divisional_chart_factor=1)
    planet_positions = [[ascendant_index,(ascendant_constellation, ascendant_longitude)]] + planet_positions
    return planet_positions
```

## E23 — Lagna index assumption in house flow

- provenance: `src/jhora/horoscope/chart/charts.py:L140-L141`

```python
    ascendant_constellation, ascendant_longitude = planet_positions[0][1][0],planet_positions[0][1][1]
    ascendant_full_longitude = (ascendant_constellation*30+ascendant_longitude)%360
```

## E15 — KP/SwissEph backend selection

- provenance: `src/jhora/horoscope/chart/charts.py:L164-L164`

```python
        bm = drik.bhaava_madhya_kp(jd, place) if bhava_madhya_method ==4 else drik.bhaava_madhya_swe(jd, place, house_code=bhava_madhya_method)
```

## E25 — House code list and hsys conversion in bhaava_madhya_swe

- provenance: `src/jhora/panchanga/drik.py:L1408-L1421`

```python
        Acceptable house system codes in Swiss Ephemeris
        hsys= ‘P’     Placidus
            ‘K’     Koch
            ‘O’     Porphyrius
            ‘R’     Regiomontanus
            ‘C’     Campanus
            ‘A’ or ‘E’     Equal (cusp 1 is Ascendant)
            ‘V’     Vehlow equal (Asc. in middle of house 1)
            ‘X’     axial rotation system
            ‘H’     azimuthal or horizontal system
            ‘T’     Polich/Page (“topocentric” system)
            ‘B’     Alcabitus
```

- provenance: `src/jhora/panchanga/drik.py:L1428-L1437`

```python
    hsys = bytes(house_code,encoding='ascii')
    global _ayanamsa_mode,_ayanamsa_value
    _, lat, lon, tz = place
    jd_utc = jd - (tz / 24.)
    if const._TROPICAL_MODE:
        flags = swe.FLG_SWIEPH
    else:
        flags = swe.FLG_SIDEREAL
        set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd) # needed for swe.houses_ex()
```

## E24 — bhaava_madhya_kp jd_utc and houses_ex call

- provenance: `src/jhora/panchanga/drik.py:L1444-L1451`

```python
    _, lat, lon, tz = place
    jd_utc = jd - (tz / 24.)
    if const._TROPICAL_MODE:
        flags = swe.FLG_SWIEPH
    else:
        flags = swe.FLG_SIDEREAL
        set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd) # needed for swe.houses_ex()
    return list(swe.houses_ex(jd_utc, lat, lon, flags = flags)[0])
```
