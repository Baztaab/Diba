from __future__ import annotations

from diba.infra.swisseph import adapter as swe_adapter
from diba.infra.swisseph.session import SwissEphSession, set_sid_mode
from diba.vedic.context import VedicCalculationContext, swe
from diba.vedic.registry import resolve_ayanamsa, resolve_house_system


def _expected_ayanamsa_for_mode(jd: float, sid_mode: int) -> float:
    with SwissEphSession():
        set_sid_mode(sid_mode, 0.0, 0.0)
        value = swe_adapter.get_ayanamsa_ut(jd)
        set_sid_mode(swe.SIDM_LAHIRI, 0.0, 0.0)
    return value


def test_set_before_use_happens_for_requested_mode() -> None:
    jd = swe.julday(2004, 1, 27, 12.0, swe.GREG_CAL)
    expected_raman = _expected_ayanamsa_for_mode(jd, swe.SIDM_RAMAN)

    with SwissEphSession():
        set_sid_mode(swe.SIDM_FAGAN_BRADLEY, 0.0, 0.0)

    ctx = VedicCalculationContext(
        jd_utc=jd,
        lat=35.7,
        lon=51.1,
        ayanamsa=resolve_ayanamsa("raman")[0],
        house_system=resolve_house_system("whole_sign"),
    )
    core = ctx.compute_core()

    assert abs(float(core["ayanamsa_deg"]) - expected_raman) <= 1e-12


def test_restore_to_baseline_happens_after_compute() -> None:
    jd = swe.julday(2004, 1, 27, 12.0, swe.GREG_CAL)
    ctx = VedicCalculationContext(
        jd_utc=jd,
        lat=35.7,
        lon=51.1,
        ayanamsa=resolve_ayanamsa("fagan")[0],
        house_system=resolve_house_system("whole_sign"),
    )
    _ = ctx.compute_core()

    with SwissEphSession():
        after_compute = swe_adapter.get_ayanamsa_ut(jd)
        set_sid_mode(swe.SIDM_LAHIRI, 0.0, 0.0)
        expected_lahiri = swe_adapter.get_ayanamsa_ut(jd)

    assert abs(after_compute - expected_lahiri) <= 1e-12
