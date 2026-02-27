# transit_tajaka_behavior_contract_map.engine_plus_consumers.md

## Snapshot identity (FACTS)

- pyjhora_root: `D:\lab\Pyjhora`
- extraction_timestamp_local: `2026-02-27 23:17:24`
- in-scope files: `11`
- in-scope file digests (SHA256):
  - `src/jhora/horoscope/transit/tajaka.py` -> `8f1d7c369363c953ff21405cf4a7243c488cc6d155315b80e279a861f58bce17` (bytes: `40858`)
  - `src/jhora/horoscope/transit/tajaka_yoga.py` -> `a77b4c87a75ab511ff86a7f70c10aca3b7d4447e5d5758defa21b1865de58347` (bytes: `23295`)
  - `src/jhora/horoscope/transit/saham.py` -> `193dbef2e6ff868752f74aad970d43440662334dd6d6eb60373368838390c6a9` (bytes: `30075`)
  - `src/jhora/horoscope/dhasa/annual/mudda.py` -> `66ea9c241703611ca21dc8a67ed4f15e8b5052ad2f46d2e88b48ebc3476c3743` (bytes: `8228`)
  - `src/jhora/horoscope/dhasa/annual/patyayini.py` -> `794b1a1a7e7bb31bdd1f0e570b18de90784dc15ff62a815a9f72481b2be1baf2` (bytes: `3611`)
  - `src/jhora/horoscope/dhasa/raasi/narayana.py` -> `7ad54f6d3e0e6380962b43dfb3c3cba8922776df9628dfa9f6b324caaf7d1a98` (bytes: `11875`)
  - `src/jhora/panchanga/drik.py` -> `9790dcdf442910b1eaa260b16c346c6696438eb6955c0a520c1be220ba3497bc` (bytes: `186944`)
  - `src/jhora/horoscope/chart/strength.py` -> `d0d92d6b4b62dbc31d40a3455e214d8b0917e8608ca1f6148a200dcb512d1d93` (bytes: `53346`)
  - `src/jhora/horoscope/chart/charts.py` -> `34c49af9fb3359fdb243f2a467404b7a849e35b9def9e2961a45a4027c8619b2` (bytes: `141395`)
  - `src/jhora/const.py` -> `2dacc910fce9babc69582491b52cde9fd23ab9dde835d41efb65fc0f79e00ba8` (bytes: `79727`)
  - `src/jhora/horoscope/main.py` -> `cecb9d933245d6df820425f80d28da3153746215c8b283c66d4fa65c86ee58bd` (bytes: `128308`)

## Scope (FACTS)

- In-scope engine files:
  - `src/jhora/horoscope/transit/tajaka.py`
  - `src/jhora/horoscope/transit/tajaka_yoga.py`
  - `src/jhora/horoscope/transit/saham.py`
  - `src/jhora/horoscope/dhasa/annual/mudda.py`
  - `src/jhora/horoscope/dhasa/annual/patyayini.py`
  - `src/jhora/horoscope/dhasa/raasi/narayana.py`
  - `src/jhora/panchanga/drik.py`
  - `src/jhora/horoscope/chart/strength.py`
  - `src/jhora/horoscope/chart/charts.py`
  - `src/jhora/const.py`
- In-scope consumers/config:
  - `src/jhora/horoscope/main.py`
- Out-of-scope:
  - UI modules
  - tests
  - `src/jhora/panchanga/drik1.py`
  - docs/data/lang folders
  - deep redesign decisions

## Pattern inventory (FACTS)

- `annual_chart`
- `varsha_pravesh`
- `maasa_pravesh`
- `sixty_hour_chart`
- `muntha`
- `muntha_house`
- `lord_of_the_year`
- `lord_of_the_month`
- `_get_lord_candidates`
- `pancha_vargeeya_bala`
- `pancha_vargeeya_bala_strength_threshold`
- `ithasala`
- `eesarpha`
- `kamboola`
- `tajaka_yoga`
- `next_solar_date`
- `__next_solar_jd`
- `inverse_lagrange`
- `tropical_year`
- `solar_longitude`
- `sidereal_longitude`
- `mudda`
- `varsha_vimsottari`
- `patyayini`
- `varsha_narayana`
- `gochara`
- `gochara_engine`

## Behavior taxonomy (FACTS)

- solar return search and ephemeris: `TT01`, `TT02`, `TT03`, `TT04`
- tajaka chart lifecycle and annual lords: `TT05`, `TT06`, `TT07`, `TT08`
- panchavargiya and tajaka yoga rules: `TT09`, `TT10`, `TT11`
- annual dhasa integration: `TT12`, `TT13`, `TT14`, `TT15`
- negative engine fact: `ABSENCE-OF-GOCHARA-ENGINE`
- residual inventory: `TT900`

## Evidence anchors (TT01..TTNN, TT900)

### TT01

- Behavior: Solar return refinement uses inverse Lagrange interpolation over sampled offsets.
- Source: `src/jhora/panchanga/drik.py:L2235-L2242`
- Excerpt:
```python
    offsets = [0.0, 0.25, 0.5, 0.75, 1.0] 
    solar_longs = [ (solar_longitude(sank_sunrise + t)) for t in offsets ]
    #print(solar_longs,sun_long)
    solar_hour = utils.inverse_lagrange(offsets, solar_longs, sun_long) # Do not move % 360 above
    #print('solar_hour',solar_hour)
    sank_jd_utc = utils.gregorian_to_jd(sank_date)
    solar_hour1 = (sank_sunrise + solar_hour - sank_jd_utc)*24+place.timezone
    next_solar_jd = swe.julday(sank_date[0],sank_date[1],sank_date[2],solar_hour1)
```
- Observed behavior: evidence line block shows the active rule in this path.

### TT02

- Behavior: next_solar_date seeds search with tropical-year based jd_extra and target solar longitude.
- Source: `src/jhora/panchanga/drik.py:L2262-L2270`
- Excerpt:
```python
    sun_long_extra = ((years-1)*360+(months-1)*30+(sixty_hours-1)*2.5)%360
    jd_extra = int(((years-1)+(months-1)/12+(sixty_hours-1)/144)*const.tropical_year) #const.sidereal_year)
    #print('jd_extra',jd_extra)
    jd_next = jd_at_dob+jd_extra
    #print('jd_next',jd_next,swe.revjul(jd_next))
    #print('sun_long_extra',sun_long_extra)
    sun_long_next = (sun_long_at_dob+sun_long_extra)%360
    #print((years,months,sixty_hours),(int(sun_long_next/30),utils.to_dms(sun_long_next%30,is_lat_long='plong')),(y,m,d,utils.to_dms(fh)))
    return __next_solar_jd(jd_next,place, sun_long_next)
```
- Observed behavior: evidence line block shows the active rule in this path.

### TT03

- Behavior: __next_solar_jd performs linear day-step bracketing with TODO convergence guard.
- Source: `src/jhora/panchanga/drik.py:L2217-L2230`
- Excerpt:
```python
    """
        TODO: Handle While loop if not converging - provide max count to stop
    """
    jd_next = jd
    sl = solar_longitude(jd_next)
    while True:
        #print(jd_next,sl,sun_long,jd_to_gregorian(jd_next))
        sank_date = swe.revjul(jd_next)
        #print('sank_date',sank_date,sun_long,sl,sun_long+1)
        if sl<sun_long+1 and sl>sun_long:
            jd_next -= 1
            break
```
- Observed behavior: evidence line block shows the active rule in this path.

### TT04

- Behavior: sidereal_longitude delegates ephemeris evaluation to swe.calc_ut with sidereal flags.
- Source: `src/jhora/panchanga/drik.py:L220-L232`
- Excerpt:
```python
    global _ayanamsa_mode,_ayanamsa_value
    _ayanamsa_default = const._DEFAULT_AYANAMSA_MODE
    if const._TROPICAL_MODE:
        flags = swe.FLG_SWIEPH
    else:
        flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | _rise_flags
        #set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd)
        set_ayanamsa_mode(_ayanamsa_default,_ayanamsa_value,jd_utc); _ayanamsa_mode = const._DEFAULT_AYANAMSA_MODE
        #print('drik sidereal long ayanamsa',_ayanamsa_mode, const._DEFAULT_AYANAMSA_MODE)
        #import inspect; print('called by',inspect.stack()[1].function)
    longi,_ = swe.calc_ut(jd_utc, planet, flags = flags)
    reset_ayanamsa_mode()
```
- Observed behavior: evidence line block shows the active rule in this path.

### TT05

- Behavior: Tajaka annual/monthly/sixty-hour charts route through drik.next_solar_date.
- Source: `src/jhora/horoscope/transit/tajaka.py:L391-L447`
- Excerpt:
```python
def annual_chart(jd_at_dob,place,divisional_chart_factor=1,years=1):
    """
        Also can be called using:
            varsha_pravesh (jd_at_dob, place, divisional_chart_factor=1, years=1)
        Create Tajaka Annual Chart. Tajaka annual chart is chart for one year at "years" from date of birth/time of birth
        @param jd_at_dob: Julian Day nummber at date/time of birth
            Note: You can use swe.julday(dob_year,dob_month,dob_day,tob_hour+tob_minutes/60.0+tob_seconds/3600.0) to get
        @param place: should be a struct os drik.Place (place,latitude,longitude,time_sone_factor)
        @param divisional_chart_factor: 1=Rasi, 2=Hora, 9=navamsa etc. See drik.division_chart_factors for details
        @param years: number of years after dob the dhasa varga chart is sought 
        @return: Tajaka annual dhasa varga chart as list of planets
            annual_planet_positions_list,[(y,m,d),utils.to_dms(fh)]
```
- Observed behavior: evidence line block shows the active rule in this path.

### TT06

- Behavior: Muntha and candidate chain for Varshesha are explicitly assembled.
- Source: `src/jhora/horoscope/transit/tajaka.py:L451-L471`
- Excerpt:
```python
def _get_lord_candidates(planet_positions,years_from_dob,natal_lagna_house,night_time_birth):
    tajaka_chart_p_to_h = utils.get_planet_house_dictionary_from_planet_positions(planet_positions)
    tajaka_chart_h_to_p = utils.get_house_to_planet_dict_from_planet_to_house_dict(tajaka_chart_p_to_h)
    " Rule-1 Sun-Sign's  or Moon-Sign's Lord?"
    candidates = []
    if night_time_birth:
        candidates.append(house.house_owner_from_planet_positions(planet_positions,tajaka_chart_p_to_h[1]))
    else:
        candidates.append(house.house_owner_from_planet_positions(planet_positions,tajaka_chart_p_to_h[0]))
    candidates.append(house.house_owner_from_planet_positions(planet_positions,natal_lagna_house))
    asc_house = tajaka_chart_p_to_h[const._ascendant_symbol]
    m_house = muntha_house(asc_house,years_from_dob)
```
- Observed behavior: evidence line block shows the active rule in this path.

### TT07

- Behavior: Varshesha tie-breaker falls to pancha_vargeeya bala max and uses pvbc.index(max).
- Source: `src/jhora/horoscope/transit/tajaka.py:L490-L503`
- Excerpt:
```python
    " No or more than one candidate benefic or malefic - so let us check highest panchavargeeya bala"
    
    pvb = strength.pancha_vargeeya_bala(jd, place)
    pvbc = [pvb[candidate] for candidate in candidates]
    #pvbcl = pvbc[lord_of_the_year]
    pvb_max = max(pvbc)
    if pvb_max > const.pancha_vargeeya_bala_strength_threshold:
        lord_of_the_year = pvbc.index(pvb_max)
        #print('Lord of year as per pancha veerya bala (max) ',lord_of_the_year,'is',pvb_max)
        return lord_of_the_year
    "rasi occupied by Sun or Moon in the annual chart - candidate-1"
    lord_of_the_year = candidates[0]
```
- Observed behavior: evidence line block shows the active rule in this path.

### TT08

- Behavior: lord_of_the_month reuses annual-lord chain and injects lord_of_year into candidates.
- Source: `src/jhora/horoscope/transit/tajaka.py:L551-L568`
- Excerpt:
```python
    lord_of_year = lord_of_the_year(jd_at_dob, place, years_from_dob)
    jd_at_years = jd_at_dob + (years_from_dob+months_from_dob/12.0)*year_value
    
    tob_hrs = drik.jd_to_gregorian(jd_at_years)[3]
    sunrise = utils.from_dms_str_to_dms(drik.sunrise(jd_at_years, place)[1]) #2.0.3
    sunrise_hrs = sunrise[0]+sunrise[1]/60.0+sunrise[2]/3600.0
    sunset = utils.from_dms_str_to_dms(drik.sunset(jd_at_years, place)[1]) #2.0.3
    sunset_hrs = sunset[0]+sunset[1]/60.0+sunset[2]/3600.0
    night_time_birth = tob_hrs > sunset_hrs or tob_hrs < sunrise_hrs
    #print('night_time_birth',night_time_birth,sunrise_hrs,tob_hrs,sunset_hrs)
    rasi_chart = charts.divisional_chart(jd_at_years, place,divisional_chart_factor=1)
    tajaka_chart_p_to_h = utils.get_planet_house_dictionary_from_planet_positions(rasi_chart)
```
- Observed behavior: evidence line block shows the active rule in this path.

### TT09

- Behavior: pancha_vargeeya_bala assembles five components then aggregates by sum/4.
- Source: `src/jhora/horoscope/chart/strength.py:L387-L401`
- Excerpt:
```python
    rasi_chart = charts.divisional_chart(jd, place, divisional_chart_factor=1)
    p_to_h_of_rasi_chart = utils.get_planet_house_dictionary_from_planet_positions(rasi_chart)
    kb = _kshetra_bala(p_to_h_of_rasi_chart)
    ub = _uchcha_bala(rasi_chart)
    hb = _hadda_bala(rasi_chart)
    drekkana_chart = charts.divisional_chart(jd, place,divisional_chart_factor=3)
    p_to_h_of_drekkana_chart = utils.get_planet_house_dictionary_from_planet_positions(drekkana_chart)
    db = _drekkana_bala(p_to_h_of_drekkana_chart)
    navamsa_chart = charts.divisional_chart(jd, place,divisional_chart_factor=9)
    p_to_h_of_navamsa_chart = utils.get_planet_house_dictionary_from_planet_positions(navamsa_chart)
    nb = _navamsa_bala(p_to_h_of_navamsa_chart)
    pvb = [kb,ub,hb,db,nb]
```
- Observed behavior: evidence line block shows the active rule in this path.

### TT10

- Behavior: Ithasala and Eesarpha rules are explicit conjunctions over aspect+deeptamsa+motion checks.
- Source: `src/jhora/horoscope/transit/tajaka_yoga.py:L69-L103`
- Excerpt:
```python
    chk1 = tajaka.planets_have_aspects(house_planet_dict, planet1, planet2)
    chk2,ithasala_type = tajaka.both_planets_within_their_deeptamsa(planet_positions,planet1, planet2)
    chk3 = tajaka.both_planets_approaching(planet_positions,planet1,planet2)
    yoga_present = chk1 and chk2 and chk3
    return yoga_present, ithasala_type
def ithasala_yoga_from_jd_place(jd,place,planet1,planet2,divisional_chart_factor=1):
    """
        Ithasala Yoga
            If two planets have an aspect and if the faster moving planet83 is less advanced in its
            rasi than the slower moving planet, then we have an ithasala yoga between the two.        
        @param planet_positions: [ ['L',(7,12,3456)], [0,(4,112,3456)],...]]
        @param asc_house: Raasi index of the ascendant/Lagnam
```
- Observed behavior: evidence line block shows the active rule in this path.

### TT11

- Behavior: deeptamsa gate includes boundary tolerance (<=1 degree) and ithasala type classification.
- Source: `src/jhora/horoscope/transit/tajaka.py:L583-L603`
- Excerpt:
```python
    planet1_deeptamsa_start,planet1_deeptamsa_end = utils.deeptaamsa_range_of_planet(planet1,planet1_long_within_raasi)
    planet2_deeptamsa_start,planet2_deeptamsa_end = utils.deeptaamsa_range_of_planet(planet2,planet2_long_within_raasi)
    chk1 = planet1_long_within_raasi >= planet2_deeptamsa_start and planet1_long_within_raasi <= planet2_deeptamsa_end
    chk1_1 = False
    if not chk1: #Check for bhavishya ithasala
        chk1_1 = abs(planet1_long_within_raasi-planet2_deeptamsa_start)<=1.0 or abs(planet1_long_within_raasi - planet2_deeptamsa_end)<=1.0
    #print('deeptamsa test',planet1,'in house',planet1_house,planet2_deeptamsa_start,planet2_deeptamsa_end,'planet1_long_within_raasi',planet1_long_within_raasi,'chk1',chk1)
    chk2 = planet2_long_within_raasi >= planet1_deeptamsa_start and planet2_long_within_raasi <= planet1_deeptamsa_end
    chk2_1 = False
    if not chk2: #Check for bhavishya ithasala
        chk2_1 = abs(planet2_long_within_raasi-planet1_deeptamsa_start)<=1.0 or abs(planet2_long_within_raasi - planet1_deeptamsa_end)<=1.0
    #print('deeptamsa test',planet2,'in house',planet2_house,planet1_deeptamsa_start,planet1_deeptamsa_end,'planet1_long_within_raasi',planet2_long_within_raasi,'chk2',chk2)
```
- Observed behavior: evidence line block shows the active rule in this path.

### TT12

- Behavior: Mudda/Varsha Vimshottari uses tropical year and /360 normalization.
- Source: `src/jhora/horoscope/dhasa/annual/mudda.py:L32-L40`
- Excerpt:
```python
year_duration = const.tropical_year#const.sidereal_year  # some say 360 days, others 365.25 or 365.2563 etc
varsha_vimsottari_adhipati = lambda nak: const.varsha_vimsottari_adhipati_list[nak % (len(const.varsha_vimsottari_adhipati_list))]

### --- Vimoshatari functions
def varsha_vimsottari_next_adhipati(lord):
    """Returns next element after `lord` in the adhipati_list"""
    current = const.varsha_vimsottari_adhipati_list.index(lord)
    next_index = (current + 1) % len(const.varsha_vimsottari_adhipati_list)
    next_lord = const.varsha_vimsottari_adhipati_list[next_index]
```
- Observed behavior: evidence line block shows the active rule in this path.

### TT13

- Behavior: Patyayini derives factors from sorted krisamsa deltas and scales with average Gregorian year.
- Source: `src/jhora/horoscope/dhasa/annual/patyayini.py:L35-L50`
- Excerpt:
```python
    cht = charts.divisional_chart(jd_years,place,divisional_chart_factor,chart_method=chart_method)
    krisamsas = cht[:-2]  # Exclude Rahu and Ketu
    krisamsas.sort(key=lambda x:x[1][1])
    #for p,(h,long) in krisamsas:
    #    print('krisamsas',p,(h,utils.to_dms(long,is_lat_long='plong')))
    patyamsas = [[p,(h,long-krisamsas[i-1][1][1])] for i,[p,(h,long)] in enumerate(krisamsas) if i>0]
    patyamsas = [krisamsas[0]]+patyamsas
    #print('patyamsas',patyamsas)
    #for p,(h,long) in patyamsas:
    #    print('patyamsas',p,(h,utils.to_dms(long,is_lat_long='plong')))
    patyamsa_sum = sum([long for _,(_,long) in patyamsas])
    _dhasa_period_factors = {p:long/patyamsa_sum for p,(_,long) in patyamsas}
```
- Observed behavior: evidence line block shows the active rule in this path.

### TT14

- Behavior: Varsha Narayana path scales dhasa_factor by /360 and seeds from next_solar_date.
- Source: `src/jhora/horoscope/dhasa/raasi/narayana.py:L53-L65`
- Excerpt:
```python
    dhasa_factor = year_duration
    if varsha_narayana:
        dhasa_factor /= 360
    dhasa_progression = const.narayana_dhasa_normal_progression[dhasa_seed_sign]
    if p_to_h[8]==dhasa_seed_sign:
        dhasa_progression = const.narayana_dhasa_ketu_exception_progression[dhasa_seed_sign]
    elif p_to_h[6]==dhasa_seed_sign:
        dhasa_progression = const.narayana_dhasa_saturn_exception_progression[dhasa_seed_sign]
    dhasa_periods = []
    jd_at_dob = utils.julian_day_number(dob, tob)
    dhasa_start_jd = drik.next_solar_date(jd_at_dob, place, years=years, months=months, sixty_hours=sixty_hours)
    for dhasa_lord in dhasa_progression:
```
- Observed behavior: evidence line block shows the active rule in this path.

### TT15

- Behavior: Main annual wrapper composes Patyayini, Mudda, and Varsha Narayana outputs.
- Source: `src/jhora/horoscope/main.py:L1073-L1077`
- Excerpt:
```python
    def _get_annual_dhasa_bhukthi(self,divisional_chart_factor=1):
        _patyayini_dhasa_bhukthi_info = self._get_patyatini_dhasa_bhukthi(divisional_chart_factor=divisional_chart_factor)
        _mudda_dhasa_bhukthi_info = self._get_varsha_vimsottari_dhasa(self.julian_day, self.Place, self.years-1,divisional_chart_factor=divisional_chart_factor)
        _varsha_narayana_dhasa_bhukthi_info = self._get_varsha_narayana_dhasa(self.Date, self.birth_time, self.Place, self.years,divisional_chart_factor=divisional_chart_factor)
        return [_patyayini_dhasa_bhukthi_info,_mudda_dhasa_bhukthi_info,_varsha_narayana_dhasa_bhukthi_info]
```
- Observed behavior: evidence line block shows the active rule in this path.

### ABSENCE-OF-GOCHARA-ENGINE

- Behavior: No direct independent non-UI gochara engine callsite was found in audited scope.
- Source: `research/transit_and_tajaka/_coverage_transit_tajaka_callsites_engine_plus_consumers.tsv:L2`
- Excerpt:
```text
Scope-EngineAudit	0	gochara_engine	not_found_in_engine_scope	ABSENCE-OF-GOCHARA-ENGINE	engine_core
```
- Observed behavior: absence is recorded as an explicit negative fact row.

### TT900

- Behavior: Residual matched rows are retained in callsite inventory.
- Source: `research/transit_and_tajaka/_coverage_transit_tajaka_callsites_engine_plus_consumers.tsv`
- Excerpt:
```text
Rows with anchor_id=TT900 remain in inventory as residual evidence.
```
- Observed behavior: non-focused matches remain visible as residual evidence.

## Conflict / ambiguity register

- `UNCERTAIN-TT-SOLAR-PRECISION`: interpolation precision depends on 5-point sampling and daily bracketing.
- `UNCERTAIN-TT-TIEBREAKER-LOGIC`: varshesha tie-break has multi-branch fallback semantics.
- `UNCERTAIN-TT-VARSHESHA-INDEX-01`: `pvbc.index(max)` returns candidate-list index, creating index-basis ambiguity.
- `UNCERTAIN-TT-GOCHARA-ISOLATION`: no isolated gochara engine module detected in audited non-UI scope.
- `UNCERTAIN-TT-PRAVESHA-PATH-01`: `pravesha_type` path in `charts.rasi_chart` can shift annual/tithi routing.

## Coverage ledger

- Inventory file: `research/transit_and_tajaka/_coverage_transit_tajaka_callsites_engine_plus_consumers.tsv`
- Inventory columns: `file`, `line`, `pattern`, `function_context`, `anchor_id`, `scope_class`
- Inventory row count: `309`
- Rows by scope_class: `engine_core=275`, `consumer_core=18`, `residual=16`
- Residual rows (`TT900`): `308`
- Absence rows (`ABSENCE-OF-GOCHARA-ENGINE`): `1`
- Solar matrix: `research/transit_and_tajaka/_coverage_transit_tajaka_solar_return_search_matrix.tsv`
- Annual-lords matrix: `research/transit_and_tajaka/_coverage_transit_tajaka_annual_lords_matrix.tsv`
- Panchavargiya matrix: `research/transit_and_tajaka/_coverage_transit_tajaka_panchavargiya_bala_matrix.tsv`
- Tajaka-yoga matrix: `research/transit_and_tajaka/_coverage_transit_tajaka_tajaka_yoga_rule_matrix.tsv`
- Annual-dhasa matrix: `research/transit_and_tajaka/_coverage_transit_tajaka_annual_dhasa_matrix.tsv`
- Output-contract matrix: `research/transit_and_tajaka/_coverage_transit_tajaka_output_contract_matrix.tsv`

## Sanity checks

- command: `rg -n "^### TT[0-9]+|^### TT900|^### ABSENCE-OF-GOCHARA-ENGINE" research/transit_and_tajaka/transit_tajaka_behavior_contract_map.engine_plus_consumers.md -S`
- command: `rg -n "UNCERTAIN-TT-" research/transit_and_tajaka/transit_tajaka_behavior_contract_map.engine_plus_consumers.md -S`
- command: `rg -n "Source:" research/transit_and_tajaka/transit_tajaka_behavior_contract_map.engine_plus_consumers.md -S`
- command: `Get-Content research/transit_and_tajaka/_coverage_transit_tajaka_callsites_engine_plus_consumers.tsv | Measure-Object -Line`
- command: `Get-Content research/transit_and_tajaka/_coverage_transit_tajaka_solar_return_search_matrix.tsv | Measure-Object -Line`
- command: `Get-Content research/transit_and_tajaka/_coverage_transit_tajaka_annual_lords_matrix.tsv | Measure-Object -Line`
- command: `Get-Content research/transit_and_tajaka/_coverage_transit_tajaka_panchavargiya_bala_matrix.tsv | Measure-Object -Line`
- command: `Get-Content research/transit_and_tajaka/_coverage_transit_tajaka_tajaka_yoga_rule_matrix.tsv | Measure-Object -Line`
- command: `Get-Content research/transit_and_tajaka/_coverage_transit_tajaka_annual_dhasa_matrix.tsv | Measure-Object -Line`
- command: `Get-Content research/transit_and_tajaka/_coverage_transit_tajaka_output_contract_matrix.tsv | Measure-Object -Line`
