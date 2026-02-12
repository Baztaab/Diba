"""Panchanga models."""

from __future__ import annotations

from pydantic import BaseModel

from .common import Meta


class PanchangaResult(BaseModel):
    status: str
    payload: dict
    meta: Meta | None = None

