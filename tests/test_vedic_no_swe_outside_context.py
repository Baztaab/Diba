from __future__ import annotations

import ast
from pathlib import Path

ALLOWED_FILES = {
    "diba/vedic/context.py",
}

FORBIDDEN_ATTR_PREFIX = "set_"
FORBIDDEN_NAMES = {
    "set_sid_mode",
    "set_topo",
    "set_ephe_path",
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


def _is_dynamic_swisseph_import(call: ast.Call) -> bool:
    # importlib.import_module("swisseph")
    if (
        isinstance(call.func, ast.Attribute)
        and isinstance(call.func.value, ast.Name)
        and call.func.value.id == "importlib"
        and call.func.attr == "import_module"
        and call.args
        and _constant_str(call.args[0]) == "swisseph"
    ):
        return True

    # __import__("swisseph")
    if (
        isinstance(call.func, ast.Name)
        and call.func.id == "__import__"
        and call.args
        and _constant_str(call.args[0]) == "swisseph"
    ):
        return True

    return False


def test_no_swisseph_import_or_state_calls_outside_allowed_modules():
    root = Path(__file__).resolve().parents[1]
    offenders: list[str] = []

    for path in _iter_py_files(root / "diba"):
        rel = str(path.relative_to(root)).replace("\\", "/")
        if rel in ALLOWED_FILES:
            continue

        tree = ast.parse(path.read_text(encoding="utf-8"), filename=rel)

        swisseph_module_aliases: set[str] = set()
        swisseph_imported_names: set[str] = set()

        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name == "swisseph":
                        swisseph_module_aliases.add(alias.asname or alias.name)
                        offenders.append(f"{rel}:{node.lineno}: forbidden import 'import swisseph'")

            elif isinstance(node, ast.ImportFrom) and node.module == "swisseph":
                for alias in node.names:
                    if alias.name == "*":
                        offenders.append(f"{rel}:{node.lineno}: forbidden 'from swisseph import *'")
                    else:
                        swisseph_imported_names.add(alias.asname or alias.name)
                        offenders.append(
                            f"{rel}:{node.lineno}: forbidden import 'from swisseph import {alias.name}'"
                        )

        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue

            if _is_dynamic_swisseph_import(node):
                offenders.append(f"{rel}:{node.lineno}: forbidden dynamic swisseph import")
                continue

            fn = node.func

            # Case A: swe.set_sid_mode(...)
            if isinstance(fn, ast.Attribute) and isinstance(fn.value, ast.Name):
                base = fn.value.id
                if base in swisseph_module_aliases:
                    if fn.attr.startswith(FORBIDDEN_ATTR_PREFIX) or fn.attr in FORBIDDEN_NAMES:
                        offenders.append(f"{rel}:{node.lineno}: forbidden SwissEph state call {base}.{fn.attr}(...)")

            # Case B: set_sid_mode(...) imported from swisseph
            if isinstance(fn, ast.Name):
                name = fn.id
                if name in swisseph_imported_names:
                    if name.startswith(FORBIDDEN_ATTR_PREFIX) or name in FORBIDDEN_NAMES:
                        offenders.append(f"{rel}:{node.lineno}: forbidden SwissEph state call {name}(...)")

    assert not offenders, "SwissEph usage outside allowed modules:\n" + "\n".join(sorted(set(offenders)))

