# JHora D24 Parity (Sweep)

compat preset: `jhora_us`

case: 2004-01-27 14:45:35 Karaj (IR)

ayanamsa: 23-53-53.46 (23.8981833333)

node_policy: mean (NONUT)

pipeline: sidereal_direct TRUE_CITRA + TRUEPOS (planets), asc = tropical − ayanamsa_override, mean nodes with NONUT

## Method sweep summary

All methods tested with D24 (Siddhamsa). The `mirror_even_sign` column below is a **manual mirror applied after engine output** (for sweep comparison). In `jhora_us`, method2 already applies the even-sign mirror.

| method | mirror_even_sign | sign_mismatch | mean_abs_diff (arcsec) | notes |
| --- | --- | --- | --- | --- |
| 1 | false | 1 | 3610.261 | Sun sign mismatch (Tau vs Vir), large degree errors |
| 1 | true  | 1 | 0.081 | Sun sign mismatch remains |
| 2 | false | 0 | 0.081 | **Best match** (all signs + degrees within ~0.1″) |
| 2 | true  | 0 | 3610.261 | Double-mirror (bad) |
| 3 | false | 2 | 3610.261 | Sun/Moon sign mismatch |
| 3 | true  | 2 | 0.081 | Sun/Moon sign mismatch remains |

## Decision

**For `jhora_us` compat only:**

- D24 label **"Rev"** maps to **method = 2**
- apply **mirror** on `d_long` **iff** D1 rasi sign is even (PyJHora even_signs)

Scope: **only** D24/method2 when `vedic_compat_mode="jhora_us"`. PyJHora mode is unchanged.

## Fixture + test

Fixture: `tests/fixtures/jhora_d24_2004.json`

Test: `tests/test_vedic_vargas_parity_jhora.py::test_jhora_parity_d24_case_2004`

Run:

```
pytest -k "jhora_parity_d24_case_2004" -q
```

## Detailed sweep (per-point)

### method 1 | mirror_even_sign=false
| point | sign | exp | pos | exp_pos | diff_arcsec | match |
| --- | --- | --- | --- | --- | --- | --- |
| ascendant | Pis | Pis | 28.597758 | 28.597731 | +0.098 | True |
| sun | Tau | Vir | 11.037123 | 18.962897 | -28532.788 | False |
| moon | Cap | Cap | 13.948737 | 16.051292 | -7569.196 | True |
| mars | Vir | Vir | 10.959344 | 10.959325 | +0.069 | True |
| mercury | Sag | Sag | 20.949554 | 20.949533 | +0.075 | True |
| jupiter | Pis | Pis | 9.163915 | 9.163897 | +0.063 | True |
| venus | Cap | Cap | 7.145258 | 7.145239 | +0.070 | True |
| saturn | Can | Can | 1.549028 | 1.549011 | +0.062 | True |
| rahu | Cap | Cap | 27.737241 | 27.737214 | +0.097 | True |
| ketu | Cap | Cap | 27.737241 | 27.737214 | +0.097 | True |

### method 1 | mirror_even_sign=true
| point | sign | exp | pos | exp_pos | diff_arcsec | match |
| --- | --- | --- | --- | --- | --- | --- |
| ascendant | Pis | Pis | 28.597758 | 28.597731 | +0.098 | True |
| sun | Tau | Vir | 18.962877 | 18.962897 | -0.072 | False |
| moon | Cap | Cap | 16.051263 | 16.051292 | -0.104 | True |
| mars | Vir | Vir | 10.959344 | 10.959325 | +0.069 | True |
| mercury | Sag | Sag | 20.949554 | 20.949533 | +0.075 | True |
| jupiter | Pis | Pis | 9.163915 | 9.163897 | +0.063 | True |
| venus | Cap | Cap | 7.145258 | 7.145239 | +0.070 | True |
| saturn | Can | Can | 1.549028 | 1.549011 | +0.062 | True |
| rahu | Cap | Cap | 27.737241 | 27.737214 | +0.097 | True |
| ketu | Cap | Cap | 27.737241 | 27.737214 | +0.097 | True |

### method 2 | mirror_even_sign=false
| point | sign | exp | pos | exp_pos | diff_arcsec | match |
| --- | --- | --- | --- | --- | --- | --- |
| ascendant | Pis | Pis | 28.597758 | 28.597731 | +0.098 | True |
| sun | Vir | Vir | 18.962877 | 18.962897 | -0.072 | True |
| moon | Cap | Cap | 16.051263 | 16.051292 | -0.104 | True |
| mars | Vir | Vir | 10.959344 | 10.959325 | +0.069 | True |
| mercury | Sag | Sag | 20.949554 | 20.949533 | +0.075 | True |
| jupiter | Pis | Pis | 9.163915 | 9.163897 | +0.063 | True |
| venus | Cap | Cap | 7.145258 | 7.145239 | +0.070 | True |
| saturn | Can | Can | 1.549028 | 1.549011 | +0.062 | True |
| rahu | Cap | Cap | 27.737241 | 27.737214 | +0.097 | True |
| ketu | Cap | Cap | 27.737241 | 27.737214 | +0.097 | True |

### method 2 | mirror_even_sign=true
| point | sign | exp | pos | exp_pos | diff_arcsec | match |
| --- | --- | --- | --- | --- | --- | --- |
| ascendant | Pis | Pis | 28.597758 | 28.597731 | +0.098 | True |
| sun | Vir | Vir | 11.037123 | 18.962897 | -28532.788 | True |
| moon | Cap | Cap | 13.948737 | 16.051292 | -7569.196 | True |
| mars | Vir | Vir | 10.959344 | 10.959325 | +0.069 | True |
| mercury | Sag | Sag | 20.949554 | 20.949533 | +0.075 | True |
| jupiter | Pis | Pis | 9.163915 | 9.163897 | +0.063 | True |
| venus | Cap | Cap | 7.145258 | 7.145239 | +0.070 | True |
| saturn | Can | Can | 1.549028 | 1.549011 | +0.062 | True |
| rahu | Cap | Cap | 27.737241 | 27.737214 | +0.097 | True |
| ketu | Cap | Cap | 27.737241 | 27.737214 | +0.097 | True |

### method 3 | mirror_even_sign=false
| point | sign | exp | pos | exp_pos | diff_arcsec | match |
| --- | --- | --- | --- | --- | --- | --- |
| ascendant | Pis | Pis | 28.597758 | 28.597731 | +0.098 | True |
| sun | Gem | Vir | 11.037123 | 18.962897 | -28532.788 | False |
| moon | Aqu | Cap | 13.948737 | 16.051292 | -7569.196 | False |
| mars | Vir | Vir | 10.959344 | 10.959325 | +0.069 | True |
| mercury | Sag | Sag | 20.949554 | 20.949533 | +0.075 | True |
| jupiter | Pis | Pis | 9.163915 | 9.163897 | +0.063 | True |
| venus | Cap | Cap | 7.145258 | 7.145239 | +0.070 | True |
| saturn | Can | Can | 1.549028 | 1.549011 | +0.062 | True |
| rahu | Cap | Cap | 27.737241 | 27.737214 | +0.097 | True |
| ketu | Cap | Cap | 27.737241 | 27.737214 | +0.097 | True |

### method 3 | mirror_even_sign=true
| point | sign | exp | pos | exp_pos | diff_arcsec | match |
| --- | --- | --- | --- | --- | --- | --- |
| ascendant | Pis | Pis | 28.597758 | 28.597731 | +0.098 | True |
| sun | Gem | Vir | 18.962877 | 18.962897 | -0.072 | False |
| moon | Aqu | Cap | 16.051263 | 16.051292 | -0.104 | False |
| mars | Vir | Vir | 10.959344 | 10.959325 | +0.069 | True |
| mercury | Sag | Sag | 20.949554 | 20.949533 | +0.075 | True |
| jupiter | Pis | Pis | 9.163915 | 9.163897 | +0.063 | True |
| venus | Cap | Cap | 7.145258 | 7.145239 | +0.070 | True |
| saturn | Can | Can | 1.549028 | 1.549011 | +0.062 | True |
| rahu | Cap | Cap | 27.737241 | 27.737214 | +0.097 | True |
| ketu | Cap | Cap | 27.737241 | 27.737214 | +0.097 | True |

