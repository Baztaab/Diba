# PyJHora Coverage (Repo-Local Evidence)

Scope: only `docs/jhora/` (vendorized PyJHora in this repo).

## 1) Ayanamsa Coverage

### Accepted IDs in PyJHora
`set_ayanamsa_mode` accepts keys from `const.available_ayanamsa_modes` (case-insensitive via `.upper()`).  
Citations: `docs/jhora/panchanga/drik.py:117`, `docs/jhora/panchanga/drik.py:130`, `docs/jhora/panchanga/drik.py:132`.

### Full ID -> SwissEph mapping
Source mapping dictionary: `docs/jhora/const.py:190`, `docs/jhora/const.py:191`, `docs/jhora/const.py:192`, `docs/jhora/const.py:193`, `docs/jhora/const.py:194`, `docs/jhora/const.py:195`, `docs/jhora/const.py:196`, `docs/jhora/const.py:197`, `docs/jhora/const.py:198`, `docs/jhora/const.py:199`.

| ID | Mapping in PyJHora |
| --- | --- |
| `FAGAN` | `swe.SIDM_FAGAN_BRADLEY` |
| `KP` | `swe.SIDM_KRISHNAMURTI` |
| `LAHIRI` | `swe.SIDM_LAHIRI` |
| `RAMAN` | `swe.SIDM_RAMAN` |
| `USHASHASHI` | `swe.SIDM_USHASHASHI` |
| `YUKTESHWAR` | `swe.SIDM_YUKTESHWAR` |
| `SURYASIDDHANTA` | `swe.SIDM_SURYASIDDHANTA` |
| `SURYASIDDHANTA_MSUN` | `swe.SIDM_SURYASIDDHANTA_MSUN` |
| `ARYABHATA` | `swe.SIDM_ARYABHATA` |
| `ARYABHATA_MSUN` | `swe.SIDM_ARYABHATA_MSUN` |
| `SS_CITRA` | `swe.SIDM_SS_CITRA` |
| `TRUE_CITRA` | `swe.SIDM_TRUE_CITRA` |
| `TRUE_REVATI` | `swe.SIDM_TRUE_REVATI` |
| `SS_REVATI` | `swe.SIDM_SS_REVATI` |
| `SENTHIL` | `''` (not a `swe.SIDM_*` constant in this dict) |
| `TRUE_LAHIRI` | `swe.SIDM_TRUE_CITRA` |
| `TRUE_PUSHYA` | `swe.SIDM_TRUE_PUSHYA` |
| `TRUE_MULA` | `swe.SIDM_TRUE_MULA` |
| `KP-SENTHIL` | `swe.SIDM_KRISHNAMURTI_VP291` |
| `SIDM_USER` | `swe.SIDM_USER` |
| `SUNDAR_SS` | `''` (not a `swe.SIDM_*` constant in this dict) |

### Default ayanamsa
Default is `LAHIRI`.  
Citation: `docs/jhora/const.py:202`.

### Important aliases / special handling
- `TRUE_LAHIRI` is mapped to `swe.SIDM_TRUE_CITRA` in the mode dictionary.  
Citation: `docs/jhora/const.py:196`.
- For regular mapped IDs, `set_ayanamsa_mode` calls `swe.set_sid_mode(const.available_ayanamsa_modes[key])`.  
Citation: `docs/jhora/panchanga/drik.py:141`.
- `SIDM_USER` uses `swe.set_sid_mode(swe.SIDM_USER, ayanamsa_value)`.  
Citation: `docs/jhora/panchanga/drik.py:133`, `docs/jhora/panchanga/drik.py:135`.
- `SENTHIL` and `SUNDAR_SS` branches compute `_ayanamsa_value` via internal model functions; no `swe.set_sid_mode(...)` call is present inside those two branches.  
Citations: `docs/jhora/panchanga/drik.py:136`, `docs/jhora/panchanga/drik.py:137`, `docs/jhora/panchanga/drik.py:138`, `docs/jhora/panchanga/drik.py:139`.

## 2) House System Coverage

### Full `indian_house_systems` list
Source: `docs/jhora/const.py:630`, `docs/jhora/const.py:631`.

| Method ID | Description in PyJHora |
| --- | --- |
| `1` | `Equal Housing - Lagna in the middle` |
| `2` | `Equal Housing - Lagna as start` |
| `3` | `Sripati method` |
| `4` | `KP Method (aka Placidus Houses method)` |
| `5` | `Each Rasi is the house` |

Default house method constant is `1`.  
Citation: `docs/jhora/const.py:637`.

### Method 5 formula (`Each Rasi is the house`)
- Method 5 branch and label in `_bhaava_madhya_new`.  
Citations: `docs/jhora/horoscope/chart/charts.py:131`, `docs/jhora/horoscope/chart/charts.py:175`.
- Formula used in code:
  - `h1 = (h + ascendant_constellation) % 12`
  - `_bhava_start = h1 * 30`
  - `_bhava_mid = _bhava_start + ascendant_longitude`
  - `_bhava_end = ((h1 + 1) % 12) * 30`  
Citation: `docs/jhora/horoscope/chart/charts.py:177`, `docs/jhora/horoscope/chart/charts.py:178`.
- Return tuple schema is `(house_start, house_cusp, house_end)`.  
Citations: `docs/jhora/horoscope/chart/charts.py:123`, `docs/jhora/horoscope/chart/charts.py:136`.
- Method 5 appends `(_bhava_start, _bhava_mid, _bhava_end)`, so the cusp field is `_bhava_mid` for method 5.  
Citation: `docs/jhora/horoscope/chart/charts.py:179`.

## 3) Node Mode Coverage

- Rahu/Ketu constants are tied to mean node:
  - `_RAHU = swe.MEAN_NODE`
  - `_KETU = -swe.MEAN_NODE`  
Citation: `docs/jhora/const.py:53`, `docs/jhora/const.py:54`.
- PyJHora planet lists include Rahu/Ketu and comment Rahu as mean node.  
Citations: `docs/jhora/panchanga/drik.py:42`, `docs/jhora/panchanga/drik.py:43`, `docs/jhora/panchanga/drik.py:44`, `docs/jhora/panchanga/drik.py:45`.
- Ketu opposite rule is explicit: `ketu = lambda rahu: (rahu + 180) % 360`.  
Citation: `docs/jhora/panchanga/drik.py:153`, `docs/jhora/panchanga/drik.py:155`.

## 4) Other SwissEph Mode/Flag Mappings (Repo-local, explicit)

- Global ephemeris path setup: `swe.set_ephe_path(_ephe_path)`.  
Citation: `docs/jhora/const.py:174`, `docs/jhora/const.py:175`.
- Panchanga rise flags: `_rise_flags = swe.BIT_HINDU_RISING | swe.FLG_TRUEPOS | swe.FLG_SPEED`.  
Citation: `docs/jhora/panchanga/drik.py:52`.
- Sidereal longitude flags:
  - tropical path: `flags = swe.FLG_SWIEPH` when `_TROPICAL_MODE` is true
  - sidereal path: `flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | _rise_flags`  
Citations: `docs/jhora/const.py:166`, `docs/jhora/panchanga/drik.py:220`, `docs/jhora/panchanga/drik.py:221`, `docs/jhora/panchanga/drik.py:223`.
- House method 4 / western codes are routed to SwissEph house calculation:
  - western code map (`P`, `K`, `O`, `R`, `C`, `A`, `V`, `X`, `H`, `T`, `B`, `M`)
  - method branch calls `drik.bhaava_madhya_swe(jd, place, house_code=bhava_madhya_method)` for western codes  
Citations: `docs/jhora/const.py:632`, `docs/jhora/const.py:633`, `docs/jhora/const.py:634`, `docs/jhora/horoscope/chart/charts.py:166`, `docs/jhora/horoscope/chart/charts.py:167`.

## Unknown/Not found in repo-local PyJHora

- No additional item.
