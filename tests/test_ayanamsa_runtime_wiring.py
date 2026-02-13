from __future__ import annotations

from diba.domain.models.common import BirthData, PlaceInput
from diba.engine import AstrologySettings, AstronomyContext, DibaEngine


def _birth() -> BirthData:
    return BirthData(
        year=1990,
        month=1,
        day=1,
        hour=12,
        minute=0,
        seconds=0.0,
        tz_str="UTC",
        place=PlaceInput(lat=0.0, lon=0.0, altitude=0.0),
    )


def test_engine_runtime_resolves_multiple_ayanamsa_modes() -> None:
    ids = ["lahiri", "raman", "true_citra"]
    values = []
    for ayanamsa_id in ids:
        engine = DibaEngine(
            session_ctx=AstronomyContext(),
            astro_settings=AstrologySettings(ayanamsa_id=ayanamsa_id),
        )
        state = engine.state(_birth())
        values.append(round(float(state.core_objects["ayanamsa_deg"]), 8))

    assert len(set(values)) >= 2


def test_engine_entrypoint_logs_when_fallback_is_used(caplog) -> None:
    caplog.clear()
    engine = DibaEngine(
        session_ctx=AstronomyContext(),
        astro_settings=AstrologySettings(
            ayanamsa_id="senthil",
            ayanamsa_on_unsupported="fallback_default",
        ),
    )
    state = engine.state(_birth())

    assert state.core_objects["ayanamsa_id"] == "lahiri"
    assert any("Ayanamsa fallback applied in engine state" in rec.message for rec in caplog.records)
