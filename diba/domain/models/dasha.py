"""Dasha models."""

from __future__ import annotations

from pydantic import BaseModel

from .common import Meta


class DashaTimeline(BaseModel):
    """Standard result model for dasha timeline outputs."""

    family: str
    scheme: str
    entries: list[dict]
    meta: Meta | None = None
