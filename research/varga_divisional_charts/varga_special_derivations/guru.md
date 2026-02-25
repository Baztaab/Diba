# PyJHora-only

## Vaiseshikamsa and vimsopaka families

Source: `src/jhora/horoscope/chart/charts.py:L1211-L1211`

```python
    return _vaiseshikamsa_bala_of_planets(jd_at_dob, place_as_tuple,const.dhasavarga_amsa_vaiseshikamsa)
```

Source: `src/jhora/horoscope/chart/charts.py:L1223-L1223`

```python
    return _vaiseshikamsa_bala_of_planets(jd_at_dob, place_as_tuple,const.shadvarga_amsa_vaiseshikamsa)
```

Source: `src/jhora/horoscope/chart/charts.py:L1235-L1235`

```python
    return _vaiseshikamsa_bala_of_planets(jd_at_dob, place_as_tuple,const.sapthavarga_amsa_vaiseshikamsa)
```

Source: `src/jhora/horoscope/chart/charts.py:L1251-L1260`

```python
def _vaiseshikamsa_bala_of_planets(jd_at_dob, place_as_tuple,amsa_vaiseshikamsa=None):
    p_d = [0 for _ in const.SUN_TO_KETU]
    p_d_s = [0 for _ in const.SUN_TO_KETU]
    p_d_c = ['' for _ in const.SUN_TO_KETU]
    for dcf in amsa_vaiseshikamsa.keys():
        planet_positions = divisional_chart(jd_at_dob, place_as_tuple,divisional_chart_factor=dcf)[:const._pp_count_upto_ketu]
        for p,(h,_) in planet_positions:
            if p == const._ascendant_symbol:
                continue
            elif h==const.moola_trikona_of_planets[p] or const.house_strengths_of_planets[p][h] > const._FRIEND:
```

Source: `src/jhora/horoscope/chart/charts.py:L1260-L1268`

```python
            elif h==const.moola_trikona_of_planets[p] or const.house_strengths_of_planets[p][h] > const._FRIEND:
                p_d[p] += 1
                p_d_c[p] += 'D'+str(dcf)+'/'
                p_d_s[p] += amsa_vaiseshikamsa[dcf]#*vv
    pdc = {}
    for p in range(9):
        p_d_c[p] = p_d_c[p][:-1]
        pdc[p] = [p_d[p],p_d_c[p],p_d_s[p]]
    return pdc
```

Source: `src/jhora/horoscope/chart/charts.py:L1311-L1311`

```python
    return _vimsopaka_bala_of_planets(jd_at_dob, place_as_tuple,const.dhasavarga_amsa_vimsopaka)
```

Source: `src/jhora/horoscope/chart/charts.py:L1323-L1323`

```python
    return _vimsopaka_bala_of_planets(jd_at_dob, place_as_tuple,const.shadvarga_amsa_vimsopaka)
```

Source: `src/jhora/horoscope/chart/charts.py:L1335-L1335`

```python
    return _vimsopaka_bala_of_planets(jd_at_dob, place_as_tuple,const.sapthavarga_amsa_vimsopaka)
```

Source: `src/jhora/horoscope/chart/charts.py:L1350-L1350`

```python
    return _vimsopaka_bala_of_planets(jd_at_dob, place_as_tuple,const.shodhasa_varga_amsa_vimsopaka)
```

## Vimsamsavarga loop on divisional_chart

Source: `src/jhora/horoscope/chart/charts.py:L1365-L1370`

```python
    planet_vimsamsa = [0 for p in const.SUN_TO_KETU]
    for _, dcf in enumerate(const.vimsamsa_varga_amsa_factors):
        planet_positions = divisional_chart(jd_at_dob, place_as_tuple, divisional_chart_factor=dcf)
        for p,(h,_) in planet_positions:
            if p == const._ascendant_symbol:
                continue
```

## Special planet longitudes and amsa extraction

Source: `src/jhora/horoscope/chart/charts.py:L1800-L1806`

```python
def special_planet_longitudes_mixed_chart(dob,tob,place,varga_factor_1=1,chart_method_1=1,varga_factor_2=1,chart_method_2=1):
    spl_planet_positions_in_rasi = special_planet_longitudes(dob, tob, place)
    if varga_factor_1==1 and varga_factor_2==1: return spl_planet_positions_in_rasi
    pp1 = spl_planet_positions_in_rasi if varga_factor_1==1 else \
            eval(divisional_chart_functions[varga_factor_1]+'(spl_planet_positions_in_rasi,chart_method=chart_method_1)')
    pp2 = pp1 if varga_factor_2==2 else eval(divisional_chart_functions[varga_factor_2]+'(pp1,chart_method=chart_method_2)')
    return pp2
```

Source: `src/jhora/horoscope/chart/charts.py:L1824-L1830`

```python
    if divisional_chart_factor==1: return spl_rasi_positions
    if (not const.TREAT_STANDARD_CHART_AS_CUSTOM) and (divisional_chart_factor in divisional_chart_functions.keys()\
            and (base_rasi==None and (chart_method !=None and chart_method >0) )):
        return eval(divisional_chart_functions[divisional_chart_factor]+'(spl_rasi_positions,chart_method)')
    elif divisional_chart_factor in range(1,const.MAX_DHASAVARGA_FACTOR+1):
        return custom_divisional_chart(spl_rasi_positions, divisional_chart_factor=divisional_chart_factor,
                    chart_method=chart_method,base_rasi=base_rasi,count_from_end_of_sign=count_from_end_of_sign)
```

Source: `src/jhora/horoscope/chart/charts.py:L1858-L1864`

```python
def _amsa(jd,place,divisional_chart_factor=1,include_upagrahas=False,include_special_lagnas=False,include_sphutas=False,
            chart_method=1,base_rasi=None,count_from_end_of_sign=None):
    "TODO: Still under testing - Exact algorithm not clear"
    y,m,d,fh = utils.jd_to_gregorian(jd); dob = drik.Date(y,m,d); tob = (fh,0,0)
    div_planet_positions = divisional_chart(jd, place,divisional_chart_factor=divisional_chart_factor,
                                            chart_method=chart_method,base_rasi=base_rasi,
                                            count_from_end_of_sign=count_from_end_of_sign)
```

Source: `src/jhora/horoscope/chart/charts.py:L1865-L1868`

```python
    def _get_amsa_index_from_longitude(p_long):
        df = 30.0/divisional_chart_factor
        return int(p_long/df)
    __amsa_planets = {}; __amsa_special = {}; __amsa_upagraha = {}; __amsa_sphuta = {}
```

Source: `src/jhora/horoscope/chart/charts.py:L2219-L2228`

```python
def _amsa_d150(jd,place,divisional_chart_factor=1,include_upagrahas=False,
          include_special_lagnas=False,include_sphutas=False,chart_method=1,base_rasi=None,count_from_end_of_sign=None):
    #msgs = get_amsa_resources()
    planet_positions = divisional_chart(jd, place, divisional_chart_factor=divisional_chart_factor,
                            chart_method=chart_method,base_rasi=base_rasi, count_from_end_of_sign=count_from_end_of_sign)
    print(planet_positions)
    f1 = 30.0/divisional_chart_factor
    _ap = []
    for p,(h,long) in planet_positions:
        pstr = utils.resource_strings['ascendant_str'] if p==const._ascendant_symbol else utils.PLANET_NAMES[p]
```

Source: `src/jhora/horoscope/chart/charts.py:L2229-L2238`

```python
        _hora = int(long//f1)+1
        if h in const.movable_signs:
            _amsa = _hora
        elif h in const.fixed_signs:
            _amsa = (151-_hora)
        else:
            _amsa = (75+_hora)%151
        #print(pstr,msgs[str(150)][_amsa])
        _ap.append(_amsa)
    return _ap
```
