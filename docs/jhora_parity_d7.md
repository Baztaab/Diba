# JHora Parity — D7 Deep Dive

compat preset: jhora_us  
case: 1988-09-11 06:45 Tehran  
commands:
- PyJHora parity: `pytest tests/test_vedic_vargas_pyjhora_d7.py`
- JHora fixture parity: `pytest tests/test_vedic_vargas_parity_jhora.py -k d7_d8_d9`

## Step 1 — PyJHora parity (source of truth)
Result: **PASS**.  
Engine D7 method=1 matches PyJHora `saptamsa_chart` point-by-point (sign + d_long) for the case above.

Method sweep (Engine vs PyJHora):
All methods 1..6 match exactly when comparing engine output against PyJHora `saptamsa_chart` using the same `rasi_positions`.

Conclusion: **Engine is consistent with PyJHora** for D7.

## Step 2 — JHora fixture sweep
Result: **FAIL** for D7 across methods 1..6.  
Mismatches persist for the same subset of points:
`ascendant, mars, mercury, jupiter, venus, saturn, rahu, ketu`  
(Sun/Moon match for methods 1–5; method 6 diverges further.)

Conclusion: **JHora fixture does not align with PyJHora D7 for this case**.

## Summary
- Engine D7 methods match PyJHora exactly → no engine bug.
- JHora fixture likely uses a different setting/profile than PyJHora’s D7 methods for this case.
- Next step (if needed): verify JHora D7 chart method or profile used to generate the fixture.
