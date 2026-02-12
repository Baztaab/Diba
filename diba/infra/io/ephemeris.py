"""Ephemeris expectations checks."""

from __future__ import annotations

from pathlib import Path


def validate_ephemeris_path(path: str) -> None:
    p = Path(path)
    if not p.exists() or not p.is_dir():
        raise ValueError(f"Invalid ephemeris path: {path}")

