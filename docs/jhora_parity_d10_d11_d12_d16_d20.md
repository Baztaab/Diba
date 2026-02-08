# JHora Parity — D10/D11/D12/D16/D20

compat preset: `jhora_us`

case: 2004-01-27 14:45:35 Karaj (IR)

ayanamsa: 23-53-53.46 (23.8981833333)

node_policy: mean

## D10 (label: 5-8) — method sweep

| method | sign mismatches | abs diff sum (arcsec) | note |
| --- | --- | --- | --- |
| 1 | 1 | 80735.100 | sign mismatch (moon) |
| 2 | 2 | 80735.100 | sign mismatch (sun, moon) |
| 3 | 0 | 0.349 | **best match** |
| 4 | 6 | 80735.100 | sign mismatches |
| 5 | 6 | 80735.100 | sign mismatches |
| 6 | 7 | 80735.100 | sign mismatches |

**Result:** JHora D10 (5-8) matches PyJHora D10 **method 3** (Parasara even reverse 9th backward).

### D10 mirror rule (compat)
Within method 3, JHora requires mirroring `d_long` for D1 even signs:

- mirror = `(30 - d_long) % 30`
- criterion: **D1 rasi_sign ∈ {Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces}**

Effect (arcsec diff, engine vs JHora):
- Sun: +0.034″
- Moon: +0.046″
- All others: |diff| ≤ 0.041″

Scope: **only D10/method3** in `jhora_us` compat. PyJHora mode unaffected.

## D16 (label: Rev)

**Result:** JHora D16 (Rev) matches PyJHora **method 2** (parivritti_even_reverse).

### D16 mirror rule (compat)
Within method 2, JHora requires mirroring `d_long` for D1 even signs:

- mirror = `(30 - d_long) % 30`
- criterion: **D1 rasi_sign ∈ {Taurus, Cancer, Virgo, Scorpio, Capricorn, Pisces}**

Effect (arcsec diff, engine vs JHora):
- Sun: +0.045″
- Moon: +0.070″
- All others: |diff| ≤ 0.068″

Scope: **only D16/method2** in `jhora_us` compat. PyJHora mode unaffected.

## D11/D12/D20 parity status

All three match JHora with small residuals (arcsec):

- D11: |diff| ≤ 0.047″
- D12: |diff| ≤ 0.057″
- D20: |diff| ≤ 0.092″

## Reproduce

Fixture:
- `tests/fixtures/jhora_d10_d11_d12_d16_d20_2004.json`

Test:
- `pytest -k "d10 or d11 or d12 or d16 or d20" -q`
