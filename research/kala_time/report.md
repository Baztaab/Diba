# kala_time

- status: active
- minors:
  - [core_kala_time_contract](./core_kala_time_contract/guru.md)
  - [edge_cases_and_risks](./edge_cases_and_risks/guru.md)
- observed PyJHora behaviors:
  - `jd_utc` is derived from local `jd` and timezone offsets at multiple callsites.
  - `sunrise()` computes `jd_utc` from Gregorian date and calls `swe.rise_trans`.
  - `local_time_to_jdut1()` uses `swe.utc_time_zone` and `swe.utc_to_jd(..., 0, ...)`.
  - `_get_tithi()` anchors tithi phase to `sunrise(jd, place)[2]`.
- cross-cutting map:
  - [sweep_2_architecture_coupling_contract_map.md](../../sweep_2_architecture_coupling_contract_map.md)
