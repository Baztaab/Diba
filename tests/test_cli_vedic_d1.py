import argparse

from diba import cli


class _Point:
    def __init__(self, lon: float) -> None:
        self.abs_pos_sidereal = lon


class _Core:
    def __init__(self) -> None:
        self.objects = {
            "sun": _Point(10.0),
            "moon": _Point(20.0),
            "mercury": _Point(30.0),
            "venus": _Point(40.0),
            "mars": _Point(50.0),
            "jupiter": _Point(60.0),
            "saturn": _Point(70.0),
            "rahu": _Point(80.0),
            "ketu": _Point(90.0),
            "ascendant": _Point(100.0),
        }


class _Model:
    def __init__(self) -> None:
        self.core = _Core()
        self.ayanamsa_deg = 23.4


def test_run_vedic_d1_parses_and_calls(monkeypatch):
    monkeypatch.setattr(
        "diba._cli.commands.vedic_d1.VedicSubjectFactory.from_birth_data",
        lambda **_kw: _Model(),
    )
    monkeypatch.setattr("diba._cli.commands.vedic_d1.resolve_ephemeris_path", lambda _cli_arg, _online: None)

    ns = argparse.Namespace(
        name="Test",
        year=2023,
        month=6,
        day=15,
        hour=12,
        minute=0,
        second=None,
        lat=48.8566,
        lng=2.3522,
        tz_str="Europe/Paris",
        online=False,
        offline=False,
        ayanamsa_id="lahiri",
        node_mode="mean",
        house_system_id="whole_sign",
        format="json",
        interactive=False,
        ephe_path=None,
    )

    result = cli.run_vedic_d1(ns)
    assert result["ayanamsa_deg"] == 23.4
    assert result["asc_sidereal_deg"] == 100.0
    assert result["asc_sidereal_sign"] == 3
