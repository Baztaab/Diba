"""
Static chart serializer for legacy v0.1 payloads.

Provides a JSON-friendly, human-readable static chart output that mirrors the
legacy `static_chart.v0.1` contract. This module is a serializer layer and uses
the canonical factory/context for all SwissEph calls.

Public API:
- format_dms
- build_static_chart_v0_1

Notes:
- Thread-safety: SwissEph calls occur inside VedicCalculationContext under a global lock.
- Determinism: Deterministic for identical inputs and ephemeris version.
- Contract: Output schema version is `static_chart.v0.1` and keys are stable.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Mapping, Optional

from diba.schemas.kr_models import VedicSettingsModel
from diba.vedic.context import VedicCalculationContext
from diba.vedic.factory import VedicSubjectFactory
from diba.vedic.registry import (
    AyanamsaSpec,
    HouseSystemSpec,
    resolve_ayanamsa,
    resolve_house_system,
    resolve_node_mode,
)

_SIGN_SHORT = ["Ar", "Ta", "Ge", "Cn", "Le", "Vi", "Li", "Sc", "Sg", "Cp", "Aq", "Pi"]
_SIGN_LONG = [
    "Aries",
    "Taurus",
    "Gemini",
    "Cancer",
    "Leo",
    "Virgo",
    "Libra",
    "Scorpio",
    "Sagittarius",
    "Capricorn",
    "Aquarius",
    "Pisces",
]

_POINT_ORDER = [
    ("asc", "ascendant"),
    ("sun", "sun"),
    ("moon", "moon"),
    ("mars", "mars"),
    ("mercury", "mercury"),
    ("jupiter", "jupiter"),
    ("venus", "venus"),
    ("saturn", "saturn"),
    ("rahu", "rahu"),
    ("ketu", "ketu"),
]


def _normalize_settings(settings: VedicSettingsModel | Mapping[str, Any]) -> VedicSettingsModel:
    if isinstance(settings, VedicSettingsModel):
        return settings
    if not isinstance(settings, Mapping):
        raise ValueError("settings must be VedicSettingsModel or mapping.")
    return VedicSettingsModel.model_validate(settings)


def _normalize_birth_data(birth_data: Mapping[str, Any]) -> tuple[int, int, int, int, int, float, str]:
    if "datetime_local" not in birth_data:
        raise ValueError("birth_data.datetime_local is required.")
    if "timezone" not in birth_data:
        raise ValueError("birth_data.timezone is required.")
    local_dt = datetime.fromisoformat(str(birth_data["datetime_local"]))
    tz_iana = str(birth_data["timezone"])
    seconds = float(local_dt.second + (local_dt.microsecond / 1_000_000.0))
    return local_dt.year, local_dt.month, local_dt.day, local_dt.hour, local_dt.minute, seconds, tz_iana


def _norm360(value: float) -> float:
    return float(value) % 360.0


def _dms_parts(deg: float) -> tuple[int, int, float]:
    total = _norm360(deg)
    d = int(total)
    rem = (total - d) * 60.0
    m = int(rem)
    s = round((rem - m) * 60.0, 2)
    if s >= 60.0:
        s = 0.0
        m += 1
    if m >= 60:
        m = 0
        d += 1
    return d, m, s


def format_dms(deg: float, *, with_sign: bool) -> str:
    """Format a degree value as a DMS string.

    Args:
        deg: Absolute longitude in degrees.
        with_sign: If True, include zodiac sign abbreviation.

    Returns:
        DMS string such as ``13°Ar05'12.34"``.

    Raises:
        None.

    Notes:
        - Thread-safety: Pure formatting; no shared state.
        - Determinism: Deterministic for identical inputs.
        - Contract: Output format is stable for `static_chart.v0.1`.

    Examples:
        >>> print(format_dms(13.0879, with_sign=True))
        13°Ar05'16.44"
    """
    d, m, s = _dms_parts(deg)
    if with_sign:
        sign_idx = int(_norm360(deg) // 30)
        sign_deg = d % 30
        return f"{sign_deg:02d}°{_SIGN_SHORT[sign_idx]}{m:02d}'{s:05.2f}\""
    return f"{d}°{m:02d}'{s:05.2f}\""


def _rasi_name(abs_pos: float) -> str:
    return _SIGN_LONG[int(_norm360(abs_pos) // 30)]


def _build_houses_whole_sign(asc_abs_pos: float) -> dict[str, dict[str, str]]:
    asc_sign = int(_norm360(asc_abs_pos) // 30)
    d, m, s = _dms_parts(asc_abs_pos)
    deg_in_sign = d % 30
    houses: dict[str, dict[str, str]] = {}
    for offset in range(12):
        sign_idx = (asc_sign + offset) % 12
        cusp = f"{deg_in_sign:02d}°{_SIGN_SHORT[sign_idx]}{m:02d}'{s:05.2f}\""
        houses[str(offset + 1)] = {"rasi": _SIGN_LONG[sign_idx], "cusp": cusp}
    return houses


def build_static_chart_v0_1(
    settings: VedicSettingsModel | Mapping[str, Any],
    birth_data: Mapping[str, Any],
    place: Mapping[str, Any],
    ephe_path: Optional[str] = None,
) -> dict[str, Any]:
    """Build the legacy `static_chart.v0.1` payload.

    Uses the canonical factory/context to compute sidereal positions and returns
    a JSON-serializable dict shaped for the v0.1 contract.

    Args:
        settings: Vedic settings model or compatible mapping.
        birth_data: Birth metadata including local datetime and timezone.
        place: Location metadata with lat/lon and optional altitude.
        ephe_path: Optional path to SwissEph data files.

    Returns:
        JSON-serializable static chart payload.

    Raises:
        ValueError: If inputs are malformed or unsupported for v0.1.

    Notes:
        - Thread-safety: SwissEph calls are serialized under a global lock.
        - Determinism: Deterministic for identical inputs and ephemeris version.
        - Contract: Output schema version is `static_chart.v0.1` and keys are stable.

    Examples:
        >>> payload = build_static_chart_v0_1(settings, birth_data, place)
        >>> payload[\"schema_version\"]
        'static_chart.v0.1'
    """
    normalized = _normalize_settings(settings)
    ayanamsa_spec: AyanamsaSpec = resolve_ayanamsa(normalized.ayanamsa_id)
    house_spec: HouseSystemSpec = resolve_house_system(normalized.house_system_id)
    node_spec = resolve_node_mode(normalized.node_mode)

    year, month, day, hour, minute, seconds, tz_iana = _normalize_birth_data(birth_data)
    lat = float(place["lat"])
    lon = float(place["lon"])
    alt_m = float(place.get("alt_m", 0.0))
    if alt_m != 0.0:
        raise ValueError("static_chart.v0.1 generator only supports alt_m=0.0.")

    # Canonical factory path for model assembly and settings validation.
    model = VedicSubjectFactory.from_birth_data(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        seconds=seconds,
        tz_str=tz_iana,
        lat=lat,
        lon=lon,
        altitude=alt_m,
        ayanamsa_id=ayanamsa_spec.id,
        node_mode=node_spec.id,
        house_system_id=house_spec.id,
        ephe_path=ephe_path,
    )

    # Raw core keeps retrograde flags used by static_chart.v0.1 payload.
    core = VedicCalculationContext(
        jd_utc=float(model.core.jd_utc),
        lat=lat,
        lon=lon,
        altitude=alt_m,
        ephe_path=ephe_path,
        ayanamsa=ayanamsa_spec,
        house_system=house_spec,
        node_mode=node_spec.id,
    ).compute_core()

    points: dict[str, dict[str, Any]] = {}
    for out_key, core_key in _POINT_ORDER:
        if core_key == "ascendant":
            abs_pos = float(model.core.objects["ascendant"].abs_pos_sidereal)
            payload: dict[str, Any] = {
                "dms": format_dms(abs_pos, with_sign=True),
                "rasi": _rasi_name(abs_pos),
            }
        elif core_key in {"rahu", "ketu"}:
            data = core["nodes"][core_key]
            abs_pos = float(data["longitude"])
            payload = {
                "dms": format_dms(abs_pos, with_sign=True),
                "rasi": _rasi_name(abs_pos),
            }
            if bool(data.get("is_retrograde")):
                payload["retrograde"] = True
        else:
            data = core["planets"][core_key]
            abs_pos = float(data["longitude"])
            payload = {
                "dms": format_dms(abs_pos, with_sign=True),
                "rasi": _rasi_name(abs_pos),
            }
            if bool(data.get("is_retrograde")):
                payload["retrograde"] = True
        points[out_key] = payload

    asc_abs = float(model.core.objects["ascendant"].abs_pos_sidereal)
    chart = {
        "schema_version": "static_chart.v0.1",
        "meta": {
            "id": str(birth_data["id"]),
            "datetime_local": str(birth_data["datetime_local"]),
            "datetime_utc": str(birth_data["datetime_utc"]),
            "timezone": tz_iana,
            "utc_offset": str(birth_data["utc_offset"]),
            "dst": bool(birth_data["dst"]),
            "zodiac": "sidereal",
            "ayanamsa_id": ayanamsa_spec.id,
            "ayanamsa_dms": format_dms(float(model.ayanamsa_deg), with_sign=False),
            "house_system_id": house_spec.id,
        },
        "location": {
            "name": str(place["name"]),
            "lat": lat,
            "lon": lon,
            "alt_m": alt_m,
        },
        "points": points,
        "houses_whole_sign": _build_houses_whole_sign(asc_abs),
    }
    return chart
