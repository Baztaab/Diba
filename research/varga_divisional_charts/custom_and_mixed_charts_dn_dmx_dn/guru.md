# PyJHora-only

## Custom Dn generation and non-cyclic configuration

Source: `src/jhora/horoscope/chart/charts.py:L1012-L1021`

```python
def custom_divisional_chart(planet_positions_in_rasi,divisional_chart_factor,chart_method=0,
                            base_rasi=None,count_from_end_of_sign=False):
    """ 
        Generates D-N chart (cyclic or non cyclic)
        @param planet_positions_in_rasi: Rasi chart planet_positions list in the format [[planet,(raasi,planet_longitude)],...]]. First element is that of Lagnam
            Example: [ ['L',(0,13.4)],[0,(11,12.7)],...]] Lagnam in Aries 13.4 degrees, Sun in Taurus 12.7 degrees
        @param divisional_chart_factor: 1.. 300
        @param chart_method:
            0=>Cyclic Parivritti variation (base_rasi=None for cyclic and base_rasi=Aries/sign for non-cyclic)
            For Non-cyclic following parameters apply
```

Source: `src/jhora/horoscope/chart/charts.py:L1022-L1031`

```python
            0=>From base for all signs
            1=>1st/7th from base if sign is odd/even
            2=>1st/9th from base if sign is odd/even
            3=>1st/5th from base if sign is odd/even
            4=>1st/11th from base if sign is odd/even
            5=>1st/3rd from base if sign is odd/even
            6=>1st/5th/9th from base if sign is movable/fixed/dual
            7=>1st/9th/5th from base if sign is movable/fixed/dual
            8=>1st/4th/7th/10th from base if sign is fire/earth/air/water
            9=>1st/10th/7th/4th from base if sign is fire/earth/air/water
```

Source: `src/jhora/horoscope/chart/charts.py:L1043-L1054`

```python
    dvf = divisional_chart_factor; f1 = 30.0/dvf
    if base_rasi==None:
        return __parivritti_cyclic(planet_positions_in_rasi, dvf,dirn=1)
    _hora_list = utils.__varga_non_cyclic(dvf, base_rasi=base_rasi, start_sign_variation=chart_method,
                                             count_from_end_of_sign=count_from_end_of_sign)
    dp = []
    for planet,[rasi_sign,long] in planet_positions_in_rasi:
        d_long = (long*dvf)%30
        hora = int(long // f1)
        hora_sign = _hora_list[rasi_sign][hora]
        dp.append([planet,[hora_sign,d_long]])
    return dp
```

Source: `src/jhora/utils.py:L956-L965`

```python
        if start_sign_variation==1 and sign in const.even_signs: start_sign = (seed+6)%12
        elif start_sign_variation==2 and sign in const.even_signs: start_sign = (seed+8)%12
        elif start_sign_variation==3 and sign in const.even_signs: start_sign = (seed+4)%12
        elif start_sign_variation==4 and sign in const.even_signs: start_sign = (seed+10)%12
        elif start_sign_variation==5 and sign in const.even_signs: start_sign = (seed+2)%12
        elif start_sign_variation==6:
            if sign in const.fixed_signs: start_sign = (seed+4)%12
            elif sign in const.dual_signs: start_sign = (seed+8)%12
        elif start_sign_variation==7:
            if sign in const.fixed_signs: start_sign = (seed+8)%12
```

Source: `src/jhora/utils.py:L967-L977`

```python
        elif start_sign_variation==8:
            if sign in const.earth_signs: start_sign = (seed+3)%12
            elif sign in const.air_signs: start_sign = (seed+6)%12
            elif sign in const.water_signs: start_sign = (seed+9)%12
        elif start_sign_variation==9:
            if sign in const.earth_signs: start_sign = (seed+9)%12
            elif sign in const.air_signs: start_sign = (seed+6)%12
            elif sign in const.water_signs: start_sign = (seed+3)%12        
        for h in range(dcf):
            t += ((start_sign+dirn*h)%12,)
        pc.append(t)
```

## Mixed chart composition (Dm x Dn)

Source: `src/jhora/horoscope/chart/charts.py:L1055-L1061`

```python
def mixed_chart(jd,place,varga_factor_1=None,chart_method_1=1,varga_factor_2=None,chart_method_2=1):
    planet_positions_in_rasi = rasi_chart(jd,place)
    if varga_factor_1==1 and varga_factor_2==1: return planet_positions_in_rasi
    pp1 = planet_positions_in_rasi if varga_factor_1==1 else \
            eval(divisional_chart_functions[varga_factor_1]+'(planet_positions_in_rasi,chart_method=chart_method_1)')
    pp2 = pp1 if varga_factor_2==2 else eval(divisional_chart_functions[varga_factor_2]+'(pp1,chart_method=chart_method_2)')
    return pp2
```

Source: `src/jhora/horoscope/chart/charts.py:L1062-L1065`

```python
def mixed_chart_from_rasi_positions(planet_positions_in_rasi,varga_factor_1=None,chart_method_1=1,varga_factor_2=None,chart_method_2=1):
    pp1 = eval(divisional_chart_functions[varga_factor_1]+'(planet_positions_in_rasi,chart_method=chart_method_1)')
    pp2 = eval(divisional_chart_functions[varga_factor_2]+'(pp1,chart_method=chart_method_2)')
    return pp2
```

## Divisional routing between standard and custom paths

Source: `src/jhora/horoscope/chart/charts.py:L1071-L1077`

```python
        if (not const.TREAT_STANDARD_CHART_AS_CUSTOM) and (divisional_chart_factor in divisional_chart_functions.keys()\
                and (base_rasi==None and (chart_method !=None and chart_method >0) )):
            return eval(divisional_chart_functions[divisional_chart_factor]+'(planet_positions_in_rasi,chart_method)')
        elif divisional_chart_factor in range(1,const.MAX_DHASAVARGA_FACTOR+1):
            return custom_divisional_chart(planet_positions_in_rasi, divisional_chart_factor=divisional_chart_factor,
                        chart_method=chart_method,base_rasi=base_rasi,count_from_end_of_sign=count_from_end_of_sign)
        else:
```

Source: `src/jhora/horoscope/chart/charts.py:L1081-L1092`

```python
def divisional_chart(jd_at_dob,place_as_tuple,divisional_chart_factor=1,
                     chart_method=1,years=1,months=1,sixty_hours=1,calculation_type='drik',pravesha_type=0,
                     base_rasi=None,count_from_end_of_sign=None):
    """
        Get divisional/varga chart
        @param jd_at_dob:Julian day number at the date/time of birth
            Note: It can be obtained from utils.julian_day_number(...)
        @param place_as_tuple - panjanga.place format
                example drik.place('Chennai,IN',13.0,78.0,+5.5)
        @param divisional_chart_factor Default=1 
            1=Raasi, 9=Navamsa. See const.divisional_chart_factors for options
        @param chart_method: See individual chart function for available chart methods 
```

Source: `src/jhora/horoscope/chart/charts.py:L1119-L1122`

```python
    planet_positions_in_rasi = rasi_chart(jd_at_dob, place_as_tuple, years,months,sixty_hours,
                                  calculation_type=calculation_type,pravesha_type=pravesha_type)
    return divisional_positions_from_rasi_positions(planet_positions_in_rasi, divisional_chart_factor=divisional_chart_factor,
                    chart_method=chart_method, base_rasi=base_rasi, count_from_end_of_sign=count_from_end_of_sign)
```
