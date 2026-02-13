from __future__ import annotations

import importlib

import pytest

import diba.infra.io.ephemeris as ephemeris_module
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


def _reload_ephemeris_module():
    return importlib.reload(ephemeris_module)


@pytest.fixture(autouse=True)
def _isolate_ephemeris_runtime_state():
    _reload_ephemeris_module()
    yield
    _reload_ephemeris_module()


def test_canonical_engine_path_wires_ephemeris_init_once(tmp_path):
    ephe_dir = tmp_path / "ephe"
    ephe_dir.mkdir()
    mod = ephemeris_module

    engine = DibaEngine(
        session_ctx=AstronomyContext(
            ephe_path=str(ephe_dir),
            ephe_expectations="de405/sepl_18",
            config_digest="digest-A",
            dev_mode=False,
        ),
        astro_settings=AstrologySettings(),
    )

    state1 = engine.state(_birth())
    assert state1.jd_ut > 0
    assert mod._EPHE_INIT_DETAILS is not None
    first_details = mod._EPHE_INIT_DETAILS

    state2 = engine.state(_birth())
    assert state2.jd_ut == state1.jd_ut
    assert mod._EPHE_INIT_DETAILS == first_details


def test_canonical_engine_path_raises_on_runtime_fingerprint_conflict(tmp_path):
    ephe_dir = tmp_path / "ephe"
    ephe_dir.mkdir()

    engine_a = DibaEngine(
        session_ctx=AstronomyContext(
            ephe_path=str(ephe_dir),
            ephe_expectations="de405/sepl_18",
            config_digest="digest-A",
            dev_mode=False,
        ),
        astro_settings=AstrologySettings(),
    )
    engine_a.state(_birth())

    engine_b = DibaEngine(
        session_ctx=AstronomyContext(
            ephe_path=str(ephe_dir),
            ephe_expectations="de405/sepl_18",
            config_digest="digest-B",
            dev_mode=False,
        ),
        astro_settings=AstrologySettings(),
    )

    with pytest.raises(RuntimeError, match="policy conflict detected"):
        engine_b.state(_birth())
