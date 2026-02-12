from diba.vedic.context import VedicCalculationContext, swe
from diba.vedic.registry import (
    HouseFetchPlan,
    HouseSystemSpec,
    resolve_ayanamsa,
    resolve_house_system,
)


def test_fetch_plan_asc_only_no_cusps():
    ctx = VedicCalculationContext(
        jd_utc=swe.julday(2004, 1, 27, 12.0, swe.GREG_CAL),
        lat=35.7,
        lon=51.1,
        ayanamsa=resolve_ayanamsa("lahiri"),
        house_system=resolve_house_system("whole_sign"),
    )
    core = ctx.compute_core()
    assert "cusps" not in core["ascendant"]


def test_fetch_plan_houses_ex_returns_cusps():
    ctx = VedicCalculationContext(
        jd_utc=swe.julday(2004, 1, 27, 12.0, swe.GREG_CAL),
        lat=35.7,
        lon=51.1,
        ayanamsa=resolve_ayanamsa("lahiri"),
        house_system=HouseSystemSpec(
            id="placidus",
            pyjhora_method=4,
            fetch_plan=HouseFetchPlan.HOUSES_EX,
            swe_hsys_code="P",
        ),
    )
    core = ctx.compute_core()
    assert "cusps" in core["ascendant"]
    assert len(core["ascendant"]["cusps"]) == 12
