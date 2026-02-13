from __future__ import annotations

from pathlib import Path

MIRROR_PAIRS = [
    (
        "docs/roadmap/EXECUTION_ROADMAP.md",
        "project_memory/EXECUTION_ROADMAP.md",
    ),
    (
        "docs/contracts/RUNTIME_CONTRACTS.md",
        "project_memory/RUNTIME_CONTRACTS.md",
    ),
    (
        "docs/architecture/ADR-001-Addendum-B-Engine-State.md",
        "project_memory/adr/ADR-001-Addendum-B-Engine-State.md",
    ),
]


def test_docs_and_project_memory_mirrors_are_in_sync() -> None:
    root = Path(__file__).resolve().parents[1]

    for repo_doc, memory_doc in MIRROR_PAIRS:
        repo_path = root / repo_doc
        memory_path = root / memory_doc
        assert repo_path.exists(), f"Missing repo mirror source: {repo_doc}"
        assert memory_path.exists(), f"Missing project memory mirror: {memory_doc}"

        repo_text = repo_path.read_text(encoding="utf-8")
        memory_text = memory_path.read_text(encoding="utf-8")
        assert repo_text == memory_text, (
            f"Mirror drift detected between {repo_doc} and {memory_doc}. "
            "Sync canonical and mirror documents."
        )
