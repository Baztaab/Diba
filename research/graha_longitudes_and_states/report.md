# graha_longitudes_and_states

- status: active
- minors:
  - [core_graha_longitudes_and_states_contract](./core_graha_longitudes_and_states_contract/guru.md)
  - [edge_cases_and_risks](./edge_cases_and_risks/guru.md)
- observed PyJHora behaviors:
  - Rahu and Ketu are represented via `swe.MEAN_NODE` and `-swe.MEAN_NODE` constants.
  - Planet speed path uses `swe.calc_ut` vector with fixed rounding factors.
  - Retrograde checks use `longi[3]` sign from `swe.calc_ut` output.
- cross-cutting map:
  - [sweep_2_architecture_coupling_contract_map.md](../../sweep_2_architecture_coupling_contract_map.md)
