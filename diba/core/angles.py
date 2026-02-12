"""Angle helpers with canonical zero-based sign contracts."""

from __future__ import annotations


def normalize360(value: float) -> float:
    """Normalize angle into [0, 360)."""
    normalized = float(value) % 360.0
    if normalized == 360.0:
        return 0.0
    if normalized < 0.0:
        return normalized + 360.0
    return normalized


def split_rasi(longitude_abs: float) -> tuple[int, float]:
    """Split absolute longitude to (rasi_index0, degree_in_sign)."""
    longitude = normalize360(longitude_abs)
    rasi_index = int(longitude // 30.0)
    degree_in_sign = longitude - (rasi_index * 30.0)

    # Float guard at the boundary.
    if degree_in_sign >= 30.0:
        degree_in_sign = 0.0
        rasi_index = (rasi_index + 1) % 12
    if degree_in_sign < 0.0:
        degree_in_sign += 30.0
        rasi_index = (rasi_index - 1) % 12
    return rasi_index, degree_in_sign

