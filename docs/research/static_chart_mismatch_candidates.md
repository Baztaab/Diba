# Static Chart Mismatch Candidates (Docs-Only Evidence)

Scope: فقط شواهد از `docs/` (بدون رجوع به کد runtime/golden/tests).

## A) JHora Compat Config for D1/Static

### A.1 Ayanamsa mode
- سند parity برای `jhora_us` صریحاً می‌گوید سیارات با `set_sid_mode(TRUE_CITRA)` + مسیر sidereal/TRUEPOS مچ می‌شوند. Citation: `docs/jhora_parity_compat_mode.md:15`, `docs/jhora_parity_compat_mode.md:23`, `docs/jhora_parity_compat_mode.md:37`.
- همان سند می‌گوید برای parity دقیق باید `ayanamsa_override_deg` دقیقاً برابر عدد چاپ‌شده در JHora باشد. Citation: `docs/jhora_parity_compat_mode.md:43`.
- در عین حال، تحقیق PyJHora می‌گوید default در خود PyJHora برابر `LAHIRI` است و `TRUE_LAHIRI -> TRUE_CITRA` alias هم وجود دارد. Citation: `docs/research/pyjhora_coverage.md:39`, `docs/research/pyjhora_coverage.md:43`, `docs/research/pyjhora_coverage.md:27`, `docs/research/pyjhora_coverage.md:31`.

### A.2 Node policy
- سند compat برای JHora parity صریحاً Mean Node را با NONUT قفل می‌کند: `mean_node_tropical - ayanamsa_override + NONUT`. Citation: `docs/jhora_parity_compat_mode.md:17`, `docs/jhora_parity_compat_mode.md:25`, `docs/jhora_parity_compat_mode.md:39`.
- در شواهد PyJHora، Rahu/Ketu نیز mean هستند (`swe.MEAN_NODE`) و Ketu = Rahu + 180. Citation: `docs/research/pyjhora_coverage.md:85`, `docs/research/pyjhora_coverage.md:90`.

### A.3 House system (whole sign method 5 + cusp rule)
- شواهد PyJHora: method 5 = «Each Rasi is the house» و cusp هر خانه = `sign_start + ascendant_longitude`. Citation: `docs/research/pyjhora_contract_evidence.md:10`, `docs/research/pyjhora_contract_evidence.md:12`, `docs/research/pyjhora_contract_evidence.md:16`.
- در compat parity، برای Asc/Houses مسیر توصیه‌شده این است: `asc_sid = asc_tropical - ayanamsa_override` (نه sidereal_direct houses_ex). Citation: `docs/jhora_parity_compat_mode.md:16`, `docs/jhora_parity_compat_mode.md:24`, `docs/jhora_parity_compat_mode.md:38`.

### A.4 SwissEph flags / path split (planets, asc, nodes)
- Planets: `SEFLG_SIDEREAL | SEFLG_TRUEPOS` در `TRUE_CITRA`. Citation: `docs/jhora_parity_compat_mode.md:15`, `docs/jhora_parity_compat_mode.md:23`.
- Asc: مسیر tropical-ayan (به‌جای sidereal houses_ex مستقیم) چون sidereal_direct آفست ثابت ~6.38" می‌دهد. Citation: `docs/jhora_parity_compat_mode.md:16`.
- Nodes: tropical mean node + `NONUT` سپس کسر ayanamsa_override؛ مسیر sidereal_direct برای نودها ~4.54" آفست می‌دهد. Citation: `docs/jhora_parity_compat_mode.md:17`, `docs/jhora_parity_compat_mode.md:25`.
- تایید تقویتی همین pipeline در D24 parity هم آمده است. Citation: `docs/jhora_parity_d24.md:9`, `docs/jhora_parity_d24.md:11`.

## B) Time Policy

- اسناد parity کیس‌ها را با `datetime local + timezone/offset` ثبت می‌کنند (مثلاً `Time Zone: +03:30`) و ayanamsa چاپ‌شده JHora را lock می‌کنند. Citation: `docs/jhora_parity_compat_mode.md:47`, `docs/jhora_parity_compat_mode.md:49`, `docs/jhora_parity_compat_mode.md:52`, `docs/jhora_parity_compat_mode.md:54`.
- اسناد معماری تاکید می‌کنند pipeline باید بر JD UTC + timezone handling بنا شود. Citation: `docs/kerykeion_arch_audit.md:42`, `docs/kerykeion_arch_audit.md:53`, `docs/kerykeion_arch_audit.md:54`.
- Unknown/Not found in docs: قاعده صریح «اولویت datetime_utc ورودی در برابر تبدیل از datetime_local+offset» برای static chart در docs پیدا نشد.

## C) Formatting Policy

- در docs parity معیار اصلی تطبیق عددی/arcsec tolerance است، نه policy صریح string-format. Citation: `docs/jhora_parity_d7_d8_d9.md:5`, `docs/jhora_parity_d4_d5_d6.md:5`, `docs/jhora_parity_d24.md:17`.
- Unknown/Not found in docs:
  - rule صریح truncate vs round برای DMS
  - تعداد رقم اعشار seconds برای `dms`
  - policy canonical برای `ayanamsa_dms`/`point dms` string rendering

## D) Top 3 Mismatch Hypotheses (Docs-Only)

### 1) Hypothesis: Static generator روی preset اشتباه اجرا می‌شود (LAHIRI default به‌جای JHora compat TRUE_CITRA + override)
- Evidence link:
  - JHora compat نیازمند `TRUE_CITRA` + `ayanamsa_override_deg` چاپ JHora است. `docs/jhora_parity_compat_mode.md:15`, `docs/jhora_parity_compat_mode.md:23`, `docs/jhora_parity_compat_mode.md:43`
  - PyJHora default عمومی `LAHIRI` است (اگر compat preset اعمال نشود). `docs/research/pyjhora_coverage.md:39`
- What to change (file+function):
  - `kerykeion/vedic/static_chart.py:build_static_chart_v0_1`
  - `kerykeion/vedic/factory.py:VedicSubjectFactory.from_birth_data`
  - یک policy لایه‌ای برای parity preset/override ورودی static pipeline.

### 2) Hypothesis: مسیر محاسبه Asc/Houses و Nodes با JHora compat یکسان نیست
- Evidence link:
  - Asc باید از `asc_tropical - ayanamsa_override` بیاید؛ sidereal houses_ex مستقیم آفست ~6.38" می‌دهد. `docs/jhora_parity_compat_mode.md:16`, `docs/jhora_parity_compat_mode.md:24`
  - Nodes باید mean+tropical+NONUT باشند؛ sidereal_direct برای nodes آفست ~4.54" می‌دهد. `docs/jhora_parity_compat_mode.md:17`, `docs/jhora_parity_compat_mode.md:25`, `docs/jhora_parity_d24.md:9`, `docs/jhora_parity_d24.md:11`
- What to change (file+function):
  - `kerykeion/vedic/context.py:VedicCalculationContext.compute_core`
  - `kerykeion/vedic/static_chart.py:build_static_chart_v0_1` (برای انتخاب مسیر compat در snapshot generation).

### 3) Hypothesis: اختلاف formatting (DMS round/truncate/precision) عامل بخشی از mismatch متنی است
- Evidence link:
  - docs parity روی arcsec numeric diff تمرکز دارد و policy صریح text formatting تعریف نکرده است. `docs/jhora_parity_d7_d8_d9.md:5`, `docs/jhora_parity_d4_d5_d6.md:5`, `docs/jhora_parity_d24.md:17`
  - docs هیچ rule صریحی برای round vs truncate و decimal digits در DMS نداده‌اند (Unknown above).
- What to change (file+function):
  - `kerykeion/vedic/static_chart.py:format_dms`
  - اگر لازم شد، یک formatter policy جدا و testable برای `static_chart.v0.1`.

## Notes
- این گزارش intentionally فقط از docs/research استفاده می‌کند و نتیجه‌ها برای تصمیم‌گیری implementation-level باید با runtime tests validate شوند.
