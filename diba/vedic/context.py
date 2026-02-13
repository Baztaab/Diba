"""
Canonical SwissEph computation context for Vedic calculations.

Provides the single, canonical runtime path for SwissEph calls aligned to
PyJHora. This module owns lock boundaries and is the only location where
SwissEph global state is configured.

Public API:
- VedicCalculationContext

Notes:
- Thread-safety: All SwissEph calls occur under a module-level global lock.
- Determinism: Deterministic for identical inputs and ephemeris version.
- Contract: Returned core payload is internal and not a public JSON contract.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, Optional

from diba.core.contracts import DEFAULT_AYANAMSA_ID
from diba.infra.swisseph import adapter as swe_adapter
from diba.infra.swisseph import swe
from diba.infra.swisseph.session import (
    SwissEphSession,
    ensure_session_active,
    set_ephe_path,
    set_sid_mode,
)
from diba.vedic.registry import (
    AYANAMSA_REGISTRY,
    AyanamsaSpec,
    HouseFetchPlan,
    HouseSystemSpec,
    VedicRegistryError,
    resolve_node_mode,
)

# PyJHora-aligned flags for sidereal planet positions
PLANET_FLAGS = (
    swe.FLG_SWIEPH
    | swe.FLG_SIDEREAL
    | swe.FLG_TRUEPOS
    | swe.FLG_SPEED
    | swe.BIT_HINDU_RISING
)

ASC_FLAGS = swe.FLG_SIDEREAL
ASC_HSYS = b"P"  # Explicitly pin to SwissEph default (Placidus)

_BASELINE_AYANAMSA_SPEC = AYANAMSA_REGISTRY[DEFAULT_AYANAMSA_ID]
BASELINE_SID_MODE = getattr(swe, str(_BASELINE_AYANAMSA_SPEC.swe_mode))


def _norm360(x: float) -> float:
    return x % 360.0


def _sripati_madhya_from_kp(kp_cusps: list[float]) -> list[float]:
    """
    Replicates PyJHora drik.bhaava_madhya_sripathi() transformation.
    Input is expected as 12 cusp values from SwissEph.
    """
    bm = [float(x) % 360.0 for x in kp_cusps[:12]]
    anchors = [0, 3, 6, 9, 12]
    for b in anchors[1:]:
        ib = anchors.index(b)
        bi1 = anchors[ib - 1] % 12
        bi2 = anchors[ib] % 12
        b1 = bm[bi1]
        b2 = bm[bi2]
        if b2 < b1:
            b2 += 360.0
        bd = abs(b2 - b1) / 3.0
        bm[(bi1 + 1) % 12] = (bm[bi1 % 12] + bd) % 360.0
        bm[(bi2 - 1) % 12] = (bm[bi2 % 12] - bd) % 360.0
    return [x % 360.0 for x in bm]


def _build_house_triplets(
    *,
    method: int,
    asc_lon: float,
    asc_sign: int,
    asc_long_in_sign: float,
    kp_cusps: list[float],
) -> list[dict[str, float]]:
    triplets: list[dict[str, float]] = []
    if method == 1:
        bhava_mid = asc_lon
        for _ in range(12):
            start = _norm360(bhava_mid - 15.0)
            end = _norm360(bhava_mid + 15.0)
            triplets.append({"start": start, "cusp": _norm360(bhava_mid), "end": end})
            bhava_mid = _norm360(bhava_mid + 30.0)
        return triplets

    if method == 2:
        bhava_start = asc_lon
        for _ in range(12):
            cusp = _norm360(bhava_start + 15.0)
            end = _norm360(cusp + 15.0)
            triplets.append({"start": _norm360(bhava_start), "cusp": cusp, "end": end})
            bhava_start = _norm360(bhava_start + 30.0)
        return triplets

    if method == 3:
        bm = _sripati_madhya_from_kp(kp_cusps)
        bm_ext = bm + [bm[0]]
        for h in range(12):
            start = _norm360(bm_ext[h])
            cusp = _norm360(0.5 * (bm_ext[h] + bm_ext[h + 1]))
            end = _norm360(bm_ext[h + 1])
            triplets.append({"start": start, "cusp": cusp, "end": end})
        return triplets

    if method == 4:
        bm = [float(x) % 360.0 for x in kp_cusps[:12]]
        bm_ext = bm + [bm[0]]
        for h in range(12):
            bmh = bm_ext[h]
            bmh1 = bm_ext[h + 1]
            if bmh1 < bmh:
                bmh1 += 360.0
            start = _norm360(bmh)
            cusp = _norm360(0.5 * (bmh + bmh1))
            end = _norm360(bmh1)
            triplets.append({"start": start, "cusp": cusp, "end": end})
        return triplets

    if method == 5:
        for h in range(12):
            h1 = (h + asc_sign) % 12
            start = float(h1 * 30.0)
            cusp = _norm360(start + asc_long_in_sign)
            end = float(((h1 + 1) % 12) * 30.0)
            triplets.append({"start": _norm360(start), "cusp": cusp, "end": _norm360(end)})
        return triplets

    raise VedicRegistryError(f"Unsupported PyJHora house method: {method}")


_CLASSIC_PLANETS = {
    "sun": swe.SUN,
    "moon": swe.MOON,
    "mercury": swe.MERCURY,
    "venus": swe.VENUS,
    "mars": swe.MARS,
    "jupiter": swe.JUPITER,
    "saturn": swe.SATURN,
}

_OUTER_PLANETS = {
    "uranus": swe.URANUS,
    "neptune": swe.NEPTUNE,
    "pluto": swe.PLUTO,
}


@dataclass(frozen=True)
class VedicCalculationContext:
    """Immutable input bundle for canonical SwissEph execution.

    Args:
        jd_utc: Julian day in UTC.
        lat: Latitude in degrees.
        lon: Longitude in degrees.
        altitude: Altitude in meters (canonical mode expects 0.0).
        ephe_path: Optional path to SwissEph data files.
        ayanamsa: Resolved ayanamsa policy spec.
        house_system: Resolved house system policy spec.
        node_mode: Node policy ID.
        include_outer: Whether to include outer planets in core output.

    Returns:
        None.

    Raises:
        None.

    Notes:
        - Thread-safety: All SwissEph calls occur under a module-level global lock.
        - Determinism: Deterministic for identical inputs and ephemeris version.
        - Contract: Output from compute_core is internal, not a public contract.

    Examples:
        >>> context = VedicCalculationContext(jd_utc=2451545.0, lat=0.0, lon=0.0)
        >>> context.jd_utc
        2451545.0
    """
    jd_utc: float
    lat: float
    lon: float
    altitude: float = 0.0
    ephe_path: Optional[str] = None
    ayanamsa: AyanamsaSpec = AyanamsaSpec("lahiri", "SIDM_LAHIRI")
    house_system: HouseSystemSpec = HouseSystemSpec(
        "whole_sign", pyjhora_method=5, fetch_plan=HouseFetchPlan.ASC_ONLY
    )
    node_mode: str = "mean"
    include_outer: bool = False

    def compute_core(self, *, manage_session: bool = True) -> Dict[str, Any]:
        """Compute the canonical core payload using SwissEph.

        Produces raw planet, node, ascendant, and house data used by higher
        layers (builders/serializers). Output keys are intended for internal
        consumption only.

        Args:
            None.

        Returns:
            Core payload dict with positions, flags, and house triplets.

        Raises:
            VedicRegistryError: If unsupported policy values are detected.

        Notes:
            - Thread-safety: All SwissEph calls occur under a module-level global lock.
            - Determinism: Deterministic for identical inputs and ephemeris version.
            - Contract: Output structure is internal and may change without notice.

        Examples:
            >>> context = VedicCalculationContext(jd_utc=2451545.0, lat=0.0, lon=0.0)
            >>> core = context.compute_core()
            >>> \"planets\" in core
            True
        """
        if self.ayanamsa.swe_mode == "SIDM_USER":
            raise VedicRegistryError(
                "Ayanamsa 'sidm_user' is disabled in canonical runtime (reason_code=disabled)."
            )
        node_spec = resolve_node_mode(self.node_mode)

        planets = dict(_CLASSIC_PLANETS)
        if self.include_outer:
            planets.update(_OUTER_PLANETS)

        planet_flags = int(PLANET_FLAGS)
        asc_flags = int(ASC_FLAGS)
        asc_hsys = ASC_HSYS.decode("ascii")

        results: Dict[str, Any] = {
            "ayanamsa_id": self.ayanamsa.id,
            "jd_utc": float(self.jd_utc),
            "ayanamsa_deg": 0.0,
            "flags": {
                "planet_flags": planet_flags,
                "asc_flags": asc_flags,
                "hsys": asc_hsys,
            },
            "planets": {},
            "nodes": {},
            "ascendant": {},
        }

        def _compute_under_active_session() -> None:
            if self.ephe_path:
                set_ephe_path(self.ephe_path)

            swe_mode = getattr(swe, self.ayanamsa.swe_mode)
            set_sid_mode(swe_mode, 0.0, 0.0)

            try:
                ayan = swe_adapter.get_ayanamsa_ut(self.jd_utc)
                results["ayanamsa_deg"] = ayan

                # Planets
                for name, pid in planets.items():
                    xx, retflag = swe_adapter.calc_ut(self.jd_utc, pid, flags=planet_flags)
                    lon = _norm360(float(xx[0]))
                    speed = float(xx[3])
                    results["planets"][name] = {
                        "longitude": lon,
                        "speed_long": speed,
                        "is_retrograde": speed < 0.0,
                        "retflag": int(retflag),
                    }

                # Nodes (Rahu/Ketu)
                node_id = getattr(swe, node_spec.swe_node)
                rahu_xx, rahu_ret = swe_adapter.calc_ut(self.jd_utc, node_id, flags=planet_flags)
                rahu_lon = _norm360(float(rahu_xx[0]))
                rahu_speed = float(rahu_xx[3])
                ketu_lon = _norm360(rahu_lon + 180.0)
                results["nodes"]["rahu"] = {
                    "longitude": rahu_lon,
                    "speed_long": rahu_speed,
                    "is_retrograde": rahu_speed < 0.0,
                    "retflag": int(rahu_ret),
                }
                results["nodes"]["ketu"] = {
                    "longitude": ketu_lon,
                    "speed_long": rahu_speed,
                    "is_retrograde": rahu_speed < 0.0,
                    "retflag": int(rahu_ret),
                }

                # Ascendant
                hsys_code = (
                    self.house_system.swe_hsys_code.encode("ascii")
                    if self.house_system.swe_hsys_code
                    else ASC_HSYS
                )
                cusps, ascmc = swe_adapter.houses_ex(
                    self.jd_utc, self.lat, self.lon, hsys_code, flags=ASC_FLAGS
                )
                asc_lon = _norm360(float(ascmc[0]))
                kp_cusps = [_norm360(float(c)) for c in cusps]
                results["ascendant"]["longitude"] = asc_lon

                asc_sign = int(asc_lon // 30.0)
                asc_long_in_sign = asc_lon - (asc_sign * 30.0)
                triplets = _build_house_triplets(
                    method=int(self.house_system.pyjhora_method),
                    asc_lon=asc_lon,
                    asc_sign=asc_sign,
                    asc_long_in_sign=asc_long_in_sign,
                    kp_cusps=kp_cusps,
                )
                results["houses"] = {
                    "method": int(self.house_system.pyjhora_method),
                    "triplets": triplets,
                }
                if self.house_system.fetch_plan == HouseFetchPlan.HOUSES_EX:
                    results["ascendant"]["cusps"] = [t["cusp"] for t in triplets]
            finally:
                set_sid_mode(BASELINE_SID_MODE, 0.0, 0.0)

        if manage_session:
            with SwissEphSession():
                _compute_under_active_session()
        else:
            ensure_session_active()
            _compute_under_active_session()

        return results
