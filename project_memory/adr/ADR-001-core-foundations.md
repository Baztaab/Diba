# ADR 001: زیرساخت‌های محاسباتی، همزمانی و داده‌های هسته

- وضعیت: Accepted
- تاریخ: 2026-02-12
- نسخه: 1.2

## Context

پروژه دیبا برای جایگزینی موتورهای قدیمی نیاز به معماری دارد که:

- صحت نجومی را حفظ کند.
- توان پردازش بالا داشته باشد.
- در محیط چندنخی امن باشد.
- ردیابی خطا از خروجی نهایی تا داده خام افمریس ممکن باشد.

## Decision Drivers

- Performance
- Determinism
- Safety
- Traceability

## Decisions

### 1) Units & Indexing

- تمام زوایا در هسته: `float64` در بازه `[0, 360)`.
- قانون داخلی: `rasi` و `bhava` همیشه `0..11`.
- نمایش `1..12` فقط در لایه خروجی/نمایش.
- Normalization در مرزهای عمومی و constructorها اجباری است.

### 2) Concurrency & Session

- `swisseph` دارای global state است و thread-safe نیست.
- فقط از مسیر session/context مجاز استفاده شود.
- تضمین‌ها:
  - Atomic state setup در ابتدای session
  - Lock acquire/release قطعی با `try/finally`
  - منع کامل call بیرون session
  - state discipline قطعی و قابل تکرار

### 3) Varga Data Model

Invariantها:

- `varga_lon_abs` در `[0, 360)`
- `rasi_index = int(varga_lon_abs // 30)`
- `deg_in_rasi = varga_lon_abs % 30`

```python
class VargaPlacement(NamedTuple):
    varga_num: int
    varga_lon_abs: float
    rasi_index: int
    deg_in_rasi: float
```

مفاهیم تفسیری (مثل dignity/deity/gender) خارج از این لایه و در annotations محاسبه شوند.

### 4) Tolerances

- ANGLE: `1e-5` degree
- TIME: `30s` برای رویدادهای مرزی (نه رویدادهای بسیار دقیق مانند eclipse)
- CLASSIFICATION: تست‌های مرزی برای لبه‌ها

### 5) Reproducibility Metadata

خروجی باید امضای محاسباتی داشته باشد، شامل حداقل:

- `engine_version`
- `swisseph_version`
- `config_digest`
- `ephe_expectations`
- `timezone_policy`

### 6) Plugin Policy

- هر پلاگین باید `__api_version__` داشته باشد.
- ناسازگاری نسخه در startup باید fail کند.

## CI Guardrails (post-ADR)

1. تست serializer: خروجی 1-based و هسته 0-based بماند.
2. قانون import: `swisseph` فقط در مسیر مجاز session/adapter import شود.

