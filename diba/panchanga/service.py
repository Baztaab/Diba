"""Facade for panchanga capability (phase-1 baseline)."""

from __future__ import annotations

from diba.domain.models.common import BirthData, Meta, RuntimePolicy
from diba.domain.models.panchanga import PanchangaResult


def compute(birth: BirthData, policy: RuntimePolicy) -> PanchangaResult:
    # Phase-1 keeps panchanga as a capability boundary with explicit status.
    payload = {
        "implemented": False,
        "message": "Panchanga detailed calculators are scheduled in capability phase.",
        "input_echo": {
            "date": [birth.year, birth.month, birth.day],
            "time": [birth.hour, birth.minute, birth.seconds],
            "tz": birth.tz_str,
            "lat": birth.place.lat,
            "lon": birth.place.lon,
            "policy": policy.model_dump(),
        },
    }
    return PanchangaResult(
        status="planned",
        payload=payload,
        meta=Meta(
            engine_version="diba-core-v5",
            swisseph_version="unknown",
            config_digest="pending",
            ephe_expectations="de405/sepl_18",
            timezone_policy="UTC",
        ),
    )

