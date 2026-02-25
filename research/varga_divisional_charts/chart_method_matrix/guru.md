# PyJHora-only

## hora_chart

- chart_method values observed: `[1, 2, 3, 4, 5, 6]`

Source: `src/jhora/horoscope/chart/charts.py:L292-L303`

```python
    if chart_method==1:
        return __parivritti_even_reverse(planet_positions_in_rasi, 2)
    elif chart_method==2:
        return _hora_traditional_parasara_chart(planet_positions_in_rasi)
    elif chart_method==3:
        return _hora_chart_raman_method(planet_positions_in_rasi)
    elif chart_method==4:
        return __parivritti_cyclic(planet_positions_in_rasi, 2)
    elif chart_method==5:
        return _hora_chart_kashinath(planet_positions_in_rasi)
    elif chart_method==6:
        return __parivritti_alternate(planet_positions_in_rasi, 2)
```

## drekkana_chart

- chart_method values observed: `[1, 2, 3, 4, 5]`

Source: `src/jhora/horoscope/chart/charts.py:L349-L358`

```python
    if chart_method==1:
        return _drekkana_chart_parasara(planet_positions_in_rasi)
    elif chart_method==2:
        return __parivritti_cyclic(planet_positions_in_rasi, dvf)
    elif chart_method==3:
        return __parivritti_alternate(planet_positions_in_rasi, dvf)
    elif chart_method==4:
        return _drekkana_chart_jagannatha(planet_positions_in_rasi)
    elif chart_method==5:
        return __parivritti_even_reverse(planet_positions_in_rasi, dvf)
```

## chaturthamsa_chart

- chart_method values observed: `[1, 2, 3, 4]`

Source: `src/jhora/horoscope/chart/charts.py:L382-L389`

```python
    if chart_method==1:
        return _chaturthamsa_parasara(planet_positions_in_rasi)
    elif chart_method==2:
        return __parivritti_cyclic(planet_positions_in_rasi, 4)
    elif chart_method==3:
        return __parivritti_even_reverse(planet_positions_in_rasi, 4)
    elif chart_method==4:
        return __parivritti_alternate(planet_positions_in_rasi, 4)
```

## panchamsa_chart

- chart_method values observed: `[2, 3, 4]`

Source: `src/jhora/horoscope/chart/charts.py:L405-L410`

```python
    if chart_method==2:
        return __parivritti_cyclic(planet_positions_in_rasi, dvf)
    elif chart_method==3:
        return __parivritti_even_reverse(planet_positions_in_rasi, dvf)
    elif chart_method==4:
        return __parivritti_alternate(planet_positions_in_rasi, dvf)
```

## shashthamsa_chart

- chart_method values observed: `[2, 3, 4]`

Source: `src/jhora/horoscope/chart/charts.py:L438-L443`

```python
    if chart_method==2:
        return __parivritti_cyclic(planet_positions_in_rasi, dvf)
    elif chart_method==3:
        return __parivritti_even_reverse(planet_positions_in_rasi, dvf)
    elif chart_method==4:
        return __parivritti_alternate(planet_positions_in_rasi, dvf)
```

## saptamsa_chart

- chart_method values observed: `[1, 2, 3, 4, 5, 6]`

Source: `src/jhora/horoscope/chart/charts.py:L471-L476`

```python
    if chart_method==4:
        return __parivritti_cyclic(planet_positions_in_rasi, dvf)
    elif chart_method==5:
        return __parivritti_even_reverse(planet_positions_in_rasi, dvf)
    elif chart_method==6:
        return __parivritti_alternate(planet_positions_in_rasi, dvf)
```

Source: `src/jhora/horoscope/chart/charts.py:L479-L488`

```python
    dirn = -1 if chart_method in [2,3] else 1
    for planet,[sign,long] in planet_positions_in_rasi:
        d_long = (long*dvf)%30
        l = int(long // f1)
        r = (sign+l)%12
        if sign in const.even_signs:
            r = (sign+dirn*(l+const.HOUSE_7))%12
            if chart_method==3:
                r = (r-const.HOUSE_7)%12
        dp.append([planet,[r,d_long]])
```

## ashtamsa_chart

- chart_method values observed: `[2, 3, 4]`

Source: `src/jhora/horoscope/chart/charts.py:L505-L510`

```python
    if chart_method==2:
        return __parivritti_cyclic(planet_positions_in_rasi, dvf)
    elif chart_method==3:
        return __parivritti_even_reverse(planet_positions_in_rasi, dvf)
    elif chart_method==4:
        return __parivritti_alternate(planet_positions_in_rasi, dvf)
```

## navamsa_chart

- chart_method values observed: `[1, 2, 3, 4, 5, 6]`

Source: `src/jhora/horoscope/chart/charts.py:L548-L555`

```python
    if chart_method==5: # This also same as traditional UKM
        return __parivritti_cyclic(planet_positions_in_rasi, dvf)
    elif chart_method==2: # Uniform Krishna Navamsa Method
        return __parivritti_even_reverse(planet_positions_in_rasi, dvf)
    elif chart_method==6:
        return __parivritti_alternate(planet_positions_in_rasi, dvf)
    elif chart_method==3: # Kalachakra Navamsa
        return _navamsa_kalachakra(planet_positions_in_rasi)
```

Source: `src/jhora/horoscope/chart/charts.py:L558-L565`

```python
    if chart_method==4:
        navamsa_dict = {0:(1,const.fire_signs),3:(-1,const.water_signs),6:(1,const.air_signs),9:(-1,const.earth_signs)}
    dp = []
    for planet,[sign,long] in planet_positions_in_rasi:
        d_long = (long*dvf)%30
        l = int(long // f1)
        r = [(seed+dirn*l)%12 for seed,(dirn,sign_list) in navamsa_dict.items() if sign in sign_list][0]
        dp.append([planet,[r,d_long]])
```

## dasamsa_chart

- chart_method values observed: `[1, 2, 3, 4, 5, 6]`

Source: `src/jhora/horoscope/chart/charts.py:L584-L589`

```python
    if chart_method==4:
        return __parivritti_cyclic(planet_positions_in_rasi, dvf)
    elif chart_method==5:
        return __parivritti_even_reverse(planet_positions_in_rasi, dvf)
    elif chart_method==6:
        return __parivritti_alternate(planet_positions_in_rasi, dvf)
```

Source: `src/jhora/horoscope/chart/charts.py:L592-L601`

```python
    dirn = -1 if chart_method in [2,3] else 1
    for planet,[sign,long] in planet_positions_in_rasi:
        d_long = (long*dvf)%30
        l = int(long // f1)
        r = (sign+l)%12
        if sign in const.even_signs:
            r = (sign+dirn*(l+8))%12
            if chart_method==2:
                r = (r-8)%12
        dp.append([planet,[r,d_long]])
```

## rudramsa_chart

- chart_method values observed: `[2, 3, 4, 5]`

Source: `src/jhora/horoscope/chart/charts.py:L622-L627`

```python
    if chart_method==3:
        return __parivritti_cyclic(planet_positions_in_rasi, dvf)
    elif chart_method==4:
        return __parivritti_even_reverse(planet_positions_in_rasi, dvf)
    elif chart_method==5:
        return __parivritti_alternate(planet_positions_in_rasi, dvf)
```

Source: `src/jhora/horoscope/chart/charts.py:L633-L636`

```python
        r = (12-sign+l)%12
        if chart_method==2: r = (11-r)%12
        dp.append([planet,[r,d_long]])
    return dp
```

## dwadasamsa_chart

- chart_method values observed: `[2, 3, 4, 5]`

Source: `src/jhora/horoscope/chart/charts.py:L653-L658`

```python
    if chart_method==3:
        return __parivritti_cyclic(planet_positions_in_rasi, dvf)
    elif chart_method==4:
        return __parivritti_even_reverse(planet_positions_in_rasi, dvf)
    elif chart_method==5:
        return __parivritti_alternate(planet_positions_in_rasi, dvf)
```

Source: `src/jhora/horoscope/chart/charts.py:L661-L665`

```python
    for planet,[sign,long] in planet_positions_in_rasi:
        dirn = -1 if sign in const.even_signs and chart_method==2 else 1
        l = (int(long//f1))
        dp.append([planet,[(sign+dirn*l)%12,(long*dvf)%30]])
    return dp
```

## shodasamsa_chart

- chart_method values observed: `[2, 3, 4]`

Source: `src/jhora/horoscope/chart/charts.py:L683-L688`

```python
    if chart_method==3:
        return __parivritti_cyclic(planet_positions_in_rasi, dvf)
    elif chart_method==2:
        return __parivritti_even_reverse(planet_positions_in_rasi, dvf)
    elif chart_method==4:
        return __parivritti_alternate(planet_positions_in_rasi, dvf)
```

## vimsamsa_chart

- chart_method values observed: `[2, 3, 4]`

Source: `src/jhora/horoscope/chart/charts.py:L716-L721`

```python
    if chart_method==3:
        return __parivritti_cyclic(planet_positions_in_rasi, dvf)
    elif chart_method==2:
        return __parivritti_even_reverse(planet_positions_in_rasi, dvf)
    elif chart_method==4:
        return __parivritti_alternate(planet_positions_in_rasi, dvf)
```

## chaturvimsamsa_chart

- chart_method values observed: `[2, 3]`

Source: `src/jhora/horoscope/chart/charts.py:L750-L759`

```python
    even_dirn = -1 if chart_method==2 else 1
    odd_base = 4
    even_base = 4 if chart_method == 3 else 3
    for planet,[sign,long] in planet_positions_in_rasi:
        d_long = (long*dvf)%30
        l = int(long // f1)
        r = (odd_base+l)%12 #4 = Leo
        if sign in const.even_signs:
            r = (even_base+even_dirn*l)%12 # 3 = Cancer
        dp.append([planet,[r,d_long]])
```

## nakshatramsa_chart

- chart_method values observed: `[2, 3]`

Source: `src/jhora/horoscope/chart/charts.py:L775-L778`

```python
    if chart_method==2:
        return __parivritti_even_reverse(planet_positions_in_rasi, dvf)
    elif chart_method==3:
        return __parivritti_alternate(planet_positions_in_rasi, dvf)
```

Source: `src/jhora/horoscope/chart/charts.py:L781-L791`

```python
    for planet,[sign,long] in planet_positions_in_rasi:
        d_long = (long*dvf)%30
        l = int(long // f1)
        r = l%12 # fiery sign
        if sign in const.earth_signs:
            r = (l+3)%12 # part from Cancer
        elif sign in const.air_signs:
            r = (l+6)%12
        elif sign in const.water_signs:
            r = (l+9)%12
        dp.append([planet,[r,d_long]])
```

## trimsamsa_chart

- chart_method values observed: `[2, 3, 4, 5]`

Source: `src/jhora/horoscope/chart/charts.py:L809-L816`

```python
    if chart_method==2:
        return __parivritti_cyclic(planet_positions_in_rasi, dvf)
    elif chart_method==4:
        return __parivritti_even_reverse(planet_positions_in_rasi, dvf)
    elif chart_method==5:
        return __parivritti_alternate(planet_positions_in_rasi, dvf)
    elif chart_method==3:
        return [[planet,[(int(long//f1)+sign)%12,(long*dvf)%30]] for planet,[sign,long] in planet_positions_in_rasi]
```

Source: `src/jhora/horoscope/chart/charts.py:L818-L827`

```python
    odd = [(0,5,0),(5,10,10),(10,18,8),(18,25,2),(25,30,6)]
    even = [(0,5,1),(5,12,5),(12,20,11),(20,25,9),(25,30,7)]
    dp = []
    for planet,[sign,long] in planet_positions_in_rasi:
        d_long = (long*dvf)%30
        if sign in const.odd_signs:
            r = [ rasi%12 for (l_min,l_max,rasi) in odd if (long >= l_min and long <= l_max) ]
        else:
            r = [ rasi%12 for (l_min,l_max,rasi) in even if (long >= l_min and long <= l_max) ]
        dp.append([planet,[r[0],d_long]]) # lth position from rasi
```

## khavedamsa_chart

- chart_method values observed: `[2, 3, 4]`

Source: `src/jhora/horoscope/chart/charts.py:L844-L849`

```python
    if chart_method==2:
        return __parivritti_cyclic(planet_positions_in_rasi, dvf)
    elif chart_method==3:
        return __parivritti_even_reverse(planet_positions_in_rasi, dvf)
    elif chart_method==4:
        return __parivritti_alternate(planet_positions_in_rasi, dvf)
```

## akshavedamsa_chart

- chart_method values observed: `[2, 3, 4]`

Source: `src/jhora/horoscope/chart/charts.py:L875-L880`

```python
    if chart_method==2:
        return __parivritti_cyclic(planet_positions_in_rasi, dvf)
    elif chart_method==3:
        return __parivritti_even_reverse(planet_positions_in_rasi, dvf)
    elif chart_method==4:
        return __parivritti_alternate(planet_positions_in_rasi, dvf)
```

## shashtyamsa_chart

- chart_method values observed: `[1, 2, 3, 4]`

Source: `src/jhora/horoscope/chart/charts.py:L908-L909`

```python
    if chart_method==3: #Parasara (from Aries even reverse)
        return __parivritti_alternate(planet_positions_in_rasi, dvf)
```

Source: `src/jhora/horoscope/chart/charts.py:L911-L918`

```python
    dp = []
    for planet,[sign,long] in planet_positions_in_rasi:
        d_long = (long*dvf)%30
        l = int(long // f1)
        dirn = -1 if (sign in const.even_signs and chart_method in [4]) else 1
        seed = 0 if chart_method in [2] else sign
        dp.append([planet,[(seed+dirn*l)%12,d_long]])
    return dp
```

## nava_navamsa_chart

- chart_method values observed: `[1, 2, 3]`

Source: `src/jhora/horoscope/chart/charts.py:L934-L939`

```python
    if chart_method==1:
        return __parivritti_cyclic(planet_positions_in_rasi, dvf)
    elif chart_method==2:
        return __parivritti_even_reverse(planet_positions_in_rasi, dvf)
    elif chart_method==3:
        return __parivritti_alternate(planet_positions_in_rasi, dvf)
```

Source: `src/jhora/horoscope/chart/charts.py:L941-L943`

```python
    pp1 = _navamsa_kalachakra(planet_positions_in_rasi,9)
    pp2 = _navamsa_kalachakra(pp1,9)
    return pp2
```

## ashtotharamsa_chart

- chart_method values observed: `[2, 3, 4]`

Source: `src/jhora/horoscope/chart/charts.py:L959-L964`

```python
    if chart_method==2:
        return __parivritti_cyclic(planet_positions_in_rasi, dvf)
    elif chart_method==3:
        return __parivritti_even_reverse(planet_positions_in_rasi, dvf)
    elif chart_method==4:
        return __parivritti_alternate(planet_positions_in_rasi, dvf)
```

Source: `src/jhora/horoscope/chart/charts.py:L966-L969`

```python
    dvf_1 = 9; chart_method_1=1; dvf_2=12; chart_method_2=1
    pp = mixed_chart_from_rasi_positions(planet_positions_in_rasi, varga_factor_1=dvf_1, chart_method_1=chart_method_1, 
                      varga_factor_2=dvf_2, chart_method_2=chart_method_2)
    return pp
```

## dwadas_dwadasamsa_chart

- chart_method values observed: `[2, 3, 4]`

Source: `src/jhora/horoscope/chart/charts.py:L985-L990`

```python
    if chart_method==2:
        return __parivritti_cyclic(planet_positions_in_rasi, dvf)
    elif chart_method==3:
        return __parivritti_even_reverse(planet_positions_in_rasi, dvf)
    elif chart_method==4:
        return __parivritti_alternate(planet_positions_in_rasi, dvf)
```

Source: `src/jhora/horoscope/chart/charts.py:L992-L995`

```python
    dvf_1 = 12; chart_method_1=1; dvf_2=12; chart_method_2=1
    pp = mixed_chart_from_rasi_positions(planet_positions_in_rasi,varga_factor_1=dvf_1,chart_method_1=chart_method_1,
                      varga_factor_2=dvf_2, chart_method_2=chart_method_2)
    return pp
```

## nadiamsa_chart

- chart_method values observed: `['pass-through']`

Source: `src/jhora/horoscope/chart/charts.py:L1010-L1011`

```python
    return divisional_positions_from_rasi_positions(planet_positions_in_rasi, divisional_chart_factor=150,
                                                    chart_method=chart_method)
```

## custom_divisional_chart

- chart_method values observed: `[0, 1, 2, 3, 4, 5, 6, 7, 8, 9]`

Source: `src/jhora/horoscope/chart/charts.py:L1043-L1047`

```python
    dvf = divisional_chart_factor; f1 = 30.0/dvf
    if base_rasi==None:
        return __parivritti_cyclic(planet_positions_in_rasi, dvf,dirn=1)
    _hora_list = utils.__varga_non_cyclic(dvf, base_rasi=base_rasi, start_sign_variation=chart_method,
                                             count_from_end_of_sign=count_from_end_of_sign)
```

Source: `src/jhora/horoscope/chart/charts.py:L1049-L1054`

```python
    for planet,[rasi_sign,long] in planet_positions_in_rasi:
        d_long = (long*dvf)%30
        hora = int(long // f1)
        hora_sign = _hora_list[rasi_sign][hora]
        dp.append([planet,[hora_sign,d_long]])
    return dp
```

## Shared method helper implementations

Source: `src/jhora/horoscope/chart/charts.py:L224-L233`

```python
def _hora_chart_raman_method(planet_positions_in_rasi):
    """ Hora Chart - D2 Chart Raman Method"""
    dvf = 2
    dp = []
    for planet,[rasi_sign,long] in planet_positions_in_rasi:
        d_long = (long*dvf)%30
        hora = int(long // 15.0)
        hora_sign = const.hora_list_raman[rasi_sign][hora]
        dp.append([planet,[hora_sign,d_long]])
    return dp
```

Source: `src/jhora/horoscope/chart/charts.py:L244-L255`

```python
def _hora_chart_kashinath(planet_positions_in_rasi):
    dvf = 2
    planet_hora = const.planet_hora_dict_for_odd_even_signs
    dp = []
    for planet,[rasi_sign,long] in planet_positions_in_rasi:
        d_long = (long*dvf)%30
        hora = int(long // 15.0)
        lord_of_rasi = house.house_owner_from_planet_positions(planet_positions_in_rasi, rasi_sign)
        if rasi_sign in const.odd_signs:
            hora_sign = planet_hora[lord_of_rasi][0] if hora==0 else planet_hora[lord_of_rasi][1] 
        else:
            hora_sign = planet_hora[lord_of_rasi][1] if hora==0 else planet_hora[lord_of_rasi][0] 
```

Source: `src/jhora/horoscope/chart/charts.py:L323-L332`

```python
def _drekkana_chart_parasara(planet_positions_in_rasi):
    """ Drekkana Chart - PVR/Traditional Parasara Method """
    dvf = 3; f1 = 30.0/dvf
    dp = []
    f2 = 4 
    for planet,[sign,long] in planet_positions_in_rasi:
        d_long = (long*dvf)%30
        l = int(long // f1)
        dp.append([planet,[(sign+l*f2)%12,d_long]]) # lth position from rasi
    return dp
```

Source: `src/jhora/horoscope/chart/charts.py:L359-L367`

```python
def _chaturthamsa_parasara(planet_positions_in_rasi):
    dvf = 4; f1 = 30.0/dvf
    dp = []
    f2 = 3
    for planet,[sign,long] in planet_positions_in_rasi:
        d_long = (long*dvf)%30
        l = int(long // f1)
        dp.append([planet,[(sign+l*f2)%12,d_long]]) # lth position from rasi
    return dp
```

Source: `src/jhora/horoscope/chart/charts.py:L523-L530`

```python
def _navamsa_kalachakra(planet_positions_in_rasi, dvf=9):
    dp =[]
    for planet,[sign,long] in planet_positions_in_rasi:
        d_long = (long*dvf)%30
        nak,padha,_ = drik.nakshatra_pada(long+sign*30)
        r = const.kalachakra_navamsa[nak-1][padha-1]
        dp.append([planet,[r,d_long]])
    return dp
```
