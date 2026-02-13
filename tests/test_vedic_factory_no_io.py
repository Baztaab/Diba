from __future__ import annotations

import ast
from pathlib import Path


def test_vedic_factory_imports_stay_pure() -> None:
    factory_path = Path(__file__).resolve().parents[1] / "diba" / "vedic" / "factory.py"
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
