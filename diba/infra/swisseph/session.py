"""Canonical SwissEph session and safety guards."""

from __future__ import annotations

import contextvars
from threading import RLock

import swisseph as swe  # noqa: TID251

_SWE_LOCK = RLock()
_SESSION_ACTIVE = contextvars.ContextVar("DIBA_SWE_SESSION_ACTIVE", default=False)
__all__ = [
    "SwissEphSession",
    "ensure_session_active",
    "set_ephe_path",
    "set_sid_mode",
    "set_topo",
    "swe",
]


class SwissEphSession:
    """Guard global-state SwissEph usage with lock + active context flag."""

    def __enter__(self) -> "SwissEphSession":
        """Enter session scope and mark active flag for this context."""
        _SWE_LOCK.acquire()
        _SESSION_ACTIVE.set(True)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        """Reset active flag and always release global SwissEph lock."""
        try:
            _SESSION_ACTIVE.set(False)
        finally:
            _SWE_LOCK.release()


def ensure_session_active() -> None:
    """Raise runtime error when SwissEph is used outside session scope."""
    if not _SESSION_ACTIVE.get():
        raise RuntimeError("SwissEph call outside active SwissEphSession")


def set_ephe_path(path: str) -> None:
    """Set SwissEph ephemeris path inside an active session."""
    ensure_session_active()
    swe.set_ephe_path(path)


def set_sid_mode(mode: int, t0: float = 0.0, ayan_t0: float = 0.0) -> None:
    """Set SwissEph sidereal mode inside an active session."""
    ensure_session_active()
    swe.set_sid_mode(mode, t0, ayan_t0)


def set_topo(lon: float, lat: float, alt: float) -> None:
    """Set SwissEph topocentric coordinates inside an active session."""
    ensure_session_active()
    swe.set_topo(lon, lat, alt)
