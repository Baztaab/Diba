"""Ephemeris path and lifecycle policy helpers."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

_ENV_EPHE = "DIBA_EPHE_PATH"
_ENV_ENVIRONMENT = "DIBA_ENV"
_MIN_EXPECTATION_TOKENS = 2

_EPHE_INIT_DIGEST: Optional[str] = None
_EPHE_INIT_DETAILS: Optional[tuple[Optional[str], str, str]] = None


def validate_ephemeris_path(path: str) -> None:
    """Validate that ephemeris path exists, is a directory, and is readable."""
    p = Path(path)
    if not p.exists() or not p.is_dir():
        raise RuntimeError(f"Invalid ephemeris path: {path}")
    if not os.access(p, os.R_OK):
        raise RuntimeError(f"Ephemeris path is not readable: {path}")


def _default_dev_cache_path() -> str:
    path = (Path.home() / ".diba" / "ephe").resolve()
    path.mkdir(parents=True, exist_ok=True)
    validate_ephemeris_path(str(path))
    return str(path)


def _packaged_ephemeris_path() -> Optional[str]:
    packaged = (Path(__file__).resolve().parents[2] / "sweph").resolve()
    if not packaged.exists():
        return None
    validate_ephemeris_path(str(packaged))
    return str(packaged)


def is_prod_environment() -> bool:
    """Return whether runtime environment is production-like."""
    env = os.getenv(_ENV_ENVIRONMENT, "dev").strip().lower()
    return env in {"prod", "production"}


def resolve_ephemeris_path(cli_arg: Optional[str] = None, *, dev_mode: bool = True) -> Optional[str]:
    """Resolve ephemeris path by deterministic precedence policy."""
    env_path = os.getenv(_ENV_EPHE)
    if env_path:
        validate_ephemeris_path(env_path)
        return env_path

    if cli_arg:
        validate_ephemeris_path(cli_arg)
        return cli_arg

    packaged_path = _packaged_ephemeris_path()
    if packaged_path:
        return packaged_path

    if not dev_mode or is_prod_environment():
        return None

    return _default_dev_cache_path()


def can_auto_download_ephemeris(*, dev_mode: bool, opt_in: bool) -> bool:
    """Return whether auto-download is allowed for this runtime."""
    return bool(dev_mode and not is_prod_environment() and opt_in)


def validate_ephe_expectations(ephe_expectations: str) -> str:
    """Validate expectations surface for runtime ephemeris policy."""
    if not isinstance(ephe_expectations, str):
        raise RuntimeError("ephe_expectations must be a string.")
    normalized = ephe_expectations.strip()
    if not normalized:
        raise RuntimeError("ephe_expectations must be non-empty.")

    tokens = [part for part in normalized.split("/") if part]
    if len(tokens) < _MIN_EXPECTATION_TOKENS:
        raise RuntimeError(
            "ephe_expectations must include provider and payload segments, e.g. 'de405/sepl_18'."
        )
    return normalized


def initialize_ephemeris_runtime(
    *,
    config_digest: str,
    ephe_expectations: str,
    configured_path: Optional[str] = None,
    dev_mode: bool = True,
) -> Optional[str]:
    """Initialize and lock process-level ephemeris runtime policy deterministically."""
    global _EPHE_INIT_DIGEST, _EPHE_INIT_DETAILS

    normalized_digest = str(config_digest).strip()
    if not normalized_digest:
        raise RuntimeError("config_digest must be a non-empty string.")

    normalized_expectations = validate_ephe_expectations(ephe_expectations)
    resolved_path = resolve_ephemeris_path(cli_arg=configured_path, dev_mode=dev_mode)
    init_details = (resolved_path, normalized_expectations, normalized_digest)

    if _EPHE_INIT_DETAILS is None:
        _EPHE_INIT_DIGEST = normalized_digest
        _EPHE_INIT_DETAILS = init_details
        return resolved_path

    if _EPHE_INIT_DETAILS == init_details:
        return resolved_path

    prev_path, prev_expectations, prev_digest = _EPHE_INIT_DETAILS
    raise RuntimeError(
        "Ephemeris runtime policy conflict detected in-process. "
        f"previous=(path={prev_path!r}, expectations={prev_expectations!r}, digest={prev_digest!r}) "
        f"new=(path={resolved_path!r}, expectations={normalized_expectations!r}, digest={normalized_digest!r})"
    )
