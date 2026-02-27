# lagna_bhava_behavior_contract_map.core_plus1hop.md

## Snapshot identity (FACTS)

- pyjhora_root: `D:\lab\Pyjhora`
- extraction_timestamp_local: `2026-02-27 02:46:13 +03:30`
- in-scope file digests (SHA256):
  - `src/jhora/panchanga/drik.py` -> `9790dcdf442910b1eaa260b16c346c6696438eb6955c0a520c1be220ba3497bc` (bytes: `186944`)
  - `src/jhora/horoscope/chart/charts.py` -> `34c49af9fb3359fdb243f2a467404b7a849e35b9def9e2961a45a4027c8619b2` (bytes: `141395`)
  - `src/jhora/const.py` -> `2dacc910fce9babc69582491b52cde9fd23ab9dde835d41efb65fc0f79e00ba8` (bytes: `79727`)
  - `src/jhora/panchanga/surya_sidhantha.py` -> `cb5190f94884e4e79d5ed0f98988fa510567bb8e8a02942d3a0a600c4ed808b9` (bytes: `29995`)
  - `src/jhora/horoscope/chart/house.py` -> `d2d0d2b9a1e382879b0f191498bcc8dc9d4ef74224925ffb522f2cc0e4329861` (bytes: `80854`)
  - `src/jhora/horoscope/chart/arudhas.py` -> `384d7794152d11fd529db018769e70c6ebaa52bd6c908762fddb8a6de0f42ee9` (bytes: `10768`)
  - `src/jhora/horoscope/chart/sphuta.py` -> `3b2d77fc54d16782823c81f3e971e36d21e667e8c984a15a611a5bf44501c1d6` (bytes: `25231`)
  - `src/jhora/utils.py` -> `861062b3abba1655b9d4e5608333f8aaa1d391b3d38ecdacbac565bf930f3875` (bytes: `70076`)

## Scope (FACTS)

- In-scope files:
  - `src/jhora/panchanga/drik.py`
  - `src/jhora/horoscope/chart/charts.py`
  - `src/jhora/const.py`
  - `src/jhora/panchanga/surya_sidhantha.py`
  - `src/jhora/horoscope/chart/house.py`
  - `src/jhora/horoscope/chart/arudhas.py`
  - `src/jhora/horoscope/chart/sphuta.py`
  - `src/jhora/utils.py`
- Out-of-scope:
  - UI modules
  - tests
  - `src/jhora/panchanga/drik1.py`
  - deep consumers outside one-hop (kept as residual inventory)

## Pattern inventory (FACTS)

- `houses_ex`
- `ascendant`
- `bhaava_madhya`
- `bhava_madhya_method`
- `house_code`
- `western_house_systems`
- `available_house_systems`
- `planet_positions[0]`
- `set_ayanamsa_mode`
- `reset_ayanamsa_mode`
- `lagna`
- `divisional_chart_factor`

## Required anchor set (FACTS)

- Producer contract: `charts.rasi_chart()` prepends Lagna row at index 0 in `planet_positions`.
- Contract fact: `planet_positions[0]` is consumed as Lagna in multiple one-hop consumers.
- Dispatch contract: `_bhaava_madhya_new()` routes methods to equal/sripati/kp/western paths.
- House backend contract: `bhaava_madhya_swe()` and `bhaava_madhya_kp()` return `houses_ex(...)[0]`.
- Ascendant output contract: `ascendant()` reads `houses_ex(...)[1][0]`.
- One-hop consumers: `arudhas.py`, `sphuta.py`, `house.py`, and `utils.py` are anchored.
- Divisional coupling: lagna-related flows with `divisional_chart_factor` are anchored.

## Evidence anchors (LH01..LH15)

### LH01

- Behavior: `rasi_chart()` prepends Lagna row at index 0 in `planet_positions`.
- Source: `src/jhora/horoscope/chart/charts.py:L95-L106`
- Excerpt:
```python
ascendant_index = const._ascendant_symbol
" Get Ascendant information"
ascendant_constellation, ascendant_longitude, _, _ = drik.ascendant(jd_years,place_as_tuple)
""" FIXED in V2.3.1 - asc long re-calculated to get full longitude value """
" Get planet information "
" planet_positions lost: [planet_id, planet_constellation, planet_longitude] "
planet_positions = drik.dhasavarga(jd_years,place_as_tuple,divisional_chart_factor=1)
planet_positions = [[ascendant_index,(ascendant_constellation, ascendant_longitude)]] + planet_positions
```
- Observed behavior: Lagna is injected before all graha rows.

### LH02

- Behavior: `_bhaava_madhya_new()` validates method and reads Lagna from `planet_positions[0]`.
- Source: `src/jhora/horoscope/chart/charts.py:L136-L141`
- Excerpt:
```python
if bhava_madhya_method not in const.available_house_systems.keys():
    warnings.warn(warn_msg)
    bhava_madhya_method = 1
ascendant_constellation, ascendant_longitude = planet_positions[0][1][0],planet_positions[0][1][1]
ascendant_full_longitude = (ascendant_constellation*30+ascendant_longitude)%360
```
- Observed behavior: Lagna index contract is hardcoded in bhava assignment orchestration.

### LH03

- Behavior: `_bhaava_madhya_new()` dispatches method 4 and western keys to KP/SwissEph backends.
- Source: `src/jhora/horoscope/chart/charts.py:L163-L164`
- Excerpt:
```python
elif bhava_madhya_method ==4 or bhava_madhya_method in const.western_house_systems.keys(): #KP Method (aka swiss ephemeris method) or western house systems
    bm = drik.bhaava_madhya_kp(jd, place) if bhava_madhya_method ==4 else drik.bhaava_madhya_swe(jd, place, house_code=bhava_madhya_method)
```
- Observed behavior: dispatch mixes numeric and letter-key method inputs.

### LH04

- Behavior: western house-system codes and merged available-house-system map are declared in constants.
- Source: `src/jhora/const.py:L632-L635`
- Excerpt:
```python
western_house_systems = {'P':'Placidus','K':'Koch','O':'Porphyrius','R':'Regiomontanus','C':'Campanus','A':'Equal (cusp 1 is Ascendant)',
                         'V':'Vehlow equal (Asc. in middle of house 1)','X':'axial rotation system','H':'azimuthal or horizontal system',
                         'T':'Polich/Page (topocentric system)','B':'Alcabitus','M':'Morinus'}
available_house_systems = {**indian_house_systems, **western_house_systems}
```
- Observed behavior: code namespace for house systems is centrally defined.

### LH05

- Behavior: `bhaava_madhya_swe()` validates `house_code`, converts to bytes `hsys`, and returns `houses_ex(...)[0]`.
- Source: `src/jhora/panchanga/drik.py:L1424-L1431`
- Excerpt A:
```python
if house_code not in const.western_house_systems.keys():
    warnings.warn(warn_msg)
    house_code = 'P'
hsys = bytes(house_code,encoding='ascii')
global _ayanamsa_mode,_ayanamsa_value
_, lat, lon, tz = place
jd_utc = jd - (tz / 24.)
```
- Source: `src/jhora/panchanga/drik.py:L1435-L1437`
- Excerpt B:
```python
flags = swe.FLG_SIDEREAL
set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd) # needed for swe.houses_ex()
return list(swe.houses_ex(jd_utc, lat, lon,hsys, flags = flags)[0])
```
- Observed behavior: cusp output uses index `[0]`; local reset is not shown in this function body.

### LH06

- Behavior: `bhaava_madhya_kp()` uses `houses_ex(...)[0]` with `jd_utc` and sidereal set path.
- Source: `src/jhora/panchanga/drik.py:L1444-L1451`
- Excerpt:
```python
_, lat, lon, tz = place
jd_utc = jd - (tz / 24.)
if const._TROPICAL_MODE:
    flags = swe.FLG_SWIEPH
else:
    flags = swe.FLG_SIDEREAL
    set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd) # needed for swe.houses_ex()
return list(swe.houses_ex(jd_utc, lat, lon, flags = flags)[0])
```
- Observed behavior: KP cusp path also uses `[0]` output and no local reset call in the shown body.

### LH07

- Behavior: `ascendant()` reads `houses_ex(...)[1][0]` and calls `reset_ayanamsa_mode()` before return.
- Source: `src/jhora/panchanga/drik.py:L1479-L1489`
- Excerpt:
```python
jd_utc = jd - (tz / 24.)
if const._TROPICAL_MODE:
    flags = swe.FLG_SWIEPH
else:
    flags = swe.FLG_SIDEREAL
    set_ayanamsa_mode(_ayanamsa_mode,_ayanamsa_value,jd) # needed for swe.houses_ex()
nirayana_lagna = swe.houses_ex(jd_utc, lat, lon, flags = flags)[1][0]
nak_no,paadha_no,_ = nakshatra_pada(nirayana_lagna)
constellation = int(nirayana_lagna / 30)
coordinates = nirayana_lagna-constellation*30
reset_ayanamsa_mode()
```
- Observed behavior: ascendant output uses ascmc index path `[1][0]` with in-function reset.

### LH08

- Behavior: `arudhas.py` consumes Lagna/house base from planet positions structure.
- Source: `src/jhora/horoscope/chart/arudhas.py:L37-L40`
- Excerpt:
```python
h_to_p = utils.get_house_planet_list_from_planet_positions(planet_positions)
p_to_h = utils.get_planet_to_house_dict_from_chart(h_to_p)
base_house = planet_positions[arudha_base][1][0]
houses = [(h+base_house)%12 for h in range(12)]
```
- Observed behavior: arudha computation depends on house index from `planet_positions` rows.

### LH09

- Behavior: `sphuta.tri_sphuta()` reads Lagna from `planet_positions[0]` and propagates `divisional_chart_factor`.
- Source: `src/jhora/horoscope/chart/sphuta.py:L38-L46`
- Excerpt:
```python
planet_positions = charts.divisional_chart(jd_at_dob, place,  
                                    divisional_chart_factor=divisional_chart_factor, chart_method=chart_method,
                                    years=years,months=months, sixty_hours=sixty_hours)
moon_long = planet_positions[const.MOON_ID+1][1][0]*30+planet_positions[const.MOON_ID+1][1][1]
asc_long = planet_positions[0][1][0]*30+planet_positions[0][1][1]
gulika = drik.gulika_longitude(dob,tob,place,divisional_chart_factor=divisional_chart_factor)
_tri_sphuta = (moon_long+asc_long+gulika_long)%360
return drik.dasavarga_from_long(_tri_sphuta, divisional_chart_factor=divisional_chart_factor)
```
- Observed behavior: Lagna index contract and divisional coupling appear in the same one-hop consumer.

### LH10

- Behavior: `utils.get_planet_to_house_dict_from_chart()` documents Lagna token and includes ascendant symbol in mapping.
- Source: `src/jhora/utils.py:L343-L350`
- Excerpt:
```python
@param house_to_planet list - in the format ['0','1/2',...] Aries has Sun, Tarus has Moon/Mars etc
        'L' is used for Lagna
@return: house_to_planet_list: 
        Format {planet_id : raasi_number, ....}
        Example: {0:0, 1:1,2:1,...} Sun in Aries, Moon in Tarus, Mars in Gemini etc
        Last element will be 'L' for Lagna
"""
p_to_h = {p:h for p in const.SUN_TO_KETU+[const._ascendant_symbol] for h,planets in enumerate(house_to_planet_list) if str(p) in planets }
```
- Observed behavior: utility mapping explicitly includes Lagna symbol in house dictionary creation.

### LH11

- Behavior: `utils.get_house_planet_list_from_planet_positions()` specifies Lagnam in target representation.
- Source: `src/jhora/utils.py:L362-L366`
- Excerpt:
```python
to convert from the format [planet,(house,planet_longitude,...]
into a dict of {house_1:planet_1/planet_2,house_2:Lagnam/planet_2,....}
@param planet_positions: Format: {planet_index:(raasi_index,planet_longitude_in_the_raasi),...
@return: house_to_planet list - in the format ['0','1/2',...] Aries has Sun, Tarus has Moon/Mars etc
```
- Observed behavior: utility contract preserves Lagna inside house-to-planet list payloads.

### LH12

- Behavior: `house.py` consumers read Lagna from `planet_positions[0]` when ascendant symbol is requested.
- Source: `src/jhora/horoscope/chart/house.py:L419-L427`
- Excerpt:
```python
if planet1==const._ascendant_symbol:
    planet1_rasi = planet_positions[0][1][0]; planet2_rasi = planet_positions[planet2+1][1][0]
    sr = stronger_rasi_from_planet_positions(planet_positions, planet1_rasi, planet2_rasi)
    if sr == planet1_rasi:
        return planet1
    else:
        return planet2
if planet2==const._ascendant_symbol:
    planet2_rasi = planet_positions[0][1][0]; planet1_rasi = planet_positions[planet1+1][1][0]
```
- Observed behavior: one-hop house logic consumes hardcoded Lagna index `[0]`.

### LH13

- Behavior: `surya_sidhantha.ascendant()` uses sidereal flag path and calls `set_ayanamsa_mode`.
- Source: `src/jhora/panchanga/surya_sidhantha.py:L174-L180`
- Excerpt:
```python
if const._TROPICAL_MODE:
    flags = swe.FLG_SWIEPH
else:
    flags = swe.FLG_SIDEREAL
    drik.set_ayanamsa_mode(drik._ayanamsa_mode,drik._ayanamsa_value,jd) # needed for swe.houses_ex()
nak_no,paadha_no,_ = drik.nakshatra_pada(asc_long)
return [const._ascendant_symbol,[asc_rasi,asc_coordinates]]#,nak_no,paadha_no]
```
- Observed behavior: sidereal state set path appears in Surya Siddhantha ascendant branch.

### LH14

- Behavior: `surya_sidhantha.planet_positions()` prepends ascendant entry to returned planet positions.
- Source: `src/jhora/panchanga/surya_sidhantha.py:L389-L390`
- Excerpt:
```python
asc = ascendant_new(jd, place, sun_long)
planet_positions_ss = [[const._ascendant_symbol,[asc[0],asc[1]]]] + planet_positions_ss
```
- Observed behavior: Lagna-first packaging pattern appears in this one-hop producer path.

### LH15

- Behavior: `special_ascendant()` computes lagna-derived result using sunrise and `divisional_chart_factor`.
- Source: `src/jhora/panchanga/drik.py:L1762-L1773`
- Excerpt:
```python
srise = sunrise(jd, place) #V2.3.1 Get sunrise JD - as we need sun longitude at sunrise
sun_rise_hours = srise[0]
time_diff_mins = (time_of_birth_in_hours-sun_rise_hours)*60
from jhora.horoscope.chart import charts
""" 
    Change in V3.6.3
    We need Sun position at sunrise. So we use srise[2] returned from sunrise function.
    Since sunrise function returns JD Local at sunrise we add local time here because charts will minus it to get UTC
"""
jd_at_sunrise = srise[2]+place.timezone/24
pp = charts.divisional_chart(jd_at_sunrise, place, 
        divisional_chart_factor=divisional_chart_factor,chart_method=chart_method,base_rasi=base_rasi,
```
- Observed behavior: lagna flow is coupled with divisional-chart selection in this path.

### LH900

- Behavior: residual callsites not expanded into dedicated `LH01..LH15` anchors.
- Source: `research/lagna_and_bhava_houses/_coverage_lagna_bhava_callsites_core_plus1hop.tsv`
- Excerpt:
```text
Rows with anchor_id=LH900 are retained as residual inventory entries.
```
- Observed behavior: residual coverage is explicit and auditable.

## Conflict / ambiguity register

- UNCERTAIN-LH-STATE-01: asymmetry exists between set/reset sidereal state in house-related callsites.
  - Evidence A: `ascendant()` includes `reset_ayanamsa_mode()` in-function. [LH07]
  - Evidence B: `bhaava_madhya_swe()` and `bhaava_madhya_kp()` return from `houses_ex` without local reset in shown bodies. [LH05, LH06]

- UNCERTAIN-LH-CODE-01: method/code path uses mixed numeric-vs-letter contract across boundaries.
  - Evidence A: `_bhaava_madhya_new()` dispatches method `4` and `western_house_systems` keys. [LH03]
  - Evidence B: `bhaava_madhya_swe()` validates `house_code` and converts to ASCII `hsys`. [LH05]
  - Evidence C: `const.western_house_systems` keys are letter codes merged in `available_house_systems`. [LH04]

## Coverage ledger

- Inventory file: `research/lagna_and_bhava_houses/_coverage_lagna_bhava_callsites_core_plus1hop.tsv`
- Inventory columns: `file`, `line`, `pattern`, `function_context`, `anchor_id`
- Inventory row count: `979`
- Unique `(file,function_context)` count: `191`
- Residual rows (`LH900`): `828`

## Sanity checks

- command: `rg -n "^### LH[0-9]+|^### LH900" research/lagna_and_bhava_houses/lagna_bhava_behavior_contract_map.core_plus1hop.md -S`
- command: `rg -n "UNCERTAIN-LH-" research/lagna_and_bhava_houses/lagna_bhava_behavior_contract_map.core_plus1hop.md -S`
- command: `rg -n "Source:" research/lagna_and_bhava_houses/lagna_bhava_behavior_contract_map.core_plus1hop.md -S`
- command: `Get-Content research/lagna_and_bhava_houses/_coverage_lagna_bhava_callsites_core_plus1hop.tsv | Measure-Object -Line`
