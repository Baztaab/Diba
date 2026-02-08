# -*- coding: utf-8 -*-
"""
Vedic Vargas (divisional charts) engine.

Port reference:
    PyJHora - docs/jhora/horoscope/chart/charts.py
    PyJHora - docs/jhora/utils.py (parivritti helpers)
    PyJHora - docs/jhora/const.py (default method table, sign groups)
    PyJHora - docs/jhora/panchanga/drik.py (nakshatra_pada for Kalachakra; future)
"""

from __future__ import annotations

from functools import lru_cache
import ast
import logging
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Optional

_LOG = logging.getLogger(__name__)

_CHART_FACTORS: dict[str, int] = {
    "D1": 1,
    "D2": 2,
    "D3": 3,
    "D4": 4,
    "D5": 5,
    "D6": 6,
    "D7": 7,
    "D8": 8,
    "D9": 9,
    "D10": 10,
    "D11": 11,
    "D12": 12,
    "D16": 16,
    "D20": 20,
    "D24": 24,
    "D27": 27,
    "D30": 30,
    "D40": 40,
    "D45": 45,
    "D60": 60,
    "D81": 81,
    "D108": 108,
    "D144": 144,
    "D150": 150,
}

_SIGNS = ["Ari", "Tau", "Gem", "Can", "Leo", "Vir", "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis"]
_FIRE_SIGNS = {0, 4, 8}
_EARTH_SIGNS = {1, 5, 9}
_AIR_SIGNS = {2, 6, 10}
_WATER_SIGNS = {3, 7, 11}
_ODD_SIGNS = {0, 2, 4, 6, 8, 10}
_EVEN_SIGNS = {1, 3, 5, 7, 9, 11}

_HOUSE_OWNERS = [2, 5, 3, 1, 0, 3, 5, 2, 4, 6, 6, 4]
_HORA_LIST_RAMAN = [
    (7, 9),
    (1, 11),
    (5, 0),
    (3, 6),
    (4, 2),
    (2, 3),
    (6, 4),
    (0, 5),
    (11, 1),
    (9, 7),
    (10, 8),
    (8, 10),
]
_DREKKANA_JAGANNATHA = [
    (0, 4, 8),
    (9, 1, 5),
    (6, 10, 2),
    (3, 7, 11),
    (0, 4, 8),
    (9, 1, 5),
    (6, 10, 2),
    (3, 7, 11),
    (0, 4, 8),
    (9, 1, 5),
    (6, 10, 2),
    (3, 7, 11),
]
_MOVABLE_SIGNS = {0, 3, 6, 9}
_FIXED_SIGNS = {1, 4, 7, 10}
_DUAL_SIGNS = {2, 5, 8, 11}
_PLANET_NAME_TO_INDEX = {
    "sun": 0,
    "moon": 1,
    "mars": 2,
    "mercury": 3,
    "jupiter": 4,
    "venus": 5,
    "saturn": 6,
    "rahu": 7,
    "ketu": 8,
}

# Mirrors docs/jhora/const.py varga_option_dict defaults (second element per D).
def _defaults_from_pyjhora_const() -> dict[str, int]:
    """
    Load default varga methods from PyJHora const.varga_option_dict when available.
    Falls back to method=1 for all charts if the source is missing.
    """
    fallback = {f"D{factor}": 1 for factor in _CHART_FACTORS.values()}
    repo_root = Path(__file__).resolve().parents[2]
    const_path = repo_root / "docs" / "jhora" / "const.py"
    if not const_path.exists():
        return fallback
    try:
        text = const_path.read_text(encoding="utf-8")
    except Exception:
        return fallback
    marker = "varga_option_dict"
    if marker not in text:
        return fallback
    try:
        start = text.index(marker)
        brace = text.index("{", start)
        end = text.index("}", brace)
        literal = text[brace : end + 1]
        parsed = ast.literal_eval(literal)
        defaults: dict[str, int] = {}
        for factor, (_, default) in parsed.items():
            defaults[f"D{int(factor)}"] = int(default)
        return {**fallback, **defaults}
    except Exception:
        return fallback


_DEFAULT_METHOD_BY_CHART: dict[str, int] = _defaults_from_pyjhora_const()


@lru_cache(maxsize=1)
def _kalachakra_navamsa_map() -> dict[int, list[int]]:
    repo_root = Path(__file__).resolve().parents[2]
    const_path = repo_root / "docs" / "jhora" / "const.py"
    if not const_path.exists():
        return {}
    try:
        text = const_path.read_text(encoding="utf-8")
        marker = "kalachakra_navamsa"
        start = text.index(marker)
        brace = text.index("{", start)
        end = text.index("}", brace)
        literal = text[brace : end + 1]
        parsed = ast.literal_eval(literal)
        return {int(k): list(v) for k, v in parsed.items()}
    except Exception:
        return {}


def _nakshatra_pada(longitude: float) -> tuple[int, int, float]:
    one_star = 360.0 / 27.0
    one_pada = 360.0 / 108.0
    quotient = int(longitude / one_star)
    remainder = longitude % one_star
    pada = int(remainder / one_pada)
    return (1 + quotient, 1 + pada, remainder)

_METHOD_LABELS: dict[str, dict[int, str]] = {
    "D1": {1: "rasi"},
    "D2": {
        1: "parivritti_even_reverse",
        2: "parasara_traditional_hora",
        3: "raman",
        4: "parivritti_cyclic",
        5: "kashinath",
        6: "parivritti_alternate",
    },
    "D3": {1: "parasara", 2: "parivritti_cyclic", 3: "parivritti_alternate", 4: "jagannatha", 5: "parivritti_even_reverse"},
    "D4": {1: "parasara", 2: "parivritti_cyclic", 3: "parivritti_even_reverse", 4: "parivritti_alternate"},
    "D5": {1: "parasara", 2: "parivritti_cyclic", 3: "parivritti_even_reverse", 4: "parivritti_alternate"},
    "D6": {1: "parasara", 2: "parivritti_cyclic", 3: "parivritti_even_reverse", 4: "parivritti_alternate"},
    "D7": {
        1: "parasara_even_forward",
        2: "parasara_even_backward",
        3: "parasara_even_reverse_end_7th",
        4: "parivritti_cyclic",
        5: "parivritti_even_reverse",
        6: "parivritti_alternate",
    },
    "D8": {1: "parasara", 2: "parivritti_cyclic", 3: "parivritti_even_reverse", 4: "parivritti_alternate"},
    "D9": {
        1: "parasara_element_seed",
        2: "parivritti_even_reverse",
        3: "kalachakra",
        4: "krishna_mishra_nadi",
        5: "parivritti_cyclic",
        6: "parivritti_alternate",
    },
    "D10": {
        1: "parasara_even_forward",
        2: "parasara_even_backward",
        3: "parasara_even_reverse_9th_backward",
        4: "parivritti_cyclic",
        5: "parivritti_even_reverse",
        6: "parivritti_alternate",
    },
    "D11": {
        1: "parasara_traditional",
        2: "raman_anti_zodiacal",
        3: "parivritti_cyclic",
        4: "parivritti_even_reverse",
        5: "parivritti_alternate",
    },
    "D12": {
        1: "parasara_traditional",
        2: "parasara_even_reverse",
        3: "parivritti_cyclic",
        4: "parivritti_even_reverse",
        5: "parivritti_alternate",
    },
    "D16": {
        1: "parasara_traditional",
        2: "parivritti_even_reverse",
        3: "parivritti_cyclic",
        4: "parivritti_alternate",
    },
    "D20": {
        1: "parasara_traditional",
        2: "parivritti_even_reverse",
        3: "parivritti_cyclic",
        4: "parivritti_alternate",
    },
    "D24": {
        1: "parasara_siddhamsa",
        2: "parasara_even_reverse",
        3: "parasara_even_double_reverse",
    },
    "D27": {
        1: "parasara_traditional",
        2: "parivritti_even_reverse",
        3: "parivritti_alternate",
        4: "parivritti_cyclic",
    },
    "D30": {
        1: "parasara_traditional",
        2: "parivritti_cyclic",
        3: "shashtyamsa_like",
        4: "parivritti_even_reverse",
        5: "parivritti_alternate",
    },
    "D40": {
        1: "parasara_traditional",
        2: "parivritti_cyclic",
        3: "parivritti_even_reverse",
        4: "parivritti_alternate",
    },
    "D45": {
        1: "parasara_traditional",
        2: "parivritti_cyclic",
        3: "parivritti_even_reverse",
        4: "parivritti_alternate",
    },
    "D60": {
        1: "parasara_from_sign",
        2: "parasara_from_aries",
        3: "parivritti_alternate",
        4: "parasara_even_reverse_from_sign",
    },
    "D81": {
        1: "parivritti_cyclic",
        2: "parivritti_even_reverse",
        3: "parivritti_alternate",
        4: "kalachakra",
    },
    "D108": {
        1: "parasara_traditional",
        2: "parivritti_cyclic",
        3: "parivritti_even_reverse",
        4: "parivritti_alternate",
    },
    "D144": {
        1: "parasara_traditional",
        2: "parivritti_cyclic",
        3: "parivritti_even_reverse",
        4: "parivritti_alternate",
    },
}

_SUPPORTED_METHODS: dict[str, set[int]] = {
    "D1": {1},
    "D2": {1, 2, 3, 4, 5, 6},
    "D3": {1, 2, 3, 4, 5},
    "D4": {1, 2, 3, 4},
    "D5": {1, 2, 3, 4},
    "D6": {1, 2, 3, 4},
    "D7": {1, 2, 3, 4, 5, 6},
    "D8": {1, 2, 3, 4},
    "D9": {1, 2, 3, 4, 5, 6},
    "D10": {1, 2, 3, 4, 5, 6},
    "D11": {1, 2, 3, 4, 5},
    "D12": {1, 2, 3, 4, 5},
    "D16": {1, 2, 3, 4},
    "D20": {1, 2, 3, 4},
    "D24": {1, 2, 3},
    "D27": {1, 2, 3, 4},
    "D30": {1, 2, 3, 4, 5},
    "D40": {1, 2, 3, 4},
    "D45": {1, 2, 3, 4},
    "D60": {1, 2, 3, 4},
    "D81": {1, 2, 3, 4},
    "D108": {1, 2, 3, 4},
    "D144": {1, 2, 3, 4},
}

_PROFILE_METHODS: dict[str, dict[str, int]] = {
    "US": {"D2": 1, "D3": 5},
}


def normalize_chart_id(chart_id: str) -> str:
    raw = chart_id.strip().upper()
    if raw.startswith("D"):
        raw = raw[1:]
    factor = int(raw)
    return f"D{factor}"


def split_abs_pos(abs_pos: float) -> tuple[int, float]:
    abs_norm = float(abs_pos) % 360.0
    sign_num = int(abs_norm // 30.0) % 12
    pos_in_sign = abs_norm % 30.0
    return sign_num, pos_in_sign


def seg_and_dlong(pos_in_sign: float, factor: int) -> tuple[int, float]:
    f1 = 30.0 / factor
    seg = int(pos_in_sign // f1)
    d_long = (pos_in_sign * factor) % 30.0
    return seg, d_long


def _seg_and_dlong_clamped(pos_in_sign: float, factor: int) -> tuple[int, float]:
    seg, d_long = seg_and_dlong(pos_in_sign, factor)
    max_seg = factor - 1
    if seg > max_seg:
        seg = max_seg
    return seg, d_long


def parivritti_cyclic(sign_num: int, seg: int, factor: int) -> int:
    return (sign_num * factor + seg) % 12


@lru_cache(maxsize=32)
def _parivritti_even_reverse_map(factor: int) -> dict[tuple[int, int], int]:
    mapping: dict[tuple[int, int], int] = {}
    varga_sign = 0
    for sign in range(0, 12, 2):
        for seg in range(0, factor):
            mapping[(sign, seg)] = varga_sign % 12
            varga_sign += 1
        sign_even = sign + 1
        for seg in range(factor - 1, -1, -1):
            mapping[(sign_even, seg)] = varga_sign % 12
            varga_sign += 1
    return mapping


def parivritti_even_reverse(sign_num: int, seg: int, factor: int) -> int:
    return _parivritti_even_reverse_map(factor)[(sign_num, seg)]


@lru_cache(maxsize=32)
def _parivritti_alternate_map(factor: int) -> dict[tuple[int, int], int]:
    mapping: dict[tuple[int, int], int] = {}
    inc = 0
    dec = 11
    for sign in range(0, 12, 2):
        for seg in range(factor):
            mapping[(sign, seg)] = inc % 12
            inc += 1
        sign_even = sign + 1
        for seg in range(factor):
            mapping[(sign_even, seg)] = dec % 12
            dec -= 1
    return mapping


def parivritti_alternate(sign_num: int, seg: int, factor: int) -> int:
    return _parivritti_alternate_map(factor)[(sign_num, seg)]


def _parivritti_cyclic_sign(sign_num: int, seg: int, _pos_in_sign: float, factor: int) -> int:
    return parivritti_cyclic(sign_num, seg, factor)


def _parivritti_even_reverse_sign(sign_num: int, seg: int, _pos_in_sign: float, factor: int) -> int:
    return parivritti_even_reverse(sign_num, seg, factor)


def _parivritti_alternate_sign(sign_num: int, seg: int, _pos_in_sign: float, factor: int) -> int:
    return parivritti_alternate(sign_num, seg, factor)


def _abs_from(value: Any) -> float:
    if hasattr(value, "abs_pos_sidereal"):
        return float(getattr(value, "abs_pos_sidereal"))
    return float(value)


def _point_payload(sign_num: int, position: float) -> dict[str, object]:
    return {
        "sign_num": sign_num,
        "sign": _SIGNS[sign_num],
        "position": float(position),
        "abs_pos": float((sign_num * 30.0 + position) % 360.0),
    }


def _core_from_points(points: Mapping[str, Mapping[str, object]]) -> dict[str, float]:
    core: dict[str, float] = {}
    for name, payload in points.items():
        sign_num = int(payload["sign_num"])
        pos = float(payload["position"])
        core[name] = (sign_num * 30.0 + pos) % 360.0
    return core


def _build_points(
    core_objects: Mapping[str, Any],
    factor: int,
    sign_fn,
    clamp: bool = False,
    *,
    mirror_even_sign: bool = False,
) -> dict[str, dict[str, object]]:
    points: dict[str, dict[str, object]] = {}
    for name, obj in core_objects.items():
        abs_pos = _abs_from(obj)
        sign_num, pos_in_sign = split_abs_pos(abs_pos)
        if clamp:
            seg, d_long = _seg_and_dlong_clamped(pos_in_sign, factor)
        else:
            seg, d_long = seg_and_dlong(pos_in_sign, factor)
        if mirror_even_sign and sign_num in _EVEN_SIGNS:
            d_long = (30.0 - d_long) % 30.0
        varga_sign = sign_fn(sign_num, seg, pos_in_sign, factor)
        points[name] = _point_payload(varga_sign, d_long)
    return points


def _planet_positions_in_rasi(core_objects: Mapping[str, Any]) -> list[list[object]]:
    positions: list[list[object]] = []
    asc_obj = core_objects.get("ascendant")
    if asc_obj is not None:
        abs_pos = _abs_from(asc_obj)
        sign_num, pos_in_sign = split_abs_pos(abs_pos)
        positions.append(["L", (sign_num, pos_in_sign)])
    for name, idx in _PLANET_NAME_TO_INDEX.items():
        obj = core_objects.get(name)
        if obj is None:
            continue
        abs_pos = _abs_from(obj)
        sign_num, pos_in_sign = split_abs_pos(abs_pos)
        positions.append([idx, (sign_num, pos_in_sign)])
    return positions


def _stronger_planet_by_longitude(core_objects: Mapping[str, Any], planet_a: int, planet_b: int) -> int:
    rev_map = {v: k for k, v in _PLANET_NAME_TO_INDEX.items()}
    name_a = rev_map.get(planet_a)
    name_b = rev_map.get(planet_b)
    if name_a is None or name_b is None:
        return planet_a
    obj_a = core_objects.get(name_a)
    obj_b = core_objects.get(name_b)
    if obj_a is None or obj_b is None:
        return planet_a
    pos_a = split_abs_pos(_abs_from(obj_a))[1]
    pos_b = split_abs_pos(_abs_from(obj_b))[1]
    return planet_a if pos_a >= pos_b else planet_b


def _house_owner_from_core(core_objects: Mapping[str, Any], sign_num: int) -> int:
    lord = _HOUSE_OWNERS[sign_num]
    if sign_num == 7:
        return _stronger_planet_by_longitude(core_objects, 2, 8)
    if sign_num == 10:
        return _stronger_planet_by_longitude(core_objects, 6, 7)
    return lord


def _chart_d1(core_objects: Mapping[str, Any], method: int, *, mirror_even_sign: bool = False) -> dict[str, object]:
    factor = 1
    _ = mirror_even_sign
    points = {}
    for name, obj in core_objects.items():
        abs_pos = _abs_from(obj)
        sign_num, pos_in_sign = split_abs_pos(abs_pos)
        points[name] = _point_payload(sign_num, pos_in_sign)
    return {
        "factor": factor,
        "method": method,
        "method_label": _METHOD_LABELS.get("D1", {}).get(method),
        "lagna": points.get("ascendant"),
        "points": points,
    }

def _chart_d3_method1(sign_num: int, seg: int, _pos_in_sign: float, _factor: int) -> int:
    return (sign_num + seg * 4) % 12


def _chart_d3_method4(sign_num: int, seg: int, _pos_in_sign: float, _factor: int) -> int:
    return _DREKKANA_JAGANNATHA[sign_num][seg]


def _chart_d3(
    core_objects: Mapping[str, Any], method: int, *, mirror_even_sign: bool = False
) -> dict[str, object]:
    """
    Drekkana (D3) method 1 derived from PyJHora charts.py (Parasara).
    """
    factor = 3
    if method == 1:
        points = _build_points(core_objects, factor, _chart_d3_method1, clamp=True)
    elif method == 2:
        points = _build_points(core_objects, factor, _parivritti_cyclic_sign, clamp=True)
    elif method == 3:
        points = _build_points(core_objects, factor, _parivritti_alternate_sign, clamp=True)
    elif method == 4:
        points = _build_points(core_objects, factor, _chart_d3_method4, clamp=True)
    elif method == 5:
        points = _build_points(
            core_objects,
            factor,
            _chart_d2_method1,
            clamp=True,
            mirror_even_sign=mirror_even_sign,
        )
    else:
        _LOG.warning("Varga D3 method %s not implemented; falling back to method 1.", method)
        method = 1
        points = _build_points(core_objects, factor, _chart_d3_method1, clamp=True)
    return {
        "factor": factor,
        "method": method,
        "method_label": _METHOD_LABELS.get("D3", {}).get(method),
        "lagna": points.get("ascendant"),
        "points": points,
    }


def _chart_d2_method1(sign_num: int, seg: int, _pos_in_sign: float, factor: int) -> int:
    return parivritti_even_reverse(sign_num, seg, factor)


def _chart_d2_method2(sign_num: int, seg: int, _pos_in_sign: float, _factor: int) -> int:
    if sign_num in _ODD_SIGNS:
        return 4 if seg == 0 else 3
    return 3 if seg == 0 else 4


def _chart_d2_method3(sign_num: int, seg: int, _pos_in_sign: float, _factor: int) -> int:
    return _HORA_LIST_RAMAN[sign_num][seg]


def _chart_d2(
    core_objects: Mapping[str, Any], method: int, *, mirror_even_sign: bool = False
) -> dict[str, object]:
    """
    Hora (D2) methods 1/2 derived from PyJHora charts.py and utils.parivritti_even_reverse.
    """
    factor = 2
    if method == 1:
        points = _build_points(
            core_objects,
            factor,
            _chart_d2_method1,
            clamp=True,
            mirror_even_sign=mirror_even_sign,
        )
    elif method == 2:
        points = _build_points(core_objects, factor, _chart_d2_method2, clamp=True)
    elif method == 3:
        points = _build_points(core_objects, factor, _chart_d2_method3, clamp=True)
    elif method == 4:
        points = _build_points(core_objects, factor, _parivritti_cyclic_sign, clamp=True)
    elif method == 5:
        planet_hora = {
            0: (4, 4),
            1: (3, 3),
            2: (7, 0),
            3: (5, 2),
            4: (11, 8),
            5: (6, 1),
            6: (10, 9),
            7: (10, 10),
            8: (4, 4),
        }
        points = {}
        for name, obj in core_objects.items():
            abs_pos = _abs_from(obj)
            sign_num, pos_in_sign = split_abs_pos(abs_pos)
            seg, d_long = _seg_and_dlong_clamped(pos_in_sign, factor)
            lord = _house_owner_from_core(core_objects, sign_num)
            if sign_num in _ODD_SIGNS:
                hora_sign = planet_hora[lord][0] if seg == 0 else planet_hora[lord][1]
            else:
                hora_sign = planet_hora[lord][1] if seg == 0 else planet_hora[lord][0]
            points[name] = _point_payload(hora_sign, d_long)
    elif method == 6:
        points = _build_points(core_objects, factor, _parivritti_alternate_sign, clamp=True)
    else:
        _LOG.warning("Varga D2 method %s not implemented; falling back to method 1.", method)
        method = 1
        points = _build_points(
            core_objects,
            factor,
            _chart_d2_method1,
            clamp=True,
            mirror_even_sign=mirror_even_sign,
        )
    return {
        "factor": factor,
        "method": method,
        "method_label": _METHOD_LABELS.get("D2", {}).get(method),
        "lagna": points.get("ascendant"),
        "points": points,
    }


def _chart_d4_method1(sign_num: int, seg: int, _pos_in_sign: float, _factor: int) -> int:
    return (sign_num + seg * 3) % 12


def _chart_d4(
    core_objects: Mapping[str, Any], method: int, *, mirror_even_sign: bool = False
) -> dict[str, object]:
    """
    Chaturthamsa (D4) methods derived from PyJHora charts.py.
    """
    factor = 4
    _ = mirror_even_sign
    if method == 1:
        points = _build_points(core_objects, factor, _chart_d4_method1, clamp=True)
    elif method == 2:
        points = _build_points(core_objects, factor, _parivritti_cyclic_sign, clamp=True)
    elif method == 3:
        points = _build_points(core_objects, factor, _parivritti_even_reverse_sign, clamp=True)
    elif method == 4:
        points = _build_points(core_objects, factor, _parivritti_alternate_sign, clamp=True)
    else:
        _LOG.warning("Varga D4 method %s not implemented; falling back to method 1.", method)
        method = 1
        points = _build_points(core_objects, factor, _chart_d4_method1, clamp=True)
    return {
        "factor": factor,
        "method": method,
        "method_label": _METHOD_LABELS.get("D4", {}).get(method),
        "lagna": points.get("ascendant"),
        "points": points,
    }


def _chart_d5_method1(sign_num: int, seg: int, _pos_in_sign: float, _factor: int) -> int:
    odd = [0, 10, 8, 2, 6]
    even = [1, 5, 11, 9, 7]
    rasi = even[seg]
    if sign_num in _ODD_SIGNS:
        rasi = odd[seg]
    return rasi % 12


def _chart_d5(
    core_objects: Mapping[str, Any], method: int, *, mirror_even_sign: bool = False
) -> dict[str, object]:
    """
    Panchamsa (D5) methods derived from PyJHora charts.py.
    """
    factor = 5
    _ = mirror_even_sign
    if method == 1:
        points = _build_points(core_objects, factor, _chart_d5_method1, clamp=True)
    elif method == 2:
        points = _build_points(core_objects, factor, _parivritti_cyclic_sign, clamp=True)
    elif method == 3:
        points = _build_points(core_objects, factor, _parivritti_even_reverse_sign, clamp=True)
    elif method == 4:
        points = _build_points(core_objects, factor, _parivritti_alternate_sign, clamp=True)
    else:
        _LOG.warning("Varga D5 method %s not implemented; falling back to method 1.", method)
        method = 1
        points = _build_points(core_objects, factor, _chart_d5_method1, clamp=True)
    return {
        "factor": factor,
        "method": method,
        "method_label": _METHOD_LABELS.get("D5", {}).get(method),
        "lagna": points.get("ascendant"),
        "points": points,
    }


def _chart_d6_method1(sign_num: int, seg: int, _pos_in_sign: float, _factor: int) -> int:
    varga_sign = seg % 12
    if sign_num in _EVEN_SIGNS:
        varga_sign = (seg + 6) % 12
    return varga_sign


def _chart_d6(
    core_objects: Mapping[str, Any], method: int, *, mirror_even_sign: bool = False
) -> dict[str, object]:
    """
    Shashthamsa (D6) methods derived from PyJHora charts.py.
    """
    factor = 6
    _ = mirror_even_sign
    if method == 1:
        points = _build_points(core_objects, factor, _chart_d6_method1, clamp=True)
    elif method == 2:
        points = _build_points(core_objects, factor, _parivritti_cyclic_sign, clamp=True)
    elif method == 3:
        points = _build_points(core_objects, factor, _parivritti_even_reverse_sign, clamp=True)
    elif method == 4:
        points = _build_points(core_objects, factor, _parivritti_alternate_sign, clamp=True)
    else:
        _LOG.warning("Varga D6 method %s not implemented; falling back to method 1.", method)
        method = 1
        points = _build_points(core_objects, factor, _chart_d6_method1, clamp=True)
    return {
        "factor": factor,
        "method": method,
        "method_label": _METHOD_LABELS.get("D6", {}).get(method),
        "lagna": points.get("ascendant"),
        "points": points,
    }


def _chart_d7_method(sign_num: int, seg: int, _pos_in_sign: float, _factor: int, method: int) -> int:
    dirn = -1 if method in {2, 3} else 1
    r = (sign_num + seg) % 12
    even_signs = {1, 3, 5, 7, 9, 11}
    if sign_num in even_signs:
        r = (sign_num + dirn * (seg + 6)) % 12
        if method == 3:
            r = (r - 6) % 12
    return r


def _chart_d7(
    core_objects: Mapping[str, Any], method: int, *, mirror_even_sign: bool = False
) -> dict[str, object]:
    """
    Saptamsa (D7) methods derived from PyJHora charts.py.
    """
    factor = 7
    _ = mirror_even_sign
    if method in {1, 2, 3}:
        def _sign_fn(sign_num: int, seg: int, pos_in_sign: float, _factor: int) -> int:
            _ = pos_in_sign
            return _chart_d7_method(sign_num, seg, pos_in_sign, _factor, method)

        points = _build_points(
            core_objects,
            factor,
            _sign_fn,
            clamp=True,
            mirror_even_sign=(method == 2 and mirror_even_sign),
        )
    elif method == 4:
        points = _build_points(core_objects, factor, _parivritti_cyclic_sign, clamp=True)
    elif method == 5:
        points = _build_points(core_objects, factor, _parivritti_even_reverse_sign, clamp=True)
    elif method == 6:
        points = _build_points(core_objects, factor, _parivritti_alternate_sign, clamp=True)
    else:
        _LOG.warning("Varga D7 method %s not implemented; falling back to method 1.", method)
        method = 1
        points = _build_points(
            core_objects,
            factor,
            lambda sign_num, seg, pos_in_sign, _factor: _chart_d7_method(
                sign_num, seg, pos_in_sign, _factor, method
            ),
            clamp=True,
        )
    return {
        "factor": factor,
        "method": method,
        "method_label": _METHOD_LABELS.get("D7", {}).get(method),
        "lagna": points.get("ascendant"),
        "points": points,
    }


def _chart_d8_method1(sign_num: int, seg: int, _pos_in_sign: float, _factor: int) -> int:
    r = seg % 12
    if sign_num in _DUAL_SIGNS:
        return (seg + 4) % 12
    if sign_num in _FIXED_SIGNS:
        return (seg + 8) % 12
    return r


def _chart_d8(
    core_objects: Mapping[str, Any], method: int, *, mirror_even_sign: bool = False
) -> dict[str, object]:
    """
    Ashtamsa (D8) methods derived from PyJHora charts.py.
    """
    factor = 8
    _ = mirror_even_sign
    if method == 1:
        points = _build_points(core_objects, factor, _chart_d8_method1, clamp=True)
    elif method == 2:
        points = _build_points(core_objects, factor, _parivritti_cyclic_sign, clamp=True)
    elif method == 3:
        points = _build_points(core_objects, factor, _parivritti_even_reverse_sign, clamp=True)
    elif method == 4:
        points = _build_points(core_objects, factor, _parivritti_alternate_sign, clamp=True)
    else:
        _LOG.warning("Varga D8 method %s not implemented; falling back to method 1.", method)
        method = 1
        points = _build_points(core_objects, factor, _chart_d8_method1, clamp=True)
    return {
        "factor": factor,
        "method": method,
        "method_label": _METHOD_LABELS.get("D8", {}).get(method),
        "lagna": points.get("ascendant"),
        "points": points,
    }
def _chart_d9_method1(sign_num: int, seg: int, _pos_in_sign: float, _factor: int) -> int:
    if sign_num in _FIRE_SIGNS:
        seed, dirn = 0, 1
    elif sign_num in _WATER_SIGNS:
        seed, dirn = 3, 1
    elif sign_num in _AIR_SIGNS:
        seed, dirn = 6, 1
    else:
        seed, dirn = 9, 1
    return (seed + dirn * seg) % 12


def _chart_d9_method4(sign_num: int, seg: int, _pos_in_sign: float, _factor: int) -> int:
    if sign_num in _FIRE_SIGNS:
        seed, dirn = 0, 1
    elif sign_num in _WATER_SIGNS:
        seed, dirn = 3, -1
    elif sign_num in _AIR_SIGNS:
        seed, dirn = 6, 1
    else:
        seed, dirn = 9, -1
    return (seed + dirn * seg) % 12


def _chart_d9_method3(sign_num: int, _seg: int, pos_in_sign: float, _factor: int) -> int:
    abs_long = (sign_num * 30.0 + pos_in_sign) % 360.0
    nak, pada, _ = _nakshatra_pada(abs_long)
    mapping = _kalachakra_navamsa_map()
    if not mapping:
        raise ValueError("Kalachakra navamsa mapping not available.")
    return mapping[nak - 1][pada - 1]


def _chart_d9(core_objects: Mapping[str, Any], method: int, *, mirror_even_sign: bool = False) -> dict[str, object]:
    factor = 9
    _ = mirror_even_sign
    if method == 1:
        points = _build_points(core_objects, factor, _chart_d9_method1)
    elif method == 2:
        points = _build_points(core_objects, factor, _parivritti_even_reverse_sign)
    elif method == 3:
        points = _build_points(core_objects, factor, _chart_d9_method3)
    elif method == 4:
        points = _build_points(core_objects, factor, _chart_d9_method4)
    elif method == 5:
        points = _build_points(core_objects, factor, _parivritti_cyclic_sign)
    elif method == 6:
        points = _build_points(core_objects, factor, _parivritti_alternate_sign)
    else:
        _LOG.warning("Varga D9 method %s not implemented; falling back to method 1.", method)
        method = 1
        points = _build_points(core_objects, factor, _chart_d9_method1)
    return {
        "factor": factor,
        "method": method,
        "method_label": _METHOD_LABELS.get("D9", {}).get(method),
        "lagna": points.get("ascendant"),
        "points": points,
    }


def _chart_d10_method(sign_num: int, seg: int, _pos_in_sign: float, _factor: int, method: int) -> int:
    dirn = -1 if method in {2, 3} else 1
    r = (sign_num + seg) % 12
    if sign_num in _EVEN_SIGNS:
        r = (sign_num + dirn * (seg + 8)) % 12
        if method == 2:
            r = (r - 8) % 12
    return r


def _chart_d10(core_objects: Mapping[str, Any], method: int, *, mirror_even_sign: bool = False) -> dict[str, object]:
    factor = 10
    if method in {1, 2, 3}:
        def _sign_fn(sign_num: int, seg: int, pos_in_sign: float, _factor: int) -> int:
            _ = pos_in_sign
            return _chart_d10_method(sign_num, seg, pos_in_sign, _factor, method)

        points = _build_points(
            core_objects,
            factor,
            _sign_fn,
            mirror_even_sign=(method == 3 and mirror_even_sign),
        )
    elif method == 4:
        points = _build_points(core_objects, factor, _parivritti_cyclic_sign)
    elif method == 5:
        points = _build_points(core_objects, factor, _parivritti_even_reverse_sign)
    elif method == 6:
        points = _build_points(core_objects, factor, _parivritti_alternate_sign)
    else:
        _LOG.warning("Varga D10 method %s not implemented; falling back to method 1.", method)
        method = 1
        points = _build_points(
            core_objects,
            factor,
            lambda sign_num, seg, pos_in_sign, _factor: _chart_d10_method(
                sign_num, seg, pos_in_sign, _factor, method
            ),
        )
    return {
        "factor": factor,
        "method": method,
        "method_label": _METHOD_LABELS.get("D10", {}).get(method),
        "lagna": points.get("ascendant"),
        "points": points,
    }


def _chart_d11_method1(sign_num: int, seg: int, _pos_in_sign: float, _factor: int) -> int:
    return (12 - sign_num + seg) % 12


def _chart_d11_method2(sign_num: int, seg: int, _pos_in_sign: float, _factor: int) -> int:
    r = _chart_d11_method1(sign_num, seg, _pos_in_sign, _factor)
    return (11 - r) % 12


def _chart_d11(core_objects: Mapping[str, Any], method: int, *, mirror_even_sign: bool = False) -> dict[str, object]:
    factor = 11
    _ = mirror_even_sign
    if method == 1:
        points = _build_points(core_objects, factor, _chart_d11_method1)
    elif method == 2:
        points = _build_points(core_objects, factor, _chart_d11_method2)
    elif method == 3:
        points = _build_points(core_objects, factor, _parivritti_cyclic_sign)
    elif method == 4:
        points = _build_points(core_objects, factor, _parivritti_even_reverse_sign)
    elif method == 5:
        points = _build_points(core_objects, factor, _parivritti_alternate_sign)
    else:
        _LOG.warning("Varga D11 method %s not implemented; falling back to method 1.", method)
        method = 1
        points = _build_points(core_objects, factor, _chart_d11_method1)
    return {
        "factor": factor,
        "method": method,
        "method_label": _METHOD_LABELS.get("D11", {}).get(method),
        "lagna": points.get("ascendant"),
        "points": points,
    }


def _chart_d12_method(sign_num: int, seg: int, _pos_in_sign: float, _factor: int, method: int) -> int:
    dirn = -1 if sign_num in _EVEN_SIGNS and method == 2 else 1
    return (sign_num + dirn * seg) % 12


def _chart_d12(core_objects: Mapping[str, Any], method: int, *, mirror_even_sign: bool = False) -> dict[str, object]:
    factor = 12
    _ = mirror_even_sign
    if method in {1, 2}:
        def _sign_fn(sign_num: int, seg: int, pos_in_sign: float, _factor: int) -> int:
            _ = pos_in_sign
            return _chart_d12_method(sign_num, seg, pos_in_sign, _factor, method)

        points = _build_points(core_objects, factor, _sign_fn)
    elif method == 3:
        points = _build_points(core_objects, factor, _parivritti_cyclic_sign)
    elif method == 4:
        points = _build_points(core_objects, factor, _parivritti_even_reverse_sign)
    elif method == 5:
        points = _build_points(core_objects, factor, _parivritti_alternate_sign)
    else:
        _LOG.warning("Varga D12 method %s not implemented; falling back to method 1.", method)
        method = 1
        points = _build_points(
            core_objects,
            factor,
            lambda sign_num, seg, pos_in_sign, _factor: _chart_d12_method(
                sign_num, seg, pos_in_sign, _factor, method
            ),
        )
    return {
        "factor": factor,
        "method": method,
        "method_label": _METHOD_LABELS.get("D12", {}).get(method),
        "lagna": points.get("ascendant"),
        "points": points,
    }


def _chart_d16_method1(sign_num: int, seg: int, _pos_in_sign: float, _factor: int) -> int:
    r = seg % 12
    if sign_num in _FIXED_SIGNS:
        return (seg + 4) % 12
    if sign_num in _DUAL_SIGNS:
        return (seg + 8) % 12
    return r


def _chart_d16(core_objects: Mapping[str, Any], method: int, *, mirror_even_sign: bool = False) -> dict[str, object]:
    factor = 16
    if method == 1:
        points = _build_points(core_objects, factor, _chart_d16_method1)
    elif method == 2:
        points = _build_points(
            core_objects,
            factor,
            _parivritti_even_reverse_sign,
            mirror_even_sign=mirror_even_sign,
        )
    elif method == 3:
        points = _build_points(core_objects, factor, _parivritti_cyclic_sign)
    elif method == 4:
        points = _build_points(core_objects, factor, _parivritti_alternate_sign)
    else:
        _LOG.warning("Varga D16 method %s not implemented; falling back to method 1.", method)
        method = 1
        points = _build_points(core_objects, factor, _chart_d16_method1)
    return {
        "factor": factor,
        "method": method,
        "method_label": _METHOD_LABELS.get("D16", {}).get(method),
        "lagna": points.get("ascendant"),
        "points": points,
    }


def _chart_d20_method1(sign_num: int, seg: int, _pos_in_sign: float, _factor: int) -> int:
    r = seg % 12
    if sign_num in _DUAL_SIGNS:
        return (seg + 4) % 12
    if sign_num in _FIXED_SIGNS:
        return (seg + 8) % 12
    return r


def _chart_d20(core_objects: Mapping[str, Any], method: int, *, mirror_even_sign: bool = False) -> dict[str, object]:
    factor = 20
    _ = mirror_even_sign
    if method == 1:
        points = _build_points(core_objects, factor, _chart_d20_method1)
    elif method == 2:
        points = _build_points(core_objects, factor, _parivritti_even_reverse_sign)
    elif method == 3:
        points = _build_points(core_objects, factor, _parivritti_cyclic_sign)
    elif method == 4:
        points = _build_points(core_objects, factor, _parivritti_alternate_sign)
    else:
        _LOG.warning("Varga D20 method %s not implemented; falling back to method 1.", method)
        method = 1
        points = _build_points(core_objects, factor, _chart_d20_method1)
    return {
        "factor": factor,
        "method": method,
        "method_label": _METHOD_LABELS.get("D20", {}).get(method),
        "lagna": points.get("ascendant"),
        "points": points,
    }


def _chart_d24_method(sign_num: int, seg: int, _pos_in_sign: float, _factor: int, method: int) -> int:
    even_dirn = -1 if method == 2 else 1
    odd_base = 4
    even_base = 4 if method == 3 else 3
    r = (odd_base + seg) % 12
    if sign_num in _EVEN_SIGNS:
        r = (even_base + even_dirn * seg) % 12
    return r


def _chart_d24(core_objects: Mapping[str, Any], method: int, *, mirror_even_sign: bool = False) -> dict[str, object]:
    factor = 24
    if method in {1, 2, 3}:
        def _sign_fn(sign_num: int, seg: int, pos_in_sign: float, _factor: int) -> int:
            _ = pos_in_sign
            return _chart_d24_method(sign_num, seg, pos_in_sign, _factor, method)

        points = _build_points(
            core_objects,
            factor,
            _sign_fn,
            mirror_even_sign=(method == 2 and mirror_even_sign),
        )
    else:
        _LOG.warning("Varga D24 method %s not implemented; falling back to method 1.", method)
        method = 1
        points = _build_points(
            core_objects,
            factor,
            lambda sign_num, seg, pos_in_sign, _factor: _chart_d24_method(
                sign_num, seg, pos_in_sign, _factor, method
            ),
        )
    return {
        "factor": factor,
        "method": method,
        "method_label": _METHOD_LABELS.get("D24", {}).get(method),
        "lagna": points.get("ascendant"),
        "points": points,
    }


def _chart_d27_method1(sign_num: int, seg: int, _pos_in_sign: float, _factor: int) -> int:
    r = seg % 12
    if sign_num in _EARTH_SIGNS:
        return (seg + 3) % 12
    if sign_num in _AIR_SIGNS:
        return (seg + 6) % 12
    if sign_num in _WATER_SIGNS:
        return (seg + 9) % 12
    return r


def _chart_d27(core_objects: Mapping[str, Any], method: int, *, mirror_even_sign: bool = False) -> dict[str, object]:
    factor = 27
    _ = mirror_even_sign
    if method == 1:
        points = _build_points(core_objects, factor, _chart_d27_method1)
    elif method == 2:
        points = _build_points(core_objects, factor, _parivritti_even_reverse_sign)
    elif method == 3:
        points = _build_points(core_objects, factor, _parivritti_alternate_sign)
    elif method == 4:
        points = _build_points(core_objects, factor, _parivritti_cyclic_sign)
    else:
        _LOG.warning("Varga D27 method %s not implemented; falling back to method 1.", method)
        method = 1
        points = _build_points(core_objects, factor, _chart_d27_method1)
    return {
        "factor": factor,
        "method": method,
        "method_label": _METHOD_LABELS.get("D27", {}).get(method),
        "lagna": points.get("ascendant"),
        "points": points,
    }


def _chart_d30_method1(sign_num: int, _seg: int, pos_in_sign: float, _factor: int) -> int:
    odd = [(0, 5, 0), (5, 10, 10), (10, 18, 8), (18, 25, 2), (25, 30, 6)]
    even = [(0, 5, 1), (5, 12, 5), (12, 20, 11), (20, 25, 9), (25, 30, 7)]
    table = odd if sign_num in _ODD_SIGNS else even
    r = table[-1][2]
    for l_min, l_max, rasi in table:
        if pos_in_sign >= l_min and pos_in_sign <= l_max:
            r = rasi
            break
    return r % 12


def _chart_d30_method3(sign_num: int, seg: int, _pos_in_sign: float, _factor: int) -> int:
    return (seg + sign_num) % 12


def _chart_d30(core_objects: Mapping[str, Any], method: int, *, mirror_even_sign: bool = False) -> dict[str, object]:
    factor = 30
    _ = mirror_even_sign
    if method == 1:
        points = _build_points(core_objects, factor, _chart_d30_method1)
    elif method == 2:
        points = _build_points(core_objects, factor, _parivritti_cyclic_sign)
    elif method == 3:
        points = _build_points(core_objects, factor, _chart_d30_method3)
    elif method == 4:
        points = _build_points(core_objects, factor, _parivritti_even_reverse_sign)
    elif method == 5:
        points = _build_points(core_objects, factor, _parivritti_alternate_sign)
    else:
        _LOG.warning("Varga D30 method %s not implemented; falling back to method 1.", method)
        method = 1
        points = _build_points(core_objects, factor, _chart_d30_method1)
    return {
        "factor": factor,
        "method": method,
        "method_label": _METHOD_LABELS.get("D30", {}).get(method),
        "lagna": points.get("ascendant"),
        "points": points,
    }


def _chart_d40_method1(sign_num: int, seg: int, _pos_in_sign: float, _factor: int) -> int:
    r = seg % 12
    if sign_num in _EVEN_SIGNS:
        return (seg + 6) % 12
    return r


def _chart_d40(core_objects: Mapping[str, Any], method: int, *, mirror_even_sign: bool = False) -> dict[str, object]:
    factor = 40
    _ = mirror_even_sign
    if method == 1:
        points = _build_points(core_objects, factor, _chart_d40_method1)
    elif method == 2:
        points = _build_points(core_objects, factor, _parivritti_cyclic_sign)
    elif method == 3:
        points = _build_points(core_objects, factor, _parivritti_even_reverse_sign)
    elif method == 4:
        points = _build_points(core_objects, factor, _parivritti_alternate_sign)
    else:
        _LOG.warning("Varga D40 method %s not implemented; falling back to method 1.", method)
        method = 1
        points = _build_points(core_objects, factor, _chart_d40_method1)
    return {
        "factor": factor,
        "method": method,
        "method_label": _METHOD_LABELS.get("D40", {}).get(method),
        "lagna": points.get("ascendant"),
        "points": points,
    }


def _chart_d45_method1(sign_num: int, seg: int, _pos_in_sign: float, _factor: int) -> int:
    r = seg % 12
    if sign_num in _FIXED_SIGNS:
        return (seg + 4) % 12
    if sign_num in _DUAL_SIGNS:
        return (seg + 8) % 12
    return r


def _chart_d45(core_objects: Mapping[str, Any], method: int, *, mirror_even_sign: bool = False) -> dict[str, object]:
    factor = 45
    _ = mirror_even_sign
    if method == 1:
        points = _build_points(core_objects, factor, _chart_d45_method1)
    elif method == 2:
        points = _build_points(core_objects, factor, _parivritti_cyclic_sign)
    elif method == 3:
        points = _build_points(core_objects, factor, _parivritti_even_reverse_sign)
    elif method == 4:
        points = _build_points(core_objects, factor, _parivritti_alternate_sign)
    else:
        _LOG.warning("Varga D45 method %s not implemented; falling back to method 1.", method)
        method = 1
        points = _build_points(core_objects, factor, _chart_d45_method1)
    return {
        "factor": factor,
        "method": method,
        "method_label": _METHOD_LABELS.get("D45", {}).get(method),
        "lagna": points.get("ascendant"),
        "points": points,
    }


def _chart_d60_method(sign_num: int, seg: int, _pos_in_sign: float, _factor: int, method: int) -> int:
    if method == 2:
        seed = 0
    else:
        seed = sign_num
    dirn = -1 if (sign_num in _EVEN_SIGNS and method == 4) else 1
    return (seed + dirn * seg) % 12


def _chart_d60(core_objects: Mapping[str, Any], method: int, *, mirror_even_sign: bool = False) -> dict[str, object]:
    factor = 60
    if method == 3:
        points = _build_points(
            core_objects,
            factor,
            _parivritti_alternate_sign,
            mirror_even_sign=mirror_even_sign,
        )
    elif method in {1, 2, 4}:
        def _sign_fn(sign_num: int, seg: int, pos_in_sign: float, _factor: int) -> int:
            _ = pos_in_sign
            return _chart_d60_method(sign_num, seg, pos_in_sign, _factor, method)

        points = _build_points(core_objects, factor, _sign_fn)
    else:
        _LOG.warning("Varga D60 method %s not implemented; falling back to method 1.", method)
        method = 1
        points = _build_points(
            core_objects,
            factor,
            lambda sign_num, seg, pos_in_sign, _factor: _chart_d60_method(
                sign_num, seg, pos_in_sign, _factor, method
            ),
        )
    return {
        "factor": factor,
        "method": method,
        "method_label": _METHOD_LABELS.get("D60", {}).get(method),
        "lagna": points.get("ascendant"),
        "points": points,
    }


def _chart_d81(core_objects: Mapping[str, Any], method: int, *, mirror_even_sign: bool = False) -> dict[str, object]:
    factor = 81
    _ = mirror_even_sign
    if method == 1:
        points = _build_points(core_objects, factor, _parivritti_cyclic_sign)
    elif method == 2:
        points = _build_points(core_objects, factor, _parivritti_even_reverse_sign)
    elif method == 3:
        points = _build_points(core_objects, factor, _parivritti_alternate_sign)
    elif method == 4:
        points_stage1 = _build_points(core_objects, 9, _chart_d9_method3)
        core_stage2 = _core_from_points(points_stage1)
        points = _build_points(core_stage2, 9, _chart_d9_method3)
    else:
        _LOG.warning("Varga D81 method %s not implemented; falling back to method 1.", method)
        method = 1
        points = _build_points(core_objects, factor, _parivritti_cyclic_sign)
    return {
        "factor": factor,
        "method": method,
        "method_label": _METHOD_LABELS.get("D81", {}).get(method),
        "lagna": points.get("ascendant"),
        "points": points,
    }


def _chart_d108(core_objects: Mapping[str, Any], method: int, *, mirror_even_sign: bool = False) -> dict[str, object]:
    factor = 108
    _ = mirror_even_sign
    if method == 1:
        chart_stage1 = _chart_d9(core_objects, 1)
        core_stage2 = _core_from_points(chart_stage1["points"])
        chart_stage2 = _chart_d12(core_stage2, 1)
        points = chart_stage2["points"]
    elif method == 2:
        points = _build_points(core_objects, factor, _parivritti_cyclic_sign)
    elif method == 3:
        points = _build_points(core_objects, factor, _parivritti_even_reverse_sign)
    elif method == 4:
        points = _build_points(core_objects, factor, _parivritti_alternate_sign)
    else:
        _LOG.warning("Varga D108 method %s not implemented; falling back to method 1.", method)
        method = 1
        chart_stage1 = _chart_d9(core_objects, 1)
        core_stage2 = _core_from_points(chart_stage1["points"])
        chart_stage2 = _chart_d12(core_stage2, 1)
        points = chart_stage2["points"]
    return {
        "factor": factor,
        "method": method,
        "method_label": _METHOD_LABELS.get("D108", {}).get(method),
        "lagna": points.get("ascendant"),
        "points": points,
    }


def _chart_d144(core_objects: Mapping[str, Any], method: int, *, mirror_even_sign: bool = False) -> dict[str, object]:
    factor = 144
    _ = mirror_even_sign
    if method == 1:
        chart_stage1 = _chart_d12(core_objects, 1)
        core_stage2 = _core_from_points(chart_stage1["points"])
        chart_stage2 = _chart_d12(core_stage2, 1)
        points = chart_stage2["points"]
    elif method == 2:
        points = _build_points(core_objects, factor, _parivritti_cyclic_sign)
    elif method == 3:
        points = _build_points(core_objects, factor, _parivritti_even_reverse_sign)
    elif method == 4:
        points = _build_points(core_objects, factor, _parivritti_alternate_sign)
    else:
        _LOG.warning("Varga D144 method %s not implemented; falling back to method 1.", method)
        method = 1
        chart_stage1 = _chart_d12(core_objects, 1)
        core_stage2 = _core_from_points(chart_stage1["points"])
        chart_stage2 = _chart_d12(core_stage2, 1)
        points = chart_stage2["points"]
    return {
        "factor": factor,
        "method": method,
        "method_label": _METHOD_LABELS.get("D144", {}).get(method),
        "lagna": points.get("ascendant"),
        "points": points,
    }


_REGISTRY: dict[str, Any] = {
    "D1": _chart_d1,
    "D2": _chart_d2,
    "D3": _chart_d3,
    "D4": _chart_d4,
    "D5": _chart_d5,
    "D6": _chart_d6,
    "D7": _chart_d7,
    "D8": _chart_d8,
    "D9": _chart_d9,
    "D10": _chart_d10,
    "D11": _chart_d11,
    "D12": _chart_d12,
    "D16": _chart_d16,
    "D20": _chart_d20,
    "D24": _chart_d24,
    "D27": _chart_d27,
    "D30": _chart_d30,
    "D40": _chart_d40,
    "D45": _chart_d45,
    "D60": _chart_d60,
    "D81": _chart_d81,
    "D108": _chart_d108,
    "D144": _chart_d144,
}


def compute_varga(
    core_objects: Mapping[str, Any],
    chart_id: str,
    method: Optional[int] = None,
    *,
    mirror_even_sign: bool = False,
) -> dict[str, object]:
    cid = normalize_chart_id(chart_id)
    if cid not in _CHART_FACTORS:
        raise ValueError(f"Unsupported varga chart id: {chart_id}")
    requested_method = method if method is not None else _DEFAULT_METHOD_BY_CHART.get(cid, 1)
    supported = _SUPPORTED_METHODS.get(cid, set())
    method_used = requested_method
    if supported and requested_method not in supported:
        _LOG.warning("Varga %s method %s not supported; falling back to default.", cid, requested_method)
        method_used = _DEFAULT_METHOD_BY_CHART.get(cid, 1)
        if supported and method_used not in supported:
            method_used = sorted(supported)[0]
    calc = _REGISTRY.get(cid)
    if calc is None:
        _LOG.warning("Varga chart %s not implemented; returning empty points.", cid)
        return {
            "factor": _CHART_FACTORS[cid],
            "method": method_used,
            "method_label": _METHOD_LABELS.get(cid, {}).get(method_used),
            "lagna": None,
            "points": {},
        }
    return calc(core_objects, method_used, mirror_even_sign=mirror_even_sign)


def compute_vargas(
    core_objects: Mapping[str, Any],
    charts: Iterable[str],
    methods: Optional[Mapping[str, int]] = None,
    *,
    mirror_even_sign: bool = False,
) -> dict[str, dict[str, object]]:
    result: dict[str, dict[str, object]] = {}
    method_map = {normalize_chart_id(k): v for k, v in (methods or {}).items()}
    for chart_id in charts:
        cid = normalize_chart_id(chart_id)
        result[cid] = compute_varga(
            core_objects, cid, method=method_map.get(cid), mirror_even_sign=mirror_even_sign
        )
    return result


def build_vargas_payload(
    core_objects: Mapping[str, Any],
    requested: Optional[Iterable[str]] = None,
    methods: Optional[Mapping[str, int]] = None,
    profile: Optional[str] = None,
    *,
    mirror_even_sign: bool = False,
) -> dict[str, object]:
    charts_list = [normalize_chart_id(cid) for cid in (requested or [])]
    provided_methods: dict[str, int] = {}
    if methods:
        for cid, method in methods.items():
            provided_methods[normalize_chart_id(cid)] = int(method)
    if profile:
        profile_key = profile.strip().upper()
        profile_methods = _PROFILE_METHODS.get(profile_key, {})
        if not profile_methods:
            _LOG.warning("Unknown varga profile %s; ignoring.", profile)
        else:
            for cid, method in profile_methods.items():
                normalized = normalize_chart_id(cid)
                if normalized not in provided_methods:
                    provided_methods[normalized] = int(method)
    charts = (
        compute_vargas(core_objects, charts_list, provided_methods, mirror_even_sign=mirror_even_sign)
        if charts_list
        else {}
    )
    resolved_methods = {cid: int(data.get("method", 1)) for cid, data in charts.items()}
    return {
        "settings": {
            "requested": charts_list,
            "default_method_by_chart": dict(_DEFAULT_METHOD_BY_CHART),
            "methods": resolved_methods,
            "profile": profile,
        },
        "charts": charts,
    }
