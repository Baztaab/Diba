from __future__ import annotations

import inspect
from pathlib import Path

from diba.engine import AstrologySettings, AstronomyContext, DibaEngine
from diba.vedic.context import VedicCalculationContext


def test_compute_core_exposes_manage_session_contract() -> None:
    sig = inspect.signature(VedicCalculationContext.compute_core)
    assert "manage_session" in sig.parameters
    assert sig.parameters["manage_session"].default is True


def test_engine_has_no_persistent_session_state() -> None:
    engine = DibaEngine(
        session_ctx=AstronomyContext(),
        astro_settings=AstrologySettings(),
    )
    assert "_session" not in engine.__dict__


def test_engine_state_builder_delegates_session_ownership_to_engine() -> None:
    root = Path(__file__).resolve().parents[1]
    src = (root / "diba/engine/state.py").read_text(encoding="utf-8")
    assert "compute_core(manage_session=not require_active_session)" in src
