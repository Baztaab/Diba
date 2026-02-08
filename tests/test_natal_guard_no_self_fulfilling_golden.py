from __future__ import annotations

from pathlib import Path
import re


ROOT = Path(__file__).resolve().parents[1]
TESTS_DIR = ROOT / "tests"

# Golden/snapshot regeneration or output-comparison gates are not allowed in runtime tests.
BANNED_PATTERNS = [
    re.compile(r"golden_outputs"),
    re.compile(r"update_goldens"),
    re.compile(r"diagnose_static_goldens"),
]


def _iter_test_files() -> list[Path]:
    excluded = {
        "test_natal_guard_no_self_fulfilling_golden.py",
    }
    return sorted(
        p for p in TESTS_DIR.rglob("test_*.py") if p.is_file() and p.name not in excluded
    )


def test_no_self_fulfilling_golden_gate_in_tests() -> None:
    offenders: list[str] = []
    for path in _iter_test_files():
        lines = path.read_text(encoding="utf-8").splitlines()
        for lineno, line in enumerate(lines, start=1):
            for pattern in BANNED_PATTERNS:
                if pattern.search(line):
                    offenders.append(f"{path.relative_to(ROOT)}:{lineno}: {line.strip()}")
                    break
    assert not offenders, "Self-fulfilling golden/snapshot gates are forbidden:\n" + "\n".join(offenders)
