"""
VedicCalculationContext (Commit B)
Canonical SwissEph computation path aligned to PyJHora.
"""

from __future__ import annotations

from dataclasses import dataclass
from threading import RLock
from typing import Optional, Dict, Any

import swisseph as swe

from kerykeion.vedic.registry import AyanamsaSpec, HouseSystemSpec, HouseFetchPlan, VedicRegistryError

_SWE_LOCK = RLock()

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

BASELINE_SID_MODE = swe.SIDM_LAHIRI


def _norm360(x: float) -> float:
    return x % 360.0


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
    jd_utc: float
    lat: float
    lon: float
    altitude: float = 0.0
    ephe_path: Optional[str] = None
    ayanamsa: AyanamsaSpec = AyanamsaSpec("lahiri", swe.SIDM_LAHIRI)
    house_system: HouseSystemSpec = HouseSystemSpec("whole_sign", fetch_plan=HouseFetchPlan.ASC_ONLY)
    include_outer: bool = False

    def compute_core(self) -> Dict[str, Any]:
        if self.ayanamsa.swe_mode == swe.SIDM_USER:
            raise VedicRegistryError("SIDM_USER is not supported in Commit B canonical context.")

        planets = dict(_CLASSIC_PLANETS)
        if self.include_outer:
            planets.update(_OUTER_PLANETS)

        results: Dict[str, Any] = {
            "ayanamsa_mode": self.ayanamsa.id,
            "jd_utc": float(self.jd_utc),
            "flags": {
                "planet_flags": int(PLANET_FLAGS),
                "asc_flags": int(ASC_FLAGS),
                "hsys": ASC_HSYS.decode("ascii"),
            },
            "planets": {},
            "nodes": {},
            "ascendant": {},
        }

        with _SWE_LOCK:
            if self.ephe_path:
                swe.set_ephe_path(self.ephe_path)

            swe.set_sid_mode(self.ayanamsa.swe_mode, 0.0, 0.0)

            try:
                # Planets
                for name, pid in planets.items():
                    xx, retflag = swe.calc_ut(self.jd_utc, pid, flags=PLANET_FLAGS)
                    lon = _norm360(float(xx[0]))
                    speed = float(xx[3])
                    results["planets"][name] = {
                        "longitude": lon,
                        "speed_long": speed,
                        "is_retrograde": speed < 0.0,
                        "retflag": int(retflag),
                    }

                # Nodes (Rahu/Ketu)
                rahu_xx, rahu_ret = swe.calc_ut(self.jd_utc, swe.MEAN_NODE, flags=PLANET_FLAGS)
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
                _, ascmc = swe.houses_ex(self.jd_utc, self.lat, self.lon, ASC_HSYS, flags=ASC_FLAGS)
                asc_lon = _norm360(float(ascmc[0]))
                results["ascendant"]["longitude"] = asc_lon
            finally:
                swe.set_sid_mode(BASELINE_SID_MODE, 0.0, 0.0)

        return results
