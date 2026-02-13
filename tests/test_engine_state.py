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


def test_engine_state_computes_base_fields():
    engine = DibaEngine(
        session_ctx=AstronomyContext(),
        astro_settings=AstrologySettings(),
    )

    state = engine.state(_birth())

    assert state.jd_ut > 0
    assert "sun" in state.planets
    assert "houses" in state.core_objects


def test_engine_session_is_reentrant_in_same_context():
    engine = DibaEngine(
        session_ctx=AstronomyContext(),
        astro_settings=AstrologySettings(),
    )

    with engine.session():
        state1 = engine.state(_birth())
        with engine.session():
            state2 = engine.state(_birth())

    assert state1.jd_ut == state2.jd_ut
    assert state1.flags == state2.flags
