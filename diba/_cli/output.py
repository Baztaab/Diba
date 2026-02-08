import json
from typing import Dict


def render_json(data: Dict) -> str:
    return json.dumps(data, indent=2, default=str)


def render_pretty_d1(data: Dict) -> str:
    planets = data.get("planets_sidereal_deg", {})
    lines = [
        f"Ayanamsa (deg): {data.get('ayanamsa_deg'):.6f}",
        f"Asc (sidereal): {data.get('asc_sidereal_deg'):.6f} deg, sign {data.get('asc_sidereal_sign')}",
        "Planets (sidereal):",
    ]
    for name, deg in planets.items():
        lines.append(f"  {name}: {deg:.6f} deg")
    return "\n".join(lines)
