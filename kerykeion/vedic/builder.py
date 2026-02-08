"""
Vedic model assembly helpers.

This module is intentionally pure assembly:
- no SwissEph calls
- no Western wiring
"""

from __future__ import annotations

from typing import Any, Mapping, Optional
import os
import warnings

from kerykeion.schemas.kr_models import (
    VedicCoreModel,
    VedicCorePointModel,
    VedicModel,
    VedicRasiD1Model,
    VedicRasiHousesModel,
    VedicSettingsModel,
)
from kerykeion.vedic.houses import whole_sign_houses
from kerykeion.vedic.rasi_d1 import build_rasi_d1_points
from kerykeion.vedic.vargas import build_vargas_payload


def _extract_core_abs(core: Mapping[str, Any]) -> dict[str, float]:
    planets = core.get("planets") or {}
    nodes = core.get("nodes") or {}
    ascendant = core.get("ascendant") or {}

    result: dict[str, float] = {}
    for name, payload in planets.items():
        result[str(name)] = float(payload["longitude"])
    for name, payload in nodes.items():
        result[str(name)] = float(payload["longitude"])
    result["ascendant"] = float(ascendant["longitude"])
    return result


def build_vedic_model(
    core: Mapping[str, Any],
    settings: VedicSettingsModel,
    *,
    varga_charts: Optional[list[str]] = None,
    varga_methods: Optional[Mapping[str, int]] = None,
    varga_profile: Optional[str] = None,
) -> VedicModel:
    core_abs = _extract_core_abs(core)
    core_model = VedicCoreModel(
        jd_utc=float(core["jd_utc"]),
        objects={name: VedicCorePointModel(abs_pos_sidereal=deg) for name, deg in core_abs.items()},
    )

    rasi_points = build_rasi_d1_points(core_abs)
    asc_abs = core_abs["ascendant"]
    rasi_houses = VedicRasiHousesModel(model="whole_sign", houses=whole_sign_houses(asc_abs))
    rasi_d1 = VedicRasiD1Model(points=rasi_points, houses=rasi_houses)

    vargas = None
    if varga_charts:
        vargas = build_vargas_payload(
            core_model.objects,
            requested=varga_charts,
            methods=varga_methods,
            profile=varga_profile,
        )

    return VedicModel(
        settings=settings,
        ayanamsa_deg=float(core["ayanamsa_deg"]),
        core=core_model,
        rasi_d1=rasi_d1,
        vargas=vargas,
    )


def build_vedic_payload(*_args: Any, **_kwargs: Any) -> None:
    """
    Retired legacy API: build_vedic_payload.

    This must never be used in runtime. It remains only to fail fast and guide
    callers toward VedicSubjectFactory/build_vedic_model.
    """
    warnings.warn(
        "build_vedic_payload is retired; use VedicSubjectFactory/build_vedic_model instead.",
        DeprecationWarning,
        stacklevel=2,
    )
    if os.getenv("BAZTAB_STRICT") == "1" or os.getenv("PYTEST_CURRENT_TEST"):
        raise RuntimeError(
            "build_vedic_payload is retired; use VedicSubjectFactory/build_vedic_model instead."
        )
    raise RuntimeError(
        "build_vedic_payload is retired; use VedicSubjectFactory/build_vedic_model instead."
    )
