"""Deterministic SwissEph state policy helpers."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from .session import set_ephe_path, set_sid_mode


@dataclass(frozen=True)
class SwissEphStateConfig:
    """Deterministic SwissEph state configuration payload."""

    sidereal_mode: int
    ephe_path: Optional[str] = None


def apply_state(config: SwissEphStateConfig) -> None:
    """Apply deterministic SwissEph state using session-bound setters."""
    if config.ephe_path:
        set_ephe_path(config.ephe_path)
    set_sid_mode(config.sidereal_mode, 0.0, 0.0)
