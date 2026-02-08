"""
Vedic subject factory for canonical runtime construction.

Creates VedicModel objects from localized birth data using the canonical
SwissEph-backed context and registry-resolved policies. This is the public
entrypoint for building a fully validated subject model.

Public API:
- VedicFactoryError
- validate_runtime_policy_input
- VedicSubjectFactory

Notes:
- Thread-safety: SwissEph calls occur inside VedicCalculationContext under a global lock.
- Determinism: Deterministic for identical inputs and ephemeris version.
- Contract: Output model structure follows schemas; changes require version bumps.
"""

from __future__ import annotations

from datetime import datetime
from typing import Mapping, Optional

import pytz
from pytz.exceptions import AmbiguousTimeError, NonExistentTimeError, UnknownTimeZoneError

from diba.schemas.kr_models import VedicModel, VedicSettingsModel
from diba.time_contract import datetime_to_julian
from diba.vedic.builder import build_vedic_model
from diba.vedic.context import VedicCalculationContext
from diba.vedic.registry import (
    VedicRegistryError,
    resolve_ayanamsa,
    resolve_house_system,
    resolve_node_mode,
)


class VedicFactoryError(ValueError):
    """Factory or input validation error.

    Args:
        *args: Error message details.

    Returns:
        None.

    Raises:
        None.

    Notes:
        - Thread-safety: Pure error type; no shared state.
        - Determinism: Deterministic for identical inputs.
        - Contract: Raised for invalid inputs or time localization failures.

    Examples:
        >>> raise VedicFactoryError("Invalid timezone")
        Traceback (most recent call last):
        ...
        diba.vedic.factory.VedicFactoryError: Invalid timezone
    """


RUNTIME_POLICY_KEYS = frozenset({"ayanamsa_id", "house_system_id", "node_mode"})


def validate_runtime_policy_input(policy: Mapping[str, object]) -> dict[str, str]:
    """Validate and normalize runtime policy input.

    Args:
        policy: Mapping with exactly the required policy keys.

    Returns:
        Normalized policy mapping with string values.

    Raises:
        VedicFactoryError: If required keys are missing or extra keys are present.

    Notes:
        - Thread-safety: Pure validation; no shared state.
        - Determinism: Deterministic for identical inputs.
        - Contract: Policy keys are fixed and versioned in the registry.

    Examples:
        >>> validate_runtime_policy_input({\"ayanamsa_id\": \"lahiri\", \"house_system_id\": \"whole_sign\", \"node_mode\": \"mean\"})
        {'ayanamsa_id': 'lahiri', 'house_system_id': 'whole_sign', 'node_mode': 'mean'}
    """
    keys = set(policy.keys())
    if keys != RUNTIME_POLICY_KEYS:
        raise VedicFactoryError(
            "Runtime policy keys must be exactly: ayanamsa_id, house_system_id, node_mode."
        )
    return {
        "ayanamsa_id": str(policy["ayanamsa_id"]),
        "house_system_id": str(policy["house_system_id"]),
        "node_mode": str(policy["node_mode"]),
    }


def _validate_lat_lon(lat: float, lon: float) -> tuple[float, float]:
    lat_f = float(lat)
    lon_f = float(lon)
    if not (-90.0 <= lat_f <= 90.0):
        raise VedicFactoryError("Latitude must be in [-90, 90].")
    if not (-180.0 <= lon_f <= 180.0):
        raise VedicFactoryError("Longitude must be in [-180, 180].")
    return lat_f, lon_f


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


def _jd_utc_from_birth_data(
    year: int,
    month: int,
    day: int,
    hour: int,
    minute: int,
    seconds: float,
    tz_str: str,
) -> float:
    try:
        sec, micros = _split_seconds(seconds)
        local_tz = pytz.timezone(tz_str)
        naive_dt = datetime(year, month, day, hour, minute, sec, micros)
        local_dt = local_tz.localize(naive_dt, is_dst=None)
    except UnknownTimeZoneError as exc:
        raise VedicFactoryError(f"Invalid timezone: {tz_str}") from exc
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


class VedicSubjectFactory:
    """Factory for building canonical Vedic subject models.

    Args:
        None.

    Returns:
        None.

    Raises:
        None.

    Notes:
        - Thread-safety: SwissEph calls occur inside VedicCalculationContext under a global lock.
        - Determinism: Deterministic for identical inputs and ephemeris version.
        - Contract: Use from_birth_data as the stable public entrypoint.

    Examples:
        >>> isinstance(VedicSubjectFactory, type)
        True
    """

    @classmethod
    def from_birth_data(
        cls,
        *,
        year: int,
        month: int,
        day: int,
        hour: int,
        minute: int,
        seconds: float = 0.0,
        tz_str: str,
        lat: float,
        lon: float,
        altitude: float = 0.0,
        ayanamsa_id: str = "lahiri",
        node_mode: str = "mean",
        house_system_id: str = "whole_sign",
        varga_charts: Optional[list[str]] = None,
        varga_methods: Optional[Mapping[str, int]] = None,
        varga_profile: Optional[str] = None,
        ephe_path: Optional[str] = None,
    ) -> VedicModel:
        """Build a VedicModel from localized birth data.

        Args:
            year: Birth year (local time).
            month: Birth month (local time).
            day: Birth day (local time).
            hour: Birth hour (local time).
            minute: Birth minute (local time).
            seconds: Birth seconds (local time, fractional allowed).
            tz_str: IANA timezone name for local time.
            lat: Latitude in degrees.
            lon: Longitude in degrees.
            altitude: Altitude in meters (must be 0.0 for canonical mode).
            ayanamsa_id: Ayanamsa policy ID.
            node_mode: Node policy ID.
            house_system_id: House system policy ID.
            varga_charts: Optional list of varga chart IDs to compute.
            varga_methods: Optional per-varga method overrides.
            varga_profile: Optional varga profile ID.
            ephe_path: Optional path to SwissEph data files.

        Returns:
            Fully assembled VedicModel.

        Raises:
            VedicFactoryError: If inputs are invalid or time localization fails.

        Notes:
            - Thread-safety: SwissEph calls are serialized under a global lock.
            - Determinism: Deterministic for identical inputs and ephemeris version.
            - Contract: Output model fields follow schema versions.

        Examples:
            >>> model = VedicSubjectFactory.from_birth_data(
            ...     year=1990,
            ...     month=1,
            ...     day=1,
            ...     hour=12,
            ...     minute=0,
            ...     seconds=0.0,
            ...     tz_str="UTC",
            ...     lat=0.0,
            ...     lon=0.0,
            ... )
            >>> model.settings.ayanamsa_id
            'lahiri'
        """
        jd_utc = _jd_utc_from_birth_data(year, month, day, hour, minute, seconds, tz_str)
        try:
            ayanamsa_spec = resolve_ayanamsa(ayanamsa_id)
            house_spec = resolve_house_system(house_system_id)
            node_spec = resolve_node_mode(node_mode)
        except VedicRegistryError as exc:
            raise VedicFactoryError(str(exc)) from exc
        lat_f, lon_f = _validate_lat_lon(lat, lon)
        altitude_f = float(altitude)
        if altitude_f != 0.0:
            raise VedicFactoryError(
                "Altitude is currently unsupported in canonical Vedic mode; use altitude=0.0."
            )

        context = VedicCalculationContext(
            jd_utc=jd_utc,
            lat=lat_f,
            lon=lon_f,
            altitude=altitude_f,
            ephe_path=ephe_path,
            ayanamsa=ayanamsa_spec,
            house_system=house_spec,
            node_mode=node_spec.id,
        )
        core = context.compute_core()

        settings = VedicSettingsModel(
            ayanamsa_id=ayanamsa_spec.id,
            node_mode=node_spec.id,
            house_system_id=house_spec.id,
        )
        return build_vedic_model(
            core=core,
            settings=settings,
            varga_charts=varga_charts,
            varga_methods=varga_methods,
            varga_profile=varga_profile,
        )
