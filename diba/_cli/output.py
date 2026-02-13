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


def render_pretty_bench(data: Dict) -> str:
    lines = [
        f"Benchmark: {data.get('benchmark')}",
        f"Samples: {data.get('sample_size')}",
        f"Profile: {data.get('tolerance_profile')}",
        f"Cache mode: {data.get('cache_mode')}",
        f"Ephemeris I/O: {data.get('ephemeris_io')}",
        f"CPU: {data.get('cpu_model')}",
        f"Machine: {data.get('machine')}",
        f"Median: {data.get('median_ms')} ms",
        f"P95: {data.get('p95_ms')} ms",
        f"Charts/sec: {data.get('charts_per_sec')}",
    ]
    return "\n".join(lines)
