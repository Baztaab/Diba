# -*- coding: utf-8 -*-
from math import isclose
import pytest
from pathlib import Path
import json

from kerykeion.astrological_subject_factory import AstrologicalSubjectFactory
from kerykeion.vedic.vargas import compute_varga


_AYANAMSA_OVERRIDE = 23.8055194444
_TOL = 5e-4
_TOL_D4D5D6 = 3e-5
_TOL_D7D8D9 = 3e-5
_TOL_D10D11D12D16D20 = 3e-5
_TOL_D60 = 1e-4
_TOL_D108 = 2e-4
_TOL_D144 = 2e-4


def _assert_point(point: dict, sign: str, position: float, tol: float = _TOL) -> None:
    assert point["sign"] == sign
    assert isclose(point["position"], position, abs_tol=tol)


def _core_abs_from_subject(subject: AstrologicalSubjectFactory) -> dict[str, float]:
    vedic = subject.model_dump()["vedic"]
    return {k: v["abs_pos_sidereal"] for k, v in vedic["core"]["objects"].items()}


def test_pyjhora_profile_us_no_compat_mirror() -> None:
    subject = AstrologicalSubjectFactory.from_birth_data(
        name="PyJHora US Profile",
        year=1997,
        month=6,
        day=7,
        hour=20,
        minute=28,
        seconds=36,
        city="Tehran",
        nation="IR",
        lng=51 + 25 / 60,
        lat=35 + 40 / 60,
        tz_str="Asia/Tehran",
        online=False,
        vedic=True,
        vedic_ayanamsa_override_deg=_AYANAMSA_OVERRIDE,
        vedic_node_policy="mean",
        vedic_vargas=["D2", "D3"],
        vedic_varga_profile="US",
    )

    vedic = subject.model_dump()["vedic"]["vargas"]["charts"]
    core_abs = _core_abs_from_subject(subject)
    expected_d2 = compute_varga(core_abs, "D2", method=1, mirror_even_sign=False)["points"]
    expected_d3 = compute_varga(core_abs, "D3", method=5, mirror_even_sign=False)["points"]
    assert vedic["D2"]["points"] == expected_d2
    assert vedic["D3"]["points"] == expected_d3


def test_jhora_parity_d2_d3_us_profile() -> None:
    subject = AstrologicalSubjectFactory.from_birth_data(
        name="JHora Parity",
        year=1997,
        month=6,
        day=7,
        hour=20,
        minute=28,
        seconds=36,
        city="Tehran",
        nation="IR",
        lng=51 + 25 / 60,
        lat=35 + 40 / 60,
        tz_str="Asia/Tehran",
        online=False,
        vedic=True,
        vedic_ayanamsa_override_deg=_AYANAMSA_OVERRIDE,
        vedic_node_policy="mean",
        vedic_vargas=["D2", "D3"],
        vedic_compat_mode="jhora_us",
    )

    vedic = subject.model_dump()["vedic"]
    d2 = vedic["vargas"]["charts"]["D2"]["points"]
    d3 = vedic["vargas"]["charts"]["D3"]["points"]

    # D2 (US) JHora reference
    _assert_point(d2["ascendant"], "Gem", 7.1912472222)
    _assert_point(d2["sun"], "Gem", 13.7350944444)
    _assert_point(d2["moon"], "Vir", 13.3015138889)
    _assert_point(d2["mars"], "Pis", 27.0574444444)
    _assert_point(d2["mercury"], "Can", 22.0916666667)
    _assert_point(d2["jupiter"], "Lib", 3.7458305556)
    _assert_point(d2["venus"], "Leo", 20.9418472222)
    _assert_point(d2["saturn"], "Aqu", 11.7807361111)
    _assert_point(d2["rahu"], "Pis", 28.1982861111)
    _assert_point(d2["ketu"], "Pis", 28.1982861111)

    # D3 (US) JHora reference
    _assert_point(d3["ascendant"], "Cap", 10.7868722222)
    _assert_point(d3["sun"], "Can", 20.6026416667)
    _assert_point(d3["moon"], "Sag", 4.9522694444)
    _assert_point(d3["mars"], "Vir", 25.5861694444)
    _assert_point(d3["mercury"], "Vir", 18.1374972222)
    _assert_point(d3["jupiter"], "Can", 5.6187472222)
    _assert_point(d3["venus"], "Sco", 1.4127694444)
    _assert_point(d3["saturn"], "Cap", 17.6711027778)
    _assert_point(d3["rahu"], "Vir", 27.2974305556)
    _assert_point(d3["ketu"], "Pis", 27.2974305556)


def _dms_to_deg(deg: int, minutes: int, seconds: float) -> float:
    return deg + minutes / 60.0 + seconds / 3600.0


def test_jhora_parity_d4_d5_d6_case_1988() -> None:
    subject = AstrologicalSubjectFactory.from_birth_data(
        name="JHora Parity D4/D5/D6",
        year=1988,
        month=9,
        day=11,
        hour=6,
        minute=45,
        seconds=0,
        city="Tehran",
        nation="IR",
        lng=51 + 9 / 60,
        lat=32 + 42 / 60,
        tz_str="Asia/Tehran",
        online=False,
        vedic=True,
        vedic_ayanamsa_override_deg=23.6835694444,
        vedic_node_policy="mean",
        vedic_vargas=["D4", "D5", "D6"],
        vedic_compat_mode="jhora_us",
    )

    charts = subject.model_dump()["vedic"]["vargas"]["charts"]
    d4 = charts["D4"]["points"]
    d5 = charts["D5"]["points"]
    d6 = charts["D6"]["points"]

    # D4 JHora reference (1988-09-11 06:45 Tehran)
    _assert_point(d4["ascendant"], "Vir", _dms_to_deg(26, 10, 5.57), tol=_TOL_D4D5D6)
    _assert_point(d4["sun"], "Tau", _dms_to_deg(9, 42, 35.01), tol=_TOL_D4D5D6)
    _assert_point(d4["moon"], "Tau", _dms_to_deg(6, 51, 37.01), tol=_TOL_D4D5D6)
    _assert_point(d4["mars"], "Vir", _dms_to_deg(4, 26, 58.66), tol=_TOL_D4D5D6)
    _assert_point(d4["mercury"], "Pis", _dms_to_deg(24, 13, 14.00), tol=_TOL_D4D5D6)
    _assert_point(d4["jupiter"], "Leo", _dms_to_deg(18, 35, 17.17), tol=_TOL_D4D5D6)
    _assert_point(d4["venus"], "Lib", _dms_to_deg(10, 49, 26.14), tol=_TOL_D4D5D6)
    _assert_point(d4["saturn"], "Sag", _dms_to_deg(9, 25, 42.51), tol=_TOL_D4D5D6)
    _assert_point(d4["rahu"], "Leo", _dms_to_deg(20, 6, 19.95), tol=_TOL_D4D5D6)
    _assert_point(d4["ketu"], "Aqu", _dms_to_deg(20, 6, 19.95), tol=_TOL_D4D5D6)

    # D5 JHora reference (1988-09-11 06:45 Tehran)
    _assert_point(d5["ascendant"], "Vir", _dms_to_deg(2, 42, 36.96), tol=_TOL_D4D5D6)
    _assert_point(d5["sun"], "Lib", _dms_to_deg(4, 38, 13.76), tol=_TOL_D4D5D6)
    _assert_point(d5["moon"], "Lib", _dms_to_deg(1, 4, 31.26), tol=_TOL_D4D5D6)
    _assert_point(d5["mars"], "Pis", _dms_to_deg(20, 33, 43.32), tol=_TOL_D4D5D6)
    _assert_point(d5["mercury"], "Cap", _dms_to_deg(15, 16, 32.51), tol=_TOL_D4D5D6)
    _assert_point(d5["jupiter"], "Pis", _dms_to_deg(0, 44, 6.46), tol=_TOL_D4D5D6)
    _assert_point(d5["venus"], "Vir", _dms_to_deg(21, 1, 47.68), tol=_TOL_D4D5D6)
    _assert_point(d5["saturn"], "Ari", _dms_to_deg(11, 47, 8.13), tol=_TOL_D4D5D6)
    _assert_point(d5["rahu"], "Gem", _dms_to_deg(10, 7, 54.94), tol=_TOL_D4D5D6)
    _assert_point(d5["ketu"], "Gem", _dms_to_deg(10, 7, 54.94), tol=_TOL_D4D5D6)

    # D6 JHora reference (1988-09-11 06:45 Tehran)
    _assert_point(d6["ascendant"], "Sco", _dms_to_deg(9, 15, 8.35), tol=_TOL_D4D5D6)
    _assert_point(d6["sun"], "Leo", _dms_to_deg(29, 33, 52.51), tol=_TOL_D4D5D6)
    _assert_point(d6["moon"], "Leo", _dms_to_deg(25, 17, 25.51), tol=_TOL_D4D5D6)
    _assert_point(d6["mars"], "Cap", _dms_to_deg(6, 40, 27.99), tol=_TOL_D4D5D6)
    _assert_point(d6["mercury"], "Aqu", _dms_to_deg(6, 19, 51.01), tol=_TOL_D4D5D6)
    _assert_point(d6["jupiter"], "Sag", _dms_to_deg(12, 52, 55.76), tol=_TOL_D4D5D6)
    _assert_point(d6["venus"], "Sag", _dms_to_deg(1, 14, 9.21), tol=_TOL_D4D5D6)
    _assert_point(d6["saturn"], "Ari", _dms_to_deg(14, 8, 33.76), tol=_TOL_D4D5D6)
    _assert_point(d6["rahu"], "Leo", _dms_to_deg(0, 9, 29.93), tol=_TOL_D4D5D6)
    _assert_point(d6["ketu"], "Leo", _dms_to_deg(0, 9, 29.93), tol=_TOL_D4D5D6)


def test_jhora_parity_d7_d8_d9_case_1988() -> None:
    fixture_path = Path("tests") / "fixtures" / "jhora_d7_d8_d9_1988.json"
    dump_path = Path("tests") / "fixtures" / "jhora_d7_d8_d9_1988_generated.json"
    if not fixture_path.exists():
        subject = AstrologicalSubjectFactory.from_birth_data(
            name="JHora Parity D7/D8/D9",
            year=1988,
            month=9,
            day=11,
            hour=6,
            minute=45,
            seconds=0,
            city="Tehran",
            nation="IR",
            lng=51 + 9 / 60,
            lat=32 + 42 / 60,
            tz_str="Asia/Tehran",
            online=False,
            vedic=True,
            vedic_ayanamsa_override_deg=23.6835694444,
            vedic_node_policy="mean",
            vedic_vargas=["D7", "D8", "D9"],
            vedic_compat_mode="jhora_us",
        )
        if dump_path.parent.exists():
            payload = subject.model_dump()["vedic"]["vargas"]["charts"]
            dump_path.parent.mkdir(parents=True, exist_ok=True)
            dump_path.write_text(json.dumps(payload, ensure_ascii=True, indent=2))
        pytest.skip("Missing JHora fixture tests/fixtures/jhora_d7_d8_d9_1988.json")

    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    subject = AstrologicalSubjectFactory.from_birth_data(
        name="JHora Parity D7/D8/D9",
        year=1988,
        month=9,
        day=11,
        hour=6,
        minute=45,
        seconds=0,
        city="Tehran",
        nation="IR",
        lng=51 + 9 / 60,
        lat=32 + 42 / 60,
        tz_str="Asia/Tehran",
        online=False,
        vedic=True,
        vedic_ayanamsa_override_deg=23.6835694444,
        vedic_node_policy="mean",
        vedic_vargas=["D7", "D8", "D9"],
        vedic_compat_mode="jhora_us",
    )

    charts = subject.model_dump()["vedic"]["vargas"]["charts"]
    for chart_id in ("D7", "D8", "D9"):
        for point, expected in data[chart_id]["points"].items():
            actual = charts[chart_id]["points"][point]
            assert actual["sign"] == expected["sign"]
            assert isclose(actual["position"], expected["position"], abs_tol=_TOL_D7D8D9)


def test_jhora_parity_d7_case_1997() -> None:
    fixture_path = Path("tests") / "fixtures" / "jhora_d7_1997.json"
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    subject = AstrologicalSubjectFactory.from_birth_data(
        name="JHora Parity D7 1997",
        year=1997,
        month=6,
        day=7,
        hour=20,
        minute=28,
        seconds=36,
        city="Tehran",
        nation="IR",
        lng=51 + 25 / 60,
        lat=35 + 40 / 60,
        tz_str="Asia/Tehran",
        online=False,
        vedic=True,
        vedic_ayanamsa_override_deg=23.8055194444,
        vedic_node_policy="mean",
        vedic_vargas=["D7"],
        vedic_varga_methods={"D7": 2},
        vedic_compat_mode="jhora_us",
    )

    charts = subject.model_dump()["vedic"]["vargas"]["charts"]
    for point, expected in data["D7"]["points"].items():
        actual = charts["D7"]["points"][point]
        assert actual["sign"] == expected["sign"]
        assert isclose(actual["position"], expected["position"], abs_tol=_TOL_D7D8D9)

    # Decision dump (D7 method2, JHora compat) for 1997 case
    d1_points = subject.model_dump()["vedic"]["rasi_d1"]["points"]
    even_signs = {1, 3, 5, 7, 9, 11}
    for point in data["D7"]["points"].keys():
        d1_sign_num = int(d1_points[point]["sign_num"])
        mirror_applied = d1_sign_num in even_signs
        print(f"D7 1997 decision: {point} d1_sign_num={d1_sign_num} mirror={mirror_applied}")


def test_jhora_parity_d7_case_1988() -> None:
    fixture_path = Path("tests") / "fixtures" / "jhora_d7_1988.json"
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    subject = AstrologicalSubjectFactory.from_birth_data(
        name="JHora Parity D7 1988",
        year=1988,
        month=9,
        day=11,
        hour=6,
        minute=45,
        seconds=0,
        city="Tehran",
        nation="IR",
        lng=51 + 9 / 60,
        lat=32 + 42 / 60,
        tz_str="Asia/Tehran",
        online=False,
        vedic=True,
        vedic_ayanamsa_override_deg=23.6835694444,
        vedic_node_policy="mean",
        vedic_vargas=["D7"],
        vedic_compat_mode="jhora_us",
    )

    charts = subject.model_dump()["vedic"]["vargas"]["charts"]
    for point, expected in data["D7"]["points"].items():
        actual = charts["D7"]["points"][point]
        assert actual["sign"] == expected["sign"]
        assert isclose(actual["position"], expected["position"], abs_tol=_TOL_D7D8D9)


def test_jhora_parity_d10_d11_d12_d16_d20_case_2004() -> None:
    fixture_path = Path("tests") / "fixtures" / "jhora_d10_d11_d12_d16_d20_2004.json"
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    ayanamsa_override = _dms_to_deg(23, 53, 53.46)
    subject = AstrologicalSubjectFactory.from_birth_data(
        name="JHora Parity D10/D11/D12/D16/D20",
        year=2004,
        month=1,
        day=27,
        hour=14,
        minute=45,
        seconds=35,
        city="Karaj",
        nation="IR",
        lng=51 + 6 / 60,
        lat=35 + 42 / 60,
        tz_str="Asia/Tehran",
        online=False,
        vedic=True,
        vedic_ayanamsa_override_deg=ayanamsa_override,
        vedic_node_policy="mean",
        vedic_vargas=["D10", "D11", "D12", "D16", "D20"],
        vedic_varga_methods={"D10": 3, "D16": 2},
        vedic_compat_mode="jhora_us",
    )

    charts = subject.model_dump()["vedic"]["vargas"]["charts"]
    for chart_id in ("D10", "D11", "D12", "D16", "D20"):
        for point, expected in data[chart_id]["points"].items():
            actual = charts[chart_id]["points"][point]
            assert actual["sign"] == expected["sign"]
            assert isclose(actual["position"], expected["position"], abs_tol=_TOL_D10D11D12D16D20)


def test_jhora_parity_d24_case_2004() -> None:
    fixture_path = Path("tests") / "fixtures" / "jhora_d24_2004.json"
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    ayanamsa_override = _dms_to_deg(23, 53, 53.46)
    subject = AstrologicalSubjectFactory.from_birth_data(
        name="JHora Parity D24",
        year=2004,
        month=1,
        day=27,
        hour=14,
        minute=45,
        seconds=35,
        city="Karaj",
        nation="IR",
        lng=51 + 6 / 60,
        lat=35 + 42 / 60,
        tz_str="Asia/Tehran",
        online=False,
        vedic=True,
        vedic_ayanamsa_override_deg=ayanamsa_override,
        vedic_node_policy="mean",
        vedic_vargas=["D24"],
        vedic_varga_methods={"D24": 2},
        vedic_compat_mode="jhora_us",
    )

    d24 = subject.model_dump()["vedic"]["vargas"]["charts"]["D24"]["points"]
    for point, expected in data["D24"]["points"].items():
        actual = d24[point]
        assert actual["sign"] == expected["sign"]
        assert isclose(actual["position"], expected["position"], abs_tol=_TOL_D10D11D12D16D20)


def test_jhora_parity_d60_d108_d144_case_2004() -> None:
    fixture_path = Path("tests") / "fixtures" / "jhora_d60_d81_d108_d144_2004.json"
    data = json.loads(fixture_path.read_text(encoding="utf-8"))
    data.pop("D81", None)
    ayanamsa_override = _dms_to_deg(23, 53, 53.46)

    subject = AstrologicalSubjectFactory.from_birth_data(
        name="JHora Parity D60/D81/D108/D144",
        year=2004,
        month=1,
        day=27,
        hour=14,
        minute=45,
        seconds=35,
        city="Karaj",
        nation="IR",
        lng=51 + 6 / 60,
        lat=35 + 42 / 60,
        tz_str="Asia/Tehran",
        online=False,
        vedic=True,
        vedic_ayanamsa_override_deg=ayanamsa_override,
        vedic_node_policy="mean",
        vedic_vargas=["D60", "D108", "D144"],
        vedic_varga_methods={"D60": 3},
        vedic_compat_mode="jhora_us",
    )

    charts = subject.model_dump()["vedic"]["vargas"]["charts"]

    # D60 (RvAr) JHora reference
    for point, expected in data["D60"]["points"].items():
        actual = charts["D60"]["points"][point]
        assert actual["sign"] == expected["sign"]
        assert isclose(actual["position"], expected["position"], abs_tol=_TOL_D60)

    # D108 JHora reference
    for point, expected in data["D108"]["points"].items():
        actual = charts["D108"]["points"][point]
        assert actual["sign"] == expected["sign"]
        assert isclose(actual["position"], expected["position"], abs_tol=_TOL_D108)

    # D144 JHora reference
    for point, expected in data["D144"]["points"].items():
        actual = charts["D144"]["points"][point]
        assert actual["sign"] == expected["sign"]
        assert isclose(actual["position"], expected["position"], abs_tol=_TOL_D144)
