# longevity_behavior_contract_map.engine_plus_consumers.md

## Snapshot identity (FACTS)

- pyjhora_root: `D:\lab\Pyjhora`
- extraction_timestamp_local: `2026-02-27 21:24:41`
- in-scope files: `6`
- in-scope file digests (SHA256):
  - `src/jhora/horoscope/dhasa/graha/aayu.py` -> `bbc866d51112f88969509e6c73fdf61912ee8e16e3811a52adc429e6e956dd96` (bytes: `33652`)
  - `src/jhora/horoscope/prediction/longevity.py` -> `a350b3fdaa8faa3d34546d2096ebed79e1e06d370d69bb7fe701682235f682c2` (bytes: `11459`)
  - `src/jhora/horoscope/chart/house.py` -> `d2d0d2b9a1e382879b0f191498bcc8dc9d4ef74224925ffb522f2cc0e4329861` (bytes: `80854`)
  - `src/jhora/horoscope/dhasa/raasi/sandhya.py` -> `09902bd78d85b2964e9aee38e6c7c441b55dbca1ec1544c0b930bfff692c7309` (bytes: `3811`)
  - `src/jhora/const.py` -> `2dacc910fce9babc69582491b52cde9fd23ab9dde835d41efb65fc0f79e00ba8` (bytes: `79727`)
  - `src/jhora/horoscope/main.py` -> `cecb9d933245d6df820425f80d28da3153746215c8b283c66d4fa65c86ee58bd` (bytes: `128308`)

## Scope (FACTS)

- In-scope engine files:
  - `src/jhora/horoscope/dhasa/graha/aayu.py`
  - `src/jhora/horoscope/prediction/longevity.py`
  - `src/jhora/horoscope/chart/house.py`
  - `src/jhora/horoscope/dhasa/raasi/sandhya.py`
  - `src/jhora/const.py`
- In-scope consumers/config:
  - `src/jhora/horoscope/main.py`
- Out-of-scope:
  - UI modules
  - tests
  - `src/jhora/panchanga/drik1.py`
  - deep consumers outside one-hop list

## Pattern inventory (FACTS)

- `harana`
- `bharana`
- `_apply_harana`
- `chakrapata`
- `astangata`
- `shatru_kshetra`
- `krurodaya`
- `aayu`
- `ayur`
- `longevity`
- `life_span`
- `pindayu`
- `nisargayu`
- `amsayu`
- `sandhya`
- `alpaayu`
- `madhyaayu`
- `poornaayu`
- `alpa`
- `madhya`
- `poorna`
- `is_amsayu`
- `min(`
- `method=`
- `NOT FULLY IMPLEMENTED`
- `return _pindayu_santhanam`
- `return _nisargayu_santhanam`
- `TODO`

## Behavior taxonomy (FACTS)

- constants and year buckets: `AY01`, `AY02`
- aayu engine routing and output contracts: `AY03`, `AY04`
- base formula paths and dead branches: `AY05`, `AY06`, `AY07`, `AY08`, `AY09`, `AY10`
- harana/bharana sequencing and operators: `AY11`, `AY12`, `AY13`, `AY14`, `AY15`, `AY16`
- parallel classification systems: `AY17`, `AY18`
- parallel ayurdasa path: `AY19`
- residual inventory: `AY900`

## Evidence anchors (AY01..AYNN, AY900)

### AY01

- Behavior: Longevity category and year matrices are defined in constants.
- Source: `src/jhora/const.py:L398-L399`
- Excerpt:
```python
longevity = {0:[(0,0),(1,2),(2,1)],1:[(0,1),(1,0),(2,2)],2:[(0,2),(1,1),(2,0)]} #0=>Fixed, 1=> Movable, 2=>Dual
longevity_years = [[32,36,40],[64,72,80],[96,108,120]] # 0th element Short Life, 1st : Middle Life, 2nd element: Long Life
```
- Observed behavior: Fixed/movable/dual mapping and year buckets are hardcoded.

### AY02

- Behavior: Pindayu/Nisargayu baseline constants and labels are module-level constants.
- Source: `src/jhora/const.py:L623-L629`
- Excerpt:
```python
pindayu_full_longevity_of_planets=[19,25,15,12,15,21,20] #in years for Sun to Saturn - when they are in highest exhaltation
pindayu_base_longevity_of_planets=[0.5*full for full in pindayu_full_longevity_of_planets] #in years for Sun to Saturn - when they are in deepest debilitation
nisargayu_full_longevity_of_planets=[20,1,2,9,18,20,50] #in years for Sun to Saturn - when they are in highest exhaltation
nisargayu_base_longevity_of_planets=[0.5*full for full in nisargayu_full_longevity_of_planets] #in years for Sun to Saturn - when they are in deepest debilitation
aayu_dhasa_types = ['pinda','nisarga','amsa']
kaala_dhasa_types = ['dawn','day','dusk','night']
aayu_types = {0:['alpaayu','0-32'],1:['madhyaayu','33-70'],2:['poornaayu','71-100']}
```
- Observed behavior: Base and full values plus aayu labels are centralized.

### AY03

- Behavior: Main consumer routes aayu dhasa via get_dhasa_antardhasa.
- Source: `src/jhora/horoscope/main.py:L1149-L1158`
- Excerpt:
```python
    def _get_aayu_dhasa_bhukthi(self,dob,tob,place,**kwargs):
        jd = utils.julian_day_number(dob, tob)
        from jhora.horoscope.dhasa.graha import aayu
        self._aayu_dhasa_type,db = aayu.get_dhasa_antardhasa(jd, place,include_antardhasa=True,**kwargs)
        dhasa_bhukti_info = []
        for i in range(len(db)):
            [dhasa_lord, bukthi_lord,bukthi_start,_]=db[i]
            dhasa_str=self._ascendant_str if dhasa_lord==const._ascendant_symbol else utils.PLANET_NAMES[dhasa_lord]
            bukthi_str=self._ascendant_str if bukthi_lord==const._ascendant_symbol else utils.PLANET_NAMES[bukthi_lord]                
            dhasa_bhukti_info.append((dhasa_str+'-'+bukthi_str,bukthi_start))
```
- Observed behavior: Consumer captures _aayu_dhasa_type and unpacks 4-field rows.

### AY04

- Behavior: Aayu engine entrypoint publishes aayu-type and dhasa rows.
- Source: `src/jhora/horoscope/dhasa/graha/aayu.py:L409-L460`
- Excerpt:
```python
def get_dhasa_antardhasa(jd,place,aayur_type=None,include_antardhasa=True,apply_haranas=True,dhasa_method=2,
                         divisional_chart_factor=9,chart_method=1):
    """
        provides Aayu dhasa bhukthi for a given date in julian day (includes birth time)
        @param jd: Julian day for birthdate and birth time
        @param place: Place as tuple (place name, latitude, longitude, timezone) 
        @param aayur_type (0=Pindayu, 1=Nisargayu, 2=Amsayu, None=Automatically determine whichever is applicable)
        @param include_antardhasa: True (include) False (exclude) antardhasa (Default=True)
        @param apply_haranas: (True/False) whether to or not to apply haranas (Default=True)
        @return: a list of [dhasa_lord,bhukthi_lord,bhukthi_start] if include_antardhasa=True
        @return: a list of [dhasa_lord,dhasa_start] if include_antardhasa=False
          Example: [ [7, 5, '1915-02-09'], [7, 0, '1917-06-10'], [7, 1, '1918-02-08'],...]
```
- Observed behavior: Dispatches among pindayu/nisargayu/amsayu using seed selector.

### AY05

- Behavior: Aayu module self-labels implementation incompleteness.
- Source: `src/jhora/horoscope/dhasa/graha/aayu.py:L22-L25`
- Excerpt:
```python
    Computation of pindayu, Nisargayu, Amsayu dasa
    NOTE: !!! DO NOT USE THIS YET - NOT FULLY IMPLEMENTED YET !!!
    
```
- Observed behavior: WIP disclaimer exists directly in module header.

### AY06

- Behavior: Pindayu base formula is implemented in santhanam path.
- Source: `src/jhora/horoscope/dhasa/graha/aayu.py:L282-L297`
- Excerpt:
```python
def _pindayu_santhanam(planet_positions,apply_haranas=True,method=1):
    planet_base_longevity = {}
    for planet in const.SUN_TO_SATURN:
        planet_long = planet_positions[planet+1][1][0]*30+planet_positions[planet+1][1][1]
        if _DEBUG: print('planet',planet,'planet_long',planet_long)
        arc_of_longevity = utils.norm360(360+planet_long - const.planet_deep_exaltation_longitudes[planet])
        if _DEBUG: print('planet',planet,'arc_of_longevity',arc_of_longevity)
        if arc_of_longevity > 180.0:
            planet_base_longevity[planet] = const.pindayu_full_longevity_of_planets[planet]*arc_of_longevity/360.0
        else:
            planet_base_longevity[planet] = const.pindayu_full_longevity_of_planets[planet] - const.pindayu_full_longevity_of_planets[planet]*arc_of_longevity/360.0
        if _DEBUG: print('planet',planet,'planet_base_longevity santhanam',planet_base_longevity[planet])
```
- Observed behavior: Arc-based base years are computed before harana.

### AY07

- Behavior: Pindayu wrapper contains dead branch after early return.
- Source: `src/jhora/horoscope/dhasa/graha/aayu.py:L299-L310`
- Excerpt:
```python
def _pindayu(planet_positions,apply_haranas=True,method=2):
    return _pindayu_santhanam(planet_positions, apply_haranas, method)
    planet_base_longevity = {}
    for planet in const.SUN_TO_SATURN:
        planet_long = planet_positions[planet+1][1][0]*30+planet_positions[planet+1][1][1]
        arc_of_longevity = utils.norm360(360+planet_long - const.planet_deep_exaltation_longitudes[planet])
        effective_arc = arc_of_longevity - 180 if arc_of_longevity > 180 else arc_of_longevity
        planet_base_longevity[planet] = const.pindayu_full_longevity_of_planets[planet]*effective_arc/360.0
    if _DEBUG: print('planet_base_longevity',planet_base_longevity)
    if apply_haranas:
        return _apply_harana(planet_positions,planet_base_longevity,method=method)
    else:
```
- Observed behavior: Code after immediate return is unreachable.

### AY08

- Behavior: Nisargayu base formula is implemented in santhanam path.
- Source: `src/jhora/horoscope/dhasa/graha/aayu.py:L312-L327`
- Excerpt:
```python
def _nisargayu_santhanam(planet_positions,apply_haranas=True,method=1):
    planet_base_longevity = {}
    for planet in const.SUN_TO_SATURN:
        planet_long = planet_positions[planet+1][1][0]*30+planet_positions[planet+1][1][1]
        if _DEBUG: print('_nisargayu_santhanam','planet_long',planet_long)
        arc_of_longevity = utils.norm360(360+planet_long - const.planet_deep_exaltation_longitudes[planet])
        if _DEBUG: print('_nisargayu_santhanam','arc_of_longevity',arc_of_longevity)
        if arc_of_longevity > 180.0:
            planet_base_longevity[planet] = const.nisargayu_full_longevity_of_planets[planet]*arc_of_longevity/360.0
        else:
            planet_base_longevity[planet] = const.nisargayu_full_longevity_of_planets[planet] - const.nisargayu_full_longevity_of_planets[planet]*arc_of_longevity/360.0
        if _DEBUG: print(planet,'planet_base_longevity santhanam',planet_base_longevity[planet])
```
- Observed behavior: Arc-based base years are computed before harana.

### AY09

- Behavior: Nisargayu wrapper contains dead branch after early return.
- Source: `src/jhora/horoscope/dhasa/graha/aayu.py:L329-L345`
- Excerpt:
```python
def _nisargayu(planet_positions,apply_haranas=True,method=2):
    return _nisargayu_santhanam(planet_positions, apply_haranas, method)
    if method==1: return _nisargayu_santhanam(planet_positions, apply_haranas, method)
    planet_base_longevity = {}
    for planet in const.SUN_TO_SATURN:
        planet_long = planet_positions[planet+1][1][0]*30+planet_positions[planet+1][1][1]
        if _DEBUG: print('_nisargayu','planet_long',planet_long)
        arc_of_longevity = utils.norm360(planet_long - const.planet_deep_exaltation_longitudes[planet])
        if _DEBUG: print('_nisargayu','arc_of_longevity',arc_of_longevity,const.planet_deep_exaltation_longitudes[planet])
        effective_arc = arc_of_longevity - 180 if arc_of_longevity > 180 else arc_of_longevity
        if _DEBUG: print('_nisargayu','effective_arc',effective_arc)
        planet_base_longevity[planet] = const.nisargayu_full_longevity_of_planets[planet]*effective_arc/360.0
```
- Observed behavior: Alternate method block is unreachable as written.

### AY10

- Behavior: Amsayu computes base then applies Bharana and Harana.
- Source: `src/jhora/horoscope/dhasa/graha/aayu.py:L348-L360`
- Excerpt:
```python
def _amsayu(planet_positions,apply_haranas=True,method=1):
    planet_base_longevity = {}
    for planet,(h,p_long) in planet_positions[1:const._pp_count_upto_saturn]: #range(7):
        planet_long = h*30+p_long
        planet_base_longevity[planet] = (planet_long*108) % 12
        if method==2:planet_base_longevity[planet] = (planet_long*60/200) %12 # Varhamihira
    if _DEBUG: print('planet_base_longevity',planet_base_longevity)
    if apply_haranas:
        bh = _bharana(planet_positions)
        ah =  _apply_harana(planet_positions,planet_base_longevity,is_amsayu=True)
        graha_aayu = {p:ah[p]*bh[p] for p in ah.keys()}
        return graha_aayu
```
- Observed behavior: Amsayu path multiplies bharana and harana results.

### AY11

- Behavior: _apply_harana composes reductions in sequential chain.
- Source: `src/jhora/horoscope/dhasa/graha/aayu.py:L246-L280`
- Excerpt:
```python
def _apply_harana(planet_positions,base_aayu,is_amsayu=False,method=2):
        """ TODO: For AMSAYU there are following special rules
            The base aayu arrived at the previous step needs to increased (Bharana) based on occupation in exaltation, 
            retrogression, Svakshetra, Vargottamamsa, Sva-navamsa, Sva-Drekkana.
            Apply Bharana on base aayu and then haranas
            The Bharanas (Increase in the Base Longevity)
                1.    When the Graha is Retrograde, Exalted or in Svakshetra, then multiply by 3.
                2.    When the Graha is in Sva-Navamsa, Sva-Drekkana or in Vargottama Navamsa, then multiply by 2.
                3.    If a multiplication by both 3 and 2 is applicable to a graha, the higher multiplication factor is applied.
            The Haranas (Decrease in the Base Longevity)
                1.    The same Haranas as the Pindayu and Nisargayu Methods are also applied here. Only Krurodaya Harana is not applied.
                2.    If more than two Haranas between Shatrukshetra and Astangata Harana is applicable to the graha, then the only the higher reduction is applied. The Chakrapata Harana is not affected by this and need to be carried out independently.
```
- Observed behavior: Reduction chain is explicit and ordered.

### AY12

- Behavior: Astangata and shatru_kshetra are combined with min().
- Source: `src/jhora/horoscope/dhasa/graha/aayu.py:L262-L267`
- Excerpt:
```python
        ah = _astangata_harana(planet_positions) # does not depend on the method
        if _DEBUG: print('_astangata_harana',ah,final_harana)
        """ Shatru Kshetra Harana """
        skh = _shatru_kshetra_harana(planet_positions)
        final_harana.update({p:min(v1,skh[p]) for p,v1 in ah.items()})
        if _DEBUG: print('_shatru_kshetra_harana',skh,final_harana)
```
- Observed behavior: Combine operator is min, not multiplicative.

### AY13

- Behavior: Chakrapata is merged through another min() pass.
- Source: `src/jhora/horoscope/dhasa/graha/aayu.py:L269-L271`
- Excerpt:
```python
        ch = _chakrapata_harana(planet_positions) if method==2 else _chakrapata_harana_santhanam(planet_positions)#jd, place)
        final_harana.update({p:min(v1,ch[p]) for p,v1 in final_harana.items()})
        if _DEBUG: print('_chakrapata_harana',ch,final_harana)
```
- Observed behavior: Sequential min aggregation continues.

### AY14

- Behavior: Krurodaya is bypassed for Amsayu.
- Source: `src/jhora/horoscope/dhasa/graha/aayu.py:L272-L276`
- Excerpt:
```python
        """ Krurodaya Harana Not applicable for Amsayu """
        kh = {p:1.0 for p in [const._ascendant_symbol]+const.SUN_TO_SATURN}
        if not is_amsayu: kh = _krurodaya_harana(planet_positions)
        final_harana.update({p:min(v1,kh[p]) for p,v1 in final_harana.items()})
        if _DEBUG: print('_krurodaya_harana',kh,final_harana)
```
- Observed behavior: is_amsayu flag disables krurodaya application.

### AY15

- Behavior: Krurodaya method-2 block includes explicit TODO for missing bullets.
- Source: `src/jhora/horoscope/dhasa/graha/aayu.py:L188-L201`
- Excerpt:
```python
def _krurodaya_harana(planet_positions,method=2):
    """
        Reduce by Sum of Graha Aayu of all the Grahas arrived at previous steps * Lagna Longitude in the Rasi / 360º
        For Krurodaya Harana, firstly the Lagna fraction needs to be found, which is to be applied to the sum of all 
            the Graha Aayus to determine the reduction that needs to be applied.
    •    This Harana is applied only when a Krura Graha viz., Surya, Shani and Shukra is rising with the Lagna.
    •    If more than one Krura Graha rises in the Lagna, then the one occupying closer to the Lagna degree is considered 
        for this Harana. The remaining are ignored.
    •    If a Shubha graha viz., Guru, Shukra, Budha and Chandra occupy or aspect the Lagna, then the Harana is halved.
    •    If a Shubha Graha also rises with the Krura Graha in the Lagna, then the Harana is ignore, provided the Shubha Graha is closer to the Lagna degree.
         
    """
```
- Observed behavior: Specification and implementation are partially diverged.

### AY16

- Behavior: Bharana factors (3x/2x) are computed in dedicated function.
- Source: `src/jhora/horoscope/dhasa/graha/aayu.py:L226-L245`
- Excerpt:
```python
def _bharana(planet_positions):
    """ This is only needed for Amsayu """
    """
    The Bharanas (Increase in the Base Longevity)
        1.    When the Graha is Retrograde, Exalted or in Svakshetra, then multiply by 3.
        2.    When the Graha is in Sva-Navamsa, Sva-Drekkana or in Vargottama Navamsa, then multiply by 2.
        3.    If a multiplication by both 3 and 2 is applicable to a graha, the higher multiplication factor is applied.
    """
    _bharana_factors = {p:1.0 for p in [const._ascendant_symbol]+const.SUN_TO_SATURN}
    retrograde_planets = charts.planets_in_retrograde(planet_positions)
    pp_3 = charts.drekkana_chart(planet_positions); pp_9 = charts.navamsa_chart(planet_positions)
    chk1 = lambda p:p in retrograde_planets or const.house_strengths_of_planets[p][planet_positions[p+1][1][0]] in [const._EXALTED_UCCHAM, const._OWNER_RULER]
```
- Observed behavior: Bharana increase rules are separated from Harana.

### AY17

- Behavior: Prediction module computes alpa/madhya/poorna class by pairing logic.
- Source: `src/jhora/horoscope/prediction/longevity.py:L152-L194`
- Excerpt:
```python
def life_span_range(jd,place):
    """
        Alpayu = 0; Madhyayu = 1; Poornayu = 2
    """
    def _get_aayu(sign1, sign2):
        if sign1 in const.fixed_signs and sign2 in const.fixed_signs:
            return 0
        elif sign1 in const.movable_signs and sign2 in const.movable_signs:
            return 2
        elif sign1 in const.dual_signs and sign2 in const.dual_signs:
            return 1
        elif (sign1 in const.fixed_signs and sign2 in const.movable_signs) or \
```
- Observed behavior: Standalone life_span_range classification path exists.

### AY18

- Behavior: House module exposes second independent longevity classification path.
- Source: `src/jhora/horoscope/chart/house.py:L1098-L1149`
- Excerpt:
```python
def longevity(dob,tob,place,divisional_chart_factor=1):
    jd = utils.julian_day_number(dob, tob)
    planet_positions = drik.dhasavarga(jd, place, divisional_chart_factor=divisional_chart_factor)
    ascendant_constellation, ascendant_longitude, _, _ = drik.ascendant(jd,place)
    planet_positions = [[const._ascendant_symbol,(ascendant_constellation, ascendant_longitude)]] + planet_positions
    rasi_type = lambda rasi:[index for index,r_type in enumerate([const.fixed_signs,const.movable_signs,const.dual_signs]) if rasi in r_type][0]
    p_to_h = utils.get_planet_house_dictionary_from_planet_positions(planet_positions)
    #print('p_to_h',p_to_h)
    h_to_p = utils.get_house_planet_list_from_planet_positions(planet_positions)
    #print('h_to_p',h_to_p)
    lagna_house = p_to_h['L']
    # first pair houses of Lagna Lord and 8th lord 
```
- Observed behavior: Parallel classification path uses const.longevity_years matrix.

### AY19

- Behavior: Sandhya is parallel ayurdasa path with fixed duration spread.
- Source: `src/jhora/horoscope/dhasa/raasi/sandhya.py:L22-L64`
- Excerpt:
```python
    Sandhya is another Ayurdasa system. Concept: Sandhya is the Dvadashāńśa Ayurdaya of the Param Ayurdaya. 
    In this dasa system, the parama-ayush is spread among the 12 Rāśis, making the dasa span of each Rāśi as 1/12th of the Paramaayush. 
    For humans the Paramayush have been agreed by savants as 120 years. Hence the span of each Sandhya Dasa is 10 years. 
    
    Also includes Panchaka Dasa Variation - wherein 10 years are divided into 3 compartments: 
    1 rasi - 61/30, 3 rasis-61/60 and 8 rasis - 61/90  - each fraction of 10 years 
"""
from jhora import utils, const
from jhora.panchanga import drik
from jhora.horoscope.chart import charts

_sandhya_duration = [10 for _ in range(12)]
```
- Observed behavior: Ayurdaya-related but distinct from pinda/nisarga/amsa.

### AY900

- Behavior: Residual matched rows are retained in callsite inventory.
- Source: `research/longevity_and_ayurdaya/_coverage_longevity_callsites_engine_plus_consumers.tsv`
- Excerpt:
```text
Rows with anchor_id=AY900 remain in inventory as residual evidence.
```
- Observed behavior: Non-focused matches remain visible as residual evidence.

## Conflict / ambiguity register

- UNCERTAIN-AY-HARANA-COMBINE: Harana aggregation uses `min` operator instead of multiplicative composition.
- UNCERTAIN-AY-DEAD-CODE: `_pindayu` and `_nisargayu` include unreachable branches after early return.
- UNCERTAIN-AY-DUPLICATE-CLASS: longevity class logic appears in both prediction and house modules.
- UNCERTAIN-AY-METHOD-PROPAGATION: method 1/2 behavior is partially divergent and partially bypassed.

## Coverage ledger

- Inventory file: `research/longevity_and_ayurdaya/_coverage_longevity_callsites_engine_plus_consumers.tsv`
- Inventory columns: `file`, `line`, `pattern`, `function_context`, `anchor_id`, `scope_class`
- Inventory row count: `1339`
- Unique `(file,function_context)` count: `389`
- Rows by scope_class: `engine_core=456`, `consumer_core=66`, `residual=817`
- Residual rows (`AY900`): `1339`
- Base matrix: `research/longevity_and_ayurdaya/_coverage_longevity_base_ayur_formula_matrix.tsv`
- Harana matrix: `research/longevity_and_ayurdaya/_coverage_longevity_harana_reduction_matrix.tsv`
- Bharana matrix: `research/longevity_and_ayurdaya/_coverage_longevity_bharana_increase_matrix.tsv`
- Classification matrix: `research/longevity_and_ayurdaya/_coverage_longevity_classification_matrix.tsv`
- Output-contract matrix: `research/longevity_and_ayurdaya/_coverage_longevity_output_contract_matrix.tsv`

## Sanity checks

- command: `rg -n "^### AY[0-9]+|^### AY900" research/longevity_and_ayurdaya/longevity_behavior_contract_map.engine_plus_consumers.md -S`
- command: `rg -n "UNCERTAIN-AY-" research/longevity_and_ayurdaya/longevity_behavior_contract_map.engine_plus_consumers.md -S`
- command: `rg -n "Source:" research/longevity_and_ayurdaya/longevity_behavior_contract_map.engine_plus_consumers.md -S`
- command: `Get-Content research/longevity_and_ayurdaya/_coverage_longevity_callsites_engine_plus_consumers.tsv | Measure-Object -Line`
- command: `Get-Content research/longevity_and_ayurdaya/_coverage_longevity_base_ayur_formula_matrix.tsv | Measure-Object -Line`
- command: `Get-Content research/longevity_and_ayurdaya/_coverage_longevity_harana_reduction_matrix.tsv | Measure-Object -Line`
- command: `Get-Content research/longevity_and_ayurdaya/_coverage_longevity_bharana_increase_matrix.tsv | Measure-Object -Line`
- command: `Get-Content research/longevity_and_ayurdaya/_coverage_longevity_classification_matrix.tsv | Measure-Object -Line`
- command: `Get-Content research/longevity_and_ayurdaya/_coverage_longevity_output_contract_matrix.tsv | Measure-Object -Line`
