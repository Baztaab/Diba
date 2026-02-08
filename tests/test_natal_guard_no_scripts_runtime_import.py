from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TESTS_DIR = ROOT / "tests"
IMPORT_RE = re.compile(r"^\s*(?:from|import)\s+scripts(?:\.|\s|$)")


def _iter_test_files() -> list[Path]:
    return sorted(p for p in TESTS_DIR.rglob("test_*.py") if p.is_file())


def test_no_scripts_import_in_tests() -> None:
    offenders: list[str] = []
    for path in _iter_test_files():
        for lineno, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if IMPORT_RE.search(line):
                offenders.append(f"{path.relative_to(ROOT)}:{lineno}: {line.strip()}")
    assert not offenders, "scripts/* imports are forbidden in tests:\n" + "\n".join(offenders)
