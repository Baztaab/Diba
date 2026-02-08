# JHora Parity — D108/D144

compat preset: `jhora_us`

case: 2004-01-27 14:45:35 Karaj (IR)

ayanamsa: 23-53-53.46 (23.8981833333)

node_policy: mean

tolerance (deg): D108=2e-4, D144=2e-4

## D108 parity

- Method: **1** (mixed D9(m1) → D12(m1))
- Sign mismatches: 0
- Max abs diff: **≤ 0.485″**

## D144 parity

- Method: **1** (mixed D12(m1) → D12(m1))
- Sign mismatches: 0
- Max abs diff: **≤ 0.657″**

## D81 parity status

D81 is **not tracked** against JHora. It is locked to **PyJHora parity only**.
See: `docs/pyjhora_parity_d81.md`.

## Reproduce

Fixture:
- `tests/fixtures/jhora_d60_d81_d108_d144_2004.json`

Test:
```
pytest -k "d108 or d144" -q
```
