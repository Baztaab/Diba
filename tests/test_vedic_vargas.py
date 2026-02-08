# -*- coding: utf-8 -*-
from diba.vedic.vargas import compute_varga


def test_d9_method1_aries_taurus_boundaries() -> None:
    core = {"sun": 0.0, "ascendant": 30.0}
    chart = compute_varga(core, "D9", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["sun"]["position"] == 0.0
    assert chart["points"]["ascendant"]["sign_num"] == 9


def test_d10_method1_aries_taurus_boundaries() -> None:
    core = {"sun": 0.0, "ascendant": 30.0}
    chart = compute_varga(core, "D10", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["sun"]["position"] == 0.0
    assert chart["points"]["ascendant"]["sign_num"] == 9


def test_d10_method1_boundaries() -> None:
    boundary = 30.0 / 10.0
    core = {
        "sun": 0.0,
        "moon": 30.0,
        "mars": boundary,
        "saturn": 29.999,
    }
    chart = compute_varga(core, "D10", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 9
    assert chart["points"]["mars"]["sign_num"] == 1
    assert chart["points"]["saturn"]["sign_num"] == 9


def test_d3_method1_boundaries() -> None:
    core = {
        "sun": 0.0,
        "moon": 10.0,
        "mars": 20.0,
        "ascendant": 30.0,
        "saturn": 29.999999,
    }
    chart = compute_varga(core, "D3", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 4
    assert chart["points"]["mars"]["sign_num"] == 8
    assert chart["points"]["ascendant"]["sign_num"] == 1
    assert chart["points"]["saturn"]["sign_num"] == 8


def test_d3_method4_jagannatha_mapping() -> None:
    core = {"sun": 0.0, "moon": 10.0, "mars": 20.0}
    chart = compute_varga(core, "D3", method=4)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 4
    assert chart["points"]["mars"]["sign_num"] == 8


def test_d2_method1_even_reverse_boundaries() -> None:
    core = {
        "sun": 0.0,
        "moon": 20.0,
        "mars": 30.0,
    }
    chart = compute_varga(core, "D2", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 1
    assert chart["points"]["mars"]["sign_num"] == 3


def test_d2_method2_parasara_boundaries() -> None:
    core = {
        "sun": 0.0,
        "moon": 20.0,
        "mars": 30.0,
        "jupiter": 50.0,
        "saturn": 14.999999,
        "venus": 15.0,
    }
    chart = compute_varga(core, "D2", method=2)
    assert chart["points"]["sun"]["sign_num"] == 4
    assert chart["points"]["moon"]["sign_num"] == 3
    assert chart["points"]["mars"]["sign_num"] == 3
    assert chart["points"]["jupiter"]["sign_num"] == 4
    assert chart["points"]["saturn"]["sign_num"] == 4
    assert chart["points"]["venus"]["sign_num"] == 3


def test_d2_method3_raman_mapping() -> None:
    core = {
        "sun": 0.0,
        "moon": 20.0,
        "mars": 30.0,
    }
    chart = compute_varga(core, "D2", method=3)
    assert chart["points"]["sun"]["sign_num"] == 7
    assert chart["points"]["moon"]["sign_num"] == 9
    assert chart["points"]["mars"]["sign_num"] == 1


def test_d2_method4_parivritti_cyclic_mapping() -> None:
    core = {"sun": 0.0, "moon": 20.0}
    chart = compute_varga(core, "D2", method=4)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 1


def test_d2_method6_parivritti_alternate_mapping() -> None:
    core = {"sun": 0.0, "moon": 20.0, "mars": 30.0}
    chart = compute_varga(core, "D2", method=6)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 1
    assert chart["points"]["mars"]["sign_num"] == 11


def test_d4_method1_boundaries() -> None:
    core = {
        "sun": 0.0,
        "moon": 7.5,
        "mars": 15.0,
        "mercury": 22.5,
        "jupiter": 30.0,
        "saturn": 29.999,
    }
    chart = compute_varga(core, "D4", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 3
    assert chart["points"]["mars"]["sign_num"] == 6
    assert chart["points"]["mercury"]["sign_num"] == 9
    assert chart["points"]["jupiter"]["sign_num"] == 1
    assert chart["points"]["saturn"]["sign_num"] == 9


def test_d5_method1_boundaries() -> None:
    core = {
        "sun": 0.0,
        "moon": 6.0,
        "mars": 29.999,
        "jupiter": 30.0,
        "saturn": 36.0,
    }
    chart = compute_varga(core, "D5", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 10
    assert chart["points"]["mars"]["sign_num"] == 6
    assert chart["points"]["jupiter"]["sign_num"] == 1
    assert chart["points"]["saturn"]["sign_num"] == 5


def test_d6_method1_boundaries() -> None:
    core = {
        "sun": 0.0,
        "moon": 5.0,
        "mars": 29.999,
        "jupiter": 30.0,
        "saturn": 35.0,
    }
    chart = compute_varga(core, "D6", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 1
    assert chart["points"]["mars"]["sign_num"] == 5
    assert chart["points"]["jupiter"]["sign_num"] == 6
    assert chart["points"]["saturn"]["sign_num"] == 7


def test_d7_method1_boundaries() -> None:
    boundary = 30.0 / 7.0
    core = {
        "sun": 0.0,
        "moon": 30.0,
        "mars": boundary,
        "saturn": 29.999,
    }
    chart = compute_varga(core, "D7", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 7
    assert chart["points"]["mars"]["sign_num"] == 1
    assert chart["points"]["saturn"]["sign_num"] == 6


def test_d7_method1_even_signs_mapping() -> None:
    core = {
        "sun": 0.0,      # Aries 0°
        "moon": 30.0,    # Taurus 0°
        "mars": 150.0,   # Virgo 0°
    }
    chart = compute_varga(core, "D7", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 7
    assert chart["points"]["mars"]["sign_num"] == 11


def test_d7_mirror_scope_only_method2() -> None:
    core = {"sun": 0.0, "moon": 35.0}
    chart_no_mirror = compute_varga(core, "D7", method=1, mirror_even_sign=False)["points"]
    chart_mirror = compute_varga(core, "D7", method=1, mirror_even_sign=True)["points"]
    assert chart_no_mirror == chart_mirror

    chart_no_mirror = compute_varga(core, "D7", method=2, mirror_even_sign=False)["points"]
    chart_mirror = compute_varga(core, "D7", method=2, mirror_even_sign=True)["points"]
    assert chart_no_mirror["sun"]["position"] == chart_mirror["sun"]["position"]
    assert chart_no_mirror["moon"]["position"] != chart_mirror["moon"]["position"]


def test_d7_mirror_disabled_without_compat() -> None:
    from diba.vedic.factory import VedicSubjectFactory

    model = VedicSubjectFactory.from_birth_data(
        year=1997,
        month=6,
        day=7,
        hour=20,
        minute=28,
        seconds=36.0,
        lon=51 + 25 / 60,
        lat=35 + 40 / 60,
        tz_str="Asia/Tehran",
        ayanamsa_id="lahiri",
        node_mode="mean",
        house_system_id="whole_sign",
        varga_charts=["D7"],
        varga_methods={"D7": 2},
    )

    core_abs = {k: v.abs_pos_sidereal for k, v in model.core.objects.items()}
    expected = compute_varga(core_abs, "D7", method=2, mirror_even_sign=False)["points"]
    actual_points = model.vargas.charts["D7"].points
    actual = {
        key: (value.model_dump() if hasattr(value, "model_dump") else value)
        for key, value in actual_points.items()
    }
    assert actual == expected


def test_d8_method1_boundaries() -> None:
    boundary = 30.0 / 8.0
    core = {
        "sun": 0.0,
        "moon": 30.0,
        "mars": 60.0,
        "jupiter": boundary,
        "saturn": 29.999,
    }
    chart = compute_varga(core, "D8", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 8
    assert chart["points"]["mars"]["sign_num"] == 4
    assert chart["points"]["jupiter"]["sign_num"] == 1
    assert chart["points"]["saturn"]["sign_num"] == 7


def test_d9_method1_boundaries() -> None:
    boundary = 30.0 / 9.0
    core = {
        "sun": 0.0,
        "moon": 30.0,
        "mars": boundary,
        "saturn": 29.999,
    }
    chart = compute_varga(core, "D9", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 9
    assert chart["points"]["mars"]["sign_num"] == 1
    assert chart["points"]["saturn"]["sign_num"] == 8


def test_d9_method3_kalachakra_indexing() -> None:
    core = {"sun": 0.0}
    chart = compute_varga(core, "D9", method=3)
    assert chart["points"]["sun"]["sign_num"] == 0


def test_d11_method1_boundaries() -> None:
    boundary = 30.0 / 11.0
    core = {
        "sun": 0.0,
        "moon": 30.0,
        "mars": boundary,
        "saturn": 29.999,
    }
    chart = compute_varga(core, "D11", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 11
    assert chart["points"]["mars"]["sign_num"] == 1
    assert chart["points"]["saturn"]["sign_num"] == 10


def test_d11_method2_raman_anti_zodiacal_mapping() -> None:
    core = {"sun": 0.0, "moon": 30.0}
    chart = compute_varga(core, "D11", method=2)
    assert chart["points"]["sun"]["sign_num"] == 11
    assert chart["points"]["moon"]["sign_num"] == 0


def test_d12_method1_boundaries() -> None:
    boundary = 30.0 / 12.0
    core = {
        "sun": 0.0,
        "moon": 30.0,
        "mars": boundary,
        "saturn": 29.999,
    }
    chart = compute_varga(core, "D12", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 1
    assert chart["points"]["mars"]["sign_num"] == 1
    assert chart["points"]["saturn"]["sign_num"] == 11


def test_d16_method1_boundaries() -> None:
    boundary = 30.0 / 16.0
    core = {
        "sun": 0.0,
        "moon": 30.0,
        "mars": boundary,
        "saturn": 29.999,
    }
    chart = compute_varga(core, "D16", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 4
    assert chart["points"]["mars"]["sign_num"] == 1
    assert chart["points"]["saturn"]["sign_num"] == 3


def test_d20_method1_boundaries() -> None:
    boundary = 30.0 / 20.0
    core = {
        "sun": 0.0,
        "moon": 30.0,
        "mars": boundary,
        "saturn": 29.999,
    }
    chart = compute_varga(core, "D20", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 8
    assert chart["points"]["mars"]["sign_num"] == 1
    assert chart["points"]["saturn"]["sign_num"] == 7


def test_d24_method1_boundaries() -> None:
    boundary = 30.0 / 24.0
    core = {
        "sun": 0.0,
        "moon": 30.0,
        "mars": boundary,
        "saturn": 29.999,
    }
    chart = compute_varga(core, "D24", method=1)
    assert chart["points"]["sun"]["sign_num"] == 4
    assert chart["points"]["moon"]["sign_num"] == 3
    assert chart["points"]["mars"]["sign_num"] == 5
    assert chart["points"]["saturn"]["sign_num"] == 3


def test_d27_method1_boundaries() -> None:
    boundary = 30.0 / 27.0
    core = {
        "sun": 0.0,
        "moon": 30.0,
        "mars": boundary,
        "saturn": 29.999,
    }
    chart = compute_varga(core, "D27", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 3
    assert chart["points"]["mars"]["sign_num"] == 1
    assert chart["points"]["saturn"]["sign_num"] == 2


def test_d27_method4_parivritti_cyclic_boundaries() -> None:
    boundary = 30.0 / 27.0
    core = {
        "sun": 0.0,
        "moon": 30.0,
        "mars": boundary,
        "saturn": 29.999,
    }
    chart = compute_varga(core, "D27", method=4)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 3
    assert chart["points"]["mars"]["sign_num"] == 1
    assert chart["points"]["saturn"]["sign_num"] == 2


def test_d30_method1_boundaries() -> None:
    core = {
        "sun": 0.0,
        "moon": 30.0,
        "mars": 5.0,
        "jupiter": 10.0,
        "saturn": 29.999,
    }
    chart = compute_varga(core, "D30", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 1
    assert chart["points"]["mars"]["sign_num"] == 0
    assert chart["points"]["jupiter"]["sign_num"] == 10
    assert chart["points"]["saturn"]["sign_num"] == 6


def test_d40_method1_boundaries() -> None:
    boundary = 30.0 / 40.0
    core = {
        "sun": 0.0,
        "moon": 30.0,
        "mars": boundary,
        "saturn": 29.999,
    }
    chart = compute_varga(core, "D40", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 6
    assert chart["points"]["mars"]["sign_num"] == 1
    assert chart["points"]["saturn"]["sign_num"] == 3


def test_d45_method1_boundaries() -> None:
    boundary = 30.0 / 45.0
    core = {
        "sun": 0.0,
        "moon": 30.0,
        "mars": boundary,
        "saturn": 29.999,
    }
    chart = compute_varga(core, "D45", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 4
    assert chart["points"]["mars"]["sign_num"] == 1
    assert chart["points"]["saturn"]["sign_num"] == 8


def test_d60_method1_boundaries() -> None:
    boundary = 30.0 / 60.0
    core = {
        "sun": 0.0,
        "moon": 30.0,
        "mars": boundary,
        "saturn": 29.999,
    }
    chart = compute_varga(core, "D60", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 1
    assert chart["points"]["mars"]["sign_num"] == 1
    assert chart["points"]["saturn"]["sign_num"] == 11


def test_d81_method1_boundaries() -> None:
    boundary = 30.0 / 81.0
    core = {
        "sun": 0.0,
        "moon": 30.0,
        "mars": boundary,
        "saturn": 29.999,
    }
    chart = compute_varga(core, "D81", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 9
    assert chart["points"]["mars"]["sign_num"] == 1
    assert chart["points"]["saturn"]["sign_num"] == 8


def test_d108_method1_boundaries() -> None:
    boundary = 30.0 / 108.0
    core = {
        "sun": 0.0,
        "moon": 30.0,
        "mars": boundary,
        "saturn": 29.999,
    }
    chart = compute_varga(core, "D108", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 9
    assert chart["points"]["mars"]["sign_num"] == 1
    assert chart["points"]["saturn"]["sign_num"] == 7


def test_d144_method1_boundaries() -> None:
    boundary = 30.0 / 144.0
    core = {
        "sun": 0.0,
        "moon": 30.0,
        "mars": boundary,
        "saturn": 29.999,
    }
    chart = compute_varga(core, "D144", method=1)
    assert chart["points"]["sun"]["sign_num"] == 0
    assert chart["points"]["moon"]["sign_num"] == 1
    assert chart["points"]["mars"]["sign_num"] == 1
    assert chart["points"]["saturn"]["sign_num"] == 10
