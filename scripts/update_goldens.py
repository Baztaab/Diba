#!/usr/bin/env python
"""
Update golden outputs for static chart snapshots.
"""
from __future__ import annotations

import json
import sys
import argparse
from pathlib import Path
from difflib import unified_diff

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from diba.vedic.static_chart import build_static_chart_v0_1

INPUT_DIR = Path("tests/golden_inputs")
OUTPUT_DIR = Path("tests/golden_outputs")


def _canonicalize_json(value):
    if isinstance(value, dict):
        return {k: _canonicalize_json(value[k]) for k in sorted(value.keys())}
    if isinstance(value, list):
        return [_canonicalize_json(item) for item in value]
    return value


def _canonical_json_text(value: dict) -> str:
    return json.dumps(_canonicalize_json(value), indent=2, sort_keys=True) + "\n"


def _unified_json_diff(expected: dict, actual: dict, *, expected_name: str, actual_name: str) -> str:
    expected_text = _canonical_json_text(expected).splitlines(keepends=True)
    actual_text = _canonical_json_text(actual).splitlines(keepends=True)
    return "".join(unified_diff(expected_text, actual_text, fromfile=expected_name, tofile=actual_name))


def generate_static_chart(input_data: dict) -> dict:
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


def _write_json(path: Path, data: dict) -> None:
    path.write_text(_canonical_json_text(data), encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Update static chart golden snapshots.")
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write generated outputs to tests/golden_outputs.",
    )
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit with non-zero status if any expected output differs from generated output.",
    )
    args = parser.parse_args(argv)

    inputs = sorted(INPUT_DIR.glob("*.json"))
    if not inputs:
        print("No golden inputs found", file=sys.stderr)
        return 1

    has_diff = False
    for input_path in inputs:
        input_data = json.loads(input_path.read_text(encoding="utf-8"))
        scenario_id = input_data.get("id")
        if not scenario_id:
            print(f"Missing id in {input_path}", file=sys.stderr)
            return 1

        output = generate_static_chart(input_data)
        output_canon = _canonicalize_json(output)

        output_path = OUTPUT_DIR / f"{scenario_id}.static_chart.expected.json"
        if args.write:
            _write_json(output_path, output_canon)
            print(f"Wrote {output_path}")
        else:
            if output_path.exists():
                expected = json.loads(output_path.read_text(encoding="utf-8"))
                expected_canon = _canonicalize_json(expected)
                if expected_canon != output_canon:
                    has_diff = True
                    diff = _unified_json_diff(
                        expected_canon,
                        output_canon,
                        expected_name=str(output_path),
                        actual_name=f"{scenario_id}.generated",
                    )
                    print(f"Diff for {scenario_id}:\n{diff}")
                else:
                    print(f"{scenario_id}: no diff")
            else:
                has_diff = True
                print(f"{scenario_id}: expected output missing at {output_path}")

    if args.check and has_diff:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
