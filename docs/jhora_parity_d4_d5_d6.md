# JHora US Parity — D4/D5/D6 (Case 1988-09-11)

compat preset: jhora_us  
case: 1988-09-11 06:45 Tehran  
tolerance test: 3e-5 deg (≈ 0.108″)  
pytest: `pytest tests/test_vedic_vargas_parity_jhora.py -k d4_d5_d6`

این سند نتایج parity برای D4/D5/D6 را ثبت می‌کند (همان pipeline “JHora US compat”).

## Case
- Date/Time: 1988-09-11 06:45:00
- Location: Tehran, Iran (51E09, 32N42)
- Time Zone: +03:30
- JHora Ayanamsa: 23-41-00.85 (≈ 23.6835694444)

## Arcsec Diffs (JHora − Kerykeion)
همه اختلاف‌ها در حد ≤ 0.02″ است.

### D4
| Point | Δ arcsec |
| --- | ---: |
| ascendant | +0.01 |
| sun | +0.00 |
| moon | -0.00 |
| mars | +0.00 |
| mercury | -0.00 |
| jupiter | +0.00 |
| venus | -0.00 |
| saturn | +0.00 |
| rahu | +0.01 |
| ketu | +0.01 |

### D5
| Point | Δ arcsec |
| --- | ---: |
| ascendant | +0.01 |
| sun | +0.00 |
| moon | -0.00 |
| mars | -0.00 |
| mercury | +0.00 |
| jupiter | -0.00 |
| venus | +0.00 |
| saturn | -0.00 |
| rahu | +0.01 |
| ketu | +0.01 |

### D6
| Point | Δ arcsec |
| --- | ---: |
| ascendant | +0.01 |
| sun | +0.00 |
| moon | -0.01 |
| mars | +0.01 |
| mercury | +0.00 |
| jupiter | +0.01 |
| venus | -0.00 |
| saturn | +0.00 |
| rahu | +0.02 |
| ketu | +0.02 |

## Notes
- این نتایج با همان pipeline تعریف‌شده در `docs/jhora_parity_compat_mode.md` گرفته شده‌اند.
