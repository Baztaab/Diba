"""Facade for compatibility capability (phase-2 state-wired baseline)."""

from __future__ import annotations

from diba.domain.models.common import Meta
from diba.domain.models.compatibility import CompatibilityResult
from diba.engine import VedicState


def _meta() -> Meta:
    return Meta(
        engine_version="diba-core-v5",
        swisseph_version="unknown",
        config_digest="pending",
        ephe_expectations="de405/sepl_18",
        timezone_policy="UTC",
    )


def compute_ashtakoota(*, state: VedicState | None = None, **_kwargs) -> CompatibilityResult:
    payload = {"implemented": False, "message": "Compatibility scoring will be expanded incrementally."}
    if state is not None:
        payload["base_location"] = state.location
    return CompatibilityResult(method="ashtakoota", payload=payload, meta=_meta())
