# D04 varga dispatch and composition

## Scope

- NON_BINDING: This pack covers dispatch/composition policy for Dn, custom Dn (`1..300`), and mixed chart (`Dm x Dn`) flows in the VARGA boundary.

## Facts

- FACT: Standard varga routing is keyed by `divisional_chart_functions` in chart engine orchestration. [Source: `research/varga_divisional_charts/core_varga_engine/guru.md -> src/jhora/horoscope/chart/charts.py:L44-L51`]
- FACT: `divisional_positions_from_rasi_positions` routes either to standard handlers or `custom_divisional_chart` under `MAX_DHASAVARGA_FACTOR`. [Source: `research/varga_divisional_charts/core_varga_engine/guru.md -> src/jhora/horoscope/chart/charts.py:L1066-L1077`; Source: `research/varga_divisional_charts/core_varga_engine/guru.md -> src/jhora/const.py:L726-L730`]
- FACT: `MAX_DHASAVARGA_FACTOR` is set to `300`, enabling custom Dn range beyond predefined handlers. [Source: `research/varga_divisional_charts/core_varga_engine/guru.md -> src/jhora/const.py:L726-L730`]
- FACT: `custom_divisional_chart` supports cyclic and non-cyclic paths and calls `utils.__varga_non_cyclic(...)` when custom base/sign variation controls are present. [Source: `research/varga_divisional_charts/custom_and_mixed_charts_dn_dmx_dn/guru.md -> src/jhora/horoscope/chart/charts.py:L1012-L1021`; Source: `research/varga_divisional_charts/custom_and_mixed_charts_dn_dmx_dn/guru.md -> src/jhora/horoscope/chart/charts.py:L1043-L1054`; Source: `research/varga_divisional_charts/custom_and_mixed_charts_dn_dmx_dn/guru.md -> src/jhora/utils.py:L956-L977`]
- FACT: Mixed composition is implemented by two-stage chaining via `mixed_chart` and `mixed_chart_from_rasi_positions`, each applying chart method per stage. [Source: `research/varga_divisional_charts/custom_and_mixed_charts_dn_dmx_dn/guru.md -> src/jhora/horoscope/chart/charts.py:L1055-L1065`]
- FACT: Chart-method behavior is distributed across many varga functions, with observed method sets varying per function and custom path supporting broader ranges including `0..9`. [Source: `research/varga_divisional_charts/chart_method_matrix/guru.md -> src/jhora/horoscope/chart/charts.py:L292-L995`; Source: `research/varga_divisional_charts/chart_method_matrix/guru.md -> src/jhora/horoscope/chart/charts.py:L1043-L1054`]
- FACT: Transit entry and conjunction utilities consume divisional and mixed chart outputs repeatedly under step/refine loops (`inverse_lagrange`), so dispatch/composition behavior affects transit coupling outputs. [Source: `research/varga_divisional_charts/varga_transit_entry_dates/guru.md -> src/jhora/horoscope/chart/charts.py:L2033-L2121`; Source: `research/varga_divisional_charts/varga_transit_entry_dates/guru.md -> src/jhora/horoscope/chart/charts.py:L2149-L2198`; Source: `research/varga_divisional_charts/varga_transit_entry_dates/guru.md -> src/jhora/utils.py:L631-L639`]
- FACT: `rasi_chart` orchestration in Sweep2 includes dhasavarga packaging, tying varga dispatch to natal pipeline assembly. [E14]
- FACT: Varga codepack manifest records snapshot-pinned source files and hashes used for reproduction of varga behavior study. [Source: `research/varga_divisional_charts/_codepack/MANIFEST.tsv`]

## Options

- Option A (NON_BINDING): Single dispatcher function plus explicit method registry keyed by `divisional_chart_factor` and method id.
- Option B (NON_BINDING): Table-driven method matrix as first-class runtime artifact, separating dispatch metadata from algorithm code.
- Option C (NON_BINDING): Plugin-based varga strategy interfaces (standard/custom/mixed) with bounded composition contracts.
- Option D (NON_BINDING): Two-stage composition orchestrator as explicit primitive (`stage1`, `stage2`) reused by both mixed and transit-coupling flows.
- Option E (NON_BINDING): Compatibility-layer approach that preserves existing branching and adds normalization/adaptation wrappers only.

## Pros and cons

- Option A
  - Pros: central routing logic; easier traceability for parity runs.
  - Cons: registry completeness and method-id validation become critical maintenance points.
- Option B
  - Pros: visible coverage map of factor/method combinations; easier gap detection.
  - Cons: potential drift between matrix metadata and underlying implementation functions.
- Option C
  - Pros: modular extension surface for new Dn families and experimental variants.
  - Cons: interface overhead and stricter contract conformance requirements across strategies.
- Option D
  - Pros: composition semantics become explicit and reusable in transit utilities.
  - Cons: adds orchestration layer that may duplicate legacy control flow paths.
- Option E
  - Pros: lowest migration friction for existing code paths and parity harness reuse.
  - Cons: preserves distributed branching complexity and may limit structural simplification.

## Impact map

- VARGA boundary contract and chart-method exposure in blueprint `VargaContract`. [Source: `architecture/core_computation_blueprint.v0.md`]
- Natal core pipeline where `rasi_chart` packages varga-related outputs. [E14]
- Transit-coupling utilities that depend on repeated divisional/mixed evaluations. [Source: `research/varga_divisional_charts/varga_transit_entry_dates/guru.md -> src/jhora/horoscope/chart/charts.py:L2033-L2121`; Source: `research/varga_divisional_charts/varga_transit_entry_dates/guru.md -> src/jhora/horoscope/chart/charts.py:L2149-L2198`]
- Varga special derivation flows that call divisional and mixed paths. [Source: `research/varga_divisional_charts/varga_special_derivations/guru.md -> src/jhora/horoscope/chart/charts.py:L1800-L1868`]
- Evidence reproducibility path anchored by varga codepack manifest. [Source: `research/varga_divisional_charts/_codepack/MANIFEST.tsv`]

## Validation plan

- Probe 1: Coverage probe for factor/method combinations against observed chart-method matrix entries, including pass-through and custom ranges. [Source: `research/varga_divisional_charts/chart_method_matrix/guru.md`]
- Probe 2: Parity probe for standard Dn dispatch paths versus custom Dn paths for overlapping factors where applicable. [Source: `research/varga_divisional_charts/core_varga_engine/guru.md -> src/jhora/horoscope/chart/charts.py:L1066-L1077`; Source: `research/varga_divisional_charts/custom_and_mixed_charts_dn_dmx_dn/guru.md -> src/jhora/horoscope/chart/charts.py:L1012-L1054`]
- Probe 3: Composition probe for `mixed_chart` and `mixed_chart_from_rasi_positions` stage ordering and stage-method effects. [Source: `research/varga_divisional_charts/custom_and_mixed_charts_dn_dmx_dn/guru.md -> src/jhora/horoscope/chart/charts.py:L1055-L1065`]
- Probe 4: Transit-coupling regression probe using divisional/mixed entry-date and conjunction search paths under fixed stepping and refinement parameters. [Source: `research/varga_divisional_charts/varga_transit_entry_dates/guru.md -> src/jhora/horoscope/chart/charts.py:L2033-L2198`; Source: `research/varga_divisional_charts/varga_transit_entry_dates/guru.md -> src/jhora/utils.py:L631-L639`]
- Probe 5: Snapshot reproducibility check using `_codepack/MANIFEST.tsv` hashes for files participating in selected parity runs. [Source: `research/varga_divisional_charts/_codepack/MANIFEST.tsv`]

## Open questions

- OPEN_QUESTION: Which method-id normalization rules are required across functions with disjoint chart_method domains?
- OPEN_QUESTION: Should mixed composition enforce explicit stage contracts (`input/output` shape and method constraints) at runtime boundaries?
- OPEN_QUESTION: How should custom non-cyclic controls (`base_rasi`, `count_from_end_of_sign`, variation) be surfaced in shared contracts without hiding defaults?
- OPEN_QUESTION: Which varga dispatch metadata should be emitted as provenance to support parity audits and transit-coupling replay?

