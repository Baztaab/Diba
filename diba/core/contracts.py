"""Determinism and tolerance contracts."""

from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ToleranceProfile:
    angle_deg: float
    time_seconds: int


def tolerance_profile(name: str | None = None) -> ToleranceProfile:
    profile = (name or os.getenv("DIBA_TOL_PROFILE", "ci")).strip().lower()
    if profile == "golden":
        return ToleranceProfile(angle_deg=1e-5, time_seconds=30)
    return ToleranceProfile(angle_deg=1e-2, time_seconds=60)

