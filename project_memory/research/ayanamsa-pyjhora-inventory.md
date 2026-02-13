# Ayanamsa Inventory From PyJHora
Date: 2026-02-13
Source repo scanned: `D:\lab\Pyjhora\src\jhora\`

## Scope and method
- Primary source-of-truth mapping: `D:\lab\Pyjhora\src\jhora\const.py:182`
- Default mode: `D:\lab\Pyjhora\src\jhora\const.py:194`
- Runtime setter (active path): `D:\lab\Pyjhora\src\jhora\panchanga\drik.py:117`
- Legacy/experimental parallel setter: `D:\lab\Pyjhora\src\jhora\panchanga\drik1.py:236`
- Name normalization is case-insensitive via `upper()`: `D:\lab\Pyjhora\src\jhora\panchanga\drik.py:130-133`, `D:\lab\Pyjhora\src\jhora\panchanga\drik1.py:245-248`

## Complete inventory (supported keys in mapping)

| PyJHora key/name | Internal id/value | SwissEph constant mapping | Source ref | Notes |
|---|---|---|---|---|
| `FAGAN` | `const.available_ayanamsa_modes['FAGAN']` | `swe.SIDM_FAGAN_BRADLEY` | `D:\lab\Pyjhora\src\jhora\const.py:182` | Standard Swiss sidereal mode |
| `KP` | `...['KP']` | `swe.SIDM_KRISHNAMURTI` | `D:\lab\Pyjhora\src\jhora\const.py:182` | Standard Swiss sidereal mode |
| `LAHIRI` | `...['LAHIRI']` | `swe.SIDM_LAHIRI` | `D:\lab\Pyjhora\src\jhora\const.py:182` | Default mode (`_DEFAULT_AYANAMSA_MODE`) |
| `RAMAN` | `...['RAMAN']` | `swe.SIDM_RAMAN` | `D:\lab\Pyjhora\src\jhora\const.py:183` | Standard Swiss sidereal mode |
| `USHASHASHI` | `...['USHASHASHI']` | `swe.SIDM_USHASHASHI` | `D:\lab\Pyjhora\src\jhora\const.py:183` | Standard Swiss sidereal mode |
| `YUKTESHWAR` | `...['YUKTESHWAR']` | `swe.SIDM_YUKTESHWAR` | `D:\lab\Pyjhora\src\jhora\const.py:184` | Standard Swiss sidereal mode |
| `SURYASIDDHANTA` | `...['SURYASIDDHANTA']` | `swe.SIDM_SURYASIDDHANTA` | `D:\lab\Pyjhora\src\jhora\const.py:184` | Standard Swiss sidereal mode |
| `SURYASIDDHANTA_MSUN` | `...['SURYASIDDHANTA_MSUN']` | `swe.SIDM_SURYASIDDHANTA_MSUN` | `D:\lab\Pyjhora\src\jhora\const.py:185` | Standard Swiss sidereal mode |
| `ARYABHATA` | `...['ARYABHATA']` | `swe.SIDM_ARYABHATA` | `D:\lab\Pyjhora\src\jhora\const.py:185` | Standard Swiss sidereal mode |
| `ARYABHATA_MSUN` | `...['ARYABHATA_MSUN']` | `swe.SIDM_ARYABHATA_MSUN` | `D:\lab\Pyjhora\src\jhora\const.py:186` | Standard Swiss sidereal mode |
| `SS_CITRA` | `...['SS_CITRA']` | `swe.SIDM_SS_CITRA` | `D:\lab\Pyjhora\src\jhora\const.py:186` | Standard Swiss sidereal mode |
| `TRUE_CITRA` | `...['TRUE_CITRA']` | `swe.SIDM_TRUE_CITRA` | `D:\lab\Pyjhora\src\jhora\const.py:187` | Standard Swiss sidereal mode |
| `TRUE_REVATI` | `...['TRUE_REVATI']` | `swe.SIDM_TRUE_REVATI` | `D:\lab\Pyjhora\src\jhora\const.py:187` | Standard Swiss sidereal mode |
| `SS_REVATI` | `...['SS_REVATI']` | `swe.SIDM_SS_REVATI` | `D:\lab\Pyjhora\src\jhora\const.py:188` | Standard Swiss sidereal mode |
| `SENTHIL` | `...['SENTHIL'] == ''` | No direct `SIDM_*` mapping in dict | `D:\lab\Pyjhora\src\jhora\const.py:188` | Computed/custom model; see logic refs (`drik.py:136`, `drik.py:86`) |
| `TRUE_LAHIRI` | `...['TRUE_LAHIRI']` | `swe.SIDM_TRUE_CITRA` | `D:\lab\Pyjhora\src\jhora\const.py:188` | Alias-like mapping to `TRUE_CITRA` constant |
| `TRUE_PUSHYA` | `...['TRUE_PUSHYA']` | `swe.SIDM_TRUE_PUSHYA` | `D:\lab\Pyjhora\src\jhora\const.py:189` | Standard Swiss sidereal mode |
| `TRUE_MULA` | `...['TRUE_MULA']` | `swe.SIDM_TRUE_MULA` | `D:\lab\Pyjhora\src\jhora\const.py:189` | Standard Swiss sidereal mode |
| `KP-SENTHIL` | `...['KP-SENTHIL']` | `swe.SIDM_KRISHNAMURTI_VP291` | `D:\lab\Pyjhora\src\jhora\const.py:190` | Hybrid-labeled key mapped directly to Swiss constant |
| `SIDM_USER` | `...['SIDM_USER']` | `swe.SIDM_USER` | `D:\lab\Pyjhora\src\jhora\const.py:191` | Caller must pass user value (`drik.py:124`, `drik.py:133-135`) |
| `SUNDAR_SS` | `...['SUNDAR_SS'] == ''` | No direct `SIDM_*` mapping in dict | `D:\lab\Pyjhora\src\jhora\const.py:191` | Computed/custom model; see logic refs (`drik.py:138`, `drik.py:65`) |

## Additional custom/experimental ayanamsa-related constructs (not in the mapping table)
- `revati_359_50` sets `SIDM_USER` with fixed value:
  - `D:\lab\Pyjhora\src\jhora\panchanga\drik1.py:47`
- `galc_cent_mid_mula` sets `SIDM_USER` with fixed value:
  - `D:\lab\Pyjhora\src\jhora\panchanga\drik1.py:48`
- Fixed-star helper `_function(point)` sets user sid mode and evaluates Citra offset:
  - `D:\lab\Pyjhora\src\jhora\utils.py:602-610`
- Commented-out candidate (not active support):
  - `"ARYABHATA_522"` in `D:\lab\Pyjhora\src\jhora\const.py:192`

## Inventory total and proof notes
- Total keys in active `available_ayanamsa_modes` mapping: **21** (lines `182-192`).
- Two keys are computed/custom placeholders in mapping (`SENTHIL`, `SUNDAR_SS`) and do not store a Swiss constant in dict.
- Inventory coverage proof links:
  - Search for definitions/mapping: `available_ayanamsa_modes`, `SIDM_`.
  - Runtime setter path: `set_ayanamsa_mode` in `drik.py` and `drik1.py`.

## Strict Recheck Addendum (missed items patched)
- Correct current mapping refs in this code snapshot:
  - `available_ayanamsa_modes`: `D:\lab\Pyjhora\src\jhora\const.py:190`
  - `_DEFAULT_AYANAMSA_MODE`: `D:\lab\Pyjhora\src\jhora\const.py:202`
- Consumer-level UI filtering (not new modes, but affects effective availability):
  - `D:\lab\Pyjhora\src\jhora\ui\panchangam.py:39` excludes `SENTHIL`, `SIDM_USER` (keeps `SUNDAR_SS`).
  - `D:\lab\Pyjhora\src\jhora\ui\horo_chart_tabs.py:58` and `D:\lab\Pyjhora\src\jhora\ui\test1.py:38` exclude `SENTHIL`, `SIDM_USER`, `SUNDAR_SS`.
- User-facing ayanamsa display path (inventory consumer):
  - `D:\lab\Pyjhora\src\jhora\panchanga\info.py:263-264` shows mode label and value via `drik.get_ayanamsa_value`.
- Test evidence for completeness of mode list:
  - `D:\lab\Pyjhora\src\jhora\tests\pvr_tests.py:5508-5528` iterates all keys and validates expected values including `KP-SENTHIL`, `SUNDAR_SS`, `SIDM_USER`.

## Exception Table (Diba Runtime Policy)

| key | runtime status in Diba | reason |
|---|---|---|
| `sidm_user` | disabled | Canonical runtime blocks manual numeric injection (`reason_code=disabled`) |
| `senthil` | recognized_not_implemented | Non-SIDM computed path not enabled in canonical runtime |
| `sundar_ss` | recognized_not_implemented | Non-SIDM computed path not enabled in canonical runtime |
