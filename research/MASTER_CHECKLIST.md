# MASTER_CHECKLIST.md

## Audit Basis

- source_of_truth: `D:\lab\Pyjhora\src\jhora`
- locked_file_backed_majors: `8`
- legacy_prelock_majors: `5`
- core_files_audited: `91`
- core_files_covered_by_manifest: `74`
- core_files_pending: `17`

## Locked File-Backed Majors

- `ashtakavarga_system`
- `dhasa_systems_and_cycle_year_length_logic`
- `graha_longitudes_and_states`
- `longevity_and_ayurdaya`
- `panchanga_components`
- `transit_and_tajaka`
- `varga_divisional_charts`
- `yogas_and_doshas`

## Legacy / Pre-Lock Research Areas

- `chakras_and_specialized_systems`
- `ephemeris_engine_contracts`
- `kala_time`
- `lagna_and_bhava_houses`
- `sidereal_state`

## Covered And Locked Domains

- `panchanga core components` -> `panchanga_components` [LOCKED]
- `ephemeris engine` -> `ephemeris_engine_contracts` [LEGACY]
- `graha longitudes and graha states` -> `graha_longitudes_and_states` [LOCKED]
- `lagna and bhava houses` -> `lagna_and_bhava_houses` [LEGACY]
- `varga divisional charts` -> `varga_divisional_charts` [LOCKED]
- `dhasa systems and cycle-year logic` -> `dhasa_systems_and_cycle_year_length_logic` [LOCKED]
- `longevity and ayurdaya` -> `longevity_and_ayurdaya` [LOCKED]
- `ashtakavarga system` -> `ashtakavarga_system` [LOCKED]
- `transit and tajaka` -> `transit_and_tajaka` [LOCKED]
- `yogas and doshas` -> `yogas_and_doshas` [LOCKED]

## Pending Core Domains

- `horoscope/README.md`: `1` pending files
- `horoscope/__init__.py`: `1` pending files
- `horoscope/chart`: `2` pending files
- `horoscope/dhasa`: `1` pending files
- `horoscope/match`: `3` pending files
- `horoscope/prediction`: `1` pending files
- `horoscope/transit`: `1` pending files
- `panchanga/root`: `3` pending files
- `src/jhora`: `4` pending files

## High-Priority Pending Files

- `src/jhora/horoscope/match/compatibility.py`
- `src/jhora/horoscope/match/README.md`

## Pending File Inventory

- `src/jhora/__init__.py`
- `src/jhora/_package_info.py`
- `src/jhora/horoscope/__init__.py`
- `src/jhora/horoscope/chart/__init__.py`
- `src/jhora/horoscope/chart/README.md`
- `src/jhora/horoscope/dhasa/README.md`
- `src/jhora/horoscope/match/__init__.py`
- `src/jhora/horoscope/match/compatibility.py`
- `src/jhora/horoscope/match/README.md`
- `src/jhora/horoscope/prediction/README.md`
- `src/jhora/horoscope/README.md`
- `src/jhora/horoscope/transit/README.md`
- `src/jhora/panchanga/__init__.py`
- `src/jhora/panchanga/khanda_khaadyaka.py`
- `src/jhora/panchanga/README.md`
- `src/jhora/README.md`
- `src/jhora/README_Package_Structure.md`

## README Coverage Status

- `src/jhora/horoscope/chart/README.md` -> `PENDING`; majors=`none`
- `src/jhora/horoscope/dhasa/README.md` -> `PENDING`; majors=`none`
- `src/jhora/horoscope/match/README.md` -> `PENDING`; majors=`none`
- `src/jhora/horoscope/prediction/README.md` -> `PENDING`; majors=`none`
- `src/jhora/horoscope/README.md` -> `PENDING`; majors=`none`
- `src/jhora/horoscope/transit/README.md` -> `PENDING`; majors=`none`
- `src/jhora/panchanga/README.md` -> `PENDING`; majors=`none`
- `src/jhora/README.md` -> `PENDING`; majors=`none`
- `src/jhora/README_Package_Structure.md` -> `PENDING`; majors=`none`

## Findings

- `horoscope/match/compatibility.py` is a full standalone engine and remains pending.
- `horoscope/chart/arudhas.py` and `horoscope/chart/sphuta.py` are already file-covered inside `varga_divisional_charts`; they are not pending in the file-backed audit, but they may still deserve a future special-points re-cut if you want a standalone major.
- Eclipse and grahana logic exists in `panchanga/drik.py`; the file itself is manifest-covered today, but the eclipse phenomenon is not isolated as its own dedicated major.
- Several `README.md` files under `horoscope`, `chart`, `dhasa`, `match`, `prediction`, `transit`, and `panchanga` are still outside manifest-backed coverage.
- `__init__.py` files are intentionally visible in this audit; they are low-risk but still pending unless copied into a major codepack.

## Recommended Next Sequence

- `match_and_compatibility`
- `eclipses_and_grahana`
- optional `special_points_and_sphuta` re-cut if you want standalone isolation instead of coverage-through-varga
- optional final pass for package `README.md` and `__init__.py` closure
