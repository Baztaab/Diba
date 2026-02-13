"""Facade for panchanga capability (phase-2 state-wired baseline)."""

from __future__ import annotations

from diba.domain.models.common import BirthData, Meta, RuntimePolicy
from diba.domain.models.panchanga import PanchangaResult
from diba.engine import AstrologySettings, AstronomyContext, DibaEngine, VedicState


def _meta() -> Meta:
    return Meta(
        engine_version="diba-core-v5",
        swisseph_version="unknown",
        config_digest="pending",
        ephe_expectations="de405/sepl_18",
        timezone_policy="UTC",
    )


def _state_from_input(birth: BirthData, policy: RuntimePolicy) -> VedicState:
    engine = DibaEngine(
        session_ctx=AstronomyContext(),
        astro_settings=AstrologySettings(
            ayanamsa_id=policy.ayanamsa_id,
            house_system_id=policy.house_system_id,
            node_mode=policy.node_mode,
        ),
    )
    return engine.state(birth)


def compute(
    birth: BirthData,
    policy: RuntimePolicy,
    *,
    state: VedicState | None = None,
) -> PanchangaResult:
    base_state = state or _state_from_input(birth, policy)
    payload = {
        "implemented": False,
        "message": "Panchanga detailed calculators are scheduled in capability phase.",
        "base_state": {
            "jd_ut": base_state.jd_ut,
            "location": base_state.location,
        },
    }
    return PanchangaResult(status="planned", payload=payload, meta=_meta())
