from __future__ import annotations

import importlib
import os

import pytest

import diba.infra.io.ephemeris as ephemeris_module


def _reload_ephemeris_module():
    return importlib.reload(ephemeris_module)


def test_env_precedence_and_fail_fast(tmp_path):
    key = "DIBA_EPHE_PATH"
    old = os.environ.get(key)
    env_path = tmp_path / "env_ephe"
    env_path.mkdir()
    configured_path = tmp_path / "configured_ephe"
    configured_path.mkdir()

    mod = _reload_ephemeris_module()
    try:
        os.environ[key] = str(env_path)
        assert mod.resolve_ephemeris_path(cli_arg=str(configured_path), dev_mode=False) == str(env_path)

        os.environ[key] = str(tmp_path / "missing_env_ephe")
        with pytest.raises(RuntimeError, match="Invalid ephemeris path"):
            mod.resolve_ephemeris_path(cli_arg=str(configured_path), dev_mode=False)
    finally:
        if old is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = old


def test_reinit_idempotent_and_conflict(tmp_path):
    key = "DIBA_EPHE_PATH"
    old = os.environ.get(key)
    configured_path = tmp_path / "configured_ephe"
    configured_path.mkdir()

    mod = _reload_ephemeris_module()
    try:
        os.environ.pop(key, None)
        first = mod.initialize_ephemeris_runtime(
            config_digest="digest-A",
            ephe_expectations="de405/sepl_18",
            configured_path=str(configured_path),
            dev_mode=False,
        )
        second = mod.initialize_ephemeris_runtime(
            config_digest="digest-A",
            ephe_expectations="de405/sepl_18",
            configured_path=str(configured_path),
            dev_mode=False,
        )
        assert first == str(configured_path)
        assert second == str(configured_path)

        with pytest.raises(RuntimeError, match="policy conflict detected"):
            mod.initialize_ephemeris_runtime(
                config_digest="digest-B",
                ephe_expectations="de405/sepl_18",
                configured_path=str(configured_path),
                dev_mode=False,
            )
    finally:
        if old is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = old


def test_expectations_validation_surface(tmp_path):
    key = "DIBA_EPHE_PATH"
    old = os.environ.get(key)
    configured_path = tmp_path / "configured_ephe"
    configured_path.mkdir()

    try:
        os.environ.pop(key, None)

        mod = _reload_ephemeris_module()
        assert mod.initialize_ephemeris_runtime(
            config_digest="digest-A",
            ephe_expectations="de405/sepl_18",
            configured_path=str(configured_path),
            dev_mode=False,
        ) == str(configured_path)

        mod = _reload_ephemeris_module()
        with pytest.raises(RuntimeError, match="non-empty"):
            mod.initialize_ephemeris_runtime(
                config_digest="digest-A",
                ephe_expectations="",
                configured_path=str(configured_path),
                dev_mode=False,
            )

        mod = _reload_ephemeris_module()
        with pytest.raises(RuntimeError, match="provider and payload"):
            mod.initialize_ephemeris_runtime(
                config_digest="digest-A",
                ephe_expectations="unknown",
                configured_path=str(configured_path),
                dev_mode=False,
            )
    finally:
        if old is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = old
