# graha_states_behavior_contract_map.engine_plus_consumers.md

## Snapshot identity (FACTS)

- pyjhora_root: `D:\lab\Pyjhora`
- extraction_timestamp_local: `2026-02-27 20:46:49`
- in-scope files: `13`
- in-scope file digests (SHA256):
  - `src/jhora/horoscope/chart/strength.py` -> `d0d92d6b4b62dbc31d40a3455e214d8b0917e8608ca1f6148a200dcb512d1d93` (bytes: `53346`)
  - `src/jhora/horoscope/chart/charts.py` -> `34c49af9fb3359fdb243f2a467404b7a849e35b9def9e2961a45a4027c8619b2` (bytes: `141395`)
  - `src/jhora/panchanga/drik.py` -> `9790dcdf442910b1eaa260b16c346c6696438eb6955c0a520c1be220ba3497bc` (bytes: `186944`)
  - `src/jhora/utils.py` -> `861062b3abba1655b9d4e5608333f8aaa1d391b3d38ecdacbac565bf930f3875` (bytes: `70076`)
  - `src/jhora/const.py` -> `2dacc910fce9babc69582491b52cde9fd23ab9dde835d41efb65fc0f79e00ba8` (bytes: `79727`)
  - `src/jhora/horoscope/main.py` -> `cecb9d933245d6df820425f80d28da3153746215c8b283c66d4fa65c86ee58bd` (bytes: `128308`)
  - `src/jhora/horoscope/chart/house.py` -> `d2d0d2b9a1e382879b0f191498bcc8dc9d4ef74224925ffb522f2cc0e4329861` (bytes: `80854`)
  - `src/jhora/horoscope/chart/dosha.py` -> `a9c1bafec6b3e2c5fae1aa87fe07153858a60ff5c41f4192e73561608fec0730` (bytes: `22973`)
  - `src/jhora/horoscope/prediction/longevity.py` -> `a350b3fdaa8faa3d34546d2096ebed79e1e06d370d69bb7fe701682235f682c2` (bytes: `11459`)
  - `src/jhora/horoscope/dhasa/graha/aayu.py` -> `bbc866d51112f88969509e6c73fdf61912ee8e16e3811a52adc429e6e956dd96` (bytes: `33652`)
  - `src/jhora/horoscope/transit/tajaka.py` -> `8f1d7c369363c953ff21405cf4a7243c488cc6d155315b80e279a861f58bce17` (bytes: `40858`)
  - `src/jhora/horoscope/transit/tajaka_yoga.py` -> `a77b4c87a75ab511ff86a7f70c10aca3b7d4447e5d5758defa21b1865de58347` (bytes: `23295`)
  - `src/jhora/horoscope/dhasa/sudharsana_chakra.py` -> `c25e166a708ecd467b4e36cca53ff9b586693cb31c40152df6e7e095c8091f83` (bytes: `6207`)

## Scope (FACTS)

- In-scope engine files:
  - `src/jhora/horoscope/chart/strength.py`
  - `src/jhora/horoscope/chart/charts.py`
  - `src/jhora/panchanga/drik.py`
  - `src/jhora/utils.py`
  - `src/jhora/const.py`
- In-scope consumers/config:
  - `src/jhora/horoscope/main.py`
  - `src/jhora/horoscope/chart/house.py`
  - `src/jhora/horoscope/chart/dosha.py`
  - `src/jhora/horoscope/prediction/longevity.py`
  - `src/jhora/horoscope/dhasa/graha/aayu.py`
  - `src/jhora/horoscope/transit/tajaka.py`
  - `src/jhora/horoscope/transit/tajaka_yoga.py`
  - `src/jhora/horoscope/dhasa/sudharsana_chakra.py`
- Out-of-scope:
  - UI modules
  - tests
  - `src/jhora/panchanga/drik1.py`
  - deep consumers outside one-hop list

## Pattern inventory (FACTS)

- `shadbala`
- `shad_bala`
- `bhava_bala`
- `sthana_bala`
- `dik_bala`
- `kala_bala`
- `cheshta_bala`
- `naisargika_bala`
- `drik_bala`
- `vimsopaka`
- `vaiseshikamsa`
- `house_strengths_of_planets`
- `moola_trikona`
- `combust`
- `combustion`
- `planets_in_combustion`
- `retrograde`
- `planets_in_retrograde`
- `vakra`
- `exalt`
- `debilit`
- `is_planet_in_exalation`
- `is_planet_in_debilitation`
- `deeptaamsa`
- `ayanamsa`
- `avastha`
- `jagrad`
- `baladi`
- `bala`
- `kumar`
- `yuva`
- `vriddha`
- `mrita`
- `\b30\b`

## Behavior taxonomy (FACTS)

- shadbala 6-part assembly and aggregation: `GS06`, `GS07`, `GS08`, `GS09`, `GS10`, `GS11`, `GS12`, `GS13`
- state logic for retrograde and combustion: `GS14`, `GS15`, `GS16`
- dignity logic across matrix and deep longitude: `GS02`, `GS17`, `GS18`, `GS20`
- constants and thresholds: `GS01`, `GS03`, `GS04`, `GS05`
- output and consumer contracts: `GS21`, `GS22`, `GS23`, `GS24`
- avastha implementation status: `ABSENCE-OF-AVASTHA`

## Evidence anchors (GS01..GSNN, ABSENCE-OF-AVASTHA, GS900)

### GS01

- Behavior: Vimsopaka/Vaiseshikamsa weight tables are constant-defined.
- Source: `src/jhora/const.py:L141-L153`
- Excerpt:
```python
dhasavarga_amsa_vimsopaka = {1:3,2:1.5,3:1.5,7:1.5,9:1.5,10:1.5,12:1.5,16:1.5,30:1.5,60:5}
shadvarga_amsa_vimsopaka = {1:6,2:2,3:4,9:5,12:2,30:1}
sapthavarga_amsa_vimsopaka = {1:5,2:2,3:3,7:1,9:2.5,12:4.5,30:2}
shodhasa_varga_amsa_vimsopaka = {1:3.5,2:1,3:1,4:0.5,7:0.5,9:3,10:0.5,12:0.5,16:2,20:0.5,24:0.5,27:0.5,30:1,40:0.5,45:0.5,60:4}
vimsamsa_varga_amsa_factors = division_chart_factors
""" In the order: Own, Adhimitra,Mithra,Neutral/Samam,Sathru,Enemy,Great Enemy/Adhisathru """
vimsopaka_planet_position_values = [20,18,15,10,7,5] 
dhasavarga_amsa_vaiseshikamsa = {1:1,2:1,3:1,7:1,9:1,10:1,12:1,16:1,30:1,60:1}
shadvarga_amsa_vaiseshikamsa = {1:1,2:1,3:1,9:1,12:1,30:1}
sapthavarga_amsa_vaiseshikamsa = {1:1,2:1,3:1,7:1,9:1,12:1,30:1}
shodhasa_varga_amsa_vaiseshikamsa = {1:1,2:1,3:1,4:1,7:1,9:1,10:1,12:1,16:1,20:1,24:1,27:1,30:1,40:1,45:1,60:1}
""" In the order: Own, Adhimitra,Mithra,Neutral/Samam,Sathru,Enemy,Great Enemy/Adhisathru """
```
- Observed behavior: Weight dictionaries and score ladders are hardcoded in const.

### GS02

- Behavior: Dignity matrix and moola-trikona lookup are constant-defined.
- Source: `src/jhora/const.py:L286-L311`
- Excerpt:
```python
house_strengths_of_planets = [
    [4, 1, 2, 2, 5, 2, 0, 3, 3, 1, 1, 3], # 0 Sun
    [2, 4, 3, 5, 3, 3, 2, 0, 2, 2, 2, 2], # 1 Moon
    [5, 2, 1, 0, 3, 1, 2, 5, 3, 4, 2, 3], # 2 Mars
    [2, 3, 5, 1, 3, 5, 3, 2, 2, 2, 2, 0], # 3 Mercury
    [3, 1, 1, 4, 3, 3, 1, 3, 5, 0, 2, 5], # 4 Jupiter
    [2, 5, 3, 1, 1, 0, 5, 2, 3, 3, 3, 4], # 5 Venus
    [0, 3, 3, 1, 1, 3, 4, 1, 2, 5, 5, 2], # 6 Saturn
    [1, 4, 4, 1, 1, 3, 3, 0, 0, 3, 1, 3], # 7 Rahu (Exalted 1,2 | Debilitated 7,8)
    [1, 0, 0, 1, 1, 3, 3, 4, 4, 3, 1, 3]  # 8 Ketu (Debilitated 1,2 | Exalted 7,8)
]
__house_strengths_of_planets_old=[[4,1,2,2,5,2,0,3,3,1,1,3],
```
- Observed behavior: Sign-level dignity and moola-trikona mapping are centralized.

### GS03

- Behavior: Combustion ranges include retrograde-specific variant.
- Source: `src/jhora/const.py:L494-L495`
- Excerpt:
```python
combustion_range_of_planets_from_sun = [12,17,14,10,11,15] #moon,mars,mercury,jupiter,venus,saturn
combustion_range_of_planets_from_sun_while_in_retrogade = [12,8,12,11,8,16] # [12,17,12,8,11,15] #moon,mars,mercury,jupiter,venus,saturn
```
- Observed behavior: Combustion threshold is branchable by retrograde state.

### GS04

- Behavior: Retrograde sun-relative windows and method switch are constants.
- Source: `src/jhora/const.py:L573-L574`
- Excerpt:
```python
planets_retrograde_limits_from_sun = {2:(164,196),3:(144,216),4:(130,230),5:(163,197),6:(115,245)}
planet_retrogression_calculation_method = 1 # 1 => Old method 2 = Wiki calculations
```
- Observed behavior: Chart-based retrograde uses configured limits and mode.

### GS05

- Behavior: Shadbala factor requirements and naisargika values are constant-based.
- Source: `src/jhora/const.py:L571-L571`
- Excerpt:
```python
naisargika_bala = [60.00,51.43,17.14,25.71,34.29,42.86,8.57,0.0,0.0]
```
- Observed behavior: Naisargika baseline values exist in const.

### GS06

- Behavior: Sthana bala aggregates uchcha/sapthavargaja/ojayugama/kendra/dreshkona.
- Source: `src/jhora/horoscope/chart/strength.py:L214-L233`
- Excerpt:
```python
def _sthana_bala(jd, place,):
    sv = const.sapthavargaja_factors
    pp_sv = {}
    for dcf in sv:
        pp = charts.divisional_chart(jd, place,divisional_chart_factor=dcf)
        pp_sv[dcf] = pp
    ub = _uchcha_bala(pp_sv[1])
    #print('uccha bala',ub)
    svb = _sapthavargaja_bala1(jd, place)
    #print('_sapthavargaja_bala',svb)
    ob = _ojayugama_bala(pp_sv[1], pp_sv[9])
    #print('_ojayugama_bala',ob)
```
- Observed behavior: Sthana sub-components are summed into one bala vector.

### GS07

- Behavior: Dig bala has dedicated directional computation path.
- Source: `src/jhora/horoscope/chart/strength.py:L419-L438`
- Excerpt:
```python
def _dig_bala(jd,place,method=1):
    if method==2: return _dig_bala_another(jd, place)
    planet_positions = charts.rasi_chart(jd, place)
    powerless_houses_of_planets = const.dig_bala_powerless_houses_of_planets
    bm = drik.bhaava_madhya(jd, place)
    dbf = [bm[p] for p in powerless_houses_of_planets]
    dbp = [0 for _ in const.SUN_TO_SATURN]
    for p,(h,long) in planet_positions[const.SUN_ID+1:const._pp_count_upto_saturn]:
        p_long = h*30+long
        dbp[p] = round(abs(dbf[p]-p_long)/3,2)
    return dbp
def _dig_bala_another(jd, place):
```
- Observed behavior: Directional strength is computed separately from other bala parts.

### GS08

- Behavior: Kala bala is composite of nine temporal contributors.
- Source: `src/jhora/horoscope/chart/strength.py:L643-L670`
- Excerpt:
```python
def _kaala_bala(jd,place):
    kb = [0 for _ in const.SUN_TO_SATURN]
    nb = _nathonnath_bala(jd, place)
    pb = _paksha_bala(jd, place)
    tb = _tribhaga_bala(jd, place)
    ab = _abdadhipathi(jd,place)# _abda_bala(jd, place)
    mb = _masadhipathi(jd, place) # _masa_bala(jd, place)
    vb = _vaaradhipathi(jd, place) # _vaara_bala(jd, place)
    hb = _hora_bala(jd, place)
    ayb = _ayana_bala(jd, place)
    yb = _yuddha_bala(jd, place)
    for p in const.SUN_TO_SATURN:
```
- Observed behavior: Kala bala sums nathonnatha/paksha/tribhaga/abda/masa/vaara/hora/ayana/yuddha.

### GS09

- Behavior: Cheshta bala has motion-oriented computation branch.
- Source: `src/jhora/horoscope/chart/strength.py:L699-L717`
- Excerpt:
```python
def _cheshta_bala(jd,place):
    pp = drik.dhasavarga(jd, place, divisional_chart_factor=1)
    cb = [0 for _ in const.SUN_TO_SATURN]
    from jhora.panchanga import surya_sidhantha
    sun_mean_long = surya_sidhantha._planet_mean_longitude(jd, place, const._SUN)
    #print('planet',0,'mean longitude',sun_mean_long)
    for p in [const._MARS, const._MERCURY, const._JUPITER, const._VENUS, const._SATURN]: #range(2,7):
        p_id = drik.planet_list.index(p)
        mean_long = surya_sidhantha._planet_mean_longitude(jd, place, p)
        seegrocha = sun_mean_long
        if p in [const._MERCURY,const._VENUS]:
            seegrocha = mean_long
```
- Observed behavior: Cheshta derives from mean/true motion relationships.

### GS10

- Behavior: Naisargika bala is direct constant projection.
- Source: `src/jhora/horoscope/chart/strength.py:L718-L719`
- Excerpt:
```python
def _naisargika_bala(jd=None,place=None):
    return const.naisargika_bala[:-2]
```
- Observed behavior: Naisargika output slices from const values.

### GS11

- Behavior: Drik bala computes benefic-minus-malefic aspect contributions.
- Source: `src/jhora/horoscope/chart/strength.py:L803-L829`
- Excerpt:
```python
def _drik_bala(jd,place):
    dk = [[ 0 for _ in const.SUN_TO_SATURN] for _ in const.SUN_TO_SATURN]
    pp = charts.rasi_chart(jd, place)
    #planets_with_mercury = [p for p,(h,_) in pp[1:] if h==pp[4][1][0] and p != 3]
    _tithi = drik.tithi(jd, place)[0]; waxing_moon = _tithi <= 15
    pp = pp[1:-2]
    subha_grahas,asubha_grahas = charts.benefics_and_malefics(jd, place,exclude_rahu_ketu=True)
    for p1 in const.SUN_TO_SATURN: # Aspected Planet
        p1_long = pp[p1][1][0]*30+pp[p1][1][1]
        for p2 in const.SUN_TO_SATURN: # Aspecting Planet
            p2_long = pp[p2][1][0]*30+pp[p2][1][1]
            dk_p1_p2 = round((360.0+p1_long-p2_long)%360,2)
```
- Observed behavior: Aspect matrix is reduced into per-planet drik bala.

### GS12

- Behavior: Shad bala assembly returns 9-slot composite payload.
- Source: `src/jhora/horoscope/chart/strength.py:L830-L854`
- Excerpt:
```python
def shad_bala(jd,place):
    sb = []
    stb = _sthana_bala(jd, place)
    #print('_sthana_bala',stb)
    sb.append(stb)
    kb = _kaala_bala(jd, place)
    #print('_kaala_bala',kb)
    sb.append(kb)
    dgb = _dig_bala(jd, place)
    #print('_dig_bala',dgb)
    sb.append(dgb)
    cb = _cheshta_bala_new(jd, place,use_epoch_table=True)
```
- Observed behavior: Return includes six components + sum + rupa + strength ratio.

### GS13

- Behavior: Bhava bala returns [raw,rupas,strength] triple.
- Source: `src/jhora/horoscope/chart/strength.py:L956-L968`
- Excerpt:
```python
def bhava_bala(jd,place):
    """
        Computes bhava bala
        Returns bhava bala as list of bhava bala followed by list of bhava bala in rupas
    """
    bab = _bhava_adhipathi_bala(jd, place)
    bdb = _bhava_dig_bala(jd, place)
    bdrb = _bhava_drik_bala(jd, place)
    bb = list(map(sum,zip(*[bab,bdb,bdrb])))
    bb = [round(b,2) for b in bb]
    bb_rupas = [round(b/60,2) for b in bb]
    bb_strength = [round(b/const.minimum_bhava_bala_rupa,2) for b in bb_rupas]
```
- Observed behavior: Bhava aggregation is normalized and returned as three arrays.

### GS14

- Behavior: Chart retrograde can use old method or sun-window method.
- Source: `src/jhora/horoscope/chart/charts.py:L1160-L1179`
- Excerpt:
```python
def planets_in_retrograde(planet_positions):
    """
        Get the list of planets that are in retrograde - based on the planet positions returned by the divisional_chart()
        @param planet_positions: planet_positions returned by divisional_chart()
        @return list of planets in retrograde 
        NOTE: USE THIS FUNCTION ONLY IF YOU HAVE TO PASS planet_positions as argument
        OTHERWISE FOR ACCURATE RESULTS use drik.planets_in_retrograde(jd, place)
    """
    if const.planet_retrogression_calculation_method == 1:
        return _planets_in_retrograde_old(planet_positions)
    retrograde_planets = []
    sun_long = planet_positions[1][1][0]*30+planet_positions[1][1][1]
```
- Observed behavior: Retrograde logic diverges by configured method.

### GS15

- Behavior: Drik retrograde uses Swiss Ephemeris speed sign.
- Source: `src/jhora/panchanga/drik.py:L233-L253`
- Excerpt:
```python
def planets_in_retrograde(jd,place):
    """
        To get the list of retrograding planets
        @param jd: julian day number (not UTC)
        @param place: Place as struct ('Place',latitude,longitude,timezone)
        @return: list of retrograding planets e.g. [3,5]
        NOTE: To find the retrograding planets for kundali charts use this function.
        There is another function in `jhora.horoscope.chart.charts` module which calculates
        retrograding planet based on their positions and is used in yoga, dhasa calculations
    """
    jd_utc = jd - place.timezone / 24.
    flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | _rise_flags
```
- Observed behavior: Negative longitudinal speed marks retrograde.

### GS16

- Behavior: Combustion depends on retrograde branch-specific threshold.
- Source: `src/jhora/horoscope/chart/charts.py:L1181-L1198`
- Excerpt:
```python
def planets_in_combustion(planet_positions,use_absolute_longitude=True):
    """
        Get the list of planets that are in combustion - based on the planet positions returned by the divisional_chart()
        @param planet_positions: planet_positions returned by divisional_chart()
        @return list of planets in combustion 
    """
    retrograde_planets = planets_in_retrograde(planet_positions) 
    sun_long = planet_positions[1][1][0]*30+planet_positions[1][1][1] if use_absolute_longitude else planet_positions[1][1][1]
    combustion_planets = []
    for p,(h,h_long) in planet_positions[const.MOON_ID+1:const._pp_count_upto_saturn]: # Exclude Lagna, Sun, Rahu and Ketu
        p_long = h*30+h_long if use_absolute_longitude else h_long
        combustion_range = const.combustion_range_of_planets_from_sun
```
- Observed behavior: Combustion range switches when planet is retrograde.

### GS17

- Behavior: Exaltation supports deep-longitude and matrix fallback.
- Source: `src/jhora/utils.py:L1259-L1270`
- Excerpt:
```python
def is_planet_in_exalation(planet,planet_house,planet_positions=None,enforce_deep_exaltation=True):
    if planet_positions is not None and enforce_deep_exaltation and planet in const.SUN_TO_SATURN:
        sign_idx, lon_in_sign = planet_positions[planet + 1][1]
        abs_longitude = (sign_idx * 30) + lon_in_sign
        deep_ex_lon = const.planet_deep_exaltation_longitudes[planet]
        if abs(abs_longitude - deep_ex_lon) <= const.planet_deep_exaltation_tolerance:
            return True
    else:
        if const.house_strengths_of_planets[planet][planet_house] >= const._EXALTED_UCCHAM:
            return True
    return False
def is_planet_strong(planet,planet_house,include_neutral_samam=False):
```
- Observed behavior: Deep exaltation tolerance can override sign-only checks.

### GS18

- Behavior: Debilitation supports deep-longitude and matrix fallback.
- Source: `src/jhora/utils.py:L1279-L1291`
- Excerpt:
```python
def is_planet_in_debilitation(planet,planet_house,planet_positions=None,enforce_deep_debilitation=True):
    if (planet_positions is not None and enforce_deep_debilitation and 
            planet not in [const.KETU_ID, const.RAHU_ID, const._ascendant_symbol]): 
        sign_idx, lon_in_sign = planet_positions[planet + 1][1]
        abs_longitude = (sign_idx * 30) + lon_in_sign
        deep_ex_lon = const.planet_deep_debilitation_longitudes[planet]
        if abs(abs_longitude - deep_ex_lon) <= const.planet_deep_debilitation_tolerance:
            return True
    else:
        if const.house_strengths_of_planets[planet][planet_house] == const._DEBILITATED_NEECHAM:
            return True
    return False
```
- Observed behavior: Deep debilitation tolerance can override sign-only checks.

### GS19

- Behavior: Weakness classifier includes combustion and multiple optional criteria.
- Source: `src/jhora/utils.py:L1305-L1370`
- Excerpt:
```python
    """
    Determine whether `planet` is weak using whichever inputs are available.

    Works with partial data:
      - If only planet_house is given → matrix debilitation.
      - If planet_positions is given → deep debilitation, combustion, malefic affliction become available.
      - If asc_house is given → dusthana test can be done relative to asc.

    Criteria applied when data allows:
      1) Debilitated by sign (matrix-based)            [needs planet_house]
      2) Deep debilitation by longitude                [needs planet_positions & enforce_deep_debilitation]
      3) Afflicted by malefics (aspect/conjunction)    [needs planet_positions]
```
- Observed behavior: Weakness is multi-criterion with feature toggles.

### GS20

- Behavior: Main wrapper exposes shadbala and bhava bala from strength module.
- Source: `src/jhora/horoscope/main.py:L902-L914`
- Excerpt:
```python
    def _get_shad_bala(self,dob,tob,place):
        from jhora.horoscope.chart import strength
        jd = utils.julian_day_number(dob, tob)
        return strength.shad_bala(jd, place)
    def _get_bhava_bala(self,dob,tob,place):
        from jhora.horoscope.chart import strength
        jd = utils.julian_day_number(dob, tob)
        bb = strength.bhava_bala(jd, place)
        #print('main bhava bala info',bb)
        import numpy as np
        bb = list(np.array(bb).T)
        #print('main bhava bala info',bb)
```
- Observed behavior: Main passes shadbala and reshapes bhava bala payload.

### GS21

- Behavior: Main wrapper consumes vimsopaka output slots by fixed indices.
- Source: `src/jhora/horoscope/main.py:L926-L943`
- Excerpt:
```python
    def _get_vimsopaka_bala(self,dob,tob,place_as_tuple):
        jd_at_dob = utils.julian_day_number(dob, tob)
        sv = charts.vimsopaka_shadvarga_of_planets(jd_at_dob, place_as_tuple)
        sv1 = {}
        for p in range(9):
            sv1[utils.PLANET_NAMES[p]]=utils.SHADVARGAMSA_NAMES[sv[p][0]]+'\n('+sv[p][1]+ ')\n'+str(round(sv[p][2],1))
        sv = charts.vimsopaka_sapthavarga_of_planets(jd_at_dob, place_as_tuple)
        sv2 = {}
        for p in range(9):
            sv2[utils.PLANET_NAMES[p]]=utils.SAPTAVARGAMSA_NAMES[sv[p][0]]+'\n('+sv[p][1]+ ')\n'+str(round(sv[p][2],1))
        sv = charts.vimsopaka_dhasavarga_of_planets(jd_at_dob, place_as_tuple)
        dv = {}
```
- Observed behavior: Consumer expects [count,tags,score] row shape.

### GS22

- Behavior: Aayu consumer composes combustion and retrograde state for longevity adjustments.
- Source: `src/jhora/horoscope/dhasa/graha/aayu.py:L46-L58`
- Excerpt:
```python
    planets_in_combustion = charts.planets_in_combustion(planet_positions)
    if _DEBUG: print('planets_in_combustion',planets_in_combustion)
    planets_in_retrograde = charts.planets_in_retrograde(planet_positions)
    """
    # The superior planets (Mars, Jupiter and Shani) are far from Surya during their retrogression
    #    Add 2,4 to ignore planets if retrograde
    [planets_in_retrograde.remove(sp) for sp in [2,4] if sp in planets_in_retrograde]
    """
    if _DEBUG: print('planets_in_retrograde',planets_in_retrograde)
    _harana_factors = {p:1.0 for p in [const._ascendant_symbol]+const.SUN_TO_SATURN}
    if _DEBUG: print('ignore_planets',ignore_planets)
    temp_dict = {p:0.5 for p in planets_in_combustion if p not in ignore_planets}
```
- Observed behavior: State lists feed fractional longevity penalties.

### GS23

- Behavior: Dosha consumer uses retrograde and combustion booleans in rule chain.
- Source: `src/jhora/horoscope/chart/dosha.py:L110-L116`
- Excerpt:
```python
    c8 = 2 in charts.planets_in_retrograde(planet_positions) ; _me.append(c8)
    c9_1 = 2 in charts.planets_in_combustion(planet_positions)
    c9_2 = mars_long < const.rasi_sandhi_duration or mars_long > (30.0-const.rasi_sandhi_duration)
    c9 = c9_1 or c9_2 ; _me.append(c9)
    c10 = house.house_owner_from_planet_positions(planet_positions, lagna_house)==const.MARS_ID; _me.append(c10)
    c11 = False ; _me.append(c11)
    c12 = const.house_strengths_of_planets[const.MARS_ID][mars_house] >= const._FRIEND; _me.append(c12)
```
- Observed behavior: Consumer uses state presence checks directly in dosha logic.

### GS24

- Behavior: Tajaka yoga consumer gates yoga outcomes on combustion/retrograde.
- Source: `src/jhora/horoscope/transit/tajaka_yoga.py:L318-L320`
- Excerpt:
```python
    chk.append([x in charts.planets_in_combustion(planet_positions) or y in charts.planets_in_combustion(planet_positions) for x,y in iy_pairs])
    chk.append([x in charts.planets_in_retrograde(planet_positions) or y in charts.planets_in_retrograde(planet_positions) for x,y in iy_pairs])
    chk.append([const.house_strengths_of_planets[x][p_to_h[x]] < const._NEUTRAL_SAMAM or const.house_strengths_of_planets[y][p_to_h[y]]<2 for x,y in iy_pairs])
```
- Observed behavior: Transit yoga conditions combine combustion and retrograde constraints.

### ABSENCE-OF-AVASTHA

- Behavior: No direct Avastha implementation found in in-scope files.
- Source: `research/graha_longitudes_and_states/_coverage_graha_states_callsites_engine_plus_consumers.tsv`
- Excerpt:
```text
Evidence row is present in generated callsite inventory.
```
- Observed behavior: Pattern scan found no explicit avastha/jagrad/baladi implementation in locked scope.

### GS900

- Behavior: Residual matched rows are retained for completeness.
- Source: `research/graha_longitudes_and_states/_coverage_graha_states_callsites_engine_plus_consumers.tsv`
- Excerpt:
```text
Evidence row is present in generated callsite inventory.
```
- Observed behavior: Non-focused matches remain visible via GS900 rows.

## Conflict / ambiguity register

- UNCERTAIN-GS-SHADBALA-01: formula and normalization vary across bala sub-components.
- UNCERTAIN-GS-STATE-01: retrograde differs between drik speed-sign and chart sun-window methods.
- UNCERTAIN-GS-COMBUST-RETRO-01: combustion logic branches on retrograde state.
- UNCERTAIN-GS-DIGNITY-01: matrix dignity and deep-longitude dignity can diverge.
- UNCERTAIN-GS-OUTIDX-01: producer payloads are heterogeneous across bala/state APIs.
- UNCERTAIN-GS-AVASTHA-ABSENCE-01: absence confirmed in locked scope.

## Coverage ledger

- Inventory file: `research/graha_longitudes_and_states/_coverage_graha_states_callsites_engine_plus_consumers.tsv`
- Inventory columns: `file`, `line`, `pattern`, `function_context`, `anchor_id`, `scope_class`
- Inventory row count: `2172`
- Unique `(file,function_context)` count: `592`
- Rows by scope_class: `engine_core=976`, `consumer_core=234`, `residual=962`
- Residual rows (`GS900`): `2171`
- Shadbala component matrix: `research/graha_longitudes_and_states/_coverage_graha_states_shadbala_component_matrix.tsv`
- State logic matrix: `research/graha_longitudes_and_states/_coverage_graha_states_state_logic_matrix.tsv`
- Output contract matrix: `research/graha_longitudes_and_states/_coverage_graha_states_output_contract_matrix.tsv`

## Sanity checks

- command: `rg -n "^### GS[0-9]+|^### ABSENCE-OF-AVASTHA|^### GS900" research/graha_longitudes_and_states/graha_states_behavior_contract_map.engine_plus_consumers.md -S`
- command: `rg -n "UNCERTAIN-GS-" research/graha_longitudes_and_states/graha_states_behavior_contract_map.engine_plus_consumers.md -S`
- command: `rg -n "Source:" research/graha_longitudes_and_states/graha_states_behavior_contract_map.engine_plus_consumers.md -S`
- command: `Get-Content research/graha_longitudes_and_states/_coverage_graha_states_callsites_engine_plus_consumers.tsv | Measure-Object -Line`
- command: `Get-Content research/graha_longitudes_and_states/_coverage_graha_states_shadbala_component_matrix.tsv | Measure-Object -Line`
- command: `Get-Content research/graha_longitudes_and_states/_coverage_graha_states_state_logic_matrix.tsv | Measure-Object -Line`
- command: `Get-Content research/graha_longitudes_and_states/_coverage_graha_states_output_contract_matrix.tsv | Measure-Object -Line`
