"""Facade for transit capability (phase-1 skeleton)."""

from __future__ import annotations

from diba.domain.models.common import Meta
from diba.domain.models.transit import TransitResult


def compute_tajaka(**_kwargs) -> TransitResult:
    return TransitResult(
        kind="tajaka",
        payload={"implemented": False, "message": "Transit full coverage is scheduled in phase-2."},
        meta=Meta(
            engine_version="diba-core-v5",
            swisseph_version="unknown",
            config_digest="pending",
            ephe_expectations="de405/sepl_18",
            timezone_policy="UTC",
        ),
    )

