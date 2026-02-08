from __future__ import annotations

import re
from pathlib import Path
import pytest

from kerykeion.vedic import builder


def _scan(pattern: str, root: Path) -> list[str]:
    rx = re.compile(pattern)
    offenders: list[str] = []
    for path in root.rglob("*.py"):
        normalized = str(path).replace("\\", "/")
        if "/docs/" in normalized or "/_archive/" in normalized:
            continue
        text = path.read_text(encoding="utf-8")
        for idx, line in enumerate(text.splitlines(), start=1):
            if rx.search(line):
                if line.lstrip().startswith("def build_vedic_payload"):
                    continue
                offenders.append(f"{normalized}:{idx}")
    return offenders


def test_no_legacy_build_vedic_payload_in_runtime() -> None:
    root = Path(__file__).resolve().parents[1] / "kerykeion"
    offenders = _scan(r"\bbuild_vedic_payload\s*\(", root)
    assert not offenders, "Legacy build_vedic_payload usage found:\n" + "\n".join(offenders)


def test_no_calc_data_in_vedic_runtime() -> None:
    root = Path(__file__).resolve().parents[1] / "kerykeion" / "vedic"
    offenders = _scan(r"\bcalc_data\b", root)
    assert not offenders, "calc_data usage found in vedic runtime:\n" + "\n".join(offenders)


def test_no_western_factory_imports_in_vedic_runtime() -> None:
    root = Path(__file__).resolve().parents[1] / "kerykeion" / "vedic"
    offenders = _scan(r"\bAstrologicalSubjectFactory\b", root)
    assert not offenders, "AstrologicalSubjectFactory referenced in vedic runtime:\n" + "\n".join(offenders)


def test_build_vedic_payload_raises_under_pytest(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("PYTEST_CURRENT_TEST", "1")
    with pytest.raises(RuntimeError):
        builder.build_vedic_payload()
    monkeypatch.delenv("PYTEST_CURRENT_TEST", raising=False)
    monkeypatch.setenv("BAZTAB_STRICT", "1")
    with pytest.raises(RuntimeError):
        builder.build_vedic_payload()
