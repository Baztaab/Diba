# yogas_doshas_behavior_contract_map.engine_plus_consumers.md

## Snapshot identity (FACTS)

- pyjhora_root: `D:\lab\Pyjhora`
- extraction_timestamp_local: `2026-02-28 05:14:21`
- in-scope files: `13`
- in-scope file digests (SHA256):
- `src/jhora/const.py` -> `2dacc910fce9babc69582491b52cde9fd23ab9dde835d41efb65fc0f79e00ba8` (bytes: `79727`)
- `src/jhora/horoscope/chart/charts.py` -> `34c49af9fb3359fdb243f2a467404b7a849e35b9def9e2961a45a4027c8619b2` (bytes: `141395`)
- `src/jhora/horoscope/chart/dosha.py` -> `a9c1bafec6b3e2c5fae1aa87fe07153858a60ff5c41f4192e73561608fec0730` (bytes: `22973`)
- `src/jhora/horoscope/chart/house.py` -> `d2d0d2b9a1e382879b0f191498bcc8dc9d4ef74224925ffb522f2cc0e4329861` (bytes: `80854`)
- `src/jhora/horoscope/chart/raja_yoga.py` -> `19f6a3810900eeba6a29f00019175ebb815a6339df32a2c107467a169827e8cd` (bytes: `38164`)
- `src/jhora/horoscope/chart/raja_yoga_bv_raman.py` -> `9739d962f75e4775ffefc3c03ddf1eeb502d1a7fba915363e9a077d287d2f80c` (bytes: `3675`)
- `src/jhora/horoscope/chart/yoga.py` -> `427cf575a2b601da85479aa7394f937b148e797a24882ac7d8fac21c57105830` (bytes: `738910`)
- `src/jhora/lang/dosha_msgs_en.json` -> `8f8e5996994ea418109b14e05f002581418943eb2ae0cc1f338fcc5b3dc35317` (bytes: `25914`)
- `src/jhora/lang/raja_yoga_msgs_en.json` -> `19cb3b86abdde3b1efc69b74dfb7569da6a4b8a1d3f55a19eab647a3d90f1fa9` (bytes: `2770`)
- `src/jhora/lang/yoga_msgs_en.json` -> `4c1c079954e32f09acdac645cf58b6cdceb6887e03aff8e79ed5b6587aebb098` (bytes: `76545`)
- `src/jhora/panchanga/drik.py` -> `9790dcdf442910b1eaa260b16c346c6696438eb6955c0a520c1be220ba3497bc` (bytes: `186944`)
- `src/jhora/ui/horo_chart_tabs.py` -> `f38615b20964505a98e25a513f58aa238a77bb7c53ad6b14b70c54cee5cb556c` (bytes: `396681`)
- `src/jhora/utils.py` -> `861062b3abba1655b9d4e5608333f8aaa1d391b3d38ecdacbac565bf930f3875` (bytes: `70076`)

## Scope (FACTS)

- In-scope engine files:
  - `src/jhora/horoscope/chart/yoga.py`
  - `src/jhora/horoscope/chart/raja_yoga.py`
  - `src/jhora/horoscope/chart/dosha.py`
  - `src/jhora/horoscope/chart/raja_yoga_bv_raman.py`
  - `src/jhora/horoscope/chart/house.py`
  - `src/jhora/horoscope/chart/charts.py`
  - `src/jhora/panchanga/drik.py`
  - `src/jhora/const.py`
  - `src/jhora/utils.py`
- In-scope resource registries:
  - `src/jhora/lang/yoga_msgs_en.json`
  - `src/jhora/lang/raja_yoga_msgs_en.json`
  - `src/jhora/lang/dosha_msgs_en.json`
- In-scope consumers:
  - `src/jhora/ui/horo_chart_tabs.py`
- Out-of-scope:
  - mutation/refactor/bug-fix
  - translation of resource files
  - UI redesign
  - test implementation changes

## Pattern inventory (FACTS)
- `yoga`
- `raja_yoga`
- `dosha`
- `manglik`
- `kuja`
- `kala_sarpa`
- `get_yoga_details`
- `get_raja_yoga_details`
- `get_dosha_details`
- `eval(`
- `_from_jd_place`
- `_from_planet_positions`
- `exception`
- `c11`
- `c14`
- `c16`
- `False`
- `vipareetha`
- `vipareeta`
- `neecha_bhanga`
- `global p_to_h`
- `p_to_h_navamsa`
- `show_exception`
- `Error executing`
- `NOTE: !!! Strength of the pairs are not checked !!!`
- `TODO: yoga functions have only one argument`
- `return _`
- `Broken_Missing_Return`

## Registry inventory (FACTS)

- `yoga_msgs_en.json` keys: `284`
- `raja_yoga_msgs_en.json` keys: `3`
- `dosha_msgs_en.json` keys: `9`

## Behavior taxonomy (FACTS)

- registry resources and prefixes: `YD01`
- eval dispatch and global state coupling: `YD02`, `YD03`, `YD04`
- raja pair caveat and subtype return: `YD05`, `YD06`
- dosha base rules and exception paths: `YD07`, `YD08`, `YD09`
- output contracts and UI coupling: `YD10`, `YD11`, `YD12`
- broken return path: `YD13`
- production absence fact: `ABSENCE-OF-RAMAN-PRODUCTION-ENGINE`
- residual inventory: `YD900`

## Evidence anchors (YD01..YDNN, YD900)

### YD01

- Behavior: Registry file prefixes and Manglik base-house constant are centralized in const.
- Source: `src/jhora/const.py:L42-L44` and `src/jhora/const.py:L1217-L1217`
- Excerpt:
```python
_DEFAULT_YOGA_JSON_FILE_PREFIX = "yoga_msgs_" 
_DEFAULT_RAJA_YOGA_JSON_FILE_PREFIX = "raja_yoga_msgs_" 
_DEFAULT_DOSHA_JSON_FILE_PREFIX = "dosha_msgs_" 
dosha_manglik_houses = [4,7,8,12]
```
- Observed behavior: Yoga, Raja Yoga and Dosha resource loading is registry-driven and Manglik uses a fixed house set from const.

### YD02

- Behavior: Yoga dispatcher loops registry keys and executes `_from_jd_place` functions via `eval`.
- Source: `src/jhora/horoscope/chart/yoga.py:L120-L133`
- Excerpt:
```python
    yoga_results = {}
    #print('divisional_chart_factor',divisional_chart_factor)
    for yoga_function,details in msgs.items():
        """ TODO: yoga functions have only one argument h_to_p. Here we call 3 args - need to synch"""
        eval_str = yoga_function+'_from_jd_place'#'_from_planet_positions'
        #print(eval_str)
        try:
            yoga_exists = eval(eval_str)(jd,place,divisional_chart_factor)#(planet_positions) ##(h_to_p)#
            if yoga_exists:
                details.insert(0,'D'+str(divisional_chart_factor))
                yoga_results[yoga_function] = details
        except Exception as e:
```
- Observed behavior: Dispatch is dynamic, unsanitized and exception-tolerant through `utils.show_exception` plus a print fallback.

### YD03

- Behavior: Yoga dispatcher relies on module-level global state for planet and house maps.
- Source: `src/jhora/horoscope/chart/yoga.py:L62-L74` and `src/jhora/horoscope/chart/yoga.py:L95-L107`
- Excerpt:
```python
def get_yoga_details_for_all_charts(jd,place,language='en',divisional_chart_factor=None):
    """
        Get all the yoga information that are present in the divisional charts for a given julian day and place
        @param jd: Julian day number
        @param place: struct (plave name, latitude, longitude, timezone)
        @param language: two letter language code (en, hi, ka, ta, te)
        @param divisional_chart_factor: None => Get for all varga charts. Or specify divisional chart number 
        @return: returns a 2D List of yoga_name, yoga_details
            yoga_name in language
            yoga_details: [chart_ID, yoga_name, yoga_desription, yoga_benfits] 
    """
    global p_to_h_navamsa, h_to_p_navamsa, asc_house_navamsa,planet_positions
def get_yoga_details(jd,place,divisional_chart_factor=1,language='en'):
    """
        Get all the yoga information that are present in the requested divisional charts for a given julian day and place
        @param jd: Julian day number
        @param place: struct (plave name, latitude, longitude, timezone)
        @param divisional_chart_factor: integer of divisional chart 1=Rasi, 2=D2, 9=D9 etc 
        @param language: two letter language code (en, hi, ka, ta, te)
        @return: returns a 2D List of yoga_name, yoga_details
            yoga_name in language
            yoga_details: [chart_ID, yoga_name, yoga_desription, yoga_benfits] 
    """
    global p_to_h, h_to_p, asc_house, planet_positions
```
- Observed behavior: Rule functions can depend on globals such as `p_to_h`, `h_to_p`, `asc_house` and navamsa equivalents instead of explicit parameters.

### YD04

- Behavior: Raja Yoga evaluation also dispatches through `eval`, but on pair candidates derived at runtime.
- Source: `src/jhora/horoscope/chart/raja_yoga.py:L108-L124`
- Excerpt:
```python
    p_to_h = utils.get_planet_house_dictionary_from_planet_positions(planet_positions)
    h_to_p = utils.get_house_planet_list_from_planet_positions(planet_positions)
    raja_yoga_results = {}
    for raja_yoga_function,details in msgs.items():
        details_str = 'D'+str(divisional_chart_factor)+'-'
        raja_yoga_pairs = get_raja_yoga_pairs_from_planet_positions(planet_positions)
        if raja_yoga_pairs:
            rp_str = ''
            for rp1,rp2 in raja_yoga_pairs:
                raja_yoga_exists = eval(raja_yoga_function+'_from_planet_positions')(planet_positions,rp1,rp2)
                if raja_yoga_exists:
                    rp_str += ' '+'[' +utils.PLANET_NAMES[rp1]+'-'+utils.PLANET_NAMES[rp2]+'] '
```
- Observed behavior: Registry keys are converted to callable names and executed against candidate planet pairs.

### YD05

- Behavior: Raja Yoga pair discovery explicitly states that pair strength is not checked.
- Source: `src/jhora/horoscope/chart/raja_yoga.py:L249-L263`
- Excerpt:
```python
def get_raja_yoga_pairs(house_to_planet_list):
    """
       To get raja yoga planet pairs from house to planet list
       NOTE: !!! Strength of the pairs are not checked !!!
        @param house_to_planet_dict: list of raasi with planet ids in them
          Example: ['','','','','2','7','1/5','0','3/4','L','','6/8'] 1st element is Aries and last is Pisces
        @return 2D List of raja yoga planet pairs
          Example: [[0,2],[3,6]] : Tow raja yoga pairs [Sun,Mars] and [Mercury,Saturn]
    """
    p_to_h = utils.get_planet_to_house_dict_from_chart(house_to_planet_list)
    asc_house = p_to_h[const._ascendant_symbol]
    lq = set(lords_of_quadrants(house_to_planet_list,asc_house))
```
- Observed behavior: Pair generation is presence-based and omits an additional strength filter.

### YD06

- Behavior: Vipareetha Raja Yoga returns subtype information instead of a plain boolean.
- Source: `src/jhora/horoscope/chart/raja_yoga.py:L295-L307`
- Excerpt:
```python
def vipareetha_raja_yoga(p_to_h,raja_yoga_planet1,raja_yoga_planet2):
    """
        Checks if given two raja yoga planets also for vipareetha raja yoga/
        Also returns the sub type of vipareetha raja yoga
            Harsh Raja Yoga, Saral Raja Yoga and Vimal Raja Yoga
        Vipareeta Raaja Yoga: The 6th, 8th and 12th houses are known as trik sthanas or
        dusthanas (bad houses). If their lords occupies dusthanas or conjoin dusthanas
        @param p_to_h: planet_to_house dictionary Example: {0:1,1:2,...'L':11,..} Sun in Ar, Moon in Ta, Lagnam in Pi
        @param raja_yoga_planet1: Planet index for first raja yoga planet  [0 to 6] Rahu/Kethu/Lagnam not supported
        @param raja_yoga_planet2: Planet index for second raja yoga planet [0 to 6] Rahu/Kethu/Lagnam not supported
        return [Boolean, Sub_type]
         Example: [True,'Harsh Raja Yoga']
```
- Observed behavior: Output shape for Raja Yoga rules is heterogeneous; at least one rule returns `[bool, subtype]`.

### YD07

- Behavior: Kala Sarpa is implemented as a direct boolean hemisphere test and Manglik returns status plus exception payload.
- Source: `src/jhora/horoscope/chart/dosha.py:L37-L60`
- Excerpt:
```python
def kala_sarpa(house_to_planet_list):
    """ Returns kala Sarpa Dosha True or False 
        If True type kala sarpa dosha can be obtained from the Rahu's house number (1..12)
        as the index of the array from dosha_msgs_<lang> file
    """
    p_to_h = utils.get_planet_to_house_dict_from_chart(house_to_planet_list)
    rahu_house = p_to_h[const.RAHU_ID]
    kpdc1 = all([any([p_to_h[ph]==(rahu_house+rkh)%12 for rkh in const.SUN_TO_SATURN]) for ph in const.SUN_TO_SATURN])
    ketu_house = p_to_h[const.KETU_ID]
    kpdc2 = all([any([p_to_h[ph]==(ketu_house+rkh)%12 for rkh in const.SUN_TO_SATURN]) for ph in const.SUN_TO_SATURN])
    #print('rahu_house',rahu_house,'ketu_house',ketu_house)
        @return: [Manglik=True/False,Exceptions-True/False,[Exception Indices or -1]]
                Exception index = 0 => No Exceptions
                Exception index >1 => Exception indices can be mapped to dosha_msgs_<lang>.json file strings.
    """
```
- Observed behavior: Dosha rules are hardcoded and their return shapes are not uniform.

### YD08

- Behavior: Manglik exception placeholders `c11` and `c14` are hardcoded to `False`.
- Source: `src/jhora/horoscope/chart/dosha.py:L103-L121`
- Excerpt:
```python
    c7 = len(house.associations_of_the_planet(planet_positions=planet_positions, planet=2))>0 ; _me.append(c7)
    c8 = 2 in charts.planets_in_retrograde(planet_positions) ; _me.append(c8)
    c9_1 = 2 in charts.planets_in_combustion(planet_positions)
    c9_2 = mars_long < const.rasi_sandhi_duration or mars_long > (30.0-const.rasi_sandhi_duration)
    c9 = c9_1 or c9_2 ; _me.append(c9)
    c10 = house.house_owner_from_planet_positions(planet_positions, lagna_house)==const.MARS_ID; _me.append(c10)
    c11 = False ; _me.append(c11)
    c12 = const.house_strengths_of_planets[const.MARS_ID][mars_house] >= const._FRIEND; _me.append(c12)
    c13 = mars_house in const.movable_signs; _me.append(c13)
    c14 = False ; _me.append(c14)
    c15 = lagna_house in [const.CANCER,const.LEO] ; _me.append(c15)
    c16 = mars_house in [p_to_h[const.JUPITER_ID], p_to_h[const.VENUS_ID]]; _me.append(c16)
```
- Observed behavior: At least two documented Manglik exception branches are present as placeholders rather than implemented logic.

### YD09

- Behavior: Manglik exception 16 documentation and code disagree on the second benefic.
- Source: `src/jhora/horoscope/chart/dosha.py:L94-L96` and `src/jhora/horoscope/chart/dosha.py:L119-L120`
- Excerpt:
```python
        15. If Lagnam is in Cancer/Kataka or Leo, then Mars is yoga karaka causes no dosha.
        16. Since Mars cojoins with Jupiter or moon, it reduces the dosha
        17. When Jupiter or Venus is in Lagna it reduces dosha
    c15 = lagna_house in [const.CANCER,const.LEO] ; _me.append(c15)
    c16 = mars_house in [p_to_h[const.JUPITER_ID], p_to_h[const.VENUS_ID]]; _me.append(c16)
```
- Observed behavior: The documentation says Jupiter or Moon, while code checks Jupiter or Venus.

### YD10

- Behavior: Dosha results are assembled as HTML strings keyed by localized titles.
- Source: `src/jhora/horoscope/chart/dosha.py:L342-L359`
- Excerpt:
```python
def get_dosha_details(jd_at_dob,place_as_tuple,language=const._DEFAULT_LANGUAGE):
    dosha_msgs = get_dosha_resources(language)
    #print(dosha_msgs)
    planet_positions = charts.rasi_chart(jd_at_dob, place_as_tuple)
    house_to_planet_list = utils.get_house_planet_list_from_planet_positions(planet_positions)
    dosha_results = {}
    """ get kala sarpa dosha """
    key_str = utils.resource_strings['kala_sarpa_dosha_str']
    ks_results = _get_kala_sarpa_results(planet_positions, dosha_msgs,key_str)
    dosha_results.update(ks_results)
    """ get manglik """
    key_str = utils.resource_strings['manglik_dosha_str']
```
- Observed behavior: Producer contract is presentation-shaped and already coupled to UI rendering needs.

### YD11

- Behavior: UI consumes dosha output as HTML fragments without additional structure parsing.
- Source: `src/jhora/ui/horo_chart_tabs.py:L5044-L5058`
- Excerpt:
```python
                dosha_results_text += "<b><u>"+yk+"</u></b><br>"
                dosha_results_text += self._dosha_results[yk]+"<br>"
        dosha_results_text = dosha_results_text[:-len("<br>")]
        self._dosha_text.setHtml(dosha_results_text)
        self._dosha_text.setReadOnly(True) #setDisabled(True)
        
    def _update_dosha_tab_information(self):
        self.tabWidget.setTabText(_dosha_tab_start,self.resources['dosha_str'])
        """ TODO: Should this be julian day, julian_years or birth-julian-day? """
        #jd = self._horo.julian_day  # For ascendant and planetary positions, dasa bukthi - use birth time
        jd = self._birth_julian_day
        place = drik.Place(self._place_name,float(self._latitude),float(self._longitude),float(self._time_zone))
```
- Observed behavior: Output contract for doshas is directly coupled to `setHtml` rendering.

### YD12

- Behavior: UI unpacks yoga and Raja Yoga producer tuples and expects each result item to contain four fields.
- Source: `src/jhora/ui/horo_chart_tabs.py:L5092-L5115`
- Excerpt:
```python
                yoga_chart,yoga_name, yoga_description, yoga_predictions = self._yoga_results[yk]
                yoga_results_text += "<b><u>"+yoga_name+" ("+yoga_chart+")</u></b><br>"
                yoga_results_text += "<b>"+self.resources['description_str']+"</b> "+yoga_description+"<br>"
                yoga_results_text += "<b>"+self.resources['prediction_str']+"</b> " +yoga_predictions+"<br><br>"
        yoga_results_text = yoga_results_text[:-len("<br>")]
        self._yoga_text.setHtml(yoga_results_text)
        self._yoga_text.setReadOnly(True) #setDisabled(True)
        
    def _update_yoga_tab_information(self):
        self.tabWidget.setTabText(_yoga_tab_start,self.resources['yoga_str'])
        """ TODO: Should this be julian day, julian_years or birth-julian-day? """
        #jd = self._horo.julian_day  # For ascendant and planetary positions, dasa bukthi - use birth time
```
- Observed behavior: Producer tuple shape and per-yoga detail indexing are fixed consumer contracts.

### YD13

- Behavior: `guhyaroga_yoga_from_planet_positions` calls the calculation helper but drops the return value.
- Source: `src/jhora/horoscope/chart/yoga.py:L12442-L12452`
- Excerpt:
```python
def guhyaroga_yoga(chart_navamsa, natural_malefics=None):
    """
        284 - The Moon should join malefics in the Navamsa of Cancer or Scorpio.
    """
    return _guhyaroga_yoga_calculation(chart_navamsa=chart_navamsa, natural_malefics=natural_malefics)
def guhyaroga_yoga_from_planet_positions(planet_positions_navamsa, natural_malefics=None):
    """
        284 - The Moon should join malefics in the Navamsa of Cancer or Scorpio.
    """
    _guhyaroga_yoga_calculation(planet_positions_navamsa=planet_positions_navamsa, natural_malefics=natural_malefics)
def guhyaroga_yoga_from_jd_place(jd,place,divisional_chart_factor=9):
```
- Observed behavior: This path is a broken missing-return branch and should not be treated as a clean boolean wrapper.

### ABSENCE-OF-RAMAN-PRODUCTION-ENGINE

- Behavior: No non-test production consumer was found for `raja_yoga_bv_raman.py`.
- Source: `research/yogas_and_doshas/_coverage_yogas_doshas_callsites_engine_plus_consumers.tsv`
- Excerpt:
```text
Scope-ProductionAudit	0	raja_yoga_bv_raman_production_consumer	not_found_in_non_test_scope	ABSENCE-OF-RAMAN-PRODUCTION-ENGINE	consumer_core
```
- Observed behavior: Production scan found no non-test call chain, while repository inspection found references only under `src/jhora/tests/pvr_tests.py`.

### YD900

- Behavior: Residual matched rows are retained in the callsite inventory.
- Source: `research/yogas_and_doshas/_coverage_yogas_doshas_callsites_engine_plus_consumers.tsv`
- Excerpt:
```text
Rows with anchor_id=YD900 remain in inventory as residual evidence.
```
- Observed behavior: Non-focused pattern hits remain visible for follow-up analysis.

## Conflict / ambiguity register

- `UNCERTAIN-YD-EVAL-SECURITY`: registry dispatch uses `eval` without explicit sanitization.
- `UNCERTAIN-YD-SHAPE-MISMATCH`: rule outputs span `bool`, list payloads, subtype tuples, HTML dicts and tuple summaries.
- `UNCERTAIN-YD-DOC-MISMATCH`: Manglik exception 16 documentation diverges from code.
- `UNCERTAIN-YD-INCOMPLETE-EXCEPTIONS`: Manglik exceptions 11 and 14 are placeholders.
- `UNCERTAIN-YD-GLOBAL-STATE-01`: yoga evaluation depends on module-level mutable globals.
- `UNCERTAIN-YD-MISSING-RETURN-01`: `guhyaroga_yoga_from_planet_positions` omits a return.
- `UNCERTAIN-YD-RAMAN-PRODUCTION-01`: BV Raman engine appears test-only in this repository state.
- `UNCERTAIN-YD-RESOURCE-KEY-DRIFT-01`: registry keys and callable coverage can drift independently.

## Coverage ledger

- Inventory file: `research/yogas_and_doshas/_coverage_yogas_doshas_callsites_engine_plus_consumers.tsv`
- Inventory columns: `file`, `line`, `pattern`, `function_context`, `anchor_id`, `scope_class`
- Inventory row count: `6418`
- Unique `(file,function_context)` count: `1599`
- Rows by scope_class: `engine_core=5377`, `consumer_core=310`, `residual=731`
- Absence rows (`ABSENCE-OF-RAMAN-PRODUCTION-ENGINE`): `1`
- Dispatch matrix: `research/yogas_and_doshas/_coverage_yoga_registry_dispatch_matrix.tsv`
- Rules matrix: `research/yogas_and_doshas/_coverage_yoga_rules_matrix.tsv`
- Dosha exceptions matrix: `research/yogas_and_doshas/_coverage_dosha_exceptions_matrix.tsv`
- Output-contract matrix: `research/yogas_and_doshas/_coverage_yoga_output_contract_matrix.tsv`

## Sanity checks

- command: `rg -n "^### YD[0-9]+|^### YD900|^### ABSENCE-OF-RAMAN-PRODUCTION-ENGINE" research/yogas_and_doshas/yogas_doshas_behavior_contract_map.engine_plus_consumers.md -S`
- command: `rg -n "UNCERTAIN-YD-" research/yogas_and_doshas/yogas_doshas_behavior_contract_map.engine_plus_consumers.md -S`
- command: `rg -n "Source:" research/yogas_and_doshas/yogas_doshas_behavior_contract_map.engine_plus_consumers.md -S`
- command: `Get-Content research/yogas_and_doshas/_coverage_yogas_doshas_callsites_engine_plus_consumers.tsv | Measure-Object -Line`
- command: `Get-Content research/yogas_and_doshas/_coverage_yoga_registry_dispatch_matrix.tsv | Measure-Object -Line`
- command: `Get-Content research/yogas_and_doshas/_coverage_yoga_rules_matrix.tsv | Measure-Object -Line`
- command: `Get-Content research/yogas_and_doshas/_coverage_dosha_exceptions_matrix.tsv | Measure-Object -Line`
- command: `Get-Content research/yogas_and_doshas/_coverage_yoga_output_contract_matrix.tsv | Measure-Object -Line`
