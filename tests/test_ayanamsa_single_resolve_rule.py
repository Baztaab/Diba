from __future__ import annotations

import ast
from pathlib import Path

ALLOWED_RESOLVE_CALLERS = {
    "diba/_cli/options.py",
    "diba/engine/state.py",
    "diba/vedic/registry.py",
}


def test_resolve_ayanamsa_is_called_only_in_entrypoints_and_registry() -> None:
    root = Path(__file__).resolve().parents[1]
    offenders: list[str] = []

    for path in (root / "diba").rglob("*.py"):
        rel = str(path.relative_to(root)).replace("\\", "/")
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel)
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            fn = node.func
            if isinstance(fn, ast.Name) and fn.id == "resolve_ayanamsa":
                if rel not in ALLOWED_RESOLVE_CALLERS:
                    offenders.append(f"{rel}:{node.lineno}")
            if isinstance(fn, ast.Attribute) and fn.attr == "resolve_ayanamsa":
                if rel not in ALLOWED_RESOLVE_CALLERS:
                    offenders.append(f"{rel}:{node.lineno}")

    assert not offenders, (
        "Single-resolve rule violated. resolve_ayanamsa call sites must stay in entrypoints/registry only:\n"
        + "\n".join(sorted(offenders))
    )
