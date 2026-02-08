# PyJHora Full-Coverage Roadmap (Non-GUI) for Kerykeion

## 1) هدف نهایی
- پوشش تمام قابلیت‌های محاسباتی PyJHora (به‌جز GUI/گرافیک) با خروجی JSON.
- حفظ و تقویت معماری Kerykeion:
- `policy` فقط در `registry`
- `mechanism` فقط در `context`
- `orchestration` فقط در `factory/services`
- `CLI` فقط parse/validate/dispatch

## 2) شواهد دامنه PyJHora (Repo-Local)
- هسته پَنچانگا و runtime نجومی: `docs/jhora/panchanga/drik.py` (157 تابع).
- موتور چارت/وارگا: `docs/jhora/horoscope/chart/charts.py` (99 تابع).
- یوگاها: `docs/jhora/horoscope/chart/yoga.py` (551 تابع).
- خانه/درشتی/کاراکا: `docs/jhora/horoscope/chart/house.py` (54 تابع).
- شَدبالا/strength: `docs/jhora/horoscope/chart/strength.py` (53 تابع).
- اسفوتاها: `docs/jhora/horoscope/chart/sphuta.py` (28 تابع).
- دوشا: `docs/jhora/horoscope/chart/dosha.py` (19 تابع).
- راجا یوگا: `docs/jhora/horoscope/chart/raja_yoga.py` (18 تابع).
- دَشاهای Graha: `docs/jhora/horoscope/dhasa/graha/*.py`.
- دَشاهای Raasi: `docs/jhora/horoscope/dhasa/raasi/*.py`.
- دَشا سالانه: `docs/jhora/horoscope/dhasa/annual/*.py`.
- ترانزیت/تاجیکا/سهم: `docs/jhora/horoscope/transit/*.py`.
- پیش‌بینی: `docs/jhora/horoscope/prediction/*.py`.
- سازگاری/مچ: `docs/jhora/horoscope/match/compatibility.py`.
- ابزارهای پَنچانگا تکمیلی: `docs/jhora/panchanga/vratha.py`, `docs/jhora/panchanga/pancha_paksha.py`, `docs/jhora/panchanga/surya_sidhantha.py`.

## 3) اصول معماری (Non-Negotiable)
- همه `swe.set_*` فقط در یک نقطه canonical: `kerykeion/vedic/context.py`.
- تمام انتخاب‌های کاربر/پالیسی فقط از registry resolve شوند.
- هیچ منطق نجومی داخل CLI.
- JSON contract versioned برای هر domain (`d1`, `panchanga`, `dasha`, `transit`, ...).
- fail-fast برای modeهای recognized-but-not-implemented.

## 4) نقشه ماژولی هدف
### 4.1 Existing (بماند و تقویت شود)
- `kerykeion/vedic/registry.py`
- `kerykeion/vedic/context.py`
- `kerykeion/vedic/factory.py`
- `kerykeion/vedic/builder.py`
- `kerykeion/vedic/static_chart.py`
- `kerykeion/vedic/vargas.py`

### 4.2 New modules (پیشنهادی)
- `kerykeion/vedic/services/panchanga_service.py`
- `kerykeion/vedic/services/varga_service.py`
- `kerykeion/vedic/services/yoga_service.py`
- `kerykeion/vedic/services/dosha_service.py`
- `kerykeion/vedic/services/strength_service.py`
- `kerykeion/vedic/services/sphuta_service.py`
- `kerykeion/vedic/services/dasha_service.py`
- `kerykeion/vedic/services/transit_service.py`
- `kerykeion/vedic/services/match_service.py`
- `kerykeion/vedic/services/prediction_service.py`
- `kerykeion/vedic/contracts/*.py` (schemas/versioned JSON contracts)
- `kerykeion/_cli/commands/vedic_*.py` (یک command per domain)

وظیفه هر service:
- گرفتن input typed
- resolve پالیسی‌ها از registry
- فراخوانی factory/context
- تبدیل خروجی raw به contract JSON

## 5) فازبندی عملیاتی

## Phase 0: Baseline Hardening (الان/فوری)
هدف:
- قفل‌کردن runtime recipe PyJHora برای time/JD/ayanamsa/nodes/houses.
- حذف هر bypass غیر canonical.

کار:
- تکمیل `registry` برای surface کامل ayanamsa + house methods + node modes.
- context lock/reset + call-order قطعی.
- اسکریپت diagnose delta_arcsec برای اختلاف‌ها.

خروجی:
- `docs/research/pyjhora_runtime_recipe.md`
- `docs/research/kerykeion_vedic_pyjhora_alignment_plan.md`
- parity test پایه D1.

Done وقتی:
- D1 parity روی کیس‌های مرجع در حد نمایشی قابل قبول باشد.

## Phase 1: JSON Contracts & Core APIs
هدف:
- استانداردسازی خروجی JSON برای domainهای اصلی.

کار:
- تعریف schemaهای versioned:
- `schemas/vedic_d1.v1.json`
- `schemas/vedic_panchanga.v1.json`
- `schemas/vedic_varga.v1.json`
- `schemas/vedic_dasha.v1.json`
- اضافه‌کردن `contracts` و serializerهای typed.

خروجی:
- APIهای پایدار برای مصرف‌کننده (UI/Backend/Agent).

Done وقتی:
- هر endpoint خروجی schema-valid و versioned بدهد.

## Phase 2: Panchanga Coverage
هدف:
- پوشش محاسبات روزانه/تقویمی PyJHora از `drik.py`.

کار (service):
- `panchanga_service.py`:
- tithi, vara, nakshatra, yoga, karana
- sunrise/sunset/moonrise/moonset
- hora, rahu kala, gulika, yamaghanta

نیاز registry:
- timezone policy
- tropical/sidereal mode policy

تست:
- parity tests against selected PyJHora cases.
- edge tests timezone/DST.

## Phase 3: Varga Coverage (D1..D144 methods/profiles)
هدف:
- پوشش کامل varga methods/profiles مشابه `charts.py`.

کار:
- توسعه `vargas.py` برای همه charts مورد نیاز.
- `varga_service.py` برای batch generation JSON.
- profile policy (US/Parashara/...).

تست:
- per-varga parity tests (numeric tolerance).
- property tests for boundaries (0/30 deg edges).

## Phase 4: House/Strength/Yoga/Dosha/Sphuta
هدف:
- تحویل domain analytics سطح بالاتر.

کار:
- `strength_service.py` ← `strength.py`
- `yoga_service.py` ← `yoga.py`
- `dosha_service.py` ← `dosha.py`
- `sphuta_service.py` ← `sphuta.py`
- `house.py` logic exposure as JSON diagnostics.

تست:
- subset parity + deterministic regression suite.

## Phase 5: Dasha Engine (Major)
هدف:
- پوشش کامل دَشاها (graha + raasi + annual + sudharsana).

کار:
- `dasha_service.py`:
- unified API: `system`, `start_policy`, `levels` (maha/antara/...)
- adapters per subsystem:
- `horoscope/dhasa/graha/*.py`
- `horoscope/dhasa/raasi/*.py`
- `horoscope/dhasa/annual/*.py`

registry additions:
- dasha system IDs
- applicability policy

تست:
- parity suite برای vimsottari + 2-3 سیستم graha + 2-3 سیستم raasi + annual.

## Phase 6: Transit/Tajaka/Saham
هدف:
- پوشش محاسبات transit سالانه/تاجیکا.

کار:
- `transit_service.py`:
- saham calculations
- tajaka yoga/aspects packages

تست:
- case-based numeric parity.

## Phase 7: Match/Compatibility
هدف:
- پوشش logic compatibility غیر گرافیکی.

کار:
- `match_service.py` wrapping `match/compatibility.py`
- output JSON explainable factors + score components.

تست:
- fixed known couples fixtures.

## Phase 8: Prediction APIs
هدف:
- JSON قابل‌مصرف برای prediction modules.

کار:
- `prediction_service.py`:
- general/longevity/naadi-marriage outputs
- trace fields برای explainability.

تست:
- contract tests + deterministic outputs.

## Phase 9: CLI/API Productization
هدف:
- CLI کامل ودیک و API پایدار.

کار:
- commandهای جدا:
- `vedic d1`
- `vedic panchanga`
- `vedic varga`
- `vedic dasha`
- `vedic transit`
- `vedic match`
- `vedic prediction`
- CLI فقط parse/validate/dispatch.

## 6) اولویت اجرا (ترتیب پیشنهادی دقیق)
1. Phase 0
2. Phase 1
3. Phase 2
4. Phase 3
5. Phase 5 (Dasha)  
6. Phase 4 (Analytics)  
7. Phase 6  
8. Phase 7  
9. Phase 8  
10. Phase 9

دلیل:
- بدون core+contracts، توسعه domainها debt تولید می‌کند.
- Dasha نیاز جدی کاربران است و باید بعد از varga و time-core بیاید.

## 7) تست و کیفیت
- `parity tests` با tolerance مشخص (deg/arcsec).
- `diagnose script` برای delta_arcsec (نه آپدیت کورکورانه expected).
- `schema validation` برای تمام خروجی‌ها.
- `no-swe-outside-context` guard test.
- `performance baseline` برای batch JSON generation.

## 8) ریسک‌ها و کنترل ریسک
- ریسک: drift در global-state SwissEph.  
کنترل: lock + baseline reset + single-context enforcement.

- ریسک: coupling CLI با نجوم.  
کنترل: service layer + strict command handlers.

- ریسک: explosion در option surface.  
کنترل: registry-driven choices + feature flags + fail-fast.

- ریسک: parity شکننده با fixtures ناسازگار.  
کنترل: diagnose-first workflow + provenance metadata در test fixtures.

## 9) Definition of Done نهایی (پروژه)
- تمام domainهای غیر GUI PyJHora endpoint JSON داشته باشند.
- برای هر domain حداقل یک contract versioned منتشر شده باشد.
- حداقل parity smoke برای هر domain برقرار باشد.
- هیچ `swe.set_*` خارج `context` وجود نداشته باشد.
- CLI ودیک full-surface با parse/validate تمیز ارائه شود.

## 10) قدم اجرایی بعدی (Immediate Next Sprint)
1. Freeze contracts for `panchanga.v1`, `varga.v1`, `dasha.v1`.
2. Implement `panchanga_service.py` + parity tests.
3. Implement `varga_service.py` batch API (all supported divisional charts).
4. Start `dasha_service.py` with `vimsottari` as first production system.
