from __future__ import annotations

import threading

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


def test_engine_session_context_isolation_across_threads() -> None:
    engine = DibaEngine(
        session_ctx=AstronomyContext(),
        astro_settings=AstrologySettings(),
    )
    barrier = threading.Barrier(2)
    errors: list[Exception] = []
    jd_values: list[float] = []

    def worker_a() -> None:
        try:
            with engine.session():
                barrier.wait(timeout=5)
                state = engine.state(_birth())
                jd_values.append(state.jd_ut)
        except Exception as exc:  # pragma: no cover
            errors.append(exc)

    def worker_b() -> None:
        try:
            barrier.wait(timeout=5)
            state = engine.state(_birth())
            jd_values.append(state.jd_ut)
        except Exception as exc:  # pragma: no cover
            errors.append(exc)

    t1 = threading.Thread(target=worker_a)
    t2 = threading.Thread(target=worker_b)

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    assert not errors
    assert len(jd_values) == 2
    assert jd_values[0] == jd_values[1]
    assert not hasattr(engine, "_session")
