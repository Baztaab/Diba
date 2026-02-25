# README_coverage_pyjhora.md

## Source scope

- Local PyJHora source of truth used:
  - `D:\lab\Pyjhora\src\jhora\README.md`
  - `D:\lab\Pyjhora\src\jhora\panchanga\README.md`
- Local root README cross-check (PyPI-facing candidate, if used in packaging):
  - `D:\lab\Pyjhora\README.md` (feature section present, package READMEs marked not fully updated)

## Non-experimental computational capability list with evidence and major mapping

- Capability: Ayanamsa mode control (`set_ayanamsa_mode`) with multiple supported modes.
  - Evidence: `D:\lab\Pyjhora\src\jhora\README.md` L219-L219; `D:\lab\Pyjhora\src\jhora\panchanga\README.md` L4-L4
  - Major mapping: `sidereal_state`
  - Coverage: COVERED

- Capability: Core panchanga calculations (`sunrise/set`, `moonrise/set`, `tithi`, `karana`, `yogam`, `vaara`, `lunar month`, `ritu`, `trikalam`, `durmuhurtham`, `abhijit muhurta`, and related calendar-time elements).
  - Evidence: `D:\lab\Pyjhora\src\jhora\README.md` L219-L219; `D:\lab\Pyjhora\src\jhora\panchanga\README.md` L5-L5
  - Major mapping: `panchanga_core`
  - Coverage: COVERED

- Capability: Sidereal planetary longitude engine and planetary state outputs (declination, speed info, retrograde support).
  - Evidence: `D:\lab\Pyjhora\src\jhora\README.md` L219-L221; `D:\lab\Pyjhora\src\jhora\README.md` L727-L727; `D:\lab\Pyjhora\src\jhora\panchanga\README.md` L6-L6; `D:\lab\Pyjhora\src\jhora\panchanga\README.md` L375-L376
  - Major mapping: `graha_longitudes_and_states`
  - Coverage: COVERED

- Capability: Bhava madhya and ascendant computation.
  - Evidence: `D:\lab\Pyjhora\src\jhora\README.md` L219-L219; `D:\lab\Pyjhora\src\jhora\panchanga\README.md` L6-L6; `D:\lab\Pyjhora\src\jhora\panchanga\README.md` L330-L341
  - Major mapping: `lagna_and_bhava_houses`
  - Coverage: COVERED

- Capability: Divisional/varga planetary positions (`dhasavarga`) and navamsa/divisional chart support.
  - Evidence: `D:\lab\Pyjhora\src\jhora\README.md` L278-L280; `D:\lab\Pyjhora\src\jhora\panchanga\README.md` L6-L6; `D:\lab\Pyjhora\src\jhora\panchanga\README.md` L359-L369
  - Major mapping: `varga_divisional_charts`
  - Coverage: COVERED

- Capability: Rasi/divisional chart orchestration and multiple house system methods (Equal, KP, Sripati, Placidus, Koch, Porphyrius, Regiomontanus, Campanus, Alcabitus, Morinus, and others listed).
  - Evidence: `D:\lab\Pyjhora\src\jhora\README.md` L278-L280; `D:\lab\Pyjhora\src\jhora\README.md` L702-L702
  - Major mapping: `lagna_and_bhava_houses`
  - Coverage: COVERED

- Capability: Upagraha longitude computation (`solar_upagraha_longitudes`, `upagraha_longitude`).
  - Evidence: `D:\lab\Pyjhora\src\jhora\README.md` L219-L219; `D:\lab\Pyjhora\src\jhora\panchanga\README.md` L384-L401
  - Major mapping: `special_lagnas_upagrahas_sphuta_arudha`
  - Coverage: COVERED

- Capability: Special lagna set (`bhava`, `hora`, `ghati`, `vighati`, `pranapada`, `indu`, `kunda`, `bhrigu bindhu`, `sree lagna`).
  - Evidence: `D:\lab\Pyjhora\src\jhora\README.md` L219-L219; `D:\lab\Pyjhora\src\jhora\README.md` L722-L722; `D:\lab\Pyjhora\src\jhora\panchanga\README.md` L428-L433; `D:\lab\Pyjhora\src\jhora\panchanga\README.md` L452-L453; `D:\lab\Pyjhora\src\jhora\panchanga\README.md` L464-L465; `D:\lab\Pyjhora\src\jhora\panchanga\README.md` L476-L477; `D:\lab\Pyjhora\src\jhora\panchanga\README.md` L488-L489; `D:\lab\Pyjhora\src\jhora\panchanga\README.md` L500-L501
  - Major mapping: `special_lagnas_upagrahas_sphuta_arudha`
  - Coverage: COVERED

- Capability: Sankranti and solar date progression (`previous/next sankranti`, `next_solar_date`).
  - Evidence: `D:\lab\Pyjhora\src\jhora\README.md` L219-L219; `D:\lab\Pyjhora\src\jhora\panchanga\README.md` L521-L529; `D:\lab\Pyjhora\src\jhora\panchanga\README.md` L535-L536
  - Major mapping: `kala_time`
  - Coverage: COVERED

- Capability: Solar/lunar eclipse search.
  - Evidence: `D:\lab\Pyjhora\src\jhora\README.md` L219-L219; `D:\lab\Pyjhora\src\jhora\README.md` L752-L752; `D:\lab\Pyjhora\src\jhora\panchanga\README.md` L548-L549; `D:\lab\Pyjhora\src\jhora\panchanga\README.md` L580-L581
  - Major mapping: `transit_gochara_and_varshaphala`
  - Coverage: COVERED

- Capability: Conjunction and transit-style progression (`next_conjunction_of_planet_pair`, `next_planet_entry_date`, `next_planet_retrograde_change_date`).
  - Evidence: `D:\lab\Pyjhora\src\jhora\README.md` L727-L728; `D:\lab\Pyjhora\src\jhora\panchanga\README.md` L612-L613; `D:\lab\Pyjhora\src\jhora\panchanga\README.md` L623-L624; `D:\lab\Pyjhora\src\jhora\panchanga\README.md` L637-L638
  - Major mapping: `transit_gochara_and_varshaphala`
  - Coverage: COVERED

- Capability: Tajaka/varshaphala computational module (`varsha pravesh`, `maasa pravesh`, `sixty_hour`, tajaka aspects and lord calculations).
  - Evidence: `D:\lab\Pyjhora\src\jhora\README.md` L354-L356
  - Major mapping: `transit_gochara_and_varshaphala`
  - Coverage: COVERED

- Capability: Saham computation module (36 sahams).
  - Evidence: `D:\lab\Pyjhora\src\jhora\README.md` L348-L350
  - Major mapping: `transit_gochara_and_varshaphala`
  - Coverage: COVERED

- Capability: Tajaka yoga module (annual yogams list).
  - Evidence: `D:\lab\Pyjhora\src\jhora\README.md` L351-L353
  - Major mapping: `transit_gochara_and_varshaphala`
  - Coverage: COVERED

- Capability: Vratha/festival calendar computations (`get_festivals_between_the_dates`, `get_festivals_of_the_day`, `get_festival`, `tithi_pravesha`).
  - Evidence: `D:\lab\Pyjhora\src\jhora\README.md` L492-L492; `D:\lab\Pyjhora\src\jhora\README.md` L736-L736; `D:\lab\Pyjhora\src\jhora\README.md` L360-L362
  - Major mapping: `vratha_festivals_calendar`
  - Coverage: COVERED

- Capability: Pancha Pakshi Sastra computation module (`jhora.panchanga.pancha_paksha`).
  - Evidence: `D:\lab\Pyjhora\src\jhora\README.md` L265-L267
  - Major mapping: `chakras_and_specialized_systems`
  - Bucket/minor name: `pancha_pakshi_sastra`
  - Coverage: COVERED

## Explicitly filtered out from this scan

- UI-only capabilities and widgets.
  - Evidence: `D:\lab\Pyjhora\src\jhora\README.md` L87-L213
- Yoga, dosha, strength, compatibility, prediction modules.
  - Evidence: `D:\lab\Pyjhora\src\jhora\README.md` L298-L345
- Items explicitly marked experimental or "do not use".
  - Evidence: `D:\lab\Pyjhora\src\jhora\README.md` L347-L347; `D:\lab\Pyjhora\src\jhora\README.md` L359-L359; `D:\lab\Pyjhora\src\jhora\README.md` L715-L715; `D:\lab\Pyjhora\src\jhora\README.md` L728-L728; `D:\lab\Pyjhora\src\jhora\panchanga\README.md` L7-L7

## Coverage verdict

- Total non-experimental computational capabilities: `16`
- Covered by existing major names: `16`
- Gap count: `0`
