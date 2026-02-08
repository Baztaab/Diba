# Kerykeion Config Architecture (Evidence-First)

Scope: only repo-local evidence. No inference without citation.

## 1) Entry points / CLI flow

### 1.1 CLI entry files
- CLI wrapper module: `kerykeion/cli.py` که dispatch/main را از `_cli.app` re-export می‌کند. Citation: `kerykeion/cli.py:1`, `kerykeion/cli.py:2`, `kerykeion/cli.py:5`.
- CLI runtime entry function: `dispatch()` در `kerykeion/_cli/app.py` که parser می‌سازد، args را parse می‌کند و command را dispatch می‌کند. Citation: `kerykeion/_cli/app.py:10`, `kerykeion/_cli/app.py:11`, `kerykeion/_cli/app.py:12`, `kerykeion/_cli/app.py:15`, `kerykeion/_cli/app.py:16`.
- `main()` در CLI با `sys.exit(dispatch(argv))` پایان می‌دهد. Citation: `kerykeion/_cli/app.py:30`, `kerykeion/_cli/app.py:31`.

### 1.2 Argument parsing / settings parsing
- Parser در `build_parser()` تعریف می‌شود و subcommand های `vedic` و `vedic d1` را می‌سازد. Citation: `kerykeion/_cli/options.py:97`, `kerykeion/_cli/options.py:98`, `kerykeion/_cli/options.py:99`, `kerykeion/_cli/options.py:101`, `kerykeion/_cli/options.py:102`, `kerykeion/_cli/options.py:104`.
- Defaults ورودی CLI برای config: `--ayanamsa` = `lahiri`، `--node-policy` = `mean`، `--house-system` = `whole-sign`. Citation: `kerykeion/_cli/options.py:121`, `kerykeion/_cli/options.py:122`, `kerykeion/_cli/options.py:123`.
- Validation/parsing لایه CLI در توابع جدا انجام می‌شود (`parse_ayanamsa`, `parse_node_policy`, `parse_house_system`, `parse_output_format`). Citation: `kerykeion/_cli/options.py:37`, `kerykeion/_cli/options.py:46`, `kerykeion/_cli/options.py:57`, `kerykeion/_cli/options.py:66`.

### 1.3 Config injection to lower layers
- `run_vedic_d1_command` مقادیر parsed را گرفته و به `VedicSubjectFactory.from_birth_data(...)` تزریق می‌کند (`ayanamsa_mode`, `node_policy`, `house_system`, `ephe_path`). Citation: `kerykeion/_cli/commands/vedic_d1.py:79`, `kerykeion/_cli/commands/vedic_d1.py:80`, `kerykeion/_cli/commands/vedic_d1.py:81`, `kerykeion/_cli/commands/vedic_d1.py:84`, `kerykeion/_cli/commands/vedic_d1.py:87`, `kerykeion/_cli/commands/vedic_d1.py:97`, `kerykeion/_cli/commands/vedic_d1.py:98`, `kerykeion/_cli/commands/vedic_d1.py:99`, `kerykeion/_cli/commands/vedic_d1.py:100`.
- Factory ورودی‌های string را به spec resolve می‌کند (`resolve_ayanamsa`, `resolve_house_system`) و context را می‌سازد؛ سپس `compute_core()` اجرا می‌شود. Citation: `kerykeion/vedic/factory.py:107`, `kerykeion/vedic/factory.py:108`, `kerykeion/vedic/factory.py:117`, `kerykeion/vedic/factory.py:123`, `kerykeion/vedic/factory.py:124`, `kerykeion/vedic/factory.py:127`.

## 2) Existing configuration patterns

### 2.1 Registry/spec/dataclass pattern
- Registry در `kerykeion/vedic/registry.py` با `@dataclass(frozen=True)` برای `AyanamsaSpec` و `HouseSystemSpec` تعریف شده است. Citation: `kerykeion/vedic/registry.py:17`, `kerykeion/vedic/registry.py:18`, `kerykeion/vedic/registry.py:24`, `kerykeion/vedic/registry.py:25`.
- داده‌های registry در `_AYANAMSA_DATA` و `_HOUSE_SYSTEM_DATA` تعریف و با `MappingProxyType` read-only می‌شوند. Citation: `kerykeion/vedic/registry.py:37`, `kerykeion/vedic/registry.py:42`, `kerykeion/vedic/registry.py:65`, `kerykeion/vedic/registry.py:66`.
- Resolverهای case-insensitive برای تبدیل input به spec وجود دارد. Citation: `kerykeion/vedic/registry.py:71`, `kerykeion/vedic/registry.py:76`, `kerykeion/vedic/registry.py:86`, `kerykeion/vedic/registry.py:91`.

### 2.2 Pattern: policy vs mechanism (examples)
- Example A (house policy): `HouseFetchPlan` policy تعریف می‌کند که house data فقط ASC باشد یا full cusps؛ mechanism در context با `houses_ex` اجرا می‌شود و براساس policy شاخه می‌زند. Citation: `kerykeion/vedic/registry.py:7`, `kerykeion/vedic/registry.py:13`, `kerykeion/vedic/registry.py:14`, `kerykeion/vedic/context.py:141`, `kerykeion/vedic/context.py:144`, `kerykeion/vedic/context.py:145`.
- Example B (node policy): policy در schema/context به `mean|true` محدود می‌شود و mechanism در context به `swe.MEAN_NODE` یا `swe.TRUE_NODE` map می‌شود. Citation: `kerykeion/schemas/kr_models.py:140`, `kerykeion/vedic/context.py:63`, `kerykeion/vedic/context.py:69`, `kerykeion/vedic/context.py:117`.
- Example C (ayanamsa policy): policy به صورت `AyanamsaSpec.swe_mode` از registry می‌آید؛ mechanism در context با `getattr(swe, swe_mode)` و `swe.set_sid_mode(...)` اعمال می‌شود. Citation: `kerykeion/vedic/registry.py:18`, `kerykeion/vedic/registry.py:20`, `kerykeion/vedic/registry.py:38`, `kerykeion/vedic/context.py:94`, `kerykeion/vedic/context.py:95`.

### 2.3 Defaults / versioning patterns
- Project/package version در `pyproject.toml` مشخص است (`5.7.0`). Citation: `pyproject.toml:1`, `pyproject.toml:3`.
- CLI defaults صریحاً در parser تعریف شده‌اند (ayanamsa/node/house). Citation: `kerykeion/_cli/options.py:121`, `kerykeion/_cli/options.py:122`, `kerykeion/_cli/options.py:123`.
- Registry defaults: `lahiri` و `whole_sign`. Citation: `kerykeion/vedic/registry.py:38`, `kerykeion/vedic/registry.py:43`.
- Context defaults هم‌راستا با registry آمده‌اند. Citation: `kerykeion/vedic/context.py:61`, `kerykeion/vedic/context.py:62`, `kerykeion/vedic/context.py:63`.
- Global settings defaults در constants مرکزی تعریف شده‌اند (مثال location defaults). Citation: `kerykeion/settings/config_constants.py:5`, `kerykeion/settings/config_constants.py:77`, `kerykeion/settings/config_constants.py:80`, `kerykeion/settings/config_constants.py:83`, `kerykeion/settings/config_constants.py:86`, `kerykeion/settings/config_constants.py:89`.
- Unknown/Not found in repo-local: هیچ schema/version migration داخلی ویژه برای config format (مثل `settings_version` field) در `KerykeionSettingsModel` دیده نشد. Citation: `kerykeion/schemas/settings_models.py:292`, `kerykeion/schemas/settings_models.py:297`.

## 3) SwissEph/global-state handling (relevant to settings)

### 3.1 Where `swe.set_*` is called (current runtime)
- فقط در `kerykeion/vedic/context.py`: `swe.set_ephe_path(...)`, `swe.set_sid_mode(...)`, و reset نهایی sid mode. Citation: `kerykeion/vedic/context.py:92`, `kerykeion/vedic/context.py:95`, `kerykeion/vedic/context.py:147`.
- Search evidence: `swe.set_*` در current package فقط همین نقاط را برمی‌گرداند. Citation: `kerykeion/vedic/context.py:92`, `kerykeion/vedic/context.py:95`, `kerykeion/vedic/context.py:147`.

### 3.2 Lock/context for global state
- یک lock سراسری `_SWE_LOCK = RLock()` وجود دارد و کل compute داخل `with _SWE_LOCK:` انجام می‌شود. Citation: `kerykeion/vedic/context.py:9`, `kerykeion/vedic/context.py:16`, `kerykeion/vedic/context.py:90`.
- Sidereal baseline reset بعد از محاسبه انجام می‌شود (`BASELINE_SID_MODE = swe.SIDM_LAHIRI`). Citation: `kerykeion/vedic/context.py:30`, `kerykeion/vedic/context.py:147`.

### 3.3 Legacy/archive handling for SwissEph state
- Legacy factory context-manager داشت (`ephemeris_context`) که `set_ephe_path`, `set_topo`, `set_sid_mode` را ست می‌کرد و topo را reset می‌کرد. Citation: `_archive/legacy_western/kerykeion/astrological_subject_factory.py:231`, `_archive/legacy_western/kerykeion/astrological_subject_factory.py:259`, `_archive/legacy_western/kerykeion/astrological_subject_factory.py:271`, `_archive/legacy_western/kerykeion/astrological_subject_factory.py:277`, `_archive/legacy_western/kerykeion/astrological_subject_factory.py:284`.
- همان legacy factory صراحتاً non-thread-safe بودن را اعلام کرده است. Citation: `_archive/legacy_western/kerykeion/astrological_subject_factory.py:561`, `_archive/legacy_western/kerykeion/astrological_subject_factory.py:562`, `_archive/legacy_western/kerykeion/astrological_subject_factory.py:563`, `_archive/legacy_western/kerykeion/astrological_subject_factory.py:564`.
- Legacy ayanamsa utilities lock/context جداگانه با restore mode داشتند. Citation: `_archive/legacy_western/kerykeion/ayanamsa.py:1`, `_archive/legacy_western/kerykeion/ayanamsa.py:2`, `_archive/legacy_western/kerykeion/ayanamsa.py:46`, `_archive/legacy_western/kerykeion/ayanamsa.py:107`, `_archive/legacy_western/kerykeion/ayanamsa.py:117`, `_archive/legacy_western/kerykeion/ayanamsa.py:124`.

## 4) Legacy/Archive mapping

### 4.1 Archive tree-level paths
- Top-level archive paths present in repo: `_archive/legacy_bridge`, `_archive/legacy_western`, `_archive/qa` (by existence of files under each path). Citation: `_archive/legacy_bridge/vedic_d1.py:1`, `_archive/legacy_western/kerykeion/siderealize.py:1`, `_archive/qa/test_vedic_vargas_parity_jhora.py:1`.
- `legacy_western` contains old module/test tree including `kerykeion/` and `tests/`, plus domain subfolders `aspects`, `charts`, `house_comparison`. Citation: `_archive/legacy_western/kerykeion/siderealize.py:1`, `_archive/legacy_western/tests/core/test_astrological_subject.py:1`, `_archive/legacy_western/kerykeion/aspects/aspects_factory.py:1`, `_archive/legacy_western/kerykeion/charts/chart_drawer.py:1`, `_archive/legacy_western/kerykeion/house_comparison/house_comparison_factory.py:1`.

### 4.2 Legacy modules related to config/cli/houses/ayanamsa/nodes
- Config-centric legacy wrapper: `_archive/legacy_western/kerykeion/backword.py` (explicit backward-compat shims + deprecation warnings + legacy node-name mapping). Citation: `_archive/legacy_western/kerykeion/backword.py:1`, `_archive/legacy_western/kerykeion/backword.py:20`, `_archive/legacy_western/kerykeion/backword.py:70`, `_archive/legacy_western/kerykeion/backword.py:71`.
- Ayanamsa legacy module: `_archive/legacy_western/kerykeion/ayanamsa.py` (thread-safe utilities with lock/context). Citation: `_archive/legacy_western/kerykeion/ayanamsa.py:1`, `_archive/legacy_western/kerykeion/ayanamsa.py:2`, `_archive/legacy_western/kerykeion/ayanamsa.py:46`, `_archive/legacy_western/kerykeion/ayanamsa.py:107`.
- Houses/nodes/config-in-one legacy factory: `_archive/legacy_western/kerykeion/astrological_subject_factory.py` (supports multiple house systems, sidereal modes, node points). Citation: `_archive/legacy_western/kerykeion/astrological_subject_factory.py:11`, `_archive/legacy_western/kerykeion/astrological_subject_factory.py:15`, `_archive/legacy_western/kerykeion/astrological_subject_factory.py:16`, `_archive/legacy_western/kerykeion/astrological_subject_factory.py:24`.
- Legacy sidereal bridge: `_archive/legacy_western/kerykeion/siderealize.py` (explicitly legacy facade؛ canonical compute در `kerykeion.vedic.context`). Citation: `_archive/legacy_western/kerykeion/siderealize.py:1`, `_archive/legacy_western/kerykeion/siderealize.py:2`, `_archive/legacy_western/kerykeion/siderealize.py:5`, `_archive/legacy_western/kerykeion/siderealize.py:59`.
- Legacy bridge helper for D1: `_archive/legacy_bridge/vedic_d1.py` (legacy helper rewritten to canonical context؛ no direct SwissEph). Citation: `_archive/legacy_bridge/vedic_d1.py:1`, `_archive/legacy_bridge/vedic_d1.py:2`, `_archive/legacy_bridge/vedic_d1.py:4`.

### 4.3 Why each is legacy (only repo-local stated reasons)
- `_archive/legacy_western/kerykeion/siderealize.py`: explicitly says legacy facade and canonical path moved to `kerykeion.vedic.context`. Citation: `_archive/legacy_western/kerykeion/siderealize.py:2`, `_archive/legacy_western/kerykeion/siderealize.py:5`, `_archive/legacy_western/kerykeion/siderealize.py:59`.
- `_archive/legacy_bridge/vedic_d1.py`: explicitly says legacy helper rewritten to canonical context and no direct SwissEph calls. Citation: `_archive/legacy_bridge/vedic_d1.py:2`, `_archive/legacy_bridge/vedic_d1.py:4`.
- `_archive/legacy_western/kerykeion/backword.py`: explicitly backward-compatibility shims + deprecation warnings. Citation: `_archive/legacy_western/kerykeion/backword.py:1`, `_archive/legacy_western/kerykeion/backword.py:20`, `_archive/legacy_western/kerykeion/backword.py:62`, `_archive/legacy_western/kerykeion/backword.py:64`.
- Repo docs describe migration target as Vedic-only and moving/removing Western modules to archive. Citation: `docs/repo_vedic_equivalency_map.md:8`, `docs/repo_vedic_equivalency_map.md:179`, `docs/kerykeion_arch_audit.md:4`, `docs/kerykeion_arch_audit.md:33`.
- Unknown/Not found in repo-local: دلیل‌های مبتنی بر commit messages برای هر فایل legacy (commit message در repo-local report extraction حاضر نیست).

## 5) Summary: How Kerykeion historically did it

### 5.1 10-15 line summary
- معماری فعلی CLI سبک command-dispatch دارد: `cli.py -> _cli.app.dispatch -> _cli.commands.vedic_d1`. Citation: `kerykeion/cli.py:5`, `kerykeion/_cli/app.py:10`, `kerykeion/_cli/app.py:16`, `kerykeion/_cli/commands/vedic_d1.py:65`.
- Parsing و validation اولیه در `_cli/options.py` انجام می‌شود و پیش از ورود به domain کنترل می‌گردد. Citation: `kerykeion/_cli/options.py:37`, `kerykeion/_cli/options.py:46`, `kerykeion/_cli/options.py:57`.
- Config domain به‌صورت spec/dataclass در registry نگه‌داری می‌شود، نه به‌صورت stringهای آزاد. Citation: `kerykeion/vedic/registry.py:17`, `kerykeion/vedic/registry.py:24`, `kerykeion/vedic/registry.py:71`, `kerykeion/vedic/registry.py:86`.
- Factory نقش orchestrator دارد: normalize/validate ورودی، resolve policy، ساخت context، و تولید model خروجی. Citation: `kerykeion/vedic/factory.py:30`, `kerykeion/vedic/factory.py:107`, `kerykeion/vedic/factory.py:117`, `kerykeion/vedic/factory.py:129`, `kerykeion/vedic/factory.py:136`.
- مکانیزم SwissEph عملاً در یک نقطه canonical متمرکز شده (`VedicCalculationContext`). Citation: `kerykeion/vedic/context.py:2`, `kerykeion/vedic/context.py:66`, `kerykeion/vedic/context.py:92`, `kerykeion/vedic/context.py:95`.
- Global state ریسک‌دار SwissEph با lock و baseline reset کنترل می‌شود. Citation: `kerykeion/vedic/context.py:16`, `kerykeion/vedic/context.py:90`, `kerykeion/vedic/context.py:147`.
- Legacy معماری قبلی (Western + backward shims) به `_archive` منتقل شده و در متن فایل‌ها با واژه `Legacy`/`Backward compatibility` مشخص است. Citation: `_archive/legacy_western/kerykeion/siderealize.py:2`, `_archive/legacy_western/kerykeion/backword.py:1`, `_archive/legacy_bridge/vedic_d1.py:2`.
- در v4->v5 migration، حذف کلاس‌های قدیمی و داشتن compatibility layer موقت صراحتاً documented شده بود. Citation: `MIGRATION_V4_TO_V5.md:11`, `MIGRATION_V4_TO_V5.md:13`, `MIGRATION_V4_TO_V5.md:23`.
- API عمومی فعلی package به‌صورت Vedic-only اکسپورت می‌شود. Citation: `kerykeion/__init__.py:3`, `kerykeion/__init__.py:5`, `kerykeion/__init__.py:8`, `kerykeion/__init__.py:9`.

### 5.2 Three implicit rules in current architecture (with evidence)
1. Rule: policyها باید validate/resolved شوند قبل از SwissEph call. Citation: `kerykeion/vedic/factory.py:107`, `kerykeion/vedic/factory.py:108`, `kerykeion/vedic/factory.py:109`, `kerykeion/vedic/registry.py:71`, `kerykeion/vedic/registry.py:86`.
2. Rule: SwissEph global-state باید centralized و lock-protected باشد. Citation: `kerykeion/vedic/context.py:16`, `kerykeion/vedic/context.py:90`, `kerykeion/vedic/context.py:92`, `kerykeion/vedic/context.py:95`, `kerykeion/vedic/context.py:147`.
3. Rule: defaults باید explicit و discoverable باشند (CLI + registry + constants). Citation: `kerykeion/_cli/options.py:121`, `kerykeion/_cli/options.py:122`, `kerykeion/_cli/options.py:123`, `kerykeion/vedic/registry.py:38`, `kerykeion/vedic/registry.py:43`, `kerykeion/settings/config_constants.py:77`.

### 5.3 Three traps / anti-patterns to avoid
1. Anti-pattern: پخش‌کردن `swe.set_*` در چند ماژول (global-state drift). Counter-evidence in current core: single location in context. Citation: `kerykeion/vedic/context.py:92`, `kerykeion/vedic/context.py:95`, `kerykeion/vedic/context.py:147`.
2. Anti-pattern: نگه‌داشتن facadeهای legacy در runtime اصلی به‌جای migration کامل. Legacy files explicitly mark facade/backward-compat. Citation: `_archive/legacy_western/kerykeion/siderealize.py:2`, `_archive/legacy_western/kerykeion/backword.py:1`, `_archive/legacy_western/kerykeion/backword.py:20`.
3. Anti-pattern: coupling زیاد بین output formatting/CLI و computation core. Current separation exists (`_cli` + `factory` + `context`), باید حفظ شود. Citation: `kerykeion/_cli/app.py:16`, `kerykeion/_cli/commands/vedic_d1.py:87`, `kerykeion/vedic/factory.py:117`, `kerykeion/vedic/context.py:66`.
