# ephemeris_engine_contracts

- status: active
- minors:
  - [core_ephemeris_engine_contract](./core_ephemeris_engine_contract/guru.md)
  - [edge_cases_and_risks](./edge_cases_and_risks/guru.md)
  - [ephemeris_behavior_contract_map.core.md](./ephemeris_behavior_contract_map.core.md)
- observed PyJHora behaviors:
  - SwissEph flags are assembled per mode and callsite.
  - `swe.calc_ut`, `swe.rise_trans`, and `swe.houses_ex` are direct integration points.
  - Ephemeris data path is set at import in `const.py`.
  - Core-7 ephemeris callsite inventory is tracked in `_coverage_ephemeris_callsites_core.tsv`.
- inventory summary:
  - callsite rows: `66`
  - unique `(file,function_context)`: `41`
  - residual callsites (`EP900`): `25`
  - `swe.version`: `not_found` (recorded as evidence-of-absence)
- cross-cutting map:
  - [sweep_2_architecture_coupling_contract_map.md](../../sweep_2_architecture_coupling_contract_map.md)
