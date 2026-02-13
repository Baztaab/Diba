"""
Vedic runtime registry and policy resolvers.

Provides canonical IDs and validation for ayanamsa, house systems, and node
policies. This module contains no SwissEph calls and only exposes read-only
registry views plus resolver helpers.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from types import MappingProxyType
from typing import Literal, Optional

AyanamsaUnsupportedModePolicy = Literal["raise", "fallback_default"]
AyanamsaReasonCode = Literal["none", "invalid", "disabled", "recognized_not_implemented"]


class HouseFetchPlan(str, Enum):
    """Strategy for fetching house data from SwissEph."""

    ASC_ONLY = "asc_only"
    HOUSES_EX = "houses_ex"


SpecStatus = Literal["implemented", "recognized_not_implemented"]


@dataclass(frozen=True)
class AyanamsaSpec:
    """Resolved ayanamsa runtime definition."""

    id: str
    swe_mode: Optional[str]
    status: SpecStatus = "implemented"
    alias_of: Optional[str] = None
    # Documentation-only while SIDM_USER is disabled in canonical runtime.
    requires_user_value: bool = False
    # Documentation-only placeholder for future non-canonical paths.
    t0: Optional[float] = None


@dataclass(frozen=True)
class ResolveReport:
    """Structured resolution report for entrypoint-level audit logging."""

    reason_code: AyanamsaReasonCode
    input_id: str
    effective_id: str
    was_fallback: bool
    fallback_from: Optional[str] = None
    default_id_used: Optional[str] = None


@dataclass(frozen=True)
class HouseSystemSpec:
    id: str
    pyjhora_method: int
    status: SpecStatus = "implemented"
    fetch_plan: Optional[HouseFetchPlan] = None
    swe_hsys_code: Optional[str] = None
    label: Optional[str] = None


@dataclass(frozen=True)
class NodeModeSpec:
    id: str
    swe_node: str
    status: SpecStatus = "implemented"


class VedicRegistryError(ValueError):
    """Registry or policy resolution error."""


class AyanamsaResolutionError(VedicRegistryError):
    """Ayanamsa resolution error with stable reason code."""

    def __init__(self, message: str, *, reason_code: AyanamsaReasonCode, input_id: str) -> None:
        super().__init__(message)
        self.reason_code = reason_code
        self.input_id = input_id


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
    # Quarantined (disabled in canonical runtime).
    "sidm_user": AyanamsaSpec("sidm_user", "SIDM_USER", requires_user_value=True),
    # Recognized in PyJHora surface but non-SIDM computed paths.
    "senthil": AyanamsaSpec("senthil", None, status="recognized_not_implemented"),
    "sundar_ss": AyanamsaSpec("sundar_ss", None, status="recognized_not_implemented"),
}

_NON_SELECTABLE_IMPLEMENTED_AYANAMSA_IDS = frozenset({"sidm_user"})

_COMPAT_ALIAS_DATA = {
    "fagan_bradley": "fagan",
    "krishnamurti": "kp",
}

_HOUSE_SYSTEM_DATA = {
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
    "4": HouseSystemSpec(
        "placidus",
        pyjhora_method=4,
        fetch_plan=HouseFetchPlan.HOUSES_EX,
        swe_hsys_code="P",
        label="KP Method (aka Placidus Houses method)",
    ),
    "5": HouseSystemSpec(
        "whole_sign",
        pyjhora_method=5,
        fetch_plan=HouseFetchPlan.ASC_ONLY,
        label="Each Rasi is the house",
    ),
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


def _validate_ayanamsa_spec(spec: AyanamsaSpec) -> None:
    if spec.status == "implemented" and not spec.swe_mode:
        raise VedicRegistryError(f"AyanamsaSpec '{spec.id}' is implemented but missing swe_mode.")
    if spec.alias_of is not None and spec.alias_of == spec.id:
        raise VedicRegistryError(f"AyanamsaSpec '{spec.id}' cannot alias itself.")


def _validate_house_spec(spec: HouseSystemSpec) -> None:
    if spec.status == "implemented" and spec.fetch_plan is None:
        raise VedicRegistryError(f"HouseSystemSpec '{spec.id}' is implemented but missing fetch_plan.")
    if spec.fetch_plan == HouseFetchPlan.HOUSES_EX:
        if not spec.swe_hsys_code or len(spec.swe_hsys_code) != 1:
            raise VedicRegistryError(
                f"HouseSystemSpec '{spec.id}' requires a single-character swe_hsys_code when fetch_plan=HOUSES_EX."
            )


for _spec in _AYANAMSA_DATA.values():
    _validate_ayanamsa_spec(_spec)
for _spec in _HOUSE_SYSTEM_DATA.values():
    _validate_house_spec(_spec)


AYANAMSA_REGISTRY = MappingProxyType(_AYANAMSA_DATA)
HOUSE_SYSTEM_REGISTRY = MappingProxyType(_HOUSE_SYSTEM_DATA)
NODE_MODE_REGISTRY = MappingProxyType(_NODE_MODE_DATA)


def _normalize_key(value: str) -> str:
    """Canonical normalization: strip + casefold + hyphen/space to underscore."""
    return str(value).strip().casefold().replace("-", "_").replace(" ", "_")


def _build_ayanamsa_alias_map() -> dict[str, str]:
    alias_map: dict[str, str] = dict(_COMPAT_ALIAS_DATA)
    for key, spec in AYANAMSA_REGISTRY.items():
        if spec.alias_of:
            alias_map[key] = spec.alias_of

    for alias in list(alias_map):
        target = alias_map[alias]
        hop = 0
        while target in alias_map and hop < 8:
            next_target = alias_map[target]
            if next_target == target:
                break
            target = next_target
            hop += 1
        alias_map[alias] = target
    return alias_map


def canonicalize_ayanamsa_id(mode: str) -> str:
    """Normalize and canonicalize ayanamsa input ID (alias -> canonical ID)."""
    if mode is None or not str(mode).strip():
        raise AyanamsaResolutionError(
            "Ayanamsa mode must be a non-empty string.",
            reason_code="invalid",
            input_id=str(mode),
        )
    normalized = _normalize_key(mode)
    return _build_ayanamsa_alias_map().get(normalized, normalized)


def _is_selectable_ayanamsa(spec: AyanamsaSpec) -> bool:
    if spec.status != "implemented":
        return False
    if spec.id in _NON_SELECTABLE_IMPLEMENTED_AYANAMSA_IDS:
        return False
    if spec.alias_of is not None:
        return False
    return bool(spec.swe_mode)


def list_ayanamsa_ids(*, selectable_only: bool = True, include_aliases: bool = False) -> list[str]:
    """List ayanamsa IDs with deterministic order."""
    canonical_ids: set[str] = set()
    for key, spec in AYANAMSA_REGISTRY.items():
        if key != spec.id:
            continue
        if selectable_only and not _is_selectable_ayanamsa(spec):
            continue
        canonical_ids.add(spec.id)

    if not include_aliases:
        return sorted(canonical_ids)

    all_ids = set(canonical_ids)
    alias_map = _build_ayanamsa_alias_map()
    for alias_key, target_key in alias_map.items():
        if alias_key == target_key:
            continue
        if selectable_only and target_key not in canonical_ids:
            continue
        all_ids.add(alias_key)
    return sorted(all_ids)


def list_house_system_ids(*, implemented_only: bool = False) -> list[str]:
    """List known house system identifiers."""
    ids = []
    for key, spec in HOUSE_SYSTEM_REGISTRY.items():
        if implemented_only and spec.status != "implemented":
            continue
        ids.append(key)
    return sorted(set(ids))


def list_node_mode_ids() -> list[str]:
    """List known node mode identifiers."""
    return sorted(NODE_MODE_REGISTRY.keys())


def _raise_unsupported_ayanamsa(*, reason_code: AyanamsaReasonCode, input_id: str) -> None:
    available = ", ".join(list_ayanamsa_ids(selectable_only=True))
    if reason_code == "recognized_not_implemented":
        raise AyanamsaResolutionError(
            f"Ayanamsa '{input_id}' is recognized but not implemented in Diba runtime. "
            f"Use one of: {available}",
            reason_code=reason_code,
            input_id=input_id,
        )
    if reason_code == "disabled":
        raise AyanamsaResolutionError(
            f"Ayanamsa '{input_id}' is disabled in canonical runtime. "
            f"Use one of: {available}",
            reason_code=reason_code,
            input_id=input_id,
        )
    raise AyanamsaResolutionError(
        f"Invalid Ayanamsa mode: '{input_id}'. Available: {available}",
        reason_code="invalid",
        input_id=input_id,
    )


def resolve_ayanamsa(
    mode: str,
    *,
    user_value: Optional[float] = None,
    on_unsupported: AyanamsaUnsupportedModePolicy = "raise",
    default_id: str = "lahiri",
) -> tuple[AyanamsaSpec, ResolveReport]:
    """
    Resolve an ayanamsa identifier into a validated spec and structured report.

    Resolver is intentionally side-effect free and does not log.
    """
    input_id = "" if mode is None else str(mode)

    try:
        canonical_id = canonicalize_ayanamsa_id(mode)
    except AyanamsaResolutionError as exc:
        reason_code = exc.reason_code
    else:
        spec = AYANAMSA_REGISTRY.get(canonical_id)
        if spec is None:
            reason_code = "invalid"
        elif spec.status != "implemented":
            reason_code = "recognized_not_implemented"
        elif not _is_selectable_ayanamsa(spec):
            reason_code = "disabled"
        elif spec.requires_user_value and user_value is None:
            reason_code = "disabled"
        else:
            return spec, ResolveReport(
                reason_code="none",
                input_id=input_id,
                effective_id=spec.id,
                was_fallback=False,
            )

    if on_unsupported == "raise":
        _raise_unsupported_ayanamsa(reason_code=reason_code, input_id=input_id)

    default_spec, _ = resolve_ayanamsa(
        default_id,
        user_value=user_value,
        on_unsupported="raise",
        default_id=default_id,
    )
    return default_spec, ResolveReport(
        reason_code=reason_code,
        input_id=input_id,
        effective_id=default_spec.id,
        was_fallback=True,
        fallback_from=input_id,
        default_id_used=default_spec.id,
    )


def resolve_house_system(sys_id: str) -> HouseSystemSpec:
    """Resolve a house system identifier into a validated spec."""
    if sys_id is None or not str(sys_id).strip():
        raise VedicRegistryError("House system must be a non-empty string")

    key = _normalize_key(sys_id)
    spec = HOUSE_SYSTEM_REGISTRY.get(key)

    if spec is None:
        raise VedicRegistryError(f"Invalid House System: '{sys_id}'. Available: {list_house_system_ids()}")
    if spec.status != "implemented":
        raise VedicRegistryError(
            f"House system '{sys_id}' is recognized but not implemented yet in Diba runtime."
        )
    _validate_house_spec(spec)
    return spec


def resolve_node_mode(node_mode: str) -> NodeModeSpec:
    """Resolve a node mode identifier into a validated spec."""
    if node_mode is None or not str(node_mode).strip():
        raise VedicRegistryError("node_mode must be a non-empty string.")
    key = _normalize_key(node_mode)
    spec = NODE_MODE_REGISTRY.get(key)
    if spec is None:
        raise VedicRegistryError(f"node_mode must be one of: {', '.join(list_node_mode_ids())}.")
    if spec.status != "implemented":
        raise VedicRegistryError(
            f"Node mode '{node_mode}' is recognized but not implemented yet in Diba runtime."
        )
    return spec
