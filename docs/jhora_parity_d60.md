# JHora D60 Parity

compat preset: `jhora_us`

case: 2004-01-27 14:45:35 Karaj (IR)

ayanamsa: 23-53-53.46 (23.8981833333)

node_policy: mean

label in JHora: **RvAr**

tolerance (deg): 1e-4

## Method sweep (D60)

| method | sign mismatches | abs diff sum (arcsec) | note |
| --- | --- | --- | --- |
| 1 | 7 | 52410.542 | sign mismatches |
| 2 | 2 | 52410.542 | sign mismatches |
| 3 | 0 | 52410.542 | **best sign match** |
| 4 | 7 | 52410.542 | sign mismatches |

## Mirror rule (compat)

JHora D60 (RvAr) matches PyJHora **method 3** with mirror for D1 even signs:

- mirror = `(30 - d_long) % 30`
- criterion: **D1 rasi_sign ∈ {Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces}**

Residual max diff after mirror: **≤ 0.276″**

Scope: **only D60/method3** in `jhora_us` compat. PyJHora mode unaffected.

## Reproduce

Fixture:
- `tests/fixtures/jhora_d60_d81_d108_d144_2004.json`

Test:
```
pytest -k "d60" -q
```
