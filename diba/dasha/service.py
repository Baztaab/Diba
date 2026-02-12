"""Facade for dasha capability (phase-1 baseline)."""

from __future__ import annotations

from diba.domain.models.common import Meta
from diba.domain.models.dasha import DashaTimeline


def compute(family: str, scheme: str, **_kwargs) -> DashaTimeline:
    return DashaTimeline(
        family=family,
        scheme=scheme,
        entries=[],
        meta=Meta(
            engine_version="diba-core-v5",
            swisseph_version="unknown",
            config_digest="pending",
            ephe_expectations="de405/sepl_18",
            timezone_policy="UTC",
        ),
    )

