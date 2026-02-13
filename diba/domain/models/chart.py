"""Chart models."""

from __future__ import annotations

from pydantic import BaseModel

from .common import Meta


class ChartResult(BaseModel):
    """Standard result model for chart computations."""

    chart_id: str
    payload: dict
    meta: Meta | None = None


class VargaResult(BaseModel):
    """Standard result model for varga computations."""

    chart_id: str
    method: int
    payload: dict
    meta: Meta | None = None
