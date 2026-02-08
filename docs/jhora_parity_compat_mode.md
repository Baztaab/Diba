# JHora US Parity (D1/D2/D3) — Compat Mode

## هدف پروژه و تعریف parity با JHora
هدف این سند قفل‌کردن یک preset پایدار برای “JHora US-compatible” است تا خروجی‌های D1/D2/D3 در Kerykeion با JHora هم‌خوانی عددی داشته باشند.  
در این مرحله، parity فقط برای D1 (راشی) و D2/D3 (US profile) تأیید شده است.

## دو کیس تست اصلی
این preset با دو کیس زیر قفل شد:

1) 2004-01-27 14:45:35 — Karaj, Iran  
2) 1988-09-11 06:45:00 — Tehran, Iran

## یافته‌های قطعی (Final Findings)
- Mirror شرطی فقط برای D2(method1) و D3(method5) لازم است، و معیار آن **D1 rasi_sign سیدریال even** است.  
- سیارات با `set_sid_mode(TRUE_CITRA)` و سپس `calc_ut(... SEFLG_SIDEREAL | SEFLG_TRUEPOS ...)` با JHora مچ می‌شوند.  
- Ascendant با `(asc_tropical − ayanamsa_override)` دقیقاً صفر می‌شود؛ اگر مستقیم از `houses_ex(... SIDEREAL)` گرفته شود، آفست ثابت ~6.38″ دارد.  
- Mean node فقط با `(mean_node_tropical − ayanamsa_override + NONUT)` صفر می‌شود؛ مسیر sidereal_direct برای نودها آفست ~4.54″ می‌دهد.  

## Pipeline نهایی

| بخش | مسیر محاسبه |
| --- | --- |
| Planets | `set_sid_mode(TRUE_CITRA)` + `swe.calc_ut(... SEFLG_SIDEREAL | SEFLG_TRUEPOS | ...)` |
| Asc/Houses | `asc_sid = asc_tropical − ayanamsa_override` |
| Mean Nodes | `rahu_sid = mean_node_tropical − ayanamsa_override` با `NONUT` (فقط روی محاسبه‌ی mean node tropical) |
| Vargas | `profile=US` → D2=method1, D3=method5 |
| Mirror | فقط برای D2m1/D3m5، فقط اگر D1 even-sign |

## Mirror Scope & Criterion
- Scope: فقط D2(method1) و D3(method5)  
- Criterion: D1 sidereal rasi_sign (همان compat pipeline)

## قواعد CLI (ساده و شفاف)
پیشنهاد عملی برای انتخاب preset:

- `vedic_compat_mode="jhora_us"`  
  - سیارات: sidereal_direct + TRUE_CITRA + TRUEPOS  
  - Asc: tropical − ayan_override  
  - Mean nodes: tropical − ayan_override + NONUT  
  - Vargas: profile=US (D2m1, D3m5)  
  - Mirror: فقط D2m1/D3m5 و فقط وقتی D1 even-sign

نکته: برای parity دقیق باید مقدار `ayanamsa_override_deg` همان عدد چاپ‌شده در JHora باشد.

## Reproduce
### Case 1 — Karaj (2004-01-27 14:45:35)
- Time Zone: +03:30  
- Place: 51E06, 35N42  
- JHora Ayanamsa: 23-53-53.46 (≈ 23.8981833333)

### Case 2 — Tehran (1988-09-11 06:45:00)
- Time Zone: +03:30  
- Place: 51E09, 32N42  
- JHora Ayanamsa: 23-41-00.85 (≈ 23.6835694444)

### JHora Settings (مرجع)
- Ayanamsa: True Lahiri/Chitrapaksha  
- Nodes: Mean  
- Vargas profile: US  

### CLI پیشنهادی (با سوییچ‌های واقعی)
نکته: CLI فعلی فقط D1 را دارد (`kerykeion vedic d1`). برای D2/D3 از Python API استفاده کنید.

```bash
python -m kerykeion.cli vedic d1 \
  --year 2004 --month 1 --day 27 --hour 14 --minute 45 --second 35 \
  --lat 35.7 --lng 51.1 --tz-str Asia/Tehran \
  --offline --ephe-path d:\\kerykeion\\data \
  --ayanamsa lahiri --node-policy mean --house-system whole-sign \
  --format json
```

### اجرای تست parity (مینیمال)
```bash
pytest tests/test_vedic_vargas_parity_jhora.py
```

### بازتولید کامل (D1/D2/D3، هر دو کیس) با Python API
```bash
python - <<'PY'
from kerykeion.astrological_subject_factory import AstrologicalSubjectFactory

cases = [
    dict(name="Karaj", year=2004, month=1, day=27, hour=14, minute=45, seconds=35,
         lat=35 + 42/60, lng=51 + 6/60, tz_str="Asia/Tehran", ayan=23.8981833333),
    dict(name="Tehran", year=1988, month=9, day=11, hour=6, minute=45, seconds=0,
         lat=32 + 42/60, lng=51 + 9/60, tz_str="Asia/Tehran", ayan=23.6835694444),
]

for c in cases:
    subject = AstrologicalSubjectFactory.from_birth_data(
        name=c["name"],
        year=c["year"], month=c["month"], day=c["day"],
        hour=c["hour"], minute=c["minute"], seconds=c["seconds"],
        lat=c["lat"], lng=c["lng"], tz_str=c["tz_str"],
        online=False,
        vedic=True,
        vedic_ayanamsa_override_deg=c["ayan"],
        vedic_compat_mode="jhora_us",
        vedic_vargas=["D1", "D2", "D3"],
    )
    print(c["name"], subject.model_dump()["vedic"]["vargas"]["charts"].keys())
PY
```

## Notes
- برای جلوگیری از شلوغی JSON، provenance و ریزتنظیمات در JSON ذخیره نمی‌شوند و فقط در مستندات ثبت شده‌اند.  
- این فایل مرجع نهایی parity است و مسیر رسمی مستندسازی در `docs/` نگهداری می‌شود.
- fixtureهای JHora فقط با `vedic_compat_mode="jhora_us"` معتبر هستند؛ `profile=US` به‌تنهایی mirror را فعال نمی‌کند.
- خارج از scope JHora: D81 فقط با PyJHora parity قفل می‌شود و در suite مربوط به JHora استفاده نمی‌شود.

## Parity Index
- `docs/jhora_parity_d4_d5_d6.md`
- `docs/jhora_parity_d7_d8_d9.md`
- `docs/jhora_parity_d7_rule.md`
- `docs/jhora_parity_d10_d11_d12_d16_d20.md`
- `docs/jhora_parity_d24.md`
- `docs/jhora_parity_d60.md`
- `docs/jhora_parity_d81_d108_d144.md`
- `docs/vargas_d10_d11_d12_d16_d20_research.md`
- `docs/vargas_d24_d27_d30_d40_d45_research.md`
- `docs/vargas_d60_research.md`
- `docs/vargas_d81_d108_d144_research.md`

## PyJHora Parity Locks
- `docs/pyjhora_parity_d81.md`
