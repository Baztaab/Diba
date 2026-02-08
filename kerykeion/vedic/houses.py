# -*- coding: utf-8 -*-
"""
Vedic house helpers (whole-sign).

Port reference:
    PyJHora - docs/jhora/horoscope/chart/charts.py (rasi chart uses whole-sign logic)
"""

from typing import List, Dict


_SIGNS = ["Ari", "Tau", "Gem", "Can", "Leo", "Vir", "Lib", "Sco", "Sag", "Cap", "Aqu", "Pis"]


def whole_sign_houses(asc_abs_pos_sidereal: float) -> List[Dict[str, object]]:
    """
    Build whole-sign houses from a sidereal Ascendant longitude.

    Returns a list of 12 entries, where index 0 is House 1.
    """
    asc_sign_num = int(float(asc_abs_pos_sidereal) // 30) % 12
    houses: List[Dict[str, object]] = []
    for i in range(12):
        sign_num = (asc_sign_num + i) % 12
        houses.append(
            {
                "house_number": i + 1,
                "sign": _SIGNS[sign_num],
                "sign_num": sign_num,
            }
        )
    return houses
