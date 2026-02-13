from __future__ import annotations

import pytest

from diba.schemas.kr_models import VedicSettingsModel
from diba.vedic.registry import (
    AyanamsaResolutionError,
    canonicalize_ayanamsa_id,
    list_ayanamsa_ids,
    resolve_ayanamsa,
)


def test_canonicalize_rules_are_stable() -> None:
    assert canonicalize_ayanamsa_id("  Fagan-Bradley  ") == "fagan"
    assert canonicalize_ayanamsa_id("Krishnamurti") == "kp"
    assert canonicalize_ayanamsa_id("True Lahiri") == "true_citra"
    assert canonicalize_ayanamsa_id("   LAHIRI   ") == "lahiri"

    with pytest.raises(AyanamsaResolutionError) as exc:
        canonicalize_ayanamsa_id("   ")
    assert exc.value.reason_code == "invalid"


def test_list_ayanamsa_ids_is_deterministic_and_canonical() -> None:
    first = list_ayanamsa_ids()
    second = list_ayanamsa_ids()
    assert first == second
    assert first == sorted(first)
    assert "true_lahiri" not in first
    assert "sidm_user" not in first

    with_aliases = list_ayanamsa_ids(include_aliases=True)
    assert "true_lahiri" in with_aliases
    assert "fagan_bradley" in with_aliases
    assert "krishnamurti" in with_aliases


def test_resolve_with_fallback_supports_all_reason_codes() -> None:
    spec_invalid, report_invalid = resolve_ayanamsa("no_such_mode", on_unsupported="fallback_default")
    assert spec_invalid.id == "lahiri"
    assert report_invalid.was_fallback is True
    assert report_invalid.reason_code == "invalid"
    assert report_invalid.effective_id == "lahiri"

    spec_disabled, report_disabled = resolve_ayanamsa("sidm_user", on_unsupported="fallback_default")
    assert spec_disabled.id == "lahiri"
    assert report_disabled.reason_code == "disabled"

    spec_recognized, report_recognized = resolve_ayanamsa("senthil", on_unsupported="fallback_default")
    assert spec_recognized.id == "lahiri"
    assert report_recognized.reason_code == "recognized_not_implemented"


def test_resolve_misconfigured_default_always_raises() -> None:
    with pytest.raises(AyanamsaResolutionError, match="Invalid Ayanamsa mode"):
        resolve_ayanamsa(
            "no_such_mode",
            on_unsupported="fallback_default",
            default_id="also_missing",
        )


def test_schema_ayanamsa_field_canonicalizes_alias_before_enum_validation() -> None:
    model = VedicSettingsModel(
        ayanamsa_id="  Fagan-Bradley ",
        node_mode="mean",
        house_system_id="whole_sign",
    )
    assert model.ayanamsa_id.value == "fagan"
