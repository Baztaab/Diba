# eclipse_behavior_contract_map.core_plus_consumers.md

## Snapshot identity (FACTS)

- pyjhora_root: `D:\lab\Pyjhora`
- extraction_timestamp_local: `2026-02-28 06:24:57`
- in-scope files: `4`
- in-scope file digests (SHA256):
- `src/jhora/panchanga/drik.py` -> `9790dcdf442910b1eaa260b16c346c6696438eb6955c0a520c1be220ba3497bc` (bytes: `186944`)
- `src/jhora/const.py` -> `2dacc910fce9babc69582491b52cde9fd23ab9dde835d41efb65fc0f79e00ba8` (bytes: `79727`)
- `src/jhora/utils.py` -> `861062b3abba1655b9d4e5608333f8aaa1d391b3d38ecdacbac565bf930f3875` (bytes: `70076`)
- `src/jhora/README.md` -> `1d25379e46f15cfa0e2fa91182ba0ea919ebab205241b671a9b126010f11850a` (bytes: `56097`)

## Scope (FACTS)

- In-scope engine files:
  - `src/jhora/panchanga/drik.py`
  - `src/jhora/const.py`
  - `src/jhora/utils.py`
- In-scope supporting documentation:
  - `src/jhora/README.md`
- In-scope consumers:
  - none found in non-UI/non-test core scope; absence recorded as a fact
- Out-of-scope:
  - refactor / bug-fix
  - eclipse wrapper behavior changes
  - retflag parser addition
  - object-model additions for eclipse result
  - Swiss Ephemeris integration changes

## Pattern inventory (FACTS)
- `eclipse`
- `grahana`
- `is_solar_eclipse`
- `next_solar_eclipse`
- `next_lunar_eclipse`
- `sol_eclipse_how`
- `sol_eclipse_when_loc`
- `lun_eclipse_when_loc`
- `retflag`
- `tret`
- `attrs`
- `geopos`
- `Place`
- `latitude`
- `longitude`
- `_TROPICAL_MODE`
- `FLG_SWIEPH`
- `FLG_SIDEREAL`
- `_rise_flags`
- `ECL_`
- `saros`
- `greatest eclipse`
- `first contact`
- `second contact`
- `third contact`
- `fourth contact`

## Behavior taxonomy (FACTS)

- place struct, flags, and jd-basis conversion: `EG01`, `EG02`, `EG03`
- solar and lunar eclipse Swiss wrappers: `EG04`, `EG05`
- raw output contracts and comment-only parsing: `EG06`, `EG07`
- dependency and release-note touchpoints: `EG08`, `EG09`
- negative facts: `ABSENCE-OF-RETFLAG-PARSER`, `ABSENCE-OF-INTERNAL-ECLIPSE-CONSUMER`
- residual inventory: `EG900`

## Evidence anchors (EG01..EGNN, EG900)

### EG01

- Behavior: `Place` is defined with latitude then longitude, while eclipse wrappers later pass those fields directly into `geopos` tuples.
- Source: `src/jhora/panchanga/drik.py:L41-L41`
- Excerpt:
```python
Place = struct('Place', ['Place','latitude', 'longitude', 'timezone'])
```
- Observed behavior: The struct field order is explicit and becomes relevant for the later `geopos` ambiguity.

### EG02

- Behavior: Utility conversion functions rebuild a Julian day from calendar date at `0.0` hours.
- Source: `src/jhora/utils.py:L697-L698`
- Excerpt:
```python
gregorian_to_jd = lambda date: swe.julday(date.year, date.month, date.day, 0.0)
jd_to_gregorian = lambda jd: swe.revjul(jd, swe.GREG_CAL)   # returns (y, m, d, fh
```
- Observed behavior: `is_solar_eclipse` can discard input time-of-day because it reconstructs JD from date only.

### EG03

- Behavior: `is_solar_eclipse` is a Swiss Ephemeris evaluation wrapper with a calendar-day reset and mode-based flag branch.
- Source: `src/jhora/panchanga/drik.py:L2292-L2301`
- Excerpt:
```python
def is_solar_eclipse(jd,place):
    y, m, d, h = jd_to_gregorian(jd)
    jd_utc = utils.gregorian_to_jd(Date(y, m, d))
    lon,lat = place.latitude, place.longitude
    if const._TROPICAL_MODE:
        flags = swe.FLG_SWIEPH
    else:
        flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | _rise_flags
    ret,_ = swe.sol_eclipse_how(jd_utc,geopos=(lon, lat,0.0),flags=flags)
    return ret
```
- Observed behavior: The function calls `swe.sol_eclipse_how` directly, resets the input JD to the day boundary, and mixes `_rise_flags` into the sidereal path.

### EG04

- Behavior: `next_solar_eclipse` delegates the search directly to `swe.sol_eclipse_when_loc` and returns raw arrays.
- Source: `src/jhora/panchanga/drik.py:L2338-L2345`
- Excerpt:
```python
    geopos = (place.latitude, place.longitude,0.0)
    retflag,tret,attrs = swe.sol_eclipse_when_loc(jd,geopos)
    #print(ecl_dict.values(),retflag)
    #if retflag in ecl_dict.values(): print( list(ecl_dict.keys())[list(ecl_dict.values()).index(retflag)])
    #y,m,d,fh_ut = utils.jd_to_gregorian(tret[1])
    #fh_l = fh_ut + place.timezone
    #ecl_local = (y,m,d,fh_l)
    return [retflag,tret,attrs]
```
- Observed behavior: No iterative search or normalization layer is implemented in PyJHora; the wrapper passes through `[retflag, tret, attrs]`.

### EG05

- Behavior: `next_lunar_eclipse` delegates the search directly to `swe.lun_eclipse_when_loc` and returns raw arrays.
- Source: `src/jhora/panchanga/drik.py:L2377-L2382`
- Excerpt:
```python
    geopos = (place.latitude, place.longitude,0.0)
    retflag,tret,attrs = swe.lun_eclipse_when_loc(jd,geopos)
    #y,m,d,fh_ut = utils.jd_to_gregorian(tret[1])
    #fh_l = fh_ut + place.timezone
    #ecl_local = (y,m,d,fh_l)
    return [retflag,tret,attrs]
```
- Observed behavior: Lunar eclipse search is the same thin-wrapper pattern as solar eclipse search.

### EG06

- Behavior: Solar eclipse docstring documents `tret` contact times and `attrs` magnitude, obscuration, altitude and Saros fields.
- Source: `src/jhora/panchanga/drik.py:L2313-L2331`
- Excerpt:
```python
            tret[0] = time of greatest eclipse (Julian day number)            
            tret[1] = first contact
            tret[2] = second contact
            tret[3] = third contact
            tret[4] = fourth contact
            
            attr[0]   fraction of solar diameter covered by moon;
                    with total/annular eclipses, it results in magnitude acc. to IMCCE.
            attr[1]   ratio of lunar diameter to solar one
            attr[2]   fraction of solar disc covered by moon (obscuration)
            attr[3]   diameter of core shadow in km
            attr[4]   azimuth of sun at tjd
```
- Observed behavior: The output contract is documented in prose but returned raw without post-processing.

### EG07

- Behavior: Eclipse type mapping via `swe.ECL_*` exists only as commented code and is not executed.
- Source: `src/jhora/panchanga/drik.py:L2334-L2341`
- Excerpt:
```python
    #ecl_dict = {"Annular":swe.ECL_ANNULAR | swe.ECL_CENTRAL | swe.ECL_NONCENTRAL,
    #            "Total":swe.ECL_TOTAL | swe.ECL_CENTRAL | swe.ECL_NONCENTRAL,
    #            "Annular Total":swe.ECL_ANNULAR_TOTAL | swe.ECL_CENTRAL | swe.ECL_NONCENTRAL,
    #            "Partial":swe.ECL_PARTIAL | swe.ECL_CENTRAL | swe.ECL_NONCENTRAL}
    geopos = (place.latitude, place.longitude,0.0)
    retflag,tret,attrs = swe.sol_eclipse_when_loc(jd,geopos)
    #print(ecl_dict.values(),retflag)
    #if retflag in ecl_dict.values(): print( list(ecl_dict.keys())[list(ecl_dict.values()).index(retflag)])
```
- Observed behavior: The codebase documents a possible type map but does not parse `retflag` into labeled eclipse types.

### EG08

- Behavior: Eclipse functions are tightly coupled to Swiss Ephemeris plus `const` and `utils` helpers.
- Source: `src/jhora/panchanga/drik.py:L2296-L2300`
- Excerpt:
```python
    if const._TROPICAL_MODE:
        flags = swe.FLG_SWIEPH
    else:
        flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | _rise_flags
    ret,_ = swe.sol_eclipse_how(jd_utc,geopos=(lon, lat,0.0),flags=flags)
```
- Observed behavior: Swiss Ephemeris is the actual math/search engine, while PyJHora only selects flags and forwards input structures.

### EG09

- Behavior: README records eclipse wrappers as a later addition to `drik.py`.
- Source: `src/jhora/README.md:L752-L752`
- Excerpt:
```text
* panchanga/drik.py - `_rise_flags` changed to `swe.BIT_HINDU_RISING`. Added new functions  `next_solar_eclipse(jd,place)` and `next_lunar_eclipse(jd,place)` to calculate next solar/lunar eclipse dates.
```
- Observed behavior: Release-note evidence confirms the wrappers were added as new functions rather than being deeply integrated into other subsystems.

### ABSENCE-OF-RETFLAG-PARSER

- Behavior: No active parser was found that converts eclipse `retflag` values into explicit labeled types.
- Source: `research/eclipses_and_grahana/_coverage_eclipses_callsites_core_plus_consumers.tsv:L2`
- Excerpt:
```text
Scope-ActiveCode	0	retflag_parser	not_found_in_active_code	ABSENCE-OF-RETFLAG-PARSER	engine_core
```
- Observed behavior: Type interpretation remains comment-level only in the active codebase.

### ABSENCE-OF-INTERNAL-ECLIPSE-CONSUMER

- Behavior: No direct non-UI, non-test consumer callsite was found for eclipse wrappers inside `src/jhora`.
- Source: `research/eclipses_and_grahana/_coverage_eclipses_callsites_core_plus_consumers.tsv:L3`
- Excerpt:
```text
Scope-ConsumerAudit	0	internal_eclipse_consumer	not_found_in_non_ui_non_test_scope	ABSENCE-OF-INTERNAL-ECLIPSE-CONSUMER	engine_core
```
- Observed behavior: The engine appears orphaned within the scoped core codebase.

### EG900

- Behavior: Residual matched rows are retained in the callsite inventory.
- Source: `research/eclipses_and_grahana/_coverage_eclipses_callsites_core_plus_consumers.tsv:L4`
- Excerpt:
```text
Scope-Residual	0	residual_inventory	retained_matches	EG900	residual
```
- Observed behavior: Non-focused matches remain visible instead of being discarded.

## Conflict / ambiguity register

- UNCERTAIN-EG-GEOPOS-ORDER: The wrapper passes `Place` fields directly into `geopos`, and the coordinate ordering is not clarified in local code.
- UNCERTAIN-EG-RETFLAG-PARSING: Eclipse type parsing exists only in comments and not in active logic.
- UNCERTAIN-EG-INTERNAL-CONSUMER: No direct non-UI consumer was found in scoped code.
- UNCERTAIN-EG-TIMEZONE-CONTRACT: `next_*` docstrings discuss UT plus manual timezone adjustment, but wrappers do not normalize returned times.
- UNCERTAIN-EG-IS-SOLAR-ECLIPSE-JD-BASIS: `is_solar_eclipse` rebuilds JD from date and may discard time-of-day semantics.

## Coverage ledger

- Inventory file: `research/eclipses_and_grahana/_coverage_eclipses_callsites_core_plus_consumers.tsv`
- Inventory columns: `file`, `line`, `pattern`, `function_context`, `anchor_id`, `scope_class`
- Inventory row count: `{callsite_count}`
- Unique `(file,function_context)` count: `{unique_file_context}`
- Rows by scope_class: `engine_core={scope_counter.get('engine_core',0)}`, `residual={scope_counter.get('residual',0)}`
- Absence rows (`ABSENCE-OF-RETFLAG-PARSER`): `{retflag_absence_rows}`
- Absence rows (`ABSENCE-OF-INTERNAL-ECLIPSE-CONSUMER`): `{consumer_absence_rows}`
- Search matrix: `research/eclipses_and_grahana/_coverage_eclipse_search_matrix.tsv`
- Output-contract matrix: `research/eclipses_and_grahana/_coverage_eclipse_output_contract_matrix.tsv`
- Dependency-touchpoints matrix: `research/eclipses_and_grahana/_coverage_eclipse_dependency_touchpoints_matrix.tsv`

## Sanity checks

- command: `rg -n "^### EG[0-9]+|^### EG900|^### ABSENCE-OF-RETFLAG-PARSER|^### ABSENCE-OF-INTERNAL-ECLIPSE-CONSUMER" research/eclipses_and_grahana/eclipse_behavior_contract_map.core_plus_consumers.md -S`
- command: `rg -n "UNCERTAIN-EG-" research/eclipses_and_grahana/eclipse_behavior_contract_map.core_plus_consumers.md -S`
- command: `rg -n "Source:" research/eclipses_and_grahana/eclipse_behavior_contract_map.core_plus_consumers.md -S`
- command: `Get-Content research/eclipses_and_grahana/_coverage_eclipses_callsites_core_plus_consumers.tsv | Measure-Object -Line`
- command: `Get-Content research/eclipses_and_grahana/_coverage_eclipse_search_matrix.tsv | Measure-Object -Line`
- command: `Get-Content research/eclipses_and_grahana/_coverage_eclipse_output_contract_matrix.tsv | Measure-Object -Line`
- command: `Get-Content research/eclipses_and_grahana/_coverage_eclipse_dependency_touchpoints_matrix.tsv | Measure-Object -Line`
