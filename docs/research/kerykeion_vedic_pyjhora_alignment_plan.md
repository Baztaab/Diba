# Kerykeion Vedic-PyJHora Alignment Plan

Goal: keep Kerykeion architecture (`policy -> mechanism -> orchestration -> CLI`) while matching PyJHora runtime recipe.

## 1) Policy (Registry only)

- Keep all PyJHora ayanamsa IDs in `kerykeion/vedic/registry.py` with explicit status:
- `implemented`: IDs with direct `swe.SIDM_*` mapping.
- `recognized_not_implemented`: computed/custom IDs (`senthil`, `sundar_ss`) unless mechanism is implemented.
- Keep alias semantics (`true_lahiri -> true_citra`) explicit in spec.
- Keep node policy surface explicit (`mean`, `true`) and centralize SwissEph node constant mapping in registry spec.
- Keep house-system policy surface explicit for methods 1..5 with PyJHora method id traceability.

## 2) Mechanism (Context only)

- Only `kerykeion/vedic/context.py` performs SwissEph global-state calls (`set_ephe_path`, `set_sid_mode`, `calc_ut`, `houses_ex`).
- Implement deterministic call order inside a lock:
1. `set_ephe_path` (optional)
2. `set_sid_mode` from resolved policy
3. compute planets/nodes/asc/houses using recipe-aligned flags
4. reset baseline sidereal mode in `finally`
- Encode PyJHora-style flags in one place:
- Sidereal planets: `SWIEPH | SIDEREAL | TRUEPOS | SPEED | BIT_HINDU_RISING`
- Sidereal houses/asc: `SIDEREAL` (+ selected house code path)
- Preserve scoped compat behavior (`jhora_us`) behind explicit guard and fail-fast validation.

## 3) Orchestration (Factory only)

- `kerykeion/vedic/factory.py` responsibilities:
- normalize/validate local datetime + timezone
- convert to UTC JD once
- resolve policy specs (`resolve_*`)
- inject resolved specs and runtime args into context
- never call SwissEph directly
- keep fail-fast for ambiguous/non-existent DST local times.

## 4) CLI (Parse/Validate only)

- `kerykeion/_cli/options.py` should only:
- expose registry-driven choices
- parse/validate user input
- provide clear errors for recognized-not-implemented options
- not contain any astrology computation logic or SwissEph calls.

## 5) Static Chart Parity Workflow

- Static chart builder uses canonical factory/context path only.
- Parity testing should compare generated actual vs expected; no fallback to expected-as-actual.
- Diagnose utility reports `delta_arcsec` for key points when mismatch occurs.

## 6) Guardrails

- No `swe.set_*` outside context.
- No fixture/golden-driven overrides in runtime.
- No hardcoded numeric patches from expected snapshots.
- Global-state lock + baseline reset remains mandatory.
