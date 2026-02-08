import pytest

from diba.vedic.registry import (
    AYANAMSA_REGISTRY,
    HOUSE_SYSTEM_REGISTRY,
    NODE_MODE_REGISTRY,
    VedicRegistryError,
    resolve_ayanamsa,
)


def test_pyjhora_sidm_mapped_ayanamsa_ids_are_present():
    expected_ids = {
        "fagan",
        "kp",
        "lahiri",
        "raman",
        "ushashashi",
        "yukteshwar",
        "suryasiddhanta",
        "suryasiddhanta_msun",
        "aryabhata",
        "aryabhata_msun",
        "ss_citra",
        "true_citra",
        "true_revati",
        "ss_revati",
        "true_lahiri",
        "true_pushya",
        "true_mula",
        "kp_senthil",
        "sidm_user",
    }
    assert expected_ids.issubset(set(AYANAMSA_REGISTRY.keys()))


def test_true_lahiri_is_alias_of_true_citra():
    spec = AYANAMSA_REGISTRY["true_lahiri"]
    assert spec.alias_of == "true_citra"
    assert spec.swe_mode == "SIDM_TRUE_CITRA"


@pytest.mark.parametrize("mode", ["senthil", "sundar_ss"])
def test_recognized_not_implemented_ayanamsa_fail_fast(mode: str):
    spec = AYANAMSA_REGISTRY[mode]
    assert spec.status == "recognized_not_implemented"
    with pytest.raises(VedicRegistryError, match="recognized but not implemented"):
        resolve_ayanamsa(mode)


def test_house_methods_1_to_5_are_surfaced():
    keys = set(HOUSE_SYSTEM_REGISTRY.keys())
    assert {"1", "2", "3", "4", "5"}.issubset(keys)


def test_node_policies_mean_and_true_are_available():
    keys = set(NODE_MODE_REGISTRY.keys())
    assert {"mean", "true"}.issubset(keys)
