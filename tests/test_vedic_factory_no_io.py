from __future__ import annotations

import ast
import sqlite3
from pathlib import Path

import pytest

from kerykeion.vedic.factory import VedicSubjectFactory


def test_vedic_factory_imports_stay_pure() -> None:
    factory_path = Path(__file__).resolve().parents[1] / "kerykeion" / "vedic" / "factory.py"
    tree = ast.parse(factory_path.read_text(encoding="utf-8"))
    banned_prefixes = ("requests", "requests_cache", "sqlite3", "fetch_geonames")
    offenders: list[str] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name
                if name.startswith(banned_prefixes):
                    offenders.append(name)
        if isinstance(node, ast.ImportFrom):
            module = node.module or ""
            if module.startswith(banned_prefixes):
                offenders.append(module)

    assert not offenders, f"Factory has forbidden IO-related imports: {sorted(set(offenders))}"


def test_vedic_factory_no_network_or_db_calls(monkeypatch: pytest.MonkeyPatch) -> None:
    calls = {"network": 0, "sqlite": 0}

    def _raise_network(*_args, **_kwargs):
        calls["network"] += 1
        raise AssertionError("Network IO is forbidden in VedicSubjectFactory.from_birth_data")

    def _raise_sqlite(*_args, **_kwargs):
        calls["sqlite"] += 1
        raise AssertionError("sqlite IO is forbidden in VedicSubjectFactory.from_birth_data")

    # Patch only if requests is importable in this environment.
    try:
        import requests  # type: ignore

        monkeypatch.setattr(requests, "get", _raise_network, raising=True)
    except Exception:
        pass

    monkeypatch.setattr(sqlite3, "connect", _raise_sqlite, raising=True)

    model = VedicSubjectFactory.from_birth_data(
        year=2004,
        month=1,
        day=27,
        hour=14,
        minute=45,
        seconds=35.0,
        tz_str="Asia/Tehran",
        lat=35.7,
        lon=51.1,
        ayanamsa_id="lahiri",
        node_mode="mean",
        house_system_id="whole_sign",
    )
    assert model.core.jd_utc > 0.0
    assert calls["network"] == 0
    assert calls["sqlite"] == 0
