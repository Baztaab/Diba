from __future__ import annotations

from pathlib import Path

DOC_MIRROR_POINTERS = [
    ("docs/research/ayanamsa-pyjhora-inventory.md", "project_memory/research/ayanamsa-pyjhora-inventory.md"),
    ("docs/research/ayanamsa-pyjhora-set-logic.md", "project_memory/research/ayanamsa-pyjhora-set-logic.md"),
    ("docs/research/ayanamsa-pyjhora-coverage.md", "project_memory/research/ayanamsa-pyjhora-coverage.md"),
]


def test_docs_research_files_explicitly_mark_mirror_pointer() -> None:
    root = Path(__file__).resolve().parents[1]
    for mirror_path, canonical_path in DOC_MIRROR_POINTERS:
        mirror = root / mirror_path
        canonical = root / canonical_path
        assert mirror.exists(), f"Missing docs mirror file: {mirror_path}"
        assert canonical.exists(), f"Missing canonical project memory file: {canonical_path}"
        text = mirror.read_text(encoding="utf-8")
        assert "Mirror/Pointer - Canonical source-of-truth:" in text
        assert canonical_path in text
