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
        _SWE_LOCK.acquire()
        _SESSION_ACTIVE.set(True)
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        try:
            _SESSION_ACTIVE.set(False)
        finally:
            _SWE_LOCK.release()


def ensure_session_active() -> None:
    if not _SESSION_ACTIVE.get():
        raise RuntimeError("SwissEph call outside active SwissEphSession")


def set_ephe_path(path: str) -> None:
    ensure_session_active()
    swe.set_ephe_path(path)


def set_sid_mode(mode: int, t0: float = 0.0, ayan_t0: float = 0.0) -> None:
    ensure_session_active()
    swe.set_sid_mode(mode, t0, ayan_t0)


def set_topo(lon: float, lat: float, alt: float) -> None:
    ensure_session_active()
    swe.set_topo(lon, lat, alt)
