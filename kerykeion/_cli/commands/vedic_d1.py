from typing import Any, Dict

from kerykeion._cli.errors import CLIError
from kerykeion._cli.options import (
    parse_ayanamsa_id,
    parse_house_system_id,
    parse_node_mode,
    parse_output_format,
    resolve_ephemeris_path,
    resolve_mode,
    validate_seconds,
)
from kerykeion._cli.prompting import prompt_choice, prompt_float, prompt_int, prompt_text
from kerykeion.vedic.factory import VedicFactoryError, VedicSubjectFactory
from kerykeion.vedic.registry import list_ayanamsa_ids, list_house_system_ids, list_node_mode_ids


def _interactive_fill(args) -> None:
    if args.name is None:
        args.name = prompt_text("Name")
    if args.year is None:
        args.year = prompt_int("Year")
    if args.month is None:
        args.month = prompt_int("Month")
    if args.day is None:
        args.day = prompt_int("Day")
    if args.hour is None:
        args.hour = prompt_int("Hour")
    if args.minute is None:
        args.minute = prompt_int("Minute")
    if args.tz_str is None:
        args.tz_str = prompt_text("Timezone (e.g., Europe/Paris)")
    if args.lat is None:
        args.lat = prompt_float("Latitude")
    if args.lng is None:
        args.lng = prompt_float("Longitude")
    if args.ayanamsa_id is None:
        args.ayanamsa_id = prompt_choice("Ayanamsa ID", list_ayanamsa_ids(), "lahiri")
    if args.node_mode is None:
        args.node_mode = prompt_choice("Node mode", list_node_mode_ids(), "mean")
    if args.house_system_id is None:
        args.house_system_id = prompt_choice("House system ID", list_house_system_ids(), "whole_sign")
    if args.format is None:
        args.format = prompt_choice("Output format", ["json", "pretty"], "pretty")


def _build_d1_output(model) -> Dict[str, Any]:
    core = model.core.objects
    asc_deg = float(core["ascendant"].abs_pos_sidereal)
    asc_sign = int(asc_deg // 30)

    planets = {}
    for name, point in core.items():
        if name == "ascendant":
            continue
        planets[name.upper()] = float(point.abs_pos_sidereal)

    return {
        "ayanamsa_deg": float(model.ayanamsa_deg),
        "asc_sidereal_deg": asc_deg,
        "asc_sidereal_sign": asc_sign,
        "planets_sidereal_deg": planets,
    }


def run_vedic_d1_command(args) -> Dict[str, Any]:
    online, _offline = resolve_mode(args)
    if online:
        raise CLIError("Online mode is not supported in Vedic-only CLI; provide tz/lat/lng.")

    if args.interactive:
        _interactive_fill(args)

    if args.tz_str is None or args.lat is None or args.lng is None:
        raise CLIError("tz_str, lat, and lng are required for Vedic calculations.")
    if None in {args.year, args.month, args.day, args.hour, args.minute}:
        raise CLIError("Date/time fields (year, month, day, hour, minute) are required.")

    second = validate_seconds(args.second)
    ayanamsa_id = parse_ayanamsa_id(args.ayanamsa_id)
    node_mode = parse_node_mode(args.node_mode)
    house_system_id = parse_house_system_id(args.house_system_id)
    parse_output_format(args.format)

    ephe_path = resolve_ephemeris_path(args.ephe_path, False)

    try:
        model = VedicSubjectFactory.from_birth_data(
            year=int(args.year),
            month=int(args.month),
            day=int(args.day),
            hour=int(args.hour),
            minute=int(args.minute),
            seconds=float(second),
            tz_str=args.tz_str,
            lat=float(args.lat),
            lon=float(args.lng),
            ayanamsa_id=ayanamsa_id,
            node_mode=node_mode,
            house_system_id=house_system_id,
            ephe_path=ephe_path,
        )
    except VedicFactoryError as exc:
        raise CLIError(str(exc)) from exc

    return _build_d1_output(model)
