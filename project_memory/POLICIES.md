# Project Policies

## Policy: PyJHora-First Research (Mandatory)

قبل از شروع هر Capability/بخش محاسباتی جدید (مثلاً: Panchanga / Dasha / Vargas / Houses / Transit / ...)، مرحله ۱ همیشه «تحقیق» است و بدون آن هیچ پیاده‌سازی وارد ریپو نمی‌شود.

### الزامات

1. **بررسی کد PyJHora/PTJHora برای همان محاسبه**
- فایل‌ها/توابع مرتبط پیدا و دقیق خوانده شود.
- قراردادهای مهم (indexing، نرمال‌سازی، flagها، edge-caseها، rounding/tolerance) استخراج شود.

2. **استخراج منطق به‌صورت یادداشت رسمی**
- قبل از کدنویسی، یک فایل یادداشت در Project Memory ساخته شود:
  - `D:\Diba\project_memory\research\<capability>-pyjhora-extract.md`
- این فایل باید شامل موارد زیر باشد:
  - مسیر فایل و نام تابع(ها) در PyJHora
  - فرمول/الگوریتم و مراحل محاسبه
  - ورودی/خروجی و قراردادهای indexing و normalization
  - موارد مرزی (0/30/360 و شبه‌خطاها)
  - هر اختلاف احتمالی با ADRهای دیبا (اگر وجود دارد)

3. **پیاده‌سازی در دیبا مطابق قراردادهای دیبا**
- منطق استخراج‌شده باید به سبک کد دیبا نوشته شود (separation of concerns، immutable-by-default، guardrailها، و رعایت قوانین SwissEph session).
- اگر PyJHora رفتاری دارد که با ADRهای دیبا تعارض دارد، تصمیم باید:
  - به‌صورت صریح در ADR/Project Memory ثبت شود.
  - و تست مرزی/رگرسیونی برایش نوشته شود.

### معیار Done

هیچ PR/Commit برای آن capability قابل قبول نیست مگر:
- فایل تحقیق در `project_memory\research\...` وجود داشته باشد.
- و تست‌های مرتبط (حداقل boundary + regression) اضافه شده باشند.

### گیت اجرایی (Machine-Enforced)

- Rule قابل enforce در CI: اگر capabilityهای تعریف‌شده در ریپو وجود/تغییر داشته باشند، research artifactهای متناظر باید در `project_memory/research/` موجود باشند و حداقل ساختار الزامی را داشته باشند.
- تست enforce:
  - `tests/test_policy_research_gate.py`

## Policy: Docstring Standard (PEP 257 + Google Style, Enforced)

تمام docstringها باید هم‌زمان:
- با اصول ساختاری PEP 257 سازگار باشند (summary line + blank line + توضیح تکمیلی).
- و در docstringهای چندخطی از Google-style sections استفاده کنند: `Args:`, `Returns:`, `Raises:` (در صورت نیاز).

### قواعد الزامی (Minimum Bar)

1. **همه docstringها با `"""` نوشته شوند.**
2. **Summary line یک خط، با علامت پایان جمله، و سپس یک خط خالی** (در docstring چندخطی).
3. **Docstring برای API عمومی اجباری است** (module/class/public function).
4. **از نوشتن signature داخل docstring خودداری شود**؛ type hints منبع اصلی type documentation است.
5. **سبک جمله** (imperative یا descriptive) آزاد است، ولی باید در یک فایل/ماژول یکدست باشد.

### قالب پیشنهادی (Template)

```python
def fn(x: int, y: int) -> int:
    """Compute something important.

    Args:
        x: Meaning of x.
        y: Meaning of y.

    Returns:
        What the function returns.

    Raises:
        ValueError: When inputs are invalid.
    """
```

### Enforcement (Ruff)

- Ruff باید قواعد docstring را با `pydocstyle` enforce کند.
- Convention باید `google` باشد تا قالب بخش‌ها یکدست و lint-friendly بماند.
- تنظیمات enforce در `pyproject.toml` نگه‌داری می‌شود.

## Policy: Canonical/Mirror Sync (Mandatory)

- منبع حقیقت برای حافظه پروژه: `project_memory/...` (و در سیستم فایل همان مسیر مطلق `D:\\Diba\\project_memory\\...`).
- هر سند mirror در `docs/...` باید با نسخه‌ی متناظر در `project_memory/...` همگام باشد.
- اختلاف بین canonical و mirror مجاز نیست.

### گیت اجرایی

- تست enforce:
  - `tests/test_memory_sync_contract.py`

## Policy: Session Ownership (Mandatory)

- مالک lifecycle سشن محاسباتی: `DibaEngine`.
- `VedicCalculationContext` لایه محاسبه است و در مسیر engine باید با `manage_session=False` مصرف شود.
- هرگونه state سشن روی objectهای اشتراکی (engine/context) ممنوع است.

### گیت اجرایی

- تست enforce:
  - `tests/test_session_ownership_contract.py`
  - `tests/test_engine_thread_session_isolation.py`
