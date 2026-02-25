# sidereal_state

- status: active
- minors:
  - [core_sidereal_state_contract](./core_sidereal_state_contract/guru.md)
  - [edge_cases_and_risks](./edge_cases_and_risks/guru.md)
- observed PyJHora behaviors:
  - `set_ayanamsa_mode()` calls `swe.set_sid_mode(...)` and mutates `const._DEFAULT_AYANAMSA_MODE`.
  - README test baseline references `const._DEFAULT_AYANAMSA_MODE='LAHIRI'`.
  - Callsites use both one-argument and three-argument `set_ayanamsa_mode(...)` forms.
  - Reset usage appears in some functions and is absent in others.
- cross-cutting map:
  - [sweep_2_architecture_coupling_contract_map.md](../../sweep_2_architecture_coupling_contract_map.md)
