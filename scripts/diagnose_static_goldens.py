#!/usr/bin/env python
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from kerykeion.vedic.static_chart import build_static_chart_v0_1

INPUT_DIR = Path("tests/golden_inputs")
OUTPUT_DIR = Path("tests/golden_outputs")

_POINT_DMS_RE = re.compile(r"^\s*(\d{1,2})°([A-Za-z]{2})(\d{2})'(\d{2}(?:\.\d+)?)\"\s*$")
_DMS_RE = re.compile(r"^\s*(\d{1,3})°(\d{2})'(\d{2}(?:\.\d+)?)\"\s*$")
_SIGN_INDEX = {
    "Ar": 0,
    "Ta": 1,
    "Ge": 2,
    "Cn": 3,
    "Le": 4,
    "Vi": 5,
    "Li": 6,
    "Sc": 7,
    "Sg": 8,
    "Cp": 9,
    "Aq": 10,
    "Pi": 11,
}


def _load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _parse_point_dms(value: str) -> float:
    m = _POINT_DMS_RE.match(str(value))
    if not m:
        raise ValueError(f"Invalid point DMS: {value}")
    deg_in_sign = int(m.group(1))
    sign = m.group(2)
    minutes = int(m.group(3))
    seconds = float(m.group(4))
    sign_index = _SIGN_INDEX[sign]
    return (sign_index * 30.0) + deg_in_sign + (minutes / 60.0) + (seconds / 3600.0)


def _parse_dms(value: str) -> float:
    m = _DMS_RE.match(str(value))
    if not m:
        raise ValueError(f"Invalid DMS: {value}")
    deg = int(m.group(1))
    minutes = int(m.group(2))
    seconds = float(m.group(3))
    return deg + (minutes / 60.0) + (seconds / 3600.0)


def _delta_arcsec(actual_deg: float, expected_deg: float) -> float:
    delta = (actual_deg - expected_deg + 540.0) % 360.0 - 180.0
    return delta * 3600.0


def _build_actual(input_data: dict) -> dict:
    settings_input = input_data.get("settings", {})
    timezone_input = input_data.get("timezone", {})
    location_input = input_data.get("location", {})

    settings = {
        "ayanamsa_mode": settings_input.get("ayanamsa_id", "lahiri"),
        "ayanamsa_source": "mode",
        "ayanamsa_override_deg": settings_input.get("ayanamsa_override_deg"),
        "node_policy": settings_input.get("node_policy", "mean"),
        "house_system": settings_input.get("house_system_id", "whole_sign"),
        "compat_mode": settings_input.get("compat_mode", "jhora_us"),
    }
    birth_data = {
        "id": input_data.get("id"),
        "datetime_local": input_data.get("datetime_local"),
        "datetime_utc": timezone_input.get("datetime_utc"),
        "timezone": timezone_input.get("iana"),
        "utc_offset": timezone_input.get("utc_offset"),
        "dst": timezone_input.get("dst_expected"),
    }
    place = {
        "name": location_input.get("name"),
        "lat": location_input.get("lat"),
        "lon": location_input.get("lon"),
        "alt_m": location_input.get("alt_m", 0.0),
    }
    return build_static_chart_v0_1(settings, birth_data, place, ephe_path=None)


def main() -> int:
    inputs = sorted(INPUT_DIR.glob("*.json"))
    if not inputs:
        print("No golden inputs found")
        return 1

    for input_path in inputs:
        input_data = _load_json(input_path)
        sid = input_data["id"]
        expected_path = OUTPUT_DIR / f"{sid}.static_chart.expected.json"
        expected = _load_json(expected_path)
        actual = _build_actual(input_data)

        print(f"=== {sid} ===")
        print(
            "meta.ayanamsa: "
            f"id actual={actual['meta']['ayanamsa_id']} expected={expected['meta']['ayanamsa_id']} | "
            f"dms actual={actual['meta']['ayanamsa_dms']} expected={expected['meta']['ayanamsa_dms']}"
        )

        for key in ("asc", "rahu", "ketu", "sun", "moon"):
            act_dms = actual["points"][key]["dms"]
            exp_dms = expected["points"][key]["dms"]
            act_deg = _parse_point_dms(act_dms)
            exp_deg = _parse_point_dms(exp_dms)
            delta = _delta_arcsec(act_deg, exp_deg)
            print(
                f"{key}: actual={act_dms} expected={exp_dms} delta_arcsec={delta:+.3f}"
            )
        print()

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
