"""Panchanga models."""

from __future__ import annotations

from pydantic import BaseModel

from .common import Meta


class PanchangaResult(BaseModel):
    """Standard result model for panchanga outputs."""

    status: str
    payload: dict
    meta: Meta | None = None
