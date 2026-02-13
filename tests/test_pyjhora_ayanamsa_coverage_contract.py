from __future__ import annotations

from pathlib import Path


def test_pyjhora_inventory_contains_exception_table_for_disabled_and_legacy_modes() -> None:
    root = Path(__file__).resolve().parents[1]
    inventory = (root / "project_memory" / "research" / "ayanamsa-pyjhora-inventory.md").read_text(
        encoding="utf-8"
    )
    assert "Exception Table" in inventory
    assert "sidm_user" in inventory.casefold()
    assert "senthil" in inventory.casefold()
    assert "sundar_ss" in inventory.casefold()
