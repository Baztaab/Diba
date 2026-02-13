from __future__ import annotations

import os
import tempfile

import pytest

from diba.infra.io.ephemeris import resolve_ephemeris_path


def test_ephemeris_env_path_must_exist_fail_fast():
    key = "DIBA_EPHE_PATH"
    old = os.environ.get(key)
    os.environ[key] = "X:/definitely/not/found"
    try:
        with pytest.raises(RuntimeError):
            resolve_ephemeris_path(cli_arg=None, dev_mode=False)
    finally:
        if old is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = old


def test_ephemeris_env_path_wins_when_valid():
    key = "DIBA_EPHE_PATH"
    old = os.environ.get(key)
    with tempfile.TemporaryDirectory() as tmpdir:
        os.environ[key] = tmpdir
        try:
            assert resolve_ephemeris_path(cli_arg=None, dev_mode=False) == tmpdir
        finally:
            if old is None:
                os.environ.pop(key, None)
            else:
                os.environ[key] = old
