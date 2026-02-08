# JHora Parity — D7/D8/D9

compat preset: jhora_us  
case: 1988-09-11 06:45 Tehran  
tolerance: 3e-5 deg (~0.108")  
pytest: `pytest tests/test_vedic_vargas_parity_jhora.py -k d7_d8_d9`

## Status
All D7/D8/D9 points match within tolerance under `jhora_us` (D7 uses method2 + compat mirror rule).

## D7/D8/D9 diff (JHora − Kerykeion)

### D7
All points within tolerance (≤ 0.020″). No sign mismatches.

### D8
All points within tolerance (≤ 0.014″). No sign mismatches.

### D9
All points within tolerance (≤ 0.020″). No sign mismatches.

## Notes
- D7 uses method2 in `jhora_us` and applies the compat mirror rule (see `docs/jhora_parity_d7_rule.md`).
- Mirror scope in core remains D2(m1)/D3(m5); D7 mirror is compat-only.
- Chiron ephemeris warning may appear if `seas_18.se1` is missing; it does not affect these points.
