"""Facade for dasha capability (phase-2 state-wired baseline)."""

from __future__ import annotations

from diba.domain.models.common import Meta
from diba.domain.models.dasha import DashaTimeline
from diba.engine import VedicState


def _meta() -> Meta:
    return Meta(
        engine_version="diba-core-v5",
        swisseph_version="unknown",
        config_digest="pending",
        ephe_expectations="de405/sepl_18",
        timezone_policy="UTC",
    )


def compute(family: str, scheme: str, *, state: VedicState | None = None, **_kwargs) -> DashaTimeline:
    """Build baseline dasha timeline payload from optional shared state."""
    entries: list[dict] = []
    if state is not None:
        entries.append({"jd_ut": state.jd_ut, "message": "Base state attached for dasha pipeline wiring."})
    return DashaTimeline(
        family=family,
        scheme=scheme,
        entries=entries,
        meta=_meta(),
    )
