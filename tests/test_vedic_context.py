import swisseph as swe

from diba.vedic.context import VedicCalculationContext, PLANET_FLAGS, ASC_FLAGS
from diba.vedic.registry import resolve_ayanamsa, resolve_house_system


def test_houses_ex_default_equivalence():
    jd = swe.julday(2004, 1, 27, 12.0, swe.GREG_CAL)
    lat, lon = 35.7, 51.1

    swe.set_sid_mode(swe.SIDM_LAHIRI)
    try:
        asc_default = swe.houses_ex(jd, lat, lon, flags=ASC_FLAGS)[1][0]
        asc_p = swe.houses_ex(jd, lat, lon, b"P", flags=ASC_FLAGS)[1][0]
    finally:
        swe.set_sid_mode(swe.SIDM_LAHIRI)

    assert abs(asc_default - asc_p) <= 1e-12


def test_bit_hindu_rising_noop_for_calc_ut():
    jd = swe.julday(2004, 1, 27, 12.0, swe.GREG_CAL)
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    base_flags = swe.FLG_SWIEPH | swe.FLG_SIDEREAL | swe.FLG_TRUEPOS | swe.FLG_SPEED
    pyj_flags = base_flags | swe.BIT_HINDU_RISING

    bodies = [swe.SUN, swe.MOON, swe.MERCURY, swe.MEAN_NODE]
    for body in bodies:
        base_xx, _ = swe.calc_ut(jd, body, flags=base_flags)
        pyj_xx, _ = swe.calc_ut(jd, body, flags=pyj_flags)
        assert abs(base_xx[0] - pyj_xx[0]) <= 1e-12


def test_calc_ut_shape_and_speed_index():
    jd = swe.julday(2004, 1, 27, 12.0, swe.GREG_CAL)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    xx, retflag = swe.calc_ut(jd, swe.SUN, flags=PLANET_FLAGS)

    assert len(xx) >= 4
    assert isinstance(xx[0], float)
    assert isinstance(xx[3], float)
    assert isinstance(retflag, int)


def test_context_compute_core_returns_retrograde_fields():
    ctx = VedicCalculationContext(
        jd_utc=swe.julday(2004, 1, 27, 12.0, swe.GREG_CAL),
        lat=35.7,
        lon=51.1,
        ayanamsa=resolve_ayanamsa("lahiri"),
        house_system=resolve_house_system("whole_sign"),
    )

    core = ctx.compute_core()

    for key in ("sun", "moon", "mercury", "venus", "mars", "jupiter", "saturn"):
        assert key in core["planets"]
        p = core["planets"][key]
        assert 0.0 <= p["longitude"] < 360.0
        assert isinstance(p["speed_long"], float)
        assert isinstance(p["is_retrograde"], bool)
        assert isinstance(p["retflag"], int)

    assert "rahu" in core["nodes"]
    assert "ketu" in core["nodes"]
    assert 0.0 <= core["nodes"]["rahu"]["longitude"] < 360.0
    assert 0.0 <= core["nodes"]["ketu"]["longitude"] < 360.0

    assert 0.0 <= core["ascendant"]["longitude"] < 360.0


def test_context_finally_enforces_baseline_sid_mode():
    jd = swe.julday(2004, 1, 27, 12.0, swe.GREG_CAL)
    swe.set_sid_mode(swe.SIDM_FAGAN_BRADLEY)

    ctx = VedicCalculationContext(
        jd_utc=jd,
        lat=35.7,
        lon=51.1,
        ayanamsa=resolve_ayanamsa("lahiri"),
        house_system=resolve_house_system("whole_sign"),
    )
    _ = ctx.compute_core()

    val_after = swe.get_ayanamsa(jd)
    swe.set_sid_mode(swe.SIDM_LAHIRI)
    val_lahiri = swe.get_ayanamsa(jd)
    assert abs(val_after - val_lahiri) <= 1e-12
