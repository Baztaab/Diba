from __future__ import annotations

import ast
from pathlib import Path

SWISSEPH_IMPORT_ALLOWLIST = {
    "diba/infra/swisseph/session.py",
}

SWISSEPH_SETTER_ALLOWLIST = {
    "diba/infra/swisseph/session.py",
}


def _iter_py_files(root: Path):
    for path in root.rglob("*.py"):
        if ".venv" in path.parts or "site-packages" in path.parts or "dist-info" in path.parts:
            continue
        yield path


def _constant_str(node: ast.AST) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def _is_swisseph_dynamic_import(call: ast.Call) -> bool:
    if (
        isinstance(call.func, ast.Attribute)
        and isinstance(call.func.value, ast.Name)
        and call.func.value.id == "importlib"
        and call.func.attr == "import_module"
        and call.args
        and _constant_str(call.args[0]) == "swisseph"
    ):
        return True

    if (
        isinstance(call.func, ast.Name)
        and call.func.id == "__import__"
        and call.args
        and _constant_str(call.args[0]) == "swisseph"
    ):
        return True

    return False


def test_swisseph_containment_and_state_setter_rules():
    root = Path(__file__).resolve().parents[1]
    offenders: list[str] = []

    for path in _iter_py_files(root / "diba"):
        rel = str(path.relative_to(root)).replace("\\", "/")
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel)

        module_aliases: set[str] = set()
        imported_names: set[str] = set()
        dynamic_aliases: set[str] = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "swisseph":
                        module_aliases.add(alias.asname or alias.name)
                        if rel not in SWISSEPH_IMPORT_ALLOWLIST:
                            offenders.append(f"{rel}:{node.lineno}: forbidden import swisseph")

            elif isinstance(node, ast.ImportFrom) and node.module == "swisseph":
                for alias in node.names:
                    if alias.name == "*":
                        offenders.append(f"{rel}:{node.lineno}: forbidden from swisseph import *")
                    else:
                        imported_names.add(alias.asname or alias.name)
                        if rel not in SWISSEPH_IMPORT_ALLOWLIST:
                            offenders.append(
                                f"{rel}:{node.lineno}: forbidden from swisseph import {alias.name}"
                            )

            elif isinstance(node, ast.Assign) and isinstance(node.value, ast.Call):
                if _is_swisseph_dynamic_import(node.value):
                    for target in node.targets:
                        if isinstance(target, ast.Name):
                            dynamic_aliases.add(target.id)
                    if rel not in SWISSEPH_IMPORT_ALLOWLIST:
                        offenders.append(f"{rel}:{node.lineno}: forbidden dynamic swisseph import")

            elif isinstance(node, ast.Call) and _is_swisseph_dynamic_import(node):
                if rel not in SWISSEPH_IMPORT_ALLOWLIST:
                    offenders.append(f"{rel}:{node.lineno}: forbidden dynamic swisseph import")

        swisseph_like_names = module_aliases | dynamic_aliases | {"swe", "swisseph"}

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            fn = node.func

            if isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name):
                if fn.value.id in swisseph_like_names and fn.attr.startswith("set_"):
                    if rel not in SWISSEPH_SETTER_ALLOWLIST:
                        offenders.append(
                            f"{rel}:{node.lineno}: forbidden swisseph state setter {fn.value.id}.{fn.attr}(...)"
                        )

            if isinstance(fn, ast.Name):
                if fn.id in imported_names and fn.id.startswith("set_"):
                    if rel not in SWISSEPH_SETTER_ALLOWLIST:
                        offenders.append(
                            f"{rel}:{node.lineno}: forbidden swisseph state setter {fn.id}(...)"
                        )

    assert not offenders, "SwissEph containment violations:\n" + "\n".join(sorted(set(offenders)))
