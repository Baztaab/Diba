from __future__ import annotations

from diba.domain.enums.generated_ayanamsa_enum import AyanamsaIdEnum
from diba.vedic.registry import list_ayanamsa_ids


def test_generated_enum_values_match_selectable_registry_ids() -> None:
    enum_values = sorted(item.value for item in AyanamsaIdEnum)
    registry_values = list_ayanamsa_ids(selectable_only=True)
    assert enum_values == registry_values
