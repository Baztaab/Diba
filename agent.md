Diba Chart‑Engine Architecture Options
Step 1 – Parity‑critical constraints from Sweep 2

The sweep_2_architecture_coupling_contract_map.md document lists evidence anchors (E##) that describe how the existing PyJHora implementation interacts with the Swiss Ephemeris and how time conversions and global state are handled. These facts are non‑negotiable for Diba because they ensure behavioural parity with the legacy engine.

Time basis and Julian Date conversions

JD_UTC definition – In PyJHora, sidereal longitude functions expect a UT‑based Julian day (jd_utc), which is computed from the civil Julian day using the place’s time‑zone offset (jd_utc = jd – place.timezone / 24). This conversion is repeated at many call sites such as planets_in_retrograde. Diba must explicitly separate jd (civil day) and jd_utc (UT day) at API boundaries.

Sunrise pipeline – The sunrise calculation constructs a date‑based jd_utc using swe.utc_time_zone and swe.utc_to_jd(..., 0). swe.rise_trans is called on this UT JD to compute sunrise, which is then fed back into the Julian‑day arithmetic. This demonstrates that different computations require distinct time bases (date vs continuous JD) and that UT offsets must be supplied explicitly.

Local‑time conversion – local_time_to_jdut1() converts a local date/time into UT1 by passing the timezone offset and zero delta T to swe.utc_to_jd(..., 0). Diba needs a clear API to translate between local time, civil JD and UT1.

Swiss Ephemeris integration

calc_ut contract – All planetary positions are computed via swe.calc_ut(jd_utc, flag) and the result’s longitude is normalized to 0–360°. Rahu/Ketu are represented by negating or selecting specific constants (e.g., swe.MEAN_NODE); the speed component in the returned vector is used to detect retrograde motion. Diba must replicate the normalization and node conventions.

Ephemeris path – The Swiss Ephemeris data path is set at import time (swe.set_ephe_path). Diba must provide a way to configure the ephemeris path before any ephemeris calls.

Sidereal mode and global state

set_sid_mode mutates global state – Calls to set_ayanamsa_mode wrap swe.set_sid_mode and mutate a module‑level constant (const._DEFAULT_AYANAMSA_MODE). Some functions (e.g., sidereal_longitude) save the current mode and reset it afterwards, while others (e.g., bhaava_madhya_kp, bhaava_madhya_swe) do not reset the mode. Diba must control this mutable global state through scoped contexts or explicit reset mechanisms to avoid unintended side effects.

House functions compute jd_utc but use civil jd for set_sid_mode – The bhaava_madhya_kp and bhaava_madhya_swe functions compute jd_utc = jd – tz/24, call set_sid_mode(jd), call swe.houses_ex(jd_utc, lat, lon, ...) and never reset the sidereal mode. This discrepancy (using jd instead of jd_utc for the sidereal epoch and omitting a reset) must be preserved or consciously replaced by a policy (open question) but cannot be ignored.

Varga and mixed charts

Divisional chart dispatch – The varga engine maps standard Dₙ functions via a dispatch table; mixed charts compose two varga stages and custom charts call custom_divisional_chart. Diba must allow method‑specific dispatching without hard‑coding a monolithic switch.

Panchanga & transit coupling

Sunrise anchored elements – Panchanga functions compute lunar phases (tithi, yoga, etc.) relative to the sunrise computed via sunrise(), and local_time_to_jdut1() uses UT conversions. This coupling means any change to sunrise computation must propagate consistently across panchanga and transit calculations.

These facts constitute the baseline contract that Diba’s architecture must respect. Any option proposed in Step 4 explicitly explains how each fact is preserved or addressed.

Step 2 – Candidate open‑source chart engines and architectural evidence

Below are ten open‑source chart computation engines (five Vedic and five Western/Tropical) inspected for architectural patterns. For each, the summary focuses on repository layout, separation of concerns, data modeling, time handling, ephemeris integration, and testing signals.

Vedic engines

VedicAstro (Python, diliprk/VedicAstro) – wraps the Flatlib library to provide Krishnamurti‑style charts. The repository contains modules such as VedicAstro.py, horary_chart.py and utils.py. The VedicHoroscopeData class stores input parameters (year, month, day, time, latitude, longitude, timezone, ayanamsa, house system) and lazily computes a flatlib.Chart object; timezone lookup uses TimezoneFinder, and UT offset is calculated via get_utc_offset. The generate_chart method constructs a flatlib.Chart using Datetime and GeoPos objects and passes the user’s house system and sidereal mode. Subsequent methods compute aspects or Vedic aspects by iterating over planets and applying custom rules. The repository uses global dictionaries for mappings (house systems, ayanamsas, aspects) and returns results as named‑tuple collections or Polars DataFrames. Time handling and ephemeris access are delegated to Flatlib; there is no global mutable state within this wrapper.

Horary chart module (VedicAstro’s horary_chart.py) – demonstrates manual Swiss Ephemeris integration. It imports swisseph directly and reads a CSV of sub‑lord divisions. Functions convert Julian days to Python datetime objects using swe.jdut1_to_utc and swe.utc_time_zone. The find_exact_ascendant_time function sets the sidereal mode (swe.set_sid_mode) before iterating over JD times and calling swe.houses_ex. It uses adaptive step sizes to search for the ascendant and converts the resulting JD back to a timezone‑corrected datetime. This module shows a more imperative approach with global constants and mutable state.

VedAstro (C#, VedAstro/VedAstro) – a large Vedic astrology project with separate components for the API, website, library, and console. The repository’s README explains that the core library works by combining event data (XML) with calculation logic to produce predictions; events are stored in XML, and each event has an enum value that links to a static calculator method, executed over a time slice to determine occurrences. The design emphasises modularity: the library is independent and used by the API and website; predictions are generated in the API rather than the client to avoid heavy browser CPU usage. Design notes recommend using structs instead of classes for small immutable data to reduce memory overhead. Although not all ephemeris calls are visible, the project shows a strong separation between data (XML) and logic (static methods) and uses enumerations and typed structures.

Core Astrology Engine (Python, core‑astrology‑engine) – a PyPI package claiming to be a production‑ready Vedic calculation library. The documentation notes Swiss Ephemeris integration with verified precision, batch processing with parallel computation, automatic timezone detection, and configurable options for dashas and panchanga. It exposes high‑level functions such as get_birth_chart, get_current_dasha, and a BatchProcessor for parallel chart generation. Although the source code is not accessible, the API indicates a layered design with a user‑facing facade (SimpleAstrology) over internal calculation modules, and shows that ephemeris integration, time handling and dasha computations are encapsulated behind simple function calls.

Jyotishganit (Python) – a high‑precision Vedic library built on NASA JPL ephemeris data via Skyfield. The library provides complete D₁–D₆₀ divisional charts, panchanga elements and Vimshottari dasha. Its features include “astronomical precision using JPL DE421 via Skyfield,” cross‑platform ephemeris storage, and JSON‑LD outputs. The quick‑start example shows a calculate_birth_chart function that accepts a datetime, latitude, longitude, timezone offset and optional name; it returns a chart object with houses, planets and panchanga, and can be serialized to JSON. This indicates a design focused on pure functions, stateless ephemeris calls via Skyfield, and structured outputs.

Western/Tropical engines

Flatlib (Python) – a widely used Western astrology library. The flatlib/datetime.py module defines Date, Time and Datetime classes that compute the Julian day as date.jdn + time.value/24 – utcoffset.value/24 – 0.5; the Datetime.jd property returns this UT‑based JD. The flatlib/ephem/swe.py module wraps Swiss Ephemeris functions such as calc_ut, houses and houses_ex, mapping internal enumerations to Swiss constants and converting results into friendly dictionaries. Flatlib uses a functional core: chart.py (not shown) assembles charts by calling these wrappers; there is no global sidereal state because Flatlib exposes ayanamsas and house systems as explicit parameters. Data is represented by simple classes (objects for planets and houses) with typed attributes; users can request tropical or sidereal zodiacs by passing modes into chart constructors.

Kerykeion (Python) – a modern library with strong typing and layered factories. The repository has modules such as charts, aspects, settings, schemas, and factory classes (ephemeris_data_factory.py, astrological_subject_factory.py). EphemerisDataFactory generates series of ephemeris data over a date range, taking parameters like step size, zodiac type (tropical or sidereal), sidereal mode, house system and perspective. It enforces safety limits on the range to prevent accidental heavy computations and returns typed models using Pydantic schemas. Settings such as default objects to include in charts are stored in a centralized configuration module; users may override these through dependency injection. The design clearly separates computation factories from presentation (SVG rendering) and uses Python type hints extensively.

Immanuel‑Python (theriftlab/immanuel) – a chart‑centric library that wraps Swiss Ephemeris and Astro.com style calculations. The README explains that the package offers classes such as Subject, Natal, SolarReturn, etc., that accept a date/time and location; passing a Subject into charts.Natal() returns an instance containing all planets, points, signs, houses, aspects and dignity scores. Users can customize which celestial objects are included by appending constants to the settings.objects list. The library provides a built‑in serializer to output chart data as human‑readable text or JSON. This design encapsulates ephemeris state behind chart classes and uses a settings module for global configuration, enabling reproducibility and testability.

Natal Engine (Node.js) – described in its README as a Node library that calculates Western astrology, Human Design and Gene Keys. The API function calculateAstrology(birthDate, birthHour, timezone, latitude?, longitude?) returns structured data including sun, moon, rising, planets, nodes and aspects. Although the code is in TypeScript/JavaScript (not fully inspected), it implies a single entry point that encapsulates time conversions, ephemeris calls and chart assembly. The library returns objects keyed by planet names and uses arrays for houses and aspects, signalling a data‑oriented design.

Astronomy Engine (multi‑language, cosinekitty/astronomy) – not strictly an astrology engine but a high‑precision astronomical library used by many chart programs. The repository claims to offer vector coordinate transforms, eclipse search functions and planetary motion using algorithms from Jean Meeus and NASA ephemerides. The library is implemented in multiple languages (C, C#, Python, JavaScript); each wrapper calls a shared core. It uses pure functions and immutable vectors, making it thread‑safe and deterministic. Several chart engines adopt this library instead of Swiss Ephemeris to avoid global state.

These projects provide diverse examples of modularization, state management, data modeling and ephemeris integration that inform the patterns distilled in Step 3.

Step 3 – Transferable architecture patterns

The following patterns are distilled from the above projects and mapped to specific Diba problems identified in Step 1. Each pattern is named, linked to at least one example project and explains why it improves upon naive approaches.

Explicit Time Context Objects – Diba must manage multiple time bases (civil JD, UT JD, local time). In Flatlib, the Datetime class encapsulates date, time and UTC offset and exposes a jd property that computes the UT‑based Julian day. Kerykeion’s factories accept datetime objects and return typed models; Immanuel uses a Subject class to hold the timestamp. Encapsulating time conversions in a dedicated TimeContext class prevents accidental mixing of jd and jd_utc and makes the conversion explicit at module boundaries. Without this, functions may misuse jd when jd_utc is required (as in PyJHora’s house functions).

Ephemeris Session/Adapter – Instead of calling Swiss Ephemeris functions directly, wrap them in a thin adapter that exposes stateless functions and hides global state. Flatlib’s ephem/swe.py maps internal object IDs to Swiss constants and returns dictionaries. Kerykeion uses an EphemerisDataFactory to produce series of positions with specified step sizes and sidereal modes. By creating an EphemerisSession in Diba that loads the ephemeris path, holds a per‑request sidereal mode and resets it on exit, we can contain the mutation of swe.set_sid_mode and guarantee reproducibility.

Sidereal Mode Context Manager – Several projects (e.g., VedicAstro’s VedicAstro.py and horary_chart.py) call swe.set_sid_mode without resetting it, leading to hidden state. A pattern observed in PyJHora’s sidereal_longitude is to save the current mode, set a new mode for the computation and restore it afterwards. Generalising this into a context manager ensures the global sidereal state is always reset even if an exception occurs. This pattern prevents cross‑call leakage and supports concurrent sessions.

Functional Pipelines for Chart Assembly – Flatlib and Jyotishganit assemble charts by piping pure functions: compute planetary positions, compute houses, compute aspects, then package results into data structures. Jyotishganit’s calculate_birth_chart returns a chart object with nested d1_chart, panchanga and divisional_charts components. This modular pipeline makes each stage testable and allows swapping algorithms (e.g., KP vs Swiss house calculation) without affecting other stages.

Type‑safe Data Models – Kerykeion defines Pydantic schemas for celestial objects and returns structured models. Immanuel’s Subject and Natal classes use typed attributes and provide JSON serialization. Strong typing improves documentation, IDE support and testability. Diba can adopt dataclasses or Pydantic models to represent graha positions, houses, varga charts and panchanga elements, ensuring that each field is validated and units are explicit.

Configuration & Settings Capsule – Immanuel exposes a settings module where users append objects (e.g., adding Ceres), and Kerykeion centralizes default objects and zodiac types in a settings file. This pattern avoids scattering configuration flags throughout the code and allows future extensions (new grahas, different ayanamsas) to be added declaratively. Diba should have a single configuration capsule that defines default ephemeris path, ayanamsa, house system and object list, with typed enumerations.

Data + Logic Separation (Event = Data × Logic) – VedAstro’s core library describes events as the product of data (stored in XML and enumerations) and logic (static calculator methods) evaluated over a time range. This separation allows new events (e.g., auspicious timings) to be added by writing a new calculator method and corresponding data entry, without modifying the event engine. Diba can adopt a similar pattern for panchanga and transit computations: data tables of tithi/nakshatra rules plus functions that evaluate them against computed positions.

Batch and Parallel Processing – Core Astrology Engine supports batch processing with a BatchProcessor that accepts a list of BatchRequest objects and spawns multiple workers. This pattern is useful for server‑side or batch chart generation and ensures that ephemeris calculations are parallelizable when state is contained per session. Diba’s architecture should allow concurrency by avoiding module‑level mutation.

Facade API with Clear Boundaries – VedicAstro exposes a high‑level VedicHoroscopeData class that hides the complexity of constructing Flatlib charts; Immanuel exposes charts.Natal, charts.SolarReturn, etc. Core Astrology Engine provides one‑line functions like get_birth_chart. This pattern simplifies user interaction and enforces layering: the facade depends on lower layers (time context, ephemeris adapter, chart pipelines) but not vice versa.

Global Configuration vs Per‑call Overrides – Some libraries (Immanuel) allow users to override global settings (e.g., adding Ceres) at runtime, while others (Flatlib) require explicit parameters. This highlights a trade‑off: global settings ease convenience but risk hidden coupling; per‑call overrides provide reproducibility but require more parameters. Diba should design configuration injection explicitly—perhaps using a configuration object that is passed through the pipeline and can be overridden for a specific call.

These patterns provide a vocabulary for constructing the architecture options described next.

Step 4 – Architecture options for Diba

Each option below is materially different and addresses the parity‑critical constraints from Step 1 while leveraging patterns from Step 3. All options define clean module boundaries, explicit dependency directions and mechanisms to contain Swiss Ephemeris global state. The diagrams are conceptual; actual file names and modules may differ.

Option 1 – Layered Functional Core with Context Managers

Summary – Build Diba as a functional pipeline where each layer performs a deterministic transformation: TimeContext → EphemerisSession → GrahaPipeline → HousesPipeline → VargaEngine → Panchanga/Transit. Swiss Ephemeris calls are wrapped in an EphemerisSession that manages the ephemeris path and sidereal mode via a context manager. Each pipeline consumes typed data models and produces new models. A high‑level facade constructs and coordinates the pipelines.

Module map and dependencies
graph TD
    ClientFacade --> TimeContext
    ClientFacade --> ConfigCapsule
    TimeContext -->|produces| JD_UTC
    EphemerisSession -->|reads| ConfigCapsule
    JD_UTC --> EphemerisSession
    EphemerisSession --> GrahaPipeline
    GrahaPipeline --> HousesPipeline
    GrahaPipeline --> VargaEngine
    HousesPipeline --> VargaEngine
    VargaEngine --> PanchangaTransit
    EphemerisSession --> SiderealStateContext
    SiderealStateContext --> EphemerisSession


Mapping to parity facts

The TimeContext encapsulates civil date/time, timezone and computes jd and jd_utc explicitly, preserving the JD vs JD_UTC separation. Each downstream layer depends on the jd_utc output.

EphemerisSession loads the Swiss Ephemeris path at initialization and offers methods like calc_ut, houses_ex, rise_trans, etc., returning normalized positions and speeds. It enters a SiderealStateContext (a context manager) that sets the ayanamsa mode before the call and restores it afterwards, addressing the global mutation issues in PyJHora.

GrahaPipeline computes planetary longitudes and states by calling EphemerisSession.calc_ut and using the sign of the speed component for retrograde detection. It applies Rahu/Ketu mapping conventions.

HousesPipeline computes ascendant and cusps by calling EphemerisSession.houses_ex with the UT JD and receives the ayanamsa from the sidereal context. Because the context manager resets the mode, misusing jd instead of jd_utc cannot occur.

VargaEngine dispatches to specific divisional chart functions based on a routing table (pattern 4) and can compose mixed charts.

PanchangaTransit uses the sunrise function from the EphemerisSession to compute tithi, yoga, etc., thus coupling to the same time basis used by TimeContext.

Scope‑creep guard – Each pipeline operates on typed models and returns immutable results; no pipeline is allowed to import from the layers above. New features (dashas, transits) must be added by creating new pipelines that depend on existing models but cannot mutate them. This guard prevents adding ad‑hoc parameters to core functions.

Pros

Deterministic and testable; each stage is a pure function given a context.

Context managers ensure global sidereal state is contained; concurrent sessions can run without interference.

Typed data models improve clarity and support future static analysis.

Extensible: new graha calculators or house methods can be inserted by replacing pipeline functions.

Cons

Functional composition may introduce performance overhead due to object creation and copying.

Strict separation means some cross‑cutting concerns (e.g., caching) require an additional layer or middleware.

Requires developers to understand the pipeline architecture; may feel heavy for simple scripts.

Failure modes / risks

If the SiderealStateContext fails to restore the sidereal mode (e.g., due to a programmer bypassing the context), global state may leak, replicating PyJHora’s bug.

Misconfigured TimeContext (wrong timezone) will propagate incorrect jd_utc values to all downstream computations; unit tests must guard against this.

Future readiness

Adding dashas or transits becomes easy: implement new pipelines that consume the GrahaPipeline and HousesPipeline outputs. Because time context is explicit, batch processing and server handling only require parallelizing independent pipelines.

To support alternate ephemerides (e.g., Astronomy Engine), implement a new EphemerisSession that respects the same interface.

Minimal validation plan

Unit tests for TimeContext verifying correct JD and JD_UTC conversion across a range of time zones.

Tests for EphemerisSession ensuring that sidereal mode is restored after calls and that outputs match PyJHora for known dates.

Pipeline integration tests comparing Diba’s outputs with PyJHora across sample charts (rasi, divisional, panchanga) to confirm parity.

Option 2 – Configurable Object Graph with Dependency Injection

Summary – Adopt a dependency‑injection (DI) approach where each component (time converter, ephemeris adapter, sidereal state manager, graha calculator, house calculator, varga router, panchanga engine) is defined as an interface (abstract base class) with one or more concrete implementations. A configuration object wires the implementations together at runtime. This allows alternative algorithms (e.g., Swiss vs Skyfield ephemeris, KP vs Placidus houses) to be swapped without modifying consumers. The DI container also carries per‑request state such as sidereal mode, ephemeris path and selected objects.

Module map and dependencies
graph TD
    ConfigCapsule -->|binds| TimeConverter
    ConfigCapsule -->|binds| EphemerisAdapter
    ConfigCapsule -->|binds| SiderealStateManager
    ConfigCapsule -->|binds| GrahaCalculator
    ConfigCapsule -->|binds| HousesCalculator
    ConfigCapsule -->|binds| VargaRouter
    ConfigCapsule -->|binds| PanchangaEngine
    ClientFacade --> ConfigCapsule
    ClientFacade --> TimeConverter
    ClientFacade --> GrahaCalculator
    GrahaCalculator --> EphemerisAdapter
    HousesCalculator --> EphemerisAdapter
    VargaRouter --> GrahaCalculator
    VargaRouter --> HousesCalculator
    SiderealStateManager --> EphemerisAdapter
    PanchangaEngine --> TimeConverter
    PanchangaEngine --> EphemerisAdapter
Mapping to parity facts
The TimeConverter interface defines methods to_jd(dt), to_jd_utc(dt), local_to_ut(dt, tz) and returns both jd and jd_utc. Implementations can use Swiss Ephemeris or standard Python libraries but must conform to the conversion rules.

EphemerisAdapter exposes methods calc_ut, houses_ex, rise_trans. Concrete implementations wrap Swiss Ephemeris or Skyfield; they accept a SiderealStateManager dependency that sets and resets the mode. The adapter ensures that Rahu/Ketu mapping and longitude normalization are applied.

SiderealStateManager centralizes calls to swe.set_sid_mode and swe.set_ephe_path. It can implement the context‑manager pattern or maintain state in an object rather than a module.

GrahaCalculator uses the ephemeris adapter to compute graha positions and states. HousesCalculator computes houses using the chosen house system; the DI container can inject either KP or Swiss algorithms, addressing the call‑site discrepancies where house functions use jd vs jd_utc.

VargaRouter holds a map of divisional chart functions (pattern 4); injecting a new implementation for a specific Dₙ automatically updates the router without modifying the core.

PanchangaEngine uses TimeConverter to compute sunrise and then derives tithi, yoga, etc.; it can be replaced by a different engine (e.g., one based on Jyotishganit) by updating the bindings.

Scope‑creep guard – All constructors enforce explicit parameter injection; default bindings live in a single configuration file. Adding new global flags is prohibited; instead, developers must add new interfaces and provide implementations. This prevents hidden global state and encourages modular growth.

Pros

High flexibility: alternative algorithms or ephemerides can be swapped by changing configuration. Useful for experimenting with Skyfield vs Swiss Ephemeris or different sidereal modes.

Encourages clear contracts and unit‑testable components. Each interface can have multiple implementations with their own tests.

Aligns with modern frameworks (FastAPI, dependency‑injector) and scales to server/batch contexts.

Cons

Increased complexity: developers must understand DI patterns and maintain configuration files.

Potential runtime overhead if the container is created per request; caching may be required.

Over‑abstraction could obscure simple flows and make debugging harder.

Failure modes / risks

Misconfigured bindings could wire incompatible implementations (e.g., a Graha calculator expecting UT JD but receiving a different time converter). Comprehensive integration tests are needed.

If an implementation fails to reset the sidereal mode, cross‑component contamination may occur; the DI container cannot enforce correct usage automatically.

Future readiness

Ideal for introducing new chart families (dashas, transits, batch) by defining new interfaces (e.g., DashaEngine) and binding them. Because components are decoupled, adding concurrency is straightforward.

Enables external contributions: third parties can implement their own EphemerisAdapter or VargaRouter and register it.

Minimal validation plan

Tests that the default configuration reproduces PyJHora results across sample charts.

Integration tests that swap in alternative implementations (e.g., Skyfield) and verify outputs remain consistent within tolerance.

Tests to ensure SiderealStateManager resets the global state after each call.

Option 3 – Stateful Engine with Immutable Snapshots

Summary – Create a stateful chart engine object that encapsulates the entire computation session (time context, ephemeris state, ayanamsa, selected objects, algorithm choices). Each call to compute a chart returns an immutable snapshot of results along with metadata describing the configuration used. The engine tracks the sidereal mode internally and provides explicit reset() methods. While less functional than Option 1, this model simplifies usage by bundling state and behaviour in a single object.
Module map and dependencies
graph TD
    ChartEngine --> TimeContext
    ChartEngine --> EphemerisState
    ChartEngine --> GrahaComputer
    ChartEngine --> HouseComputer
    ChartEngine --> VargaComputer
    ChartEngine --> PanchangaComputer
    EphemerisState -->|sets/resets| SwissEph
    GrahaComputer --> EphemerisState
    HouseComputer --> EphemerisState
    VargaComputer --> GrahaComputer
    VargaComputer --> HouseComputer
    PanchangaComputer --> TimeContext
    PanchangaComputer --> EphemerisState
Mapping to parity facts
ChartEngine holds attributes for ephemeris path, ayanamsa, house system and selected objects. When compute_chart() is called with a date/time and location, it creates a TimeContext that stores jd and jd_utc and passes it to internal computers. This encapsulation ensures jd vs jd_utc separation.

EphemerisState sets the ephemeris path on initialization and exposes methods set_sid_mode(jd_epoch) and reset_sid_mode(). Each computer calls EphemerisState.set_sid_mode with the correct epoch (for houses this may be jd_utc or jd, matching PyJHora’s behaviour). After the engine finishes computations, reset_sid_mode() is called.

GrahaComputer computes planet positions and speeds using swisseph.calc_ut, applying Rahu/Ketu mapping and normalizing angles. HouseComputer computes houses and ascendant using swisseph.houses_ex and can choose between KP or Placidus algorithms.

VargaComputer dispatches divisional chart functions and caches results to avoid recomputation. PanchangaComputer calculates tithi and sunrise using swisseph.rise_trans and the TimeContext.

Each result snapshot includes a metadata header (date, timezone, ayanamsa, house system, object list) to ensure reproducibility and auditability.

Scope‑creep guard – The ChartEngine’s public API is minimal: methods to set configuration, compute charts, reset state and export snapshots. New features must be added as separate methods that do not mutate existing snapshots. Attempting to modify internal state after computing a chart raises an error.

Pros

Simple mental model for users: instantiate an engine with desired configuration and call compute_chart(). Good for scripting and interactive sessions.

Encapsulation avoids passing configuration objects around and reduces the number of parameters in method signatures.

The snapshot metadata provides audit trails and supports caching; identical configurations yield cache hits.

Cons

Stateful design makes concurrent use more challenging; each thread must own its own engine instance.

If developers bypass reset_sid_mode(), state leaks could occur; the object must carefully manage its lifecycle.

Extending to server contexts may require pool management of engine instances, adding complexity.

Failure modes / risks

Misuse of the engine (e.g., calling compute_chart() after modifying internal settings without resetting) could lead to inconsistent results.

Large numbers of snapshots may consume memory; careful caching and disposal are required.

Future readiness

Adding new families (dashas, transits) means adding new computation methods that reuse existing state. Because the engine holds configuration, new methods can easily access needed context.

Suitable for interactive notebooks or desktop applications where stateful sessions are natural.

Minimal validation plan

Tests verifying that repeated calls with identical configuration and inputs return identical snapshots.

Tests ensuring that changing the ayanamsa or house system triggers a reset and yields different results.

Tests to ensure EphemerisState resets the sidereal mode after each computation.

Comparison summary

Option 1 uses a functional pipeline with context managers. It offers high testability and concurrency but requires strict adherence to pure functions and may feel heavy for simple tasks.

Option 2 relies on dependency injection to configure interchangeable components. It maximizes flexibility but introduces configuration complexity and risks miswiring.

Option 3 uses a stateful engine with immutable snapshots. It provides a simple facade and auditability but is less suitable for concurrent server environments and relies on disciplined state management.

Each option addresses the parity‑critical constraints and leverages patterns from open‑source engines. The choice depends on Diba’s priorities: testability and concurrency (Option 1), configurability and extensibility (Option 2), or simplicity and encapsulated state (Option 3).
It outlines the parity-critical coupling constraints from PyJHora, surveys five Vedic and five tropical open-source chart engines for architectural evidence, distills ten transferable design patterns, and proposes three distinct architecture options for Diba—functional pipelines with context managers, a dependency-injection object graph, and a stateful engine with immutable snapshots—each mapped to the identified constraints, with pros/cons, risk analysis and future readiness. Let me know if you need any changes or further exploration.