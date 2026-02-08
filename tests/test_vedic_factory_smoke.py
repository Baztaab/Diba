from diba.schemas.kr_models import VedicModel
from diba.vedic.factory import VedicSubjectFactory


def test_vedic_factory_smoke_and_determinism():
    kwargs = {
        "year": 2004,
        "month": 1,
        "day": 27,
        "hour": 14,
        "minute": 45,
        "seconds": 35.0,
        "tz_str": "Asia/Tehran",
        "lat": 35.7,
        "lon": 51.1,
        "ayanamsa_id": "lahiri",
        "node_mode": "mean",
        "house_system_id": "whole_sign",
    }
    first = VedicSubjectFactory.from_birth_data(**kwargs)
    second = VedicSubjectFactory.from_birth_data(**kwargs)

    assert isinstance(first, VedicModel)
    assert isinstance(second, VedicModel)

    required = {
        "sun",
        "moon",
        "mercury",
        "venus",
        "mars",
        "jupiter",
        "saturn",
        "ascendant",
        "rahu",
        "ketu",
    }
    assert required.issubset(first.core.objects.keys())

    for key in required:
        lon = first.core.objects[key].abs_pos_sidereal
        assert 0.0 <= lon < 360.0

    for key in required:
        assert (
            first.core.objects[key].abs_pos_sidereal
            == second.core.objects[key].abs_pos_sidereal
        )
