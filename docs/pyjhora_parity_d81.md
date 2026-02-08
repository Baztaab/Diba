# PyJHora Parity — D81 (Nava-Navamsa)

## هدف
قفل‌کردن D81 بر اساس PyJHora به‌عنوان “golden truth”، مستقل از JHora و بدون وابستگی به ephemeris/JD.

## کیس مرجع
- 2004-01-27 14:45:35 — Karaj, Iran
- Ayanamsa override: 23.8981833333
- Nodes: mean
- compat_mode: **خاموش** (PyJHora mode)

## روش تست
برای جلوگیری از اختلاف ephemeris، ابتدا `rasi_positions` از خروجی `rasi_d1` ساخته می‌شود. سپس:
- PyJHora: `nava_navamsa_chart(rasi_positions, chart_method=...)`
- Engine: `compute_varga(core_abs, "D81", method=...)`

مقایسه:
- `sign_num` برابر
- `position` با tolerance بسیار تنگ (`< 1e-9`)

## روش‌های پوشش داده‌شده
- method 1 (default)
- method 2 (parivritti even reverse)
- method 3 (parivritti alternate)

## اجرای تست
```bash
pytest -k "pyjhora_d81" -q
```

## یادداشت
این تست فقط parity با PyJHora را قفل می‌کند و به JHora-compat وابسته نیست.
