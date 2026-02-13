"""Facade for chart capability."""

from __future__ import annotations

from diba.domain.models.chart import ChartResult, VargaResult
from diba.domain.models.common import BirthData, Meta, PlaceInput, RuntimePolicy
from diba.engine import AstrologySettings, AstronomyContext, DibaEngine, VedicState
from diba.vedic.vargas import compute_varga as _compute_varga


def _meta() -> Meta:
    return Meta(
        engine_version="diba-core-v5",
        swisseph_version="unknown",
        config_digest="pending",
        ephe_expectations="de405/sepl_18",
        timezone_policy="UTC",
    )


def _state_from_kwargs(kwargs: dict) -> VedicState:
    birth = BirthData(
        year=int(kwargs["year"]),
        month=int(kwargs["month"]),
        day=int(kwargs["day"]),
        hour=int(kwargs["hour"]),
        minute=int(kwargs["minute"]),
        seconds=float(kwargs.get("seconds", 0.0)),
        tz_str=str(kwargs["tz_str"]),
        place=PlaceInput(
            lat=float(kwargs["lat"]),
            lon=float(kwargs["lon"]),
            altitude=float(kwargs.get("altitude", 0.0)),
        ),
    )
    policy = RuntimePolicy(
        ayanamsa_id=str(kwargs.get("ayanamsa_id", "lahiri")),
        house_system_id=str(kwargs.get("house_system_id", "whole_sign")),
        node_mode=str(kwargs.get("node_mode", "mean")),
    )
    engine = DibaEngine(
        session_ctx=AstronomyContext(ephe_path=kwargs.get("ephe_path")),
        astro_settings=AstrologySettings(
            ayanamsa_id=policy.ayanamsa_id,
            house_system_id=policy.house_system_id,
            node_mode=policy.node_mode,
        ),
    )
    return engine.state(birth)


def compute_d1(*, state: VedicState | None = None, **kwargs) -> ChartResult:
    base_state = state or _state_from_kwargs(kwargs)
    payload = {
        "jd_ut": base_state.jd_ut,
        "location": base_state.location,
        "planets": base_state.planets,
        "houses": base_state.houses,
        "flags": base_state.flags,
    }
    return ChartResult(chart_id="D1", payload=payload, meta=_meta())


def compute_varga(
    core_objects: dict | None = None,
    chart_id: str = "D9",
    method: int | None = None,
    *,
    state: VedicState | None = None,
) -> VargaResult:
    core = core_objects if core_objects is not None else (state.core_objects if state is not None else None)
    if core is None:
        raise ValueError("compute_varga requires either core_objects or state.")

    result = _compute_varga(core, chart_id, method=method)
    return VargaResult(
        chart_id=chart_id,
        method=int(result.get("method", method or 1)),
        payload=result,
        meta=_meta(),
    )
