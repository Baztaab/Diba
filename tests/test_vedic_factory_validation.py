import pytest

from diba.vedic.factory import VedicFactoryError, VedicSubjectFactory, _split_seconds


def test_split_seconds_rounding_carry_edges():
    sec, micros = _split_seconds(59.9999994)
    assert sec == 59
    assert micros == 999999

    with pytest.raises(VedicFactoryError, match="seconds must be < 60"):
        _split_seconds(59.9999996)


def test_factory_rejects_none_or_invalid_node_mode():
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
        "house_system_id": "whole_sign",
    }
    with pytest.raises(VedicFactoryError, match="node_mode must be a non-empty string"):
        VedicSubjectFactory.from_birth_data(**kwargs, node_mode=None)
    with pytest.raises(VedicFactoryError, match="node_mode must be one of"):
        VedicSubjectFactory.from_birth_data(**kwargs, node_mode="  invalid ")


def test_factory_rejects_invalid_lat_lon():
    kwargs = {
        "year": 2004,
        "month": 1,
        "day": 27,
        "hour": 14,
        "minute": 45,
        "seconds": 35.0,
        "tz_str": "Asia/Tehran",
        "ayanamsa_id": "lahiri",
        "house_system_id": "whole_sign",
        "node_mode": "mean",
    }
    with pytest.raises(VedicFactoryError, match="Latitude must be in"):
        VedicSubjectFactory.from_birth_data(**kwargs, lat=200.0, lon=51.1)
    with pytest.raises(VedicFactoryError, match="Longitude must be in"):
        VedicSubjectFactory.from_birth_data(**kwargs, lat=35.7, lon=999.0)


def test_factory_rejects_non_zero_altitude():
    with pytest.raises(VedicFactoryError, match="Altitude is currently unsupported"):
        VedicSubjectFactory.from_birth_data(
            year=2004,
            month=1,
            day=27,
            hour=14,
            minute=45,
            seconds=35.0,
            tz_str="Asia/Tehran",
            lat=35.7,
            lon=51.1,
            altitude=1000.0,
            ayanamsa_id="lahiri",
            node_mode="mean",
            house_system_id="whole_sign",
        )


def test_factory_wraps_dst_ambiguous_and_nonexistent():
    base = {
        "year": 2021,
        "month": 11,
        "day": 7,
        "hour": 1,
        "minute": 30,
        "seconds": 0.0,
        "tz_str": "America/New_York",
        "lat": 40.7,
        "lon": -74.0,
        "ayanamsa_id": "lahiri",
        "node_mode": "mean",
        "house_system_id": "whole_sign",
    }
    with pytest.raises(VedicFactoryError, match="Ambiguous local datetime"):
        VedicSubjectFactory.from_birth_data(**base)

    nonexistent = dict(base)
    nonexistent.update({"month": 3, "day": 14, "hour": 2, "minute": 30})
    with pytest.raises(VedicFactoryError, match="Non-existent local datetime"):
        VedicSubjectFactory.from_birth_data(**nonexistent)


def test_factory_wraps_invalid_timezone_and_date():
    with pytest.raises(VedicFactoryError, match="Invalid timezone"):
        VedicSubjectFactory.from_birth_data(
            year=2004,
            month=1,
            day=27,
            hour=14,
            minute=45,
            seconds=35.0,
            tz_str="Bad/Timezone",
            lat=35.7,
            lon=51.1,
            ayanamsa_id="lahiri",
            node_mode="mean",
            house_system_id="whole_sign",
        )

    with pytest.raises(VedicFactoryError, match="day is out of range"):
        VedicSubjectFactory.from_birth_data(
            year=2004,
            month=2,
            day=30,
            hour=14,
            minute=45,
            seconds=35.0,
            tz_str="Asia/Tehran",
            lat=35.7,
            lon=51.1,
            ayanamsa_id="lahiri",
            node_mode="mean",
            house_system_id="whole_sign",
        )
