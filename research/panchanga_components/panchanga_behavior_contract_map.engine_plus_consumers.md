# panchanga_behavior_contract_map.engine_plus_consumers.md

## Snapshot identity (FACTS)

- pyjhora_root: `D:\lab\Pyjhora`
- extraction_timestamp_local: `2026-02-27 04:17:11 +0330`
- in-scope files: `9`
- in-scope file digests (SHA256):
  - `src/jhora/const.py` -> `2dacc910fce9babc69582491b52cde9fd23ab9dde835d41efb65fc0f79e00ba8` (bytes: `79727`)
  - `src/jhora/horoscope/chart/charts.py` -> `34c49af9fb3359fdb243f2a467404b7a849e35b9def9e2961a45a4027c8619b2` (bytes: `141395`)
  - `src/jhora/horoscope/main.py` -> `cecb9d933245d6df820425f80d28da3153746215c8b283c66d4fa65c86ee58bd` (bytes: `128308`)
  - `src/jhora/panchanga/drik.py` -> `9790dcdf442910b1eaa260b16c346c6696438eb6955c0a520c1be220ba3497bc` (bytes: `186944`)
  - `src/jhora/panchanga/info.py` -> `22202a60c9b0192b65677bbc0282b23cf29e30ee6173a7497f05f73ea5ca23b7` (bytes: `28011`)
  - `src/jhora/panchanga/pancha_paksha.py` -> `80512153abd4ae83d43e2deb76d994995c1e6b5ca41cb12bfb61b2ce415bbc75` (bytes: `10014`)
  - `src/jhora/panchanga/surya_sidhantha.py` -> `cb5190f94884e4e79d5ed0f98988fa510567bb8e8a02942d3a0a600c4ed808b9` (bytes: `29995`)
  - `src/jhora/panchanga/vratha.py` -> `88e2eb31edeb521779bdf91f818797ae391418e37dd3da67ba492b250ea785e4` (bytes: `48575`)
  - `src/jhora/utils.py` -> `861062b3abba1655b9d4e5608333f8aaa1d391b3d38ecdacbac565bf930f3875` (bytes: `70076`)

## Scope (FACTS)

- In-scope files:
  - `src/jhora/panchanga/drik.py`
  - `src/jhora/panchanga/surya_sidhantha.py`
  - `src/jhora/panchanga/vratha.py`
  - `src/jhora/panchanga/info.py`
  - `src/jhora/panchanga/pancha_paksha.py`
  - `src/jhora/horoscope/chart/charts.py`
  - `src/jhora/horoscope/main.py`
  - `src/jhora/const.py`
  - `src/jhora/utils.py`
- Out-of-scope:
  - UI modules
  - tests
  - `src/jhora/panchanga/drik1.py`
  - `src/jhora/panchanga/khanda_khaadyaka.py` (residual note only)

## Pattern inventory (FACTS)

- `tithi`
- `vaara`
- `nakshatra`
- `nakshathra`
- `nakshatra_pada`
- `yoga`
- `karana`
- `sunrise`
- `sunset`
- `moonrise`
- `moonset`
- `ahargana`
- `kali_ahargana`
- `mahabharatha`
- `festival_data`
- `load_festival_data`
- `skip_days`
- `while`
- `use_planet_speed_for_panchangam_end_timings`
- `use_aharghana_for_vaara_calcuation`
- `muhurtha`
- `kaalam`
- `choghadiya`
- `balam`
- `hora`

## Behavior taxonomy (FACTS)

- epoch and switches: `PG01`, `PG02`, `PG14`, `PG15`, `PG28`
- tithi engine branches and Mahabharatha time-skip: `PG03`, `PG04`, `PG05`, `PG06`, `PG07`
- nakshatra and yoga end-time branches: `PG08`, `PG09`, `PG10`, `PG11`, `PG12`, `PG36`, `PG37`
- karana and vaara contracts: `PG13`, `PG14`
- vratha step-solvers and search composition: `PG16`, `PG17`, `PG18`, `PG19`, `PG20`
- CSV IO and lazy global state: `PG21`, `PG22`
- core consumer index contracts: `PG23`, `PG24`, `PG25`, `PG26`, `PG27`, `PG38`, `PG39`
- alternate surya-siddhantha paths: `PG28`, `PG29`, `PG30`
- secondary/orphan components index: `PG31`, `PG32`, `PG33`, `PG34`, `PG35`, `PG900`

## Evidence anchors (PG01..PG39, PG900)

### PG01

- Behavior: Special pre-Kali tithi adjustment constants and vaara switch are module-level constants.
- Source: `src/jhora/const.py:L599-L605`
- Excerpt:
```python
""" SPECIAL CASE OF TITHI SKIPPING BEFORE MAHABHARATHA TIME 
    See Dr. Jayasree Saranatha Mahabharatha date validation book
"""
increase_tithi_by_one_before_kali_yuga = True
mahabharatha_tithi_julian_day = 588465.5

use_aharghana_for_vaara_calcuation = False # V4.4.5
```
- Observed behavior: Epoch threshold and weekday-mode switch are defined as constants.

### PG02

- Behavior: Planet-speed timing switch for Panchanga end-time flow is a global constant.
- Source: `src/jhora/const.py:L1175-L1175`
- Excerpt:
```python
use_planet_speed_for_panchangam_end_timings = True # True # Changed to False in V4.6.0
```
- Observed behavior: Global toggle exists for planet-speed based end-time branch.

### PG03

- Behavior: _get_tithi uses sunrise anchor, computes phase at sunrise, and applies pre-Kali increment rule.
- Source: `src/jhora/panchanga/drik.py:L477-L488`
- Excerpt:
```python
    tz = place.timezone
    # First convert jd to UTC  # 2.0.3
    y, m, d,bt = jd_to_gregorian(jd)
    jd_utc = utils.gregorian_to_jd(Date(y, m, d))
    # 1. Find time of sunrise
    rise = sunrise(jd, place)[2] # V2.2.8
    # 2. Find tithi at this JDN
    moon_phase = _special_tithi_phase(rise, planet1, planet2, tithi_index, cycle)
    today = ceil(moon_phase / 12)
    """ SPECIAL CASE OF TITHI SKIPPING BEFORE MAHABHARATHA TIME 
        See Dr. Jayasree Saranatha Mahabharatha date validation book """
    if const.increase_tithi_by_one_before_kali_yuga and jd < const.mahabharatha_tithi_julian_day: #V3.2.0
```
- Observed behavior: Tithi baseline is sunrise-anchored and includes Mahabharatha-era increment condition.

### PG04

- Behavior: tithi_using_planet_speed includes Mahabharatha increment in speed-based path.
- Source: `src/jhora/panchanga/drik.py:L541-L549`
- Excerpt:
```python
        """ SPECIAL CASE OF TITHI SKIPPING BEFORE MAHABHARATHA TIME 
            See Dr. Jayasree Saranatha Mahabharatha date validation book
        """
        #"""
        if const.increase_tithi_by_one_before_kali_yuga and jd < const.mahabharatha_tithi_julian_day: #V3.2.0
            #print('tithi increased by 1 before mahabharatha date from',tithi_no,'to',tithi_no+1)
            tithi_no = (tithi_no)%30+1
        #"""
        return [tithi_no,start_time,end_time]
```
- Observed behavior: Speed-based tithi branch applies the same pre-Kali increment condition.

### PG05

- Behavior: tithi dispatches to planet-speed or inverse-lagrange branch using constant switch.
- Source: `src/jhora/panchanga/drik.py:L571-L574`
- Excerpt:
```python
    if const.use_planet_speed_for_panchangam_end_timings:
        return tithi_using_planet_speed(jd, place, tithi_index, planet1, planet2, cycle)
    else:
        return tithi_using_inverse_lagrange(jd, place, tithi_index, planet1, planet2, cycle)
```
- Observed behavior: Runtime branch selection is controlled by one global switch.

### PG06

- Behavior: tithi_using_inverse_lagrange wraps _get_tithi and normalizes start/end payload.
- Source: `src/jhora/panchanga/drik.py:L589-L598`
- Excerpt:
```python
    def __get_tithi_lagrange(jd,place,tithi_index=tithi_index,planet1=planet1, planet2=planet2,cycle=cycle):
        _tithi = _get_tithi(jd,place,tithi_index,planet1,planet2,cycle=cycle)
        _tithi_prev = _get_tithi(jd-1,place,tithi_index,planet1,planet2,cycle=cycle)
        _tithi_no = _tithi[0]; _tithi_start = _tithi_prev[1]; _tithi_end = _tithi[1]
        if _tithi_start < 24.0:
            _tithi_start = -_tithi_start
        elif _tithi_start > 24:
            _tithi_start -= 24.0
        result = [_tithi_no,_tithi_start,_tithi_end]
        return result
```
- Observed behavior: Inverse-lagrange wrapper builds the tithi result payload from current and previous day.

### PG07

- Behavior: Inverse-lagrange branch appends next-tithi payload when end-time is intra-day.
- Source: `src/jhora/panchanga/drik.py:L599-L603`
- Excerpt:
```python
    ret = __get_tithi_lagrange(jd,place,tithi_index=tithi_index,planet1=planet1, planet2=planet2,cycle=cycle)
    if ret[2] < 24.0:
        ret1 = __get_tithi_lagrange(jd+ret[2]/24,place,tithi_index=tithi_index,planet1=planet1, planet2=planet2,cycle=cycle)
        _next_tithi = (ret[0])%30+1; _next_tithi_start_time = ret[2]; _next_tithi_end_time = ret[2]+ret1[2]
        ret += [_next_tithi,_next_tithi_start_time,_next_tithi_end_time]
```
- Observed behavior: Optional next-tithi segment is appended for two-tithi-in-day case.

### PG08

- Behavior: _get_nakshathra computes JD variants, anchors to sunrise, and samples moon longitude offsets.
- Source: `src/jhora/panchanga/drik.py:L656-L662`
- Excerpt:
```python
    tz = place.timezone
    y, m, d, _ = utils.jd_to_gregorian(jd)
    jd_ut = utils.gregorian_to_jd(Date(y, m, d))
    jd_utc = jd - place.timezone / 24.
    rise = sunrise(jd_utc, place)[2]
    offsets = [0.0, 0.25, 0.5, 0.75, 1.0]
    longitudes = [sidereal_longitude(rise + t, const._MOON) for t in offsets]
```
- Observed behavior: Nakshatra core path is sunrise-anchored and uses sampled longitudes.

### PG09

- Behavior: nakshatra result is assembled from current/previous helper outputs with positional indices.
- Source: `src/jhora/panchanga/drik.py:L728-L736`
- Excerpt:
```python
    _nak = _get_nakshathra(jd, place)
    _nak_prev = _get_nakshathra(jd-1, place)
    _nak_no = _nak[0]; _pad_no = _nak[1]; _nak_start = _nak_prev[2]; _nak_end = _nak[2]
    if _nak_start < 24.0:
        _nak_start = -_nak_start
    elif _nak_start > 24:
        _nak_start -= 24.0
    result = [_nak_no,_pad_no,_nak_start,_nak_end]+_nak[3:]
    return result
```
- Observed behavior: Output shape is built with explicit index positions for number, pada, start, and end.

### PG10

- Behavior: _get_yogam uses offset samples plus inverse_lagrange for end-time resolution.
- Source: `src/jhora/panchanga/drik.py:L791-L802`
- Excerpt:
```python
    # 3. Compute longitudinal sums at intervals of 0.25 days from sunrise
    offsets = [0.0,0.25, 0.5, 0.75, 1.0]
    """ Use only Moon/Sun longitudes for end time calculations and not the speeds of respective planets """
    planet1_long_diff = [ (lunar_longitude(rise + t) - lunar_longitude(rise)) % 360 for t in offsets ]
    planet2_long_diff = [ (solar_longitude(rise + t,) - solar_longitude(rise)) % 360 for t in offsets ]
    total_motion = [ (tithi_index*(p1+p2)+(cycle-1)*180)%360 for (p1, p2) in zip(planet1_long_diff, planet2_long_diff) ]
    
    # 4. Find end time by 4-point inverse Lagrange interpolation
    y = total_motion
    x = offsets
    # compute fraction of day (after sunrise) needed to traverse 'degrees_left'
    approx_end = utils.inverse_lagrange(x, y, degrees_left)
```
- Observed behavior: Yoga end-time resolution uses interpolation over sampled longitudinal motion.

### PG11

- Behavior: yogam switches between speed-based and old branch using the same global switch.
- Source: `src/jhora/panchanga/drik.py:L820-L827`
- Excerpt:
```python
def yogam(jd,place,tithi_index=1,planet1=const._MOON,planet2=const._SUN,cycle=1):
    if not const.use_planet_speed_for_panchangam_end_timings: return yogam_old(jd, place)
    _,_,_,jd_hours = utils.jd_to_gregorian(jd)
    def _get_yogam_new(jd):
        jd_utc = jd - place.timezone/24.
        yoga_phase = _special_yoga_phase(jd_utc, planet1=planet1, planet2=planet2, tithi_index=tithi_index, cycle=cycle)
        total = yoga_phase % 360
        one_yoga = 360/27
```
- Observed behavior: Yoga path has dual branch selection controlled by global switch.

### PG12

- Behavior: yogam speed branch computes next segment with jd + result[2] argument.
- Source: `src/jhora/panchanga/drik.py:L840-L843`
- Excerpt:
```python
    result = _get_yogam_new(jd)
    if result[2] < 24:
        next_res = _get_yogam_new(jd+result[2])
        next_res [1] = result[2];
```
- Observed behavior: Next-segment call uses direct addition of result[2] onto jd input.

### PG13

- Behavior: karana derives half-tithi split from tithi start/end midpoint.
- Source: `src/jhora/panchanga/drik.py:L883-L891`
- Excerpt:
```python
    _tithi = tithi(jd,place)
    _t_start = _tithi[1]; _t_end = _tithi[2]; _t_mid = 0.5*(_t_start+_t_end)
    _karana = _tithi[0]*2-1
    if birth_time_hrs> _t_mid: # second half of tithi
        _karana += 1
        _k_start = _t_mid; _k_end = _t_end
    else: # first of tithi
        _k_start = _t_start; _k_end = _t_mid
    return _karana,_k_start,_k_end
```
- Observed behavior: Karana payload is computed from tithi-derived midpoint logic.

### PG14

- Behavior: vaara uses either ahargana formula or ceil(jd+1) formula based on constant switch.
- Source: `src/jhora/panchanga/drik.py:L899-L899`
- Excerpt:
```python
    return ( int(ahargana(jd)) % 7 + 5) % 7 if const.use_aharghana_for_vaara_calcuation else int(ceil(jd + 1) % 7)  
```
- Observed behavior: Weekday formula is branch-selected by constant flag.

### PG15

- Behavior: ahargana and kali_ahargana_days are anchored to Mahabharatha epoch constant.
- Source: `src/jhora/panchanga/drik.py:L988-L989`
- Excerpt:
```python
ahargana = lambda jd: jd - const.mahabharatha_tithi_julian_day
kali_ahargana_days = lambda jd: int(ahargana(jd))
```
- Observed behavior: Ahargana epoch uses mahabharatha_tithi_julian_day constant.

### PG16

- Behavior: tithi_dates uses skip_days heuristic and day-wise while loop iteration.
- Source: `src/jhora/panchanga/vratha.py:L186-L190`
- Excerpt:
```python
    skip_days = 14
    if len(tithi_index_list) > 1:
        skip_days = 1
    while cur_jd < end_jd:
        cur_tithi = panchanga.tithi(cur_jd, panchanga_place)
```
- Observed behavior: Tithi search advances by fixed skip steps with while-loop scanning.

### PG17

- Behavior: nakshathra_dates uses skip_days heuristic and reads positional indices from nakshatra payload.
- Source: `src/jhora/panchanga/vratha.py:L227-L235`
- Excerpt:
```python
    skip_days = 26
    if len(nakshathra_index_list) > 1:
        skip_days = 1
    while cur_jd < end_jd:
        current_nakshathra = panchanga.nakshatra(cur_jd, panchanga_place)
        cur_date = panchanga.jd_to_gregorian(cur_jd)[0:3]
        if current_nakshathra[0] in nakshathra_index_list and cur_date not in special_vratha_dates:
            starts_at = current_nakshathra[1]
            ends_at = current_nakshathra[2]
```
- Observed behavior: Nakshatra search consumes index-based payload fields and fixed-step scanning.

### PG18

- Behavior: yoga_dates uses skip_days heuristic and index-based yogam payload access.
- Source: `src/jhora/panchanga/vratha.py:L260-L268`
- Excerpt:
```python
    skip_days = 26
    if len(yoga_index_list) > 0:
        skip_days = 1
    while cur_jd < end_jd:
        cur_yoga = panchanga.yogam(cur_jd, panchanga_place)
        cur_date = panchanga.jd_to_gregorian(cur_jd)[0:3]
        if cur_yoga[0] in yoga_index_list:
            ends_at = cur_yoga[1]; tag = utils.YOGAM_LIST[cur_yoga[0]-1] +' '+res['yogam_str']
            if tag_y not in tag: tag += tag_y
```
- Observed behavior: Yoga search uses fixed-step loop and positional payload fields.

### PG19

- Behavior: search enters festival mode when all Panchanga filters are absent.
- Source: `src/jhora/panchanga/vratha.py:L383-L386`
- Excerpt:
```python
    if all(x is None for x in (tithi_index, nakshathra_index, yoga_index, tamil_month_index)):
        if _debug_print: print('search for festival from csv')
        fest_data = get_festivals_between_the_dates(panchanga_start_date, panchanga_end_date, panchanga_place,festival_name_contains=festival_name_contains)
        if len(fest_data)>0:
```
- Observed behavior: Festival-mode branch is selected by absence of tithi/nakshatra/yoga/month filters.

### PG20

- Behavior: search delegates to tithi_dates and nakshathra_dates in filter mode.
- Source: `src/jhora/panchanga/vratha.py:L394-L405`
- Excerpt:
```python
    if tithi_index !=None:
        tithi_results = tithi_dates(panchanga_place, panchanga_start_date, _panchanga_end_date, [tithi_index])
        if _debug_print: print('tithi_results',tithi_results)
        if len(tithi_results) == 0: return []
        _special_vratha_dates = tithi_results
    #print('_special_vratha_dates',_special_vratha_dates)
    # Nakshathra search
    if nakshathra_index is not None:
        if _debug_print: print('finding nakshathra dates ')
        if len(_special_vratha_dates)==0:
            nakshathra_results = nakshathra_dates(panchanga_place, panchanga_start_date, panchanga_end_date, [nakshathra_index])
            if len(nakshathra_results) == 0: return []
```
- Observed behavior: Filter-mode path composes helper searches incrementally.

### PG21

- Behavior: festival_data is global state and load_festival_data reads CSV into memory.
- Source: `src/jhora/panchanga/vratha.py:L645-L652`
- Excerpt:
```python
festival_data = []

# Function to load festival data from CSV file
def load_festival_data(file_path=const._FESTIVAL_FILE):
    global festival_data
    with open(file_path, mode='r', encoding='utf-8-sig') as file:
        reader = csv.DictReader(file)
        festival_data = [row for row in reader]
```
- Observed behavior: Festival CSV is loaded into module-global list state.

### PG22

- Behavior: get_festivals_of_the_day lazily loads festival_data when state is empty.
- Source: `src/jhora/panchanga/vratha.py:L688-L694`
- Excerpt:
```python
def get_festivals_of_the_day(jd,place,festival_name_contains=None):
    global festival_data
    if len(festival_data) == 0: load_festival_data(const._FESTIVAL_FILE)
    matching_festivals = []
    criteria_list = [_get_criteria_for_the_day(jd, place, use_purnimanta_system=c) for c in [None,False,True]]
    check_rows = festival_data if festival_name_contains is None \
        else [row for row in festival_data if festival_name_contains.casefold() in row['Festival_en'].casefold()]
```
- Observed behavior: Festival retrieval path has lazy-loading behavior over global state.

### PG23

- Behavior: info consumer reads nakshatra payload indices for display assembly.
- Source: `src/jhora/panchanga/info.py:L89-L96`
- Excerpt:
```python
    key = utils.resource_strings['nakshatra_str']
    nak = drik.nakshatra(jd,place)
    frac_left = 100*utils.get_fraction(nak[2], nak[3], birth_time_hrs)
    frac_str = ' ('+"{0:.2f}".format(frac_left)+'% ' + utils.resource_strings['balance_str']+' )'
    value = utils.NAKSHATRA_LIST[nak[0]-1]+' '+  \
                ' ('+utils.PLANET_SHORT_NAMES[utils.nakshathra_lord(nak[0])]+') '+ utils.resource_strings['paadham_str']+\
                str(nak[1]) + ' '+ utils.to_dms(nak[3]) + ' ' + utils.resource_strings['ends_at_str']+frac_str
    results_dict[key] = value
```
- Observed behavior: Consumer code maps nakshatra positional fields directly.

### PG24

- Behavior: main consumer uses nakshatra positional fields for calendar output.
- Source: `src/jhora/horoscope/main.py:L183-L190`
- Excerpt:
```python
        nak = drik.nakshatra(jd,place)
        frac_left = 100*utils.get_fraction(nak[2],nak[3],birth_time_hrs)
        #print('nakshatra',nak,frac_left)
        calendar_info[cal_key_list['nakshatra_str']] = utils.NAKSHATRA_LIST[nak[0]-1]+' '+  \
                    ' ('+utils.PLANET_SHORT_NAMES[utils.nakshathra_lord(nak[0])]+') '+ cal_key_list['paadham_str']+\
                    str(nak[1]) + ' '+ utils.to_dms(nak[2]) + ' '+ cal_key_list['starts_at_str'] + ' ' + \
                    utils.to_dms(nak[3]) + ' ' + cal_key_list['ends_at_str'] + \
                    ' ('+"{0:.2f}".format(frac_left)+'% ' + cal_key_list['balance_str']+' )'
```
- Observed behavior: Main calendar path consumes positional nakshatra fields.

### PG25

- Behavior: pancha_paksha consumes tithi[0] and nakshatra[0] indexes.
- Source: `src/jhora/panchanga/pancha_paksha.py:L62-L65`
- Excerpt:
```python
    return drik.nakshatra(jd, place)[0]
def _get_paksha(jd,place):
    _tithi = drik.tithi(jd, place)[0]
    return 1 if _tithi <= 15 else 2
```
- Observed behavior: Pancha paksha flow depends on scalar indexes from tithi and nakshatra.

### PG26

- Behavior: pancha_paksha flow is sunrise-anchored and uses vaara index.
- Source: `src/jhora/panchanga/pancha_paksha.py:L80-L85`
- Excerpt:
```python
    sunrise_jd = drik.sunrise(jd, place)[-1]
    if jd < sunrise_jd:
        jd -= 1
        sunrise_jd = drik.sunrise(jd, place)[-1]
    weekday_index = drik.vaara(jd)+1
    paksha_index = pancha_paksha._get_paksha(jd, place)
```
- Observed behavior: Consumer flow uses sunrise-jd boundary and weekday index.

### PG27

- Behavior: charts consumer uses tithi index for benefic/malefic branch logic.
- Source: `src/jhora/horoscope/chart/charts.py:L1687-L1692`
- Excerpt:
```python
    _tithi = drik.tithi(jd, place)[0]
    if method == 2:
        if _tithi > 15:
            malefics.append(1)
        else:
            benefics.append(1)
```
- Observed behavior: Chart behavior depends on tithi scalar index.

### PG28

- Behavior: surya_sidhantha kali_ahargana is tied to Mahabharatha epoch and weekday alignment.
- Source: `src/jhora/panchanga/surya_sidhantha.py:L41-L45`
- Excerpt:
```python
    kad = int(jd - const.mahabharatha_tithi_julian_day) # (jd - 588466)
    wday = int(kad) % 7
    wdayjd = drik.vaara(jd)
    winc = (wdayjd - 5 - wday)
    wdayc = (wday + winc + 5) % 7
```
- Observed behavior: Alternate model keeps epoch-linked ahargana calculation.

### PG29

- Behavior: surya_sidhantha tithi computes sun/moon angular difference and end-time from daily motions.
- Source: `src/jhora/panchanga/surya_sidhantha.py:L420-L431`
- Excerpt:
```python
def tithi(jd, place):
    pp = planet_positions(jd, place)
    sun_long = pp[1][1][0]*30+pp[1][1][1]
    moon_long = pp[2][1][0]*30+pp[2][1][1]
    l_diff = (moon_long+360-sun_long)%360
    _tithi = (l_diff/12)%30
    _tithi_no = math.ceil(_tithi)
    _td_left = _tithi_no*12-l_diff
    sun_dm = _true_daily_motion_planet(jd, const._SUN)
    moon_dm = _true_daily_motion_planet(jd, const._MOON)
    _th_left = _td_left/(moon_dm-sun_dm)*24.0
    _,_,_,h = utils.jd_to_gregorian(jd)
```
- Observed behavior: Alternate tithi path uses direct daily-motion formula.

### PG30

- Behavior: surya_sidhantha nakshatra computes remainder-based end-time from moon daily motion.
- Source: `src/jhora/panchanga/surya_sidhantha.py:L435-L442`
- Excerpt:
```python
def nakshatra(jd,place):
    pp = planet_positions(jd, place)
    moon_long = pp[2][1][0]*30+pp[2][1][1]
    nak_no,padham_no,_ = drik.nakshatra_pada(moon_long)
    rem = (nak_no / 27 * 360.)-moon_long
    moon_dm = _true_daily_motion_planet(jd, const._MOON)
    _nak_left = rem/moon_dm*24.0
    _,_,_,h = utils.jd_to_gregorian(jd)
```
- Observed behavior: Alternate nakshatra path uses direct remainder-to-time conversion.

### PG31

- Behavior: gauri_choghadiya derives day segments from sunrise/sunset windows.
- Source: `src/jhora/panchanga/drik.py:L1134-L1143`
- Excerpt:
```python
def gauri_choghadiya(jd, place):
    """
        Get end times of gauri chogadiya for the given julian day
        Chogadiya is 1/8th of daytime or nighttime practiced as time measure in North India 
        @param jd: Julian Day Number of the date/time
        @param place: Place as struct ('Place',latitude,longitude,timezone)
        @return: [(chogadiyua type,start_time_string,end_time_string)...]
    """
    srise = sunrise(jd, place); sset = sunset(jd,place,gauri_choghadiya_setting=True)
    day_dur = (sset[0] - srise[0])/24
```
- Observed behavior: Secondary component consumes sunrise/sunset and weekday-dependent tables.

### PG32

- Behavior: trikalam computes intervals by weekday offsets from sunrise.
- Source: `src/jhora/panchanga/drik.py:L1191-L1200`
- Excerpt:
```python
def trikalam(jd, place, option='raahu kaalam'):
    """
        Get tri kaalam (Raahu kaalam, yama kandam and Kuligai Kaalam) for the given Julian day
        @param jd: Julian Day Number of the date/time
        @param place: Place as struct ('Place',latitude,longitude,timezone)
        @param option: one of 'raahu kaalam', 'gulikai', 'yamagandam'. Default:'raahu kaalam' 
            Note: One can use separate lambda function for each of these options
        raahu_kaalam = lambda jd, place: trikalam(jd, place, 'raahu kaalam')
            yamaganda_kaalam = lambda jd, place: trikalam(jd, place, 'yamagandam')
            gulikai_kaalam = lambda jd, place: trikalam(jd, place, 'gulikai')
```
- Observed behavior: Secondary component uses weekday-offset schedule from sunrise anchor.

### PG33

- Behavior: durmuhurtam uses sunrise/sunset/day/night durations and weekday offsets.
- Source: `src/jhora/panchanga/drik.py:L1224-L1233`
- Excerpt:
```python
def durmuhurtam(jd, place):
    """
        Get dhur muhurtham timing for the given julian day
        @param jd: Julian Day Number of the date/time
        @param place: Place as struct ('Place',latitude,longitude,timezone)
        @return: start and end time of dhur muhurtham - as list e.g. [start_time, end_time]
    """
    # Night = today's sunset to tomorrow's sunrise
    srise = sunrise(jd, place)[0]; day_dur = day_length(jd,place); night_dur = night_length(jd,place)
    sset = sunset(jd,place)[0]
```
- Observed behavior: Secondary component blends day/night durations with weekday-specific offsets.

### PG34

- Behavior: chandrabalam consumes sunrise boundary and nakshatra/moon transitions.
- Source: `src/jhora/panchanga/drik.py:L2987-L2993`
- Excerpt:
```python
def chandrabalam(jd,place):
    ascs = [(ulm[0],ulm[1]) for ulm in udhaya_lagna_muhurtha(jd, place)]
    moon = int(lunar_longitude(jd)/30)+1
    next_sunrise = sunrise(jd+1,place)[-1]
    cb_good = [1,3,6,7,10]
    cb = [ah for ah,at in ascs if utils.count_rasis(ah,moon) in cb_good and at < next_sunrise]
    next_moon = next_planet_entry_date(planet=1, jd=jd, place=place)[0]
```
- Observed behavior: Secondary component combines sunrise boundary with moon progression checks.

### PG35

- Behavior: pushkara_yoga consumes tithi/vaara/nakshatra with sunrise boundary.
- Source: `src/jhora/panchanga/drik.py:L3137-L3142`
- Excerpt:
```python
    _tithi_list = [2, 17, 7, 22, 12, 27]; _day_list = [1,3,7]
    _dwi_star_list = [5, 14, 23]; _tri_star_list = [16, 7, 3, 11, 21, 25]
    tit = tithi(jd, place); _t_no = tit[0]; _t_start = tit[1]; _t_end = tit[2]
    day = vaara(jd)+1
    nk = nakshatra(jd, place);nak = nk[0]; _n_start = nk[2]; _n_end = nk[3]
    srise1 = sunrise(jd,place)[0]; srise2 = sunrise(jd+1,place)
```
- Observed behavior: Secondary component composes multiple Panchanga primitives with sunrise gates.

### PG36

- Behavior: nakshatra return contract documents and assembles positional payload.
- Source: `src/jhora/panchanga/drik.py:L723-L730`
- Excerpt:
```python
        @return [nakshatra number, nakshatra starting time, nakshatra ending time, nakshatra fraction left, 
                 next nakshatra number, next nakshatra starting time, next nakshatra ending time, next nakshatra fraction left]
          next nakshatra index and next nakshatra time is additionally returned if two nakshatras on same day 
          nakshatra number = [1..27]  Aswini to Revathi
    """
    _nak = _get_nakshathra(jd, place)
    _nak_prev = _get_nakshathra(jd-1, place)
    _nak_no = _nak[0]; _pad_no = _nak[1]; _nak_start = _nak_prev[2]; _nak_end = _nak[2]
```
- Observed behavior: Producer contract exposes positional output layout for nakshatra payload.

### PG37

- Behavior: yogam_old return contract documents positional payload layout.
- Source: `src/jhora/panchanga/drik.py:L853-L857`
- Excerpt:
```python
        @return [yogam number, yogam starting time, yogam ending time, yogam fraction left, 
                 next yogam number, next yogam starting time, next yogam ending time, next yogam fraction left]
          next yogam index and next yogam time is additionally returned if two yogams on same day 
          yogam index = [1..27]  1 = Vishkambha, 2 = Priti, ..., 27 = Vaidhrti
    """
```
- Observed behavior: Producer contract exposes positional output layout for yoga payload.

### PG38

- Behavior: nakshathra_dates assigns starts_at from current_nakshathra[1] and ends_at from [2].
- Source: `src/jhora/panchanga/vratha.py:L234-L237`
- Excerpt:
```python
            starts_at = current_nakshathra[1]
            ends_at = current_nakshathra[2]
            tag = utils.NAKSHATRA_LIST[current_nakshathra[0]-1]
            special_vratha_dates.append((cur_date,starts_at,ends_at,tag))
```
- Observed behavior: Consumer index usage differs from producer contract interpretation.

### PG39

- Behavior: yoga_dates stores ends_at from cur_yoga[1] field.
- Source: `src/jhora/panchanga/vratha.py:L267-L270`
- Excerpt:
```python
            ends_at = cur_yoga[1]; tag = utils.YOGAM_LIST[cur_yoga[0]-1] +' '+res['yogam_str']
            if tag_y not in tag: tag += tag_y
            special_vratha_dates.append((cur_date,ends_at,tag))
            if panchanga_end_date is None :
```
- Observed behavior: Consumer index usage for yoga timing differs from producer contract interpretation.

### PG900

- Behavior: Residual callsites that match pattern inventory and are not part of dedicated PG01..PG39 anchors.
- Source: `research/panchanga_components/_coverage_panchanga_callsites_engine_plus_consumers.tsv`
- Excerpt:
```text
Rows with anchor_id=PG900 remain in inventory as residual index evidence.
```
- Observed behavior: residual index keeps non-primary and secondary components visible in scope.

## Conflict / ambiguity register

- UNCERTAIN-PG-ENDTIME-01: end-time solver behavior differs between inverse-lagrange and speed-based branches.
  - Evidence: `PG03`, `PG04`, `PG05`, `PG10`, `PG11`
- UNCERTAIN-PG-OUTIDX-01: producer payload contracts and consumer index usage are not uniform across all callsites.
  - Evidence: `PG36`, `PG37`, `PG38`, `PG39`
- UNCERTAIN-PG-STEP-01: fixed skip-day stepping is used in vratha search loops.
  - Evidence: `PG16`, `PG17`, `PG18`
- UNCERTAIN-PG-IO-STATE-01: festival CSV loading and global mutable state are coupled in festival paths.
  - Evidence: `PG21`, `PG22`, `PG19`
- UNCERTAIN-PG-ORPHAN-01: secondary components consume Panchanga primitives outside five-core component list.
  - Evidence: `PG31`, `PG32`, `PG33`, `PG34`, `PG35`
- UNCERTAIN-PG-UNIT-01: yogam next-segment call uses `jd + result[2]` directly.
  - Evidence: `PG12`

## Coverage ledger

- Inventory file: `research/panchanga_components/_coverage_panchanga_callsites_engine_plus_consumers.tsv`
- Inventory columns: `file`, `line`, `pattern`, `function_context`, `anchor_id`, `scope_class`
- Inventory row count: `1714`
- Unique `(file,function_context)` count: `307`
- Rows by scope_class: `engine_core=651`, `engine_helper=139`, `consumer_core=469`, `residual=455`
- Residual rows (`PG900`): `1532`
- Algorithm matrix: `research/panchanga_components/_coverage_panchanga_algorithm_matrix.tsv`
- Output contract matrix: `research/panchanga_components/_coverage_panchanga_output_contract_matrix.tsv`

## Sanity checks

- command: `rg -n "^### PG[0-9]+|^### PG900" research/panchanga_components/panchanga_behavior_contract_map.engine_plus_consumers.md -S`
- command: `rg -n "UNCERTAIN-PG-" research/panchanga_components/panchanga_behavior_contract_map.engine_plus_consumers.md -S`
- command: `rg -n "Source:" research/panchanga_components/panchanga_behavior_contract_map.engine_plus_consumers.md -S`
- command: `Get-Content research/panchanga_components/_coverage_panchanga_callsites_engine_plus_consumers.tsv | Measure-Object -Line`
- command: `Get-Content research/panchanga_components/_coverage_panchanga_algorithm_matrix.tsv | Measure-Object -Line`
- command: `Get-Content research/panchanga_components/_coverage_panchanga_output_contract_matrix.tsv | Measure-Object -Line`
