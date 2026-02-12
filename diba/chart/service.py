"""Facade for chart capability."""

from __future__ import annotations

from diba.domain.models.chart import ChartResult, VargaResult
from diba.domain.models.common import Meta
from diba.vedic.factory import VedicSubjectFactory
from diba.vedic.vargas import compute_varga as _compute_varga


def compute_d1(**kwargs) -> ChartResult:
    model = VedicSubjectFactory.from_birth_data(**kwargs)
    payload = model.model_dump()
    return ChartResult(
        chart_id="D1",
        payload=payload,
        meta=Meta(
            engine_version="diba-core-v5",
            swisseph_version="unknown",
            config_digest="pending",
            ephe_expectations="de405/sepl_18",
            timezone_policy="UTC",
        ),
    )


def compute_varga(core_objects: dict, chart_id: str, method: int | None = None) -> VargaResult:
    result = _compute_varga(core_objects, chart_id, method=method)
    return VargaResult(
        chart_id=result.get("factor") and chart_id or chart_id,
        method=int(result.get("method", method or 1)),
        payload=result,
        meta=Meta(
            engine_version="diba-core-v5",
            swisseph_version="unknown",
            config_digest="pending",
            ephe_expectations="de405/sepl_18",
            timezone_policy="UTC",
        ),
    )

