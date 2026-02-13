"""Transit models."""

from __future__ import annotations

from pydantic import BaseModel

from .common import Meta


class TransitResult(BaseModel):
    """Standard result model for transit computations."""

    kind: str
    payload: dict
    meta: Meta | None = None
