from __future__ import annotations

import os

from diba.core.contracts import tolerance_profile


def test_tolerance_profile_uses_env_selector() -> None:
    key = "DIBA_TOL_PROFILE"
    old = os.environ.get(key)

    try:
        os.environ[key] = "golden"
        golden = tolerance_profile()
        assert golden.angle_deg == 1e-5
        assert golden.time_seconds == 30

        os.environ[key] = "ci"
        ci = tolerance_profile()
        assert ci.angle_deg == 1e-2
        assert ci.time_seconds == 60
    finally:
        if old is None:
            os.environ.pop(key, None)
        else:
            os.environ[key] = old
