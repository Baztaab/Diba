"""Time conversion helpers."""

from __future__ import annotations

from datetime import datetime

from diba.time_contract import datetime_to_julian


def datetime_utc_to_jd(value: datetime) -> float:
    """Convert UTC datetime to Julian day number."""
    return float(datetime_to_julian(value))
