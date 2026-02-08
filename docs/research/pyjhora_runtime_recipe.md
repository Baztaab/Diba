# PyJHora Runtime Recipe (Repo-Local Evidence)

Scope: evidence only from `docs/jhora/` in this repository.

## A) Time/JD Policy

- Core place contract includes timezone in hours: `Place = struct(..., timezone)`. Source: `docs/jhora/panchanga/drik.py:41`.
- PyJHora commonly accepts `jd` as local-JD and converts to UTC-JD before SwissEph calls via `jd_utc = jd - place.timezone / 24.`. Sources: `docs/jhora/panchanga/drik.py:241`, `docs/jhora/panchanga/drik.py:274`, `docs/jhora/panchanga/drik.py:1429`, `docs/jhora/panchanga/drik.py:1477`.
- `sidereal_longitude` explicitly documents UTC-JD requirement and conversion rule `JD_UTC = JD - timezone_hours`. Source: `docs/jhora/panchanga/drik.py:212`, `docs/jhora/panchanga/drik.py:214`, `docs/jhora/panchanga/drik.py:215`.
- Ephemeris path is set globally at import-time in constants: `swe.set_ephe_path(_ephe_path)`. Sources: `docs/jhora/const.py:174`, `docs/jhora/const.py:175`.
- No `swe.set_topo(...)` usage was found in `docs/jhora/panchanga/drik.py` (repo-local search result).

## B) Ayanamsa Policy

- Ayanamsa mode table is defined in `available_ayanamsa_modes` and maps IDs to `swe.SIDM_*` constants. Sources: `docs/jhora/const.py:190`, `docs/jhora/const.py:196`, `docs/jhora/const.py:199`.
- Default ayanamsa mode is `LAHIRI`. Source: `docs/jhora/const.py:202`.
- `set_ayanamsa_mode(...)` behavior:
- Regular mapped IDs: `swe.set_sid_mode(const.available_ayanamsa_modes[key])`. Source: `docs/jhora/panchanga/drik.py:141`.
- `SIDM_USER`: `swe.set_sid_mode(swe.SIDM_USER, ayanamsa_value)`. Sources: `docs/jhora/panchanga/drik.py:133`, `docs/jhora/panchanga/drik.py:135`.
- `SENTHIL` and `SUNDAR_SS`: computed ayanamsa value path, no direct `set_sid_mode(...)` in those branches. Sources: `docs/jhora/panchanga/drik.py:136`, `docs/jhora/panchanga/drik.py:137`, `docs/jhora/panchanga/drik.py:138`, `docs/jhora/panchanga/drik.py:139`.
- Reset policy uses `reset_ayanamsa_mode`: restores configured mode, with fallback to Lahiri for user/computed branches. Sources: `docs/jhora/panchanga/drik.py:148`, `docs/jhora/panchanga/drik.py:149`, `docs/jhora/panchanga/drik.py:150`.
- Important alias in mapping: `TRUE_LAHIRI -> swe.SIDM_TRUE_CITRA`. Source: `docs/jhora/const.py:196`.

## C) Zodiac Mode and Planet/Asc/Node Paths

- Tropical/sidereal switch is controlled by `_TROPICAL_MODE` (default `False`). Source: `docs/jhora/const.py:166`.
- Sidereal planet longitude path (`sidereal_longitude`):
- Sidereal flags = `swe.FLG_SWIEPH | swe.FLG_SIDEREAL | _rise_flags`. Source: `docs/jhora/panchanga/drik.py:223`.
- `_rise_flags = swe.BIT_HINDU_RISING | swe.FLG_TRUEPOS | swe.FLG_SPEED`. Source: `docs/jhora/panchanga/drik.py:52`.
- Planet computation uses `swe.calc_ut(jd_utc, planet, flags=flags)` after `set_ayanamsa_mode(...)`, then `reset_ayanamsa_mode()`. Sources: `docs/jhora/panchanga/drik.py:225`, `docs/jhora/panchanga/drik.py:228`, `docs/jhora/panchanga/drik.py:229`.
- Ascendant path (`ascendant`): uses `swe.houses_ex(jd_utc, lat, lon, flags=swe.FLG_SIDEREAL)` in sidereal mode after `set_ayanamsa_mode(...)`, then reset. Sources: `docs/jhora/panchanga/drik.py:1481`, `docs/jhora/panchanga/drik.py:1482`, `docs/jhora/panchanga/drik.py:1483`, `docs/jhora/panchanga/drik.py:1487`.
- KP/western house cusps path also uses `swe.houses_ex(...)` with sidereal flags in sidereal mode. Sources: `docs/jhora/panchanga/drik.py:1433`, `docs/jhora/panchanga/drik.py:1434`, `docs/jhora/panchanga/drik.py:1435`, `docs/jhora/panchanga/drik.py:1447`, `docs/jhora/panchanga/drik.py:1448`, `docs/jhora/panchanga/drik.py:1449`.

## D) House System Policy (1..5)

- Canonical list (`indian_house_systems`):
- 1: Equal Housing - Lagna in the middle
- 2: Equal Housing - Lagna as start
- 3: Sripati method
- 4: KP Method (Placidus)
- 5: Each Rasi is the house
Sources: `docs/jhora/const.py:630`, `docs/jhora/const.py:631`.

- Method formulas in `_bhaava_madhya_new`:
- Method 1: start=`mid-15`, cusp=`mid`, end=`mid+15`; then advance by 30 deg. Sources: `docs/jhora/panchanga/drik.py:1355`, `docs/jhora/panchanga/drik.py:1358`, `docs/jhora/panchanga/drik.py:1360`.
- Method 2: start=`mid`, cusp=`start+15`, end=`cusp+15`; then advance start by 30 deg. Sources: `docs/jhora/panchanga/drik.py:1362`, `docs/jhora/panchanga/drik.py:1365`, `docs/jhora/panchanga/drik.py:1367`.
- Method 3: uses `bhaava_madhya_sripathi`; triplets built from consecutive sripati boundaries. Sources: `docs/jhora/panchanga/drik.py:1369`, `docs/jhora/panchanga/drik.py:1370`, `docs/jhora/panchanga/drik.py:1372`.
- Method 4: uses KP (`bhaava_madhya_kp`) / western house code (`bhaava_madhya_swe`) and midpoint interpolation. Sources: `docs/jhora/panchanga/drik.py:1375`, `docs/jhora/panchanga/drik.py:1376`, `docs/jhora/panchanga/drik.py:1381`.
- Method 5: per-sign house, `h1=(h+asc_sign)%12`, start=`h1*30`, cusp=`start+asc_longitude`, end=`(h1+1)*30`. Sources: `docs/jhora/panchanga/drik.py:1384`, `docs/jhora/panchanga/drik.py:1387`.

## E) Node Policy

- PyJHora constants define Rahu/Ketu from mean node: `_RAHU = swe.MEAN_NODE`, `_KETU = -swe.MEAN_NODE`. Sources: `docs/jhora/const.py:54`, `docs/jhora/const.py:53`.
- Planet lists annotate Rahu/Ketu with mean node usage. Sources: `docs/jhora/panchanga/drik.py:43`, `docs/jhora/panchanga/drik.py:45`.
- Ketu is explicitly opposite Rahu: `ketu = lambda rahu: (rahu + 180) % 360`. Source: `docs/jhora/panchanga/drik.py:155`.
- Repo-local `drik.py` does not show explicit `swe.TRUE_NODE` usage in the node constant setup path.
- Repo-local `drik.py` does not show explicit `swe.FLG_NONUT` in the standard sidereal node pipeline.

## Call Order (PyJHora-style, from source)

1. Prepare JD in UTC (`jd_utc`) from local JD/timezone convention. Sources: `docs/jhora/panchanga/drik.py:214`, `docs/jhora/panchanga/drik.py:241`.
2. Set ayanamsa mode (`set_ayanamsa_mode`). Sources: `docs/jhora/panchanga/drik.py:117`, `docs/jhora/panchanga/drik.py:141`.
3. Execute SwissEph calls (`calc_ut` / `houses_ex`) with sidereal/tropical flags. Sources: `docs/jhora/panchanga/drik.py:223`, `docs/jhora/panchanga/drik.py:228`, `docs/jhora/panchanga/drik.py:1483`.
4. Reset sidereal mode (`reset_ayanamsa_mode`) after call path. Sources: `docs/jhora/panchanga/drik.py:148`, `docs/jhora/panchanga/drik.py:229`, `docs/jhora/panchanga/drik.py:1487`.
