"""Facade for transit capability (phase-2 state-wired baseline)."""

from __future__ import annotations

from diba.domain.models.common import Meta
from diba.domain.models.transit import TransitResult
from diba.engine import VedicState


def _meta() -> Meta:
    return Meta(
        engine_version="diba-core-v5",
        swisseph_version="unknown",
        config_digest="pending",
        ephe_expectations="de405/sepl_18",
        timezone_policy="UTC",
    )


def compute_tajaka(*, state: VedicState | None = None, **_kwargs) -> TransitResult:
    payload = {"implemented": False, "message": "Transit full coverage is scheduled in phase-2."}
    if state is not None:
        payload["base_jd_ut"] = state.jd_ut
    return TransitResult(kind="tajaka", payload=payload, meta=_meta())
