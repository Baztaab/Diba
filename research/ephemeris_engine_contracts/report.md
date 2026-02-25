# ephemeris_engine_contracts

- status: active
- minors:
  - [core_ephemeris_engine_contract](./core_ephemeris_engine_contract/guru.md)
  - [edge_cases_and_risks](./edge_cases_and_risks/guru.md)
- observed PyJHora behaviors:
  - SwissEph flags are assembled per mode and callsite.
  - `swe.calc_ut`, `swe.rise_trans`, and `swe.houses_ex` are direct integration points.
  - Ephemeris data path is set at import in `const.py`.
- cross-cutting map:
  - [sweep_2_architecture_coupling_contract_map.md](../../sweep_2_architecture_coupling_contract_map.md)
