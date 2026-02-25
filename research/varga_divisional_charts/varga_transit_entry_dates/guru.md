# PyJHora-only

## Divisional chart planet entry date wrappers and stepping

Source: `src/jhora/horoscope/chart/charts.py:L2007-L2012`

```python
def previous_planet_entry_date_divisional_chart(jd,place,planet,divisional_chart_factor=1,chart_method=1,base_rasi=None,
                              count_from_end_of_sign=None,increment_days=1,precision=0.1,raasi=None):
    return next_planet_entry_date_divisional_chart(jd,place,planet,divisional_chart_factor=divisional_chart_factor,direction=-1,
                                  chart_method=chart_method,base_rasi=base_rasi,
                                  count_from_end_of_sign=count_from_end_of_sign,increment_days=increment_days,
                                  precision=precision,raasi=raasi)
```

Source: `src/jhora/horoscope/chart/charts.py:L2033-L2041`

```python
    increment_days=1.0/24.0/60.0/divisional_chart_factor if planet in ['L',1] else 0.1/divisional_chart_factor
    planet_index = 0 if planet=='L' else planet+1
    sla = divisional_chart(jd, place, divisional_chart_factor=divisional_chart_factor, 
                chart_method=chart_method,base_rasi=base_rasi, count_from_end_of_sign=count_from_end_of_sign)[planet_index][1]
    sl = sla[0]*30+sla[1]
    if raasi==None:
        multiple = (((sl//30)+1)%12)*30
        if direction==-1: multiple = (sl//30)%12*30
        if planet == 7:
```

Source: `src/jhora/horoscope/chart/charts.py:L2048-L2054`

```python
    while True:
        if sl < (multiple+precision) and sl>(multiple-precision):
            break
        jd += increment_days*direction
        sla = divisional_chart(jd, place, divisional_chart_factor=divisional_chart_factor, 
                    chart_method=chart_method,base_rasi=base_rasi, count_from_end_of_sign=count_from_end_of_sign)[planet_index][1]
        sl = sla[0]*30+sla[1]
```

Source: `src/jhora/horoscope/chart/charts.py:L2056-L2064`

```python
    offsets = [t*0.25 for t in range(-5,5)] if planet !='L' else [t*increment_days for t in range(-5,5)]
    planet_longs = []
    for t in offsets:
        sla = divisional_chart(jd+t, place, divisional_chart_factor=divisional_chart_factor, 
                    chart_method=chart_method,base_rasi=base_rasi, count_from_end_of_sign=count_from_end_of_sign)[planet_index][1]
        sl = sla[0]*30+sla[1]
        planet_longs.append(sl)
    planet_hour = utils.inverse_lagrange(offsets, planet_longs, multiple) # Do not move % 360 above
    jd += planet_hour
```

Source: `src/jhora/horoscope/chart/charts.py:L2065-L2068`

```python
    sla = divisional_chart(jd, place, divisional_chart_factor=divisional_chart_factor, 
                chart_method=chart_method,base_rasi=base_rasi, count_from_end_of_sign=count_from_end_of_sign)[planet_index][1]
    planet_long = sla[0]*30+sla[1]
    return jd,planet_long
```

## Mixed chart planet entry date wrappers and stepping

Source: `src/jhora/horoscope/chart/charts.py:L2070-L2075`

```python
def previous_planet_entry_date_mixed_chart(jd,place,planet,varga_factor_1=None,chart_method_1=None,
                                       varga_factor_2=None,chart_method_2=None,
                                       direction=1,precision=0.1,raasi=None):
    return next_planet_entry_date_mixed_chart(jd,place,planet,varga_factor_1=varga_factor_1,
                            chart_method_1=chart_method_1,varga_factor_2=varga_factor_2,chart_method_2=chart_method_2,
                                       direction=1,precision=0.1,raasi=None)
```

Source: `src/jhora/horoscope/chart/charts.py:L2091-L2099`

```python
    increment_days=1.0/24.0/60.0 if planet in ['L'] else 0.1
    planet_index = 0 if planet=='L' else planet+1
    sla = mixed_chart(jd, place, varga_factor_1=varga_factor_1, chart_method_1=chart_method_1,
                      varga_factor_2=varga_factor_2, chart_method_2=chart_method_2)[planet_index][1]
    sl = sla[0]*30+sla[1]
    if raasi==None:
        multiple = (((sl//30)+1)%12)*30
        if direction==-1: multiple = (sl//30)%12*30
    else: 
```

Source: `src/jhora/horoscope/chart/charts.py:L2101-L2107`

```python
    while True:
        if sl < (multiple+precision) and sl>(multiple-precision):
            break
        jd += increment_days*direction
        sla = mixed_chart(jd, place, varga_factor_1=varga_factor_1, chart_method_1=chart_method_1,
                      varga_factor_2=varga_factor_2, chart_method_2=chart_method_2)[planet_index][1]
        sl = sla[0]*30+sla[1]
```

Source: `src/jhora/horoscope/chart/charts.py:L2108-L2114`

```python
    offsets = [t*0.25 for t in range(-5,5)] if planet !='L' else [t*increment_days for t in range(-5,5)]
    planet_longs = []
    for t in offsets:
        sla = mixed_chart(jd, place, varga_factor_1=varga_factor_1, chart_method_1=chart_method_1,
                      varga_factor_2=varga_factor_2, chart_method_2=chart_method_2)[planet_index][1]
        sl = sla[0]*30+sla[1]
        planet_longs.append(sl)
```

Source: `src/jhora/horoscope/chart/charts.py:L2116-L2121`

```python
    planet_hour = utils.inverse_lagrange(offsets, planet_longs, multiple) # Do not move % 360 above
    jd += planet_hour
    sla = mixed_chart(jd, place, varga_factor_1=varga_factor_1, chart_method_1=chart_method_1,
                      varga_factor_2=varga_factor_2, chart_method_2=chart_method_2)[planet_index][1]
    planet_long = sla[0]*30+sla[1]
    return jd,planet_long
```

## Divisional conjunction search path

Source: `src/jhora/horoscope/chart/charts.py:L2136-L2143`

```python
    _planet_speeds = [361]+[abs(psi[3]) for p,psi in drik.planets_speed_info(jd, place).items()]
    p1_speed = _planet_speeds[0] if p1=='L' else _planet_speeds[p1+1]
    p2_speed = _planet_speeds[0] if p2=='L' else _planet_speeds[p2+1]
    increment_days = increment_speed_factor/p1_speed if p1_speed > p2_speed else increment_speed_factor/p2_speed
    _DEBUG_ = False
    if (p1==const.RAHU_ID and p2==const.KETU_ID) or (p1==const.KETU_ID and p2==const.RAHU_ID):
        warnings.warn("Rahu and Ketu do not conjoin ever. Program returns error")
        return None
```

Source: `src/jhora/horoscope/chart/charts.py:L2149-L2156`

```python
    while search_counter < max_days_to_search:
        cur_jd += increment_days
        sla = divisional_chart(cur_jd, place, divisional_chart_factor=divisional_chart_factor, 
                    chart_method=chart_method,base_rasi=base_rasi, count_from_end_of_sign=count_from_end_of_sign)[pi1][1]
        p1_long = sla[0]*30+sla[1]
        sla = divisional_chart(cur_jd, place, divisional_chart_factor=divisional_chart_factor, 
                    chart_method=chart_method,base_rasi=base_rasi, count_from_end_of_sign=count_from_end_of_sign)[pi2][1]
        p2_long = sla[0]*30+sla[1]
```

Source: `src/jhora/horoscope/chart/charts.py:L2165-L2172`

```python
                sla = divisional_chart(jdt, place, divisional_chart_factor=divisional_chart_factor, 
                            chart_method=chart_method,base_rasi=base_rasi, count_from_end_of_sign=count_from_end_of_sign)[pi1][1]
                p1_long = sla[0]*30+sla[1]
                sla = divisional_chart(jdt, place, divisional_chart_factor=divisional_chart_factor, 
                            chart_method=chart_method,base_rasi=base_rasi, count_from_end_of_sign=count_from_end_of_sign)[pi2][1]
                p2_long = sla[0]*30+sla[1]
                long_diff = (360+p1_long-p2_long-separation_angle)%360
                long_diff_list.append(long_diff)
```

Source: `src/jhora/horoscope/chart/charts.py:L2177-L2183`

```python
                conj_jd = utils.inverse_lagrange(jd_list, long_diff_list, 0.0)
                sla = divisional_chart(conj_jd, place, divisional_chart_factor=divisional_chart_factor, 
                            chart_method=chart_method,base_rasi=base_rasi, count_from_end_of_sign=count_from_end_of_sign)[pi1][1]
                p1_long = sla[0]*30+sla[1]
                sla = divisional_chart(conj_jd, place, divisional_chart_factor=divisional_chart_factor, 
                            chart_method=chart_method,base_rasi=base_rasi, count_from_end_of_sign=count_from_end_of_sign)[pi2][1]
                p2_long = sla[0]*30+sla[1]
```

Source: `src/jhora/horoscope/chart/charts.py:L2192-L2198`

```python
                    sla = divisional_chart(conj_jd, place, divisional_chart_factor=divisional_chart_factor, 
                                chart_method=chart_method,base_rasi=base_rasi, count_from_end_of_sign=count_from_end_of_sign)[pi1][1]
                    p1_long = sla[0]*30+sla[1]
                    sla = divisional_chart(conj_jd, place, divisional_chart_factor=divisional_chart_factor, 
                                chart_method=chart_method,base_rasi=base_rasi, count_from_end_of_sign=count_from_end_of_sign)[pi2][1]
                    p2_long = sla[0]*30+sla[1]
                    return conj_jd, p1_long, p2_long
```

## Root-finding helper used in varga transit tuning

Source: `src/jhora/utils.py:L631-L639`

```python
def inverse_lagrange(x, y, ya):
  """Given two lists x and y, find the value of x = xa when y = ya, i.e., f(xa) = ya"""
  assert(len(x) == len(y))
  total = 0
  for i in range(len(x)):
    numer = 1
    denom = 1
    for j in range(len(x)):
      if j != i:
```
