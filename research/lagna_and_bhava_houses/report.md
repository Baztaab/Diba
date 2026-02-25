# lagna_and_bhava_houses

- status: active
- minors:
  - [core_lagna_and_bhava_houses_contract](./core_lagna_and_bhava_houses_contract/guru.md)
  - [edge_cases_and_risks](./edge_cases_and_risks/guru.md)
- observed PyJHora behaviors:
  - `rasi_chart()` prefixes Lagna at `planet_positions[0]`.
  - `_bhaava_madhya_new()` derives `ascendant_full_longitude` from `planet_positions[0]` and selects KP/SwissEph backend.
  - `bhaava_madhya_swe()` and `bhaava_madhya_kp()` use `swe.houses_ex(...)[0]`.
  - `ascendant()` uses `swe.houses_ex(...)[1][0]` and resets ayanamsa mode before return.
- cross-cutting map:
  - [sweep_2_architecture_coupling_contract_map.md](../../sweep_2_architecture_coupling_contract_map.md)
