"""Chart models."""

from __future__ import annotations

from pydantic import BaseModel

from .common import Meta


class ChartResult(BaseModel):
    chart_id: str
    payload: dict
    meta: Meta | None = None


class VargaResult(BaseModel):
    chart_id: str
    method: int
    payload: dict
    meta: Meta | None = None

