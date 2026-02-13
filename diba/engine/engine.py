"""Context-aware computation engine with stateless session handling."""

from __future__ import annotations

import contextvars
from contextlib import contextmanager
from typing import Iterator

from diba.domain.models.common import BirthData
from diba.infra.swisseph.session import SwissEphSession

from .state import AstrologySettings, AstronomyContext, VedicState, build_vedic_state

_ENGINE_SESSION_DEPTH = contextvars.ContextVar("DIBA_ENGINE_SESSION_DEPTH", default=0)


class DibaEngine:
    """Stateless orchestrator for shared Vedic base-state computation."""

    def __init__(self, session_ctx: AstronomyContext, astro_settings: AstrologySettings) -> None:
        self.session_ctx = session_ctx
        self.astro_settings = astro_settings

    @contextmanager
    def session(self) -> Iterator[None]:
        depth = _ENGINE_SESSION_DEPTH.get()
        token = _ENGINE_SESSION_DEPTH.set(depth + 1)
        outer = depth == 0
        swe_session = SwissEphSession() if outer else None
        try:
            if swe_session is not None:
                swe_session.__enter__()
            yield
        finally:
            if swe_session is not None:
                swe_session.__exit__(None, None, None)
            _ENGINE_SESSION_DEPTH.reset(token)

    def state(self, birth_data: BirthData) -> VedicState:
        if _ENGINE_SESSION_DEPTH.get() > 0:
            return build_vedic_state(
                birth_data,
                self.session_ctx,
                self.astro_settings,
                require_active_session=True,
            )

        with self.session():
            return build_vedic_state(
                birth_data,
                self.session_ctx,
                self.astro_settings,
                require_active_session=True,
            )
