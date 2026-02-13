import argparse
import logging
from enum import Enum
from typing import Optional

from diba._cli.errors import ValidationError
from diba.core.contracts import DEFAULT_AYANAMSA_ID
from diba.infra.io.ephemeris import resolve_ephemeris_path as _resolve_ephemeris_path
from diba.vedic.registry import (
    AyanamsaSpec,
    VedicRegistryError,
    list_ayanamsa_ids,
    list_house_system_ids,
    list_node_mode_ids,
    resolve_ayanamsa,
    resolve_house_system,
    resolve_node_mode,
)

_LOG = logging.getLogger(__name__)


class OutputFormat(str, Enum):
    JSON = "json"
    PRETTY = "pretty"


def validate_seconds(value: Optional[int]) -> int:
    if value is None:
        return 0
    if 0 <= value < 60:
        return value
    raise ValidationError("Seconds must be between 0 and 59.")


def parse_is_dst(value: Optional[str]) -> Optional[bool]:
    if value is None:
        return None
    lowered = str(value).lower()
    if lowered in {"true", "1", "yes", "y"}:
        return True
    if lowered in {"false", "0", "no", "n"}:
        return False
    raise ValidationError("is_dst must be true/false.")


def parse_ayanamsa_spec(
    name: str,
    *,
    on_unsupported: str = "raise",
    default_id: str = DEFAULT_AYANAMSA_ID,
) -> AyanamsaSpec:
    try:
        spec, report = resolve_ayanamsa(
            name,
            on_unsupported=on_unsupported,
            default_id=default_id,
        )
        if report.was_fallback:
            _LOG.warning(
                "Ayanamsa fallback applied in CLI parse: reason_code=%s input_id=%s fallback_id=%s",
                report.reason_code,
                report.input_id,
                report.effective_id,
            )
        return spec
    except VedicRegistryError as exc:
        raise ValidationError(str(exc)) from exc


def parse_ayanamsa_id(
    name: str,
    *,
    on_unsupported: str = "raise",
    default_id: str = DEFAULT_AYANAMSA_ID,
) -> str:
    return parse_ayanamsa_spec(name, on_unsupported=on_unsupported, default_id=default_id).id


def parse_node_mode(name: str) -> str:
    try:
        return resolve_node_mode(name).id
    except VedicRegistryError as exc:
        raise ValidationError(str(exc)) from exc


def parse_house_system_id(name: str) -> str:
    try:
        return resolve_house_system(name).id
    except VedicRegistryError as exc:
        raise ValidationError(str(exc)) from exc


def parse_output_format(name: str) -> OutputFormat:
    key = name.lower()
    if key == "json":
        return OutputFormat.JSON
    if key == "pretty":
        return OutputFormat.PRETTY
    raise ValidationError(f"Unsupported format '{name}'.")


def validate_offline_requires(offline: bool, tz_str: Optional[str], lat: Optional[float], lng: Optional[float]) -> None:
    if offline and (tz_str is None or lat is None or lng is None):
        raise ValidationError("Offline mode requires tz_str, lat, and lng.")


def validate_online_requires(online: bool, interactive: bool, city: Optional[str], nation: Optional[str]) -> None:
    if online and not interactive and (city is None or nation is None):
        raise ValidationError("Online mode requires city and nation (or use --interactive).")


def resolve_ephemeris_path(cli_arg: Optional[str], _offline: bool) -> Optional[str]:
    return _resolve_ephemeris_path(cli_arg=cli_arg, dev_mode=bool(_offline))


def resolve_mode(args) -> tuple[bool, bool]:
    if getattr(args, "online", False):
        return True, False
    if getattr(args, "offline", False):
        return False, True
    return False, True  # default offline (Vedic-only)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="diba", description="Diba CLI")
    subparsers = parser.add_subparsers(dest="command")

    vedic = subparsers.add_parser("vedic", help="Vedic tools")
    vedic_sub = vedic.add_subparsers(dest="vedic_command")

    d1 = vedic_sub.add_parser("d1", help="Compute Vedic D1 (whole sign) chart")
    d1.add_argument("--name")
    d1.add_argument("--year", type=int)
    d1.add_argument("--month", type=int)
    d1.add_argument("--day", type=int)
    d1.add_argument("--hour", type=int)
    d1.add_argument("--minute", type=int)
    d1.add_argument("--second", type=int)
    d1.add_argument("--city")
    d1.add_argument("--nation")
    d1.add_argument("--lat", type=float)
    d1.add_argument("--lng", type=float)
    d1.add_argument("--tz-str")
    d1.add_argument("--is-dst")
    group = d1.add_mutually_exclusive_group(required=False)
    group.add_argument("--online", action="store_true", help="Use online lookup")
    group.add_argument("--offline", action="store_true", help="Use offline data")
    d1.add_argument("--ayanamsa-id", choices=list_ayanamsa_ids(selectable_only=True), default="lahiri")
    d1.add_argument("--node-mode", choices=list_node_mode_ids(), default="mean")
    d1.add_argument("--house-system-id", choices=list_house_system_ids(), default="whole_sign")
    d1.add_argument("--format", default="pretty")
    d1.add_argument("--interactive", action="store_true", help="Prompt for missing values")
    d1.add_argument("--ephe-path", help="Set Swiss Ephemeris path")

    bench = subparsers.add_parser("bench", help="Benchmark tools")
    bench_sub = bench.add_subparsers(dest="bench_command")
    state_base = bench_sub.add_parser("state-base", help="Benchmark base state orchestration")
    state_base.add_argument("--n", type=int, default=1000, help="Number of benchmark iterations")
    state_base.add_argument("--tol-profile", choices=["ci", "golden"], help="Tolerance profile label in output")
    state_base.add_argument("--warm-cache", action="store_true", help="Run one warm-up compute before timing")
    state_base.add_argument("--include-ephe-io", action="store_true", help="Include ephemeris init in timing")
    state_base.add_argument("--ephe-path", help="Set Swiss Ephemeris path")
    state_base.add_argument("--format", default="json")

    return parser
