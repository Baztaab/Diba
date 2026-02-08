from __future__ import annotations

import json
from pathlib import Path

from kerykeion.vedic.factory import VedicSubjectFactory
from kerykeion.vedic.vargas import compute_varga


FIXTURE_PATH = Path(__file__).resolve().parent / "fixtures" / "jhora_d60_d81_d108_d144_2004.json"


def _load_d81_points() -> dict[str, dict[str, object]]:
    payload = json.loads(FIXTURE_PATH.read_text(encoding="utf-8"))
    return payload["D81"]["points"]


def test_d81_jhora_fixture_shape() -> None:
    points = _load_d81_points()
    required = {
        "ascendant",
        "sun",
        "moon",
        "mars",
        "mercury",
        "jupiter",
        "venus",
        "saturn",
        "rahu",
        "ketu",
    }
    assert required == set(points.keys())
    for point in points.values():
        assert "sign" in point
        assert "position" in point


def test_d81_engine_keys_match_jhora_oracle_keys() -> None:
    fixture_points = _load_d81_points()
    model = VedicSubjectFactory.from_birth_data(
        year=2004,
        month=1,
        day=27,
        hour=14,
        minute=45,
        seconds=35.0,
        lon=51 + 6 / 60,
        lat=35 + 42 / 60,
        tz_str="Asia/Tehran",
        ayanamsa_id="lahiri",
        node_mode="mean",
        house_system_id="whole_sign",
    )
    core = {k: v.abs_pos_sidereal for k, v in model.core.objects.items()}
    engine_points = compute_varga(core, "D81", method=1)["points"]
    assert set(engine_points.keys()) == set(fixture_points.keys())
