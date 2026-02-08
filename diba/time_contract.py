"""
Time contract adapter utilities for Julian Day handling.

- SwissEph calls must use UTC-based Julian Day (JD_UTC).
- Panchanga-style/local functions may accept local JD but must convert using tz_offset_hours/24.
"""

from datetime import datetime
from typing import Optional

from diba.utilities import datetime_to_julian


def jd_utc_from_local(jd_local: float, tz_offset_hours: float) -> float:
    """Convert local JD to UTC JD: JD_UTC = JD_local - tz_offset_hours/24."""
    return jd_local - tz_offset_hours / 24.0


def jd_local_from_utc(jd_utc: float, tz_offset_hours: float) -> float:
    """Convert UTC JD to local JD: JD_local = JD_UTC + tz_offset_hours/24."""
    return jd_utc + tz_offset_hours / 24.0


def get_subject_jd_utc(subject) -> float:
    """
    Return the canonical UTC JD from a subject.

    SwissEph calls must consume this UTC-based value.
    """
    return float(subject.julian_day)


def _local_dt_from_subject(subject) -> Optional[datetime]:
    iso_local = getattr(subject, "iso_formatted_local_datetime", None)
    if not iso_local:
        return None
    try:
        return datetime.fromisoformat(iso_local)
    except ValueError:
        return None


def get_subject_jd_local(subject) -> float:
    """
    Return local JD for a subject.

    Prefer subject.julian_day_local; otherwise derive from iso_formatted_local_datetime.
    Panchanga-style functions may accept this local JD but must internally convert with tz_offset_hours/24.
    """
    if getattr(subject, "julian_day_local", None) is not None:
        return float(subject.julian_day_local)
    local_dt = _local_dt_from_subject(subject)
    if local_dt is None:
        raise ValueError("Cannot derive local JD: missing julian_day_local and iso_formatted_local_datetime.")
    return datetime_to_julian(local_dt)
