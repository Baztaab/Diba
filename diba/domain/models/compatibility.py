"""Compatibility models."""

from __future__ import annotations

from pydantic import BaseModel

from .common import Meta


class CompatibilityResult(BaseModel):
    method: str
    payload: dict
    meta: Meta | None = None

