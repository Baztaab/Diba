from __future__ import annotations

import importlib
import inspect
import pkgutil
from pathlib import Path


def test_no_swe_outside_context_or_registry():
    vedic_path = Path(__file__).resolve().parents[1] / "kerykeion" / "vedic"
    allowed_import = {"kerykeion.vedic.context"}
    allowed_calls = {"kerykeion.vedic.context"}

    for module_info in pkgutil.walk_packages([str(vedic_path)], prefix="kerykeion.vedic."):
        module = importlib.import_module(module_info.name)
        source = inspect.getsource(module)

        if module_info.name not in allowed_import:
            assert "import swisseph" not in source, module_info.name
        if module_info.name not in allowed_calls:
            assert "swe." not in source, module_info.name


def test_no_swe_calls_outside_context_in_repo() -> None:
    root = Path(__file__).resolve().parents[1] / "kerykeion"
    allowed = {str(root / "vedic" / "context.py").replace("\\", "/")}

    offenders = []
    for path in root.rglob("*.py"):
        normalized = str(path).replace("\\", "/")
        if "/_archive/" in normalized or "/docs/" in normalized:
            continue
        if normalized in allowed:
            continue
        text = path.read_text(encoding="utf-8")
        if "import swisseph" in text or "swe." in text:
            offenders.append(normalized)

    assert not offenders, "SwissEph calls outside context:\n" + "\n".join(sorted(offenders))
