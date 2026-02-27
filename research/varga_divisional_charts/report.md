# varga_divisional_charts

- status: active
- minors:
  - [core_varga_engine](./core_varga_engine/guru.md)
  - [chart_method_matrix](./chart_method_matrix/guru.md)
  - [custom_and_mixed_charts_dn_dmx_dn](./custom_and_mixed_charts_dn_dmx_dn/guru.md)
  - [varga_special_derivations](./varga_special_derivations/guru.md)
  - [varga_transit_entry_dates](./varga_transit_entry_dates/guru.md)
- codepack:
  - `./_codepack/src/...`
  - `./_codepack/MANIFEST.tsv`
- engine-plus-consumers extraction:
  - [varga_behavior_contract_map.engine_plus_consumers.md](./varga_behavior_contract_map.engine_plus_consumers.md)
  - [`_coverage_varga_callsites_engine_plus_consumers.tsv`](./_coverage_varga_callsites_engine_plus_consumers.tsv)
  - [`_coverage_varga_method_matrix.tsv`](./_coverage_varga_method_matrix.tsv)
- observed PyJHora behaviors:
  - Standard Dn functions are mapped through `divisional_chart_functions`.
  - `divisional_positions_from_rasi_positions` dispatches standard Dn handlers or `custom_divisional_chart`.
  - `custom_divisional_chart` supports cyclic and non-cyclic paths with `chart_method` and base controls.
  - Mixed charts compose two varga stages through `mixed_chart` or `mixed_chart_from_rasi_positions`.
  - Divisional and mixed entry-date utilities step and refine by `utils.inverse_lagrange`.
- cross-cutting map:
  - [sweep_2_architecture_coupling_contract_map.md](../../sweep_2_architecture_coupling_contract_map.md)

## Inventory summary

- count of varga functions found: `63`
- count of chart_method-bearing functions: `149`
- count of codepack files: `63`
- count of focused anchors in map: `29` (`VG01..VG28` + `VG900`)
- count of residual rows in coverage TSV: `2714`
