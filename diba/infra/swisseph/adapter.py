"""Session-aware SwissEph wrappers."""

from __future__ import annotations

from typing import Any, Tuple

from .session import ensure_session_active, swe


def get_ayanamsa_ut(jd_utc: float) -> float:
    ensure_session_active()
    if hasattr(swe, "get_ayanamsa_ut"):
        return float(swe.get_ayanamsa_ut(jd_utc))
    return float(swe.get_ayanamsa(jd_utc + swe.deltat(jd_utc)))


def calc_ut(jd_utc: float, planet_id: int, flags: int) -> Tuple[Any, int]:
    ensure_session_active()
    return swe.calc_ut(jd_utc, planet_id, flags=flags)


def houses_ex(jd_utc: float, lat: float, lon: float, hsys: bytes, flags: int):
    ensure_session_active()
    return swe.houses_ex(jd_utc, lat, lon, hsys, flags=flags)
