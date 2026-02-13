"""Shared base state models for engine-driven computation."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Optional

import pytz
from pytz.exceptions import AmbiguousTimeError, NonExistentTimeError, UnknownTimeZoneError

from diba.domain.models.common import BirthData
from diba.infra.io.ephemeris import resolve_ephemeris_path
from diba.time_contract import datetime_to_julian
from diba.vedic.context import VedicCalculationContext
from diba.vedic.factory import VedicFactoryError
from diba.vedic.registry import resolve_ayanamsa, resolve_house_system, resolve_node_mode


@dataclass(frozen=True)
class AstronomyContext:
    ephe_path: Optional[str] = None
    include_outer: bool = False


@dataclass(frozen=True)
class AstrologySettings:
    ayanamsa_id: str = "lahiri"
    house_system_id: str = "whole_sign"
    node_mode: str = "mean"


@dataclass(frozen=True)
class VedicState:
    birth_data: BirthData
    astronomy_context: AstronomyContext
    astrology_settings: AstrologySettings
    jd_ut: float
    time_model: Dict[str, Any]
    location: Dict[str, float]
    planets: Dict[str, Dict[str, Any]]
    houses: Dict[str, Any]
    flags: Dict[str, Any]
    core_objects: Dict[str, Any]


def _split_seconds(seconds: float) -> tuple[int, int]:
    if seconds < 0:
        raise VedicFactoryError("seconds must be >= 0")
    sec_int = int(seconds)
    frac = float(seconds) - float(sec_int)
    micros = int(round(frac * 1_000_000))
    if micros >= 1_000_000:
        sec_int += 1
        micros -= 1_000_000
    if sec_int >= 60:
        raise VedicFactoryError("seconds must be < 60")
    return sec_int, micros


def _to_jd_ut(birth: BirthData) -> float:
    try:
        sec, micros = _split_seconds(float(birth.seconds))
        local_tz = pytz.timezone(birth.tz_str)
        naive_dt = datetime(
            int(birth.year),
            int(birth.month),
            int(birth.day),
            int(birth.hour),
            int(birth.minute),
            sec,
            micros,
        )
        local_dt = local_tz.localize(naive_dt, is_dst=None)
    except UnknownTimeZoneError as exc:
        raise VedicFactoryError(f"Invalid timezone: {birth.tz_str}") from exc
    except AmbiguousTimeError as exc:
        raise VedicFactoryError(
            "Ambiguous local datetime due to DST transition; pass an unambiguous time."
        ) from exc
    except NonExistentTimeError as exc:
        raise VedicFactoryError(
            "Non-existent local datetime due to DST transition; pass a valid local time."
        ) from exc
    except ValueError as exc:
        raise VedicFactoryError(str(exc)) from exc

    utc_dt = local_dt.astimezone(pytz.utc)
    return float(datetime_to_julian(utc_dt))


def build_vedic_state(
    birth_data: BirthData,
    astronomy_context: AstronomyContext,
    astrology_settings: AstrologySettings,
    *,
    require_active_session: bool,
) -> VedicState:
    jd_ut = _to_jd_ut(birth_data)

    ayanamsa = resolve_ayanamsa(astrology_settings.ayanamsa_id)
    house_system = resolve_house_system(astrology_settings.house_system_id)
    node_mode = resolve_node_mode(astrology_settings.node_mode)

    effective_ephe_path = resolve_ephemeris_path(
        cli_arg=astronomy_context.ephe_path,
        dev_mode=True,
    )

    context = VedicCalculationContext(
        jd_utc=jd_ut,
        lat=float(birth_data.place.lat),
        lon=float(birth_data.place.lon),
        altitude=float(birth_data.place.altitude),
        ephe_path=effective_ephe_path,
        ayanamsa=ayanamsa,
        house_system=house_system,
        node_mode=node_mode.id,
        include_outer=bool(astronomy_context.include_outer),
    )

    core = context.compute_core(manage_session=not require_active_session)

    return VedicState(
        birth_data=birth_data,
        astronomy_context=astronomy_context,
        astrology_settings=astrology_settings,
        jd_ut=jd_ut,
        time_model={
            "calendar": [birth_data.year, birth_data.month, birth_data.day],
            "clock": [birth_data.hour, birth_data.minute, birth_data.seconds],
            "tz": birth_data.tz_str,
            "jd_ut": jd_ut,
        },
        location={
            "lat": float(birth_data.place.lat),
            "lon": float(birth_data.place.lon),
            "altitude": float(birth_data.place.altitude),
        },
        planets=dict(core.get("planets", {})),
        houses=dict(core.get("houses", {})),
        flags=dict(core.get("flags", {})),
        core_objects=core,
    )
