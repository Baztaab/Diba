# PyJHora-only

## Entry mapping for standard Dn functions

Source: `src/jhora/horoscope/chart/charts.py:L44-L51`

```python
divisional_chart_functions = {2:'hora_chart',3:'drekkana_chart',4:'chaturthamsa_chart',5:'panchamsa_chart',
                              6:'shashthamsa_chart',7:'saptamsa_chart',8:'ashtamsa_chart',9:'navamsa_chart',
                              10:'dasamsa_chart',11:'rudramsa_chart',12:'dwadasamsa_chart',16:'shodasamsa_chart',
                              20:'vimsamsa_chart',24:'chaturvimsamsa_chart',27:'nakshatramsa_chart',30:'trimsamsa_chart',
                              40:'khavedamsa_chart',45:'akshavedamsa_chart',60:'shashtyamsa_chart',
                              81:'nava_navamsa_chart',108:'ashtotharamsa_chart',144:'dwadas_dwadasamsa_chart',
                              #150:'nadiamsa_chart'
                              }
```

## Standard varga entry and routing

Source: `src/jhora/horoscope/chart/charts.py:L1066-L1077`

```python
def divisional_positions_from_rasi_positions(planet_positions_in_rasi,divisional_chart_factor=1,
                     chart_method=1,base_rasi=None,count_from_end_of_sign=None):
    if divisional_chart_factor==1:
        return planet_positions_in_rasi
    else:
        if (not const.TREAT_STANDARD_CHART_AS_CUSTOM) and (divisional_chart_factor in divisional_chart_functions.keys()\
                and (base_rasi==None and (chart_method !=None and chart_method >0) )):
            return eval(divisional_chart_functions[divisional_chart_factor]+'(planet_positions_in_rasi,chart_method)')
        elif divisional_chart_factor in range(1,const.MAX_DHASAVARGA_FACTOR+1):
            return custom_divisional_chart(planet_positions_in_rasi, divisional_chart_factor=divisional_chart_factor,
                        chart_method=chart_method,base_rasi=base_rasi,count_from_end_of_sign=count_from_end_of_sign)
        else:
```

Source: `src/jhora/horoscope/chart/charts.py:L1119-L1122`

```python
    planet_positions_in_rasi = rasi_chart(jd_at_dob, place_as_tuple, years,months,sixty_hours,
                                  calculation_type=calculation_type,pravesha_type=pravesha_type)
    return divisional_positions_from_rasi_positions(planet_positions_in_rasi, divisional_chart_factor=divisional_chart_factor,
                    chart_method=chart_method, base_rasi=base_rasi, count_from_end_of_sign=count_from_end_of_sign)
```

## Dn limits and standard factor list

Source: `src/jhora/const.py:L140-L140`

```python
division_chart_factors = [1,2,3,4,5,6,7,8,9,10,11,12,16,20,24,27,30,40,45,60,81,108,144]
```

Source: `src/jhora/const.py:L726-L730`

```python
MAX_DHASAVARGA_FACTOR = 300
DEFAULT_CUSTOM_VARGA_FACTOR=57
# If True standard vargas such as D2,D3 etc will follow custom calculations and not standard calculations
""" DO NOT CHANGE THIS TO TRUE. NOT IMPLEMENTED YET """
TREAT_STANDARD_CHART_AS_CUSTOM = False
```

## Planet longitude to dasavarga and dhasavarga engine

Source: `src/jhora/panchanga/drik.py:L1505-L1510`

```python
    one_pada = (360.0 / (12 * divisional_chart_factor))  # There are also 108 navamsas
    one_sign = 12.0 * one_pada    # = 40 degrees exactly
    signs_elapsed = longitude / one_sign
    fraction_left = signs_elapsed % 1
    constellation = int(fraction_left * 12)
    long_in_raasi = (longitude-(constellation*30)) % 30
```

Source: `src/jhora/panchanga/drik.py:L1546-L1556`

```python
    jd_utc = jd - place.timezone / 24.
    positions = []
    for planet in planet_list:
        p_id = planet_list.index(planet)
        if planet != const._KETU:
            nirayana_long = sidereal_longitude(jd_utc, planet)
        else: # Ketu
            nirayana_long = ketu(sidereal_longitude(jd_utc, const._RAHU)) # 7 = swe.RAHU
        divisional_chart = dasavarga_from_long(nirayana_long,divisional_chart_factor)
        positions.append([p_id, divisional_chart])
    return positions
```

## Shared helper algorithms used by chart methods

Source: `src/jhora/horoscope/chart/charts.py:L214-L223`

```python
def __parivritti_even_reverse(planet_positions_in_rasi,dvf,dirn=1):
    f1 = 30.0/dvf
    _hora_list = utils.parivritti_even_reverse(dvf,dirn)
    hora_sign = lambda r,h: [s1 for r1,h1,s1 in _hora_list if r1==r and h1==h][0]
    dp = []
    for planet,[rasi_sign,long] in planet_positions_in_rasi:
        d_long = (long*dvf)%30
        hora = int(long // f1)
        dp.append([planet,[hora_sign(rasi_sign,hora),d_long]])
    return dp
```

Source: `src/jhora/horoscope/chart/charts.py:L234-L243`

```python
def __parivritti_cyclic(planet_positions_in_rasi,dvf,dirn=1):
    f1 = 30.0/dvf
    _hora_list = utils.parivritti_cyclic(dvf,dirn)
    dp = []
    for planet,[rasi_sign,long] in planet_positions_in_rasi:
        d_long = (long*dvf)%30
        hora = int(long // f1)
        hora_sign = _hora_list[rasi_sign][hora]
        dp.append([planet,[hora_sign,d_long]])
    return dp
```

Source: `src/jhora/horoscope/chart/charts.py:L314-L322`

```python
def __parivritti_alternate(planet_positions_in_rasi,dvf,dirn=1):
    f1 = 30.0/dvf; _hora_list = utils.parivritti_alternate(dvf,dirn)
    dp = []
    for planet,[rasi_sign,long] in planet_positions_in_rasi:
        d_long = (long*dvf)%30
        hora = int(long // f1)
        hora_sign = _hora_list[rasi_sign][hora]
        dp.append([planet,[hora_sign,d_long]])
    return dp
```

Source: `src/jhora/utils.py:L861-L870`

```python
def parivritti_even_reverse(dcf,dirn=1):
    """
        generates parivritti tuple (rasi_sign, hora_portion_of_varga, varga_sign)
        in this method for varga factor = 2 (hora chart)
            for the first sign hora portion increases from 0 to 1 (varga factor - 1)
            for the next sign hora portion decreases from 1 to 0
            for rasi = 0 the tuples are (0,0,0), (0,1,1) (the middle hora element 0 and 1)
            for next rasi = 1 (1,1,2), (1,0,3) (the middle hora element 1 and 0)
        in this method for varga factor = 3 (drekkana chart)
            for the first sign hora portion increases from 0 to 2
```

Source: `src/jhora/utils.py:L899-L906`

```python
    pc = []
    hs = 0
    for _ in range(12):
        t = tuple()
        for _ in range(dcf):
            t += (hs%12,); hs = (hs+dirn)%12
        pc.append(t)
    return pc
```

Source: `src/jhora/utils.py:L925-L934`

```python
def __varga_non_cyclic(dcf,base_rasi=0,start_sign_variation=1,count_from_end_of_sign=False):
    """
        STILL UNDER EXPERIMENT
        generates varga non_cyclic varga rasi tuple (rasi_sign, hora_portion_of_varga, varga_sign)
        @param divisional_chart_factor: 1.. 300
        @param start_sign_variation:
            0=>start from base for all signs
            1=>1st/7th from base if sign is odd/even
            2=>1st/9th from base if sign is odd/even
            3=>1st/5th from base if sign is odd/even
```

## Node and sidereal-mode behavior used by divisional computations

Source: `src/jhora/const.py:L53-L54`

```python
_KETU = -swe.MEAN_NODE; KETU_ID = 8
_RAHU = swe.MEAN_NODE; RAHU_ID = 7
```

Source: `src/jhora/panchanga/drik.py:L227-L232`

```python
        set_ayanamsa_mode(_ayanamsa_default,_ayanamsa_value,jd_utc); _ayanamsa_mode = const._DEFAULT_AYANAMSA_MODE
        #print('drik sidereal long ayanamsa',_ayanamsa_mode, const._DEFAULT_AYANAMSA_MODE)
        #import inspect; print('called by',inspect.stack()[1].function)
    longi,_ = swe.calc_ut(jd_utc, planet, flags = flags)
    reset_ayanamsa_mode()
    return utils.norm360(longi[0]) # degrees
```
