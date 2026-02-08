# -*- coding: utf-8 -*-
"""
Vedic Rasi (D1) helpers.

Port reference:
    PyJHora - docs/jhora/horoscope/chart/charts.py (rasi_chart)
"""

from typing import Dict

from kerykeion.schemas.kr_models import VedicRasiPointModel


_SIGNS = ["Ari", "Tau", "Gem", "Can", "Leo", "Vir", "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis"]


def _sign_info(abs_pos: float) -> tuple[str, int, float]:
    sign_num = int(float(abs_pos) // 30) % 12
    sign = _SIGNS[sign_num]
    position = float(abs_pos) % 30.0
    return sign, sign_num, position


def build_rasi_d1_points(abs_positions: Dict[str, float]) -> Dict[str, VedicRasiPointModel]:
    """
    Build minimal D1 point entries from sidereal absolute positions.

    Keys should align with core object keys (e.g., sun, moon, ascendant).
    """
    points: Dict[str, VedicRasiPointModel] = {}
    for name, abs_pos in abs_positions.items():
        sign, sign_num, position = _sign_info(abs_pos)
        points[name] = VedicRasiPointModel(
            name=name,
            sign=sign,
            sign_num=sign_num,
            position=position,
            abs_pos=float(abs_pos),
        )
    return points
