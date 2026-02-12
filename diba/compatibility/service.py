"""Facade for compatibility capability."""

from __future__ import annotations

from diba.domain.models.common import Meta
from diba.domain.models.compatibility import CompatibilityResult


def compute_ashtakoota(**_kwargs) -> CompatibilityResult:
    return CompatibilityResult(
        method="ashtakoota",
        payload={"implemented": False, "message": "Compatibility scoring will be expanded incrementally."},
        meta=Meta(
            engine_version="diba-core-v5",
            swisseph_version="unknown",
            config_digest="pending",
            ephe_expectations="de405/sepl_18",
            timezone_policy="UTC",
        ),
    )

