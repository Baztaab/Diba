"""Ephemeris path and lifecycle policy helpers."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

_ENV_EPHE = "DIBA_EPHE_PATH"
_ENV_ENVIRONMENT = "DIBA_ENV"


def validate_ephemeris_path(path: str) -> None:
    p = Path(path)
    if not p.exists() or not p.is_dir():
        raise RuntimeError(f"Invalid ephemeris path: {path}")


def _default_dev_cache_path() -> str:
    return str((Path.home() / ".diba" / "ephe").resolve())


def is_prod_environment() -> bool:
    env = os.getenv(_ENV_ENVIRONMENT, "dev").strip().lower()
    return env in {"prod", "production"}


def resolve_ephemeris_path(cli_arg: Optional[str] = None, *, dev_mode: bool = True) -> Optional[str]:
    env_path = os.getenv(_ENV_EPHE)
    if env_path:
        validate_ephemeris_path(env_path)
        return env_path

    if cli_arg:
        validate_ephemeris_path(cli_arg)
        return cli_arg

    if not dev_mode or is_prod_environment():
        return None

    return _default_dev_cache_path()


def can_auto_download_ephemeris(*, dev_mode: bool, opt_in: bool) -> bool:
    return bool(dev_mode and not is_prod_environment() and opt_in)
