"""API v1 serializer helpers."""

from __future__ import annotations

from diba.core.indexing import rasi0_to_rasi1


def serialize_rasi_index(index0: int) -> int:
    """Serialize zero-based rasi index to one-based public representation."""
    return rasi0_to_rasi1(index0)
