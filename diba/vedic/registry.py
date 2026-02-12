"""
Vedic runtime registry and policy resolvers.

Provides canonical IDs and validation for ayanamsa, house systems, and node
policies. This module contains no SwissEph calls and only exposes read-only
registry views plus resolver helpers.

Public API:
- VedicRegistryError
- AYANAMSA_REGISTRY
- HOUSE_SYSTEM_REGISTRY
- NODE_POLICY_REGISTRY
- list_ayanamsa_ids
- list_house_system_ids
- list_node_mode_ids
- resolve_ayanamsa
- resolve_house_system
- resolve_node_mode

Notes:
- Thread-safety: Pure read-only data; safe for concurrent use.
- Determinism: Outputs are deterministic for identical inputs.
- Contract: Registry IDs are stable; changes require a versioned policy update.
"""

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Literal, Optional


class HouseFetchPlan(str, Enum):
    """
    Strategy for fetching house data from SwissEph.
    Determines if we need full house cusp calculation or just the Ascendant.
    """

    ASC_ONLY = "asc_only"
    HOUSES_EX = "houses_ex"


SpecStatus = Literal["implemented", "recognized_not_implemented"]


@dataclass(frozen=True)
class AyanamsaSpec:
    id: str
    swe_mode: Optional[str]
    status: SpecStatus = "implemented"
    alias_of: Optional[str] = None
    requires_user_value: bool = False
    t0: Optional[float] = None  # Future-proofing (e.g. for SIDM_USER scenarios)


@dataclass(frozen=True)
class HouseSystemSpec:
    id: str
    pyjhora_method: int
    status: SpecStatus = "implemented"
    fetch_plan: Optional[HouseFetchPlan] = None
    swe_hsys_code: Optional[str] = None  # Required iff fetch_plan == HOUSES_EX
    label: Optional[str] = None


@dataclass(frozen=True)
class NodeModeSpec:
    id: str
    swe_node: str
    status: SpecStatus = "implemented"


class VedicRegistryError(ValueError):
    """Registry or policy resolution error.

    Args:
        *args: Error message details.

    Returns:
        None.

    Raises:
        None.

    Notes:
        - Thread-safety: Pure error type; no shared state.
        - Determinism: Deterministic for identical inputs.
        - Contract: Raised for invalid registry configuration or unsupported settings.

    Examples:
        >>> raise VedicRegistryError("Invalid ayanamsa")
        Traceback (most recent call last):
        ...
        diba.vedic.registry.VedicRegistryError: Invalid ayanamsa
    """


# --- Internal Data ---

_AYANAMSA_DATA = {
    "lahiri": AyanamsaSpec("lahiri", "SIDM_LAHIRI"),
    "fagan": AyanamsaSpec("fagan", "SIDM_FAGAN_BRADLEY"),
    "kp": AyanamsaSpec("kp", "SIDM_KRISHNAMURTI"),
    "raman": AyanamsaSpec("raman", "SIDM_RAMAN"),
    "ushashashi": AyanamsaSpec("ushashashi", "SIDM_USHASHASHI"),
    "yukteshwar": AyanamsaSpec("yukteshwar", "SIDM_YUKTESHWAR"),
    "suryasiddhanta": AyanamsaSpec("suryasiddhanta", "SIDM_SURYASIDDHANTA"),
    "suryasiddhanta_msun": AyanamsaSpec("suryasiddhanta_msun", "SIDM_SURYASIDDHANTA_MSUN"),
    "aryabhata": AyanamsaSpec("aryabhata", "SIDM_ARYABHATA"),
    "aryabhata_msun": AyanamsaSpec("aryabhata_msun", "SIDM_ARYABHATA_MSUN"),
    "ss_citra": AyanamsaSpec("ss_citra", "SIDM_SS_CITRA"),
    "true_citra": AyanamsaSpec("true_citra", "SIDM_TRUE_CITRA"),
    "true_revati": AyanamsaSpec("true_revati", "SIDM_TRUE_REVATI"),
    "ss_revati": AyanamsaSpec("ss_revati", "SIDM_SS_REVATI"),
    "true_lahiri": AyanamsaSpec("true_lahiri", "SIDM_TRUE_CITRA", alias_of="true_citra"),
    "true_pushya": AyanamsaSpec("true_pushya", "SIDM_TRUE_PUSHYA"),
    "true_mula": AyanamsaSpec("true_mula", "SIDM_TRUE_MULA"),
    "kp_senthil": AyanamsaSpec("kp_senthil", "SIDM_KRISHNAMURTI_VP291"),
    "sidm_user": AyanamsaSpec("sidm_user", "SIDM_USER", requires_user_value=True),
    # Recognized in PyJHora surface but non-SIDM computed paths.
    "senthil": AyanamsaSpec("senthil", None, status="recognized_not_implemented"),
    "sundar_ss": AyanamsaSpec("sundar_ss", None, status="recognized_not_implemented"),
}

_HOUSE_SYSTEM_DATA = {
    # PyJHora methods 1..5 with stable canonical IDs.
    "1": HouseSystemSpec(
        "equal_lagna_mid",
        pyjhora_method=1,
        fetch_plan=HouseFetchPlan.ASC_ONLY,
        label="Equal Housing - Lagna in the middle",
    ),
    "2": HouseSystemSpec(
        "equal_lagna_start",
        pyjhora_method=2,
        fetch_plan=HouseFetchPlan.ASC_ONLY,
        label="Equal Housing - Lagna as start",
    ),
    "3": HouseSystemSpec(
        "sripati",
        pyjhora_method=3,
        fetch_plan=HouseFetchPlan.HOUSES_EX,
        swe_hsys_code="P",
        label="Sripati method",
    ),
    # method 4 (KP/Placidus) maps to SwissEph houses_ex with Placidus code.
    "4": HouseSystemSpec(
        "placidus",
        pyjhora_method=4,
        fetch_plan=HouseFetchPlan.HOUSES_EX,
        swe_hsys_code="P",
        label="KP Method (aka Placidus Houses method)",
    ),
    # method 5 = each rasi is house / whole-sign surface.
    "5": HouseSystemSpec(
        "whole_sign",
        pyjhora_method=5,
        fetch_plan=HouseFetchPlan.ASC_ONLY,
        label="Each Rasi is the house",
    ),
    # Backward-compatible aliases.
    "whole_sign": HouseSystemSpec("whole_sign", pyjhora_method=5, fetch_plan=HouseFetchPlan.ASC_ONLY),
    "whole-sign": HouseSystemSpec("whole_sign", pyjhora_method=5, fetch_plan=HouseFetchPlan.ASC_ONLY),
    "equal_lagna_mid": HouseSystemSpec(
        "equal_lagna_mid",
        pyjhora_method=1,
        fetch_plan=HouseFetchPlan.ASC_ONLY,
        label="Equal Housing - Lagna in the middle",
    ),
    "equal_lagna_start": HouseSystemSpec(
        "equal_lagna_start",
        pyjhora_method=2,
        fetch_plan=HouseFetchPlan.ASC_ONLY,
        label="Equal Housing - Lagna as start",
    ),
    "sripati": HouseSystemSpec(
        "sripati",
        pyjhora_method=3,
        fetch_plan=HouseFetchPlan.HOUSES_EX,
        swe_hsys_code="P",
        label="Sripati method",
    ),
    "kp": HouseSystemSpec("placidus", pyjhora_method=4, fetch_plan=HouseFetchPlan.HOUSES_EX, swe_hsys_code="P"),
    "placidus": HouseSystemSpec("placidus", pyjhora_method=4, fetch_plan=HouseFetchPlan.HOUSES_EX, swe_hsys_code="P"),
}

_NODE_MODE_DATA = {
    "mean": NodeModeSpec("mean", "MEAN_NODE"),
    "true": NodeModeSpec("true", "TRUE_NODE"),
}


# --- Internal Validation Logic ---

def _validate_ayanamsa_spec(spec: AyanamsaSpec) -> None:
    if spec.status == "implemented":
        if not spec.swe_mode:
            raise VedicRegistryError(f"AyanamsaSpec '{spec.id}' is implemented but missing swe_mode.")
    if spec.alias_of is not None and spec.alias_of == spec.id:
        raise VedicRegistryError(f"AyanamsaSpec '{spec.id}' cannot alias itself.")


def _validate_house_spec(spec: HouseSystemSpec) -> None:
    """Ensures logic consistency for house systems before returning spec."""
    if spec.status == "implemented" and spec.fetch_plan is None:
        raise VedicRegistryError(
            f"HouseSystemSpec '{spec.id}' is implemented but missing fetch_plan."
        )
    if spec.fetch_plan == HouseFetchPlan.HOUSES_EX:
        if not spec.swe_hsys_code or len(spec.swe_hsys_code) != 1:
            raise VedicRegistryError(
                f"HouseSystemSpec '{spec.id}' requires a single-character swe_hsys_code when fetch_plan=HOUSES_EX."
            )


# --- Fail-Fast: Validate Registry on Import ---
for _spec in _AYANAMSA_DATA.values():
    _validate_ayanamsa_spec(_spec)
for _spec in _HOUSE_SYSTEM_DATA.values():
    _validate_house_spec(_spec)


# --- Public Read-Only Registry Views ---
AYANAMSA_REGISTRY = MappingProxyType(_AYANAMSA_DATA)
HOUSE_SYSTEM_REGISTRY = MappingProxyType(_HOUSE_SYSTEM_DATA)
NODE_MODE_REGISTRY = MappingProxyType(_NODE_MODE_DATA)


# --- Public Resolvers ---

def _normalize_key(value: str) -> str:
    return str(value).strip().casefold().replace("-", "_").replace(" ", "_")


def list_ayanamsa_ids(*, implemented_only: bool = False) -> list[str]:
    """List known ayanamsa identifiers.

    Args:
        implemented_only: If True, return only implemented entries.

    Returns:
        Sorted unique list of ayanamsa IDs.

    Raises:
        None.

    Notes:
        - Thread-safety: Pure read-only lookup.
        - Determinism: Stable ordering for identical registry contents.
        - Contract: IDs are stable; changes require policy/version updates.

    Examples:
        >>> "lahiri" in list_ayanamsa_ids()
        True
    """
    ids = []
    for key, spec in AYANAMSA_REGISTRY.items():
        if implemented_only and spec.status != "implemented":
            continue
        ids.append(key)
    return sorted(set(ids))


def list_house_system_ids(*, implemented_only: bool = False) -> list[str]:
    """List known house system identifiers.

    Args:
        implemented_only: If True, return only implemented entries.

    Returns:
        Sorted unique list of house system IDs.

    Raises:
        None.

    Notes:
        - Thread-safety: Pure read-only lookup.
        - Determinism: Stable ordering for identical registry contents.
        - Contract: IDs are stable; changes require policy/version updates.

    Examples:
        >>> "whole_sign" in list_house_system_ids()
        True
    """
    ids = []
    for key, spec in HOUSE_SYSTEM_REGISTRY.items():
        if implemented_only and spec.status != "implemented":
            continue
        ids.append(key)
    return sorted(set(ids))


def list_node_mode_ids() -> list[str]:
    """List known node mode identifiers.

    Args:
        None.

    Returns:
        Sorted list of node mode IDs.

    Raises:
        None.

    Notes:
        - Thread-safety: Pure read-only lookup.
        - Determinism: Stable ordering for identical registry contents.
        - Contract: IDs are stable; changes require policy/version updates.

    Examples:
        >>> "mean" in list_node_mode_ids()
        True
    """
    return sorted(NODE_MODE_REGISTRY.keys())


def resolve_ayanamsa(mode: str, *, user_value: Optional[float] = None) -> AyanamsaSpec:
    """Resolve an ayanamsa identifier into a validated spec.

    Args:
        mode: Ayanamsa ID (case-insensitive).
        user_value: Required only for SIDM_USER entries.

    Returns:
        Resolved AyanamsaSpec.

    Raises:
        VedicRegistryError: If mode is empty, unknown, or not implemented.
        VedicRegistryError: If SIDM_USER is selected without user_value.

    Notes:
        - Thread-safety: Pure read-only lookup.
        - Determinism: Stable resolution for identical inputs.
        - Contract: Resolved IDs are stable; changes require policy updates.

    Examples:
        >>> resolve_ayanamsa("lahiri").id
        'lahiri'
    """
    if mode is None or not str(mode).strip():
        raise VedicRegistryError("Ayanamsa mode must be a non-empty string")

    key = _normalize_key(mode)
    spec = AYANAMSA_REGISTRY.get(key)

    if spec is None:
        raise VedicRegistryError(
            f"Invalid Ayanamsa mode: '{mode}'. Available: {list_ayanamsa_ids()}"
        )
    if spec.status != "implemented":
        raise VedicRegistryError(
            f"Ayanamsa '{mode}' is recognized but not implemented yet in Diba runtime."
        )
    if spec.requires_user_value and user_value is None:
        raise VedicRegistryError(
            f"Ayanamsa '{mode}' requires a user-provided ayanamsa value (SIDM_USER)."
        )
    return spec


def resolve_house_system(sys_id: str) -> HouseSystemSpec:
    """Resolve a house system identifier into a validated spec.

    Args:
        sys_id: House system ID (case-insensitive).

    Returns:
        Resolved HouseSystemSpec.

    Raises:
        VedicRegistryError: If sys_id is empty, unknown, or not implemented.

    Notes:
        - Thread-safety: Pure read-only lookup.
        - Determinism: Stable resolution for identical inputs.
        - Contract: Resolved IDs are stable; changes require policy updates.

    Examples:
        >>> resolve_house_system("whole_sign").id
        'whole_sign'
    """
    if sys_id is None or not str(sys_id).strip():
        raise VedicRegistryError("House system must be a non-empty string")

    key = _normalize_key(sys_id)
    spec = HOUSE_SYSTEM_REGISTRY.get(key)

    if spec is None:
        raise VedicRegistryError(
            f"Invalid House System: '{sys_id}'. Available: {list_house_system_ids()}"
        )
    if spec.status != "implemented":
        raise VedicRegistryError(
            f"House system '{sys_id}' is recognized but not implemented yet in Diba runtime."
        )
    _validate_house_spec(spec)
    return spec


def resolve_node_mode(node_mode: str) -> NodeModeSpec:
    """Resolve a node mode identifier into a validated spec.

    Args:
        node_mode: Node mode ID (case-insensitive).

    Returns:
        Resolved NodePolicySpec.

    Raises:
        VedicRegistryError: If node_mode is empty, unknown, or not implemented.

    Notes:
        - Thread-safety: Pure read-only lookup.
        - Determinism: Stable resolution for identical inputs.
        - Contract: Resolved IDs are stable; changes require policy updates.

    Examples:
        >>> resolve_node_mode("mean").id
        'mean'
    """
    if node_mode is None or not str(node_mode).strip():
        raise VedicRegistryError("node_mode must be a non-empty string.")
    key = _normalize_key(node_mode)
    spec = NODE_MODE_REGISTRY.get(key)
    if spec is None:
        raise VedicRegistryError(
            f"node_mode must be one of: {', '.join(list_node_mode_ids())}."
        )
    if spec.status != "implemented":
        raise VedicRegistryError(
            f"Node mode '{node_mode}' is recognized but not implemented yet in Diba runtime."
        )
    return spec
