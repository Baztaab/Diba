from __future__ import annotations

import pytest

from diba.vedic.context import VedicCalculationContext, swe
from diba.vedic.registry import (
    AYANAMSA_REGISTRY,
    AyanamsaResolutionError,
    VedicRegistryError,
    resolve_ayanamsa,
    resolve_house_system,
)


def test_disabled_and_recognized_modes_fail_fast_in_resolver() -> None:
    with pytest.raises(AyanamsaResolutionError) as sidm_exc:
        resolve_ayanamsa("sidm_user")
    assert sidm_exc.value.reason_code == "disabled"

    with pytest.raises(AyanamsaResolutionError) as senthil_exc:
        resolve_ayanamsa("senthil")
    assert senthil_exc.value.reason_code == "recognized_not_implemented"

    with pytest.raises(AyanamsaResolutionError) as sundar_exc:
        resolve_ayanamsa("sundar_ss")
    assert sundar_exc.value.reason_code == "recognized_not_implemented"


def test_sidm_user_is_disabled_in_canonical_context() -> None:
    ctx = VedicCalculationContext(
        jd_utc=swe.julday(2004, 1, 27, 12.0, swe.GREG_CAL),
        lat=35.7,
        lon=51.1,
        ayanamsa=AYANAMSA_REGISTRY["sidm_user"],
        house_system=resolve_house_system("whole_sign"),
    )
    with pytest.raises(VedicRegistryError, match="reason_code=disabled"):
        ctx.compute_core()
