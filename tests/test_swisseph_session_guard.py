import pytest

from diba.infra.swisseph import swe
from diba.infra.swisseph.session import SwissEphSession, set_sid_mode


def test_state_setter_requires_active_session():
    with pytest.raises(RuntimeError):
        set_sid_mode(swe.SIDM_LAHIRI, 0.0, 0.0)


def test_state_setter_allows_calls_inside_session():
    with SwissEphSession():
        set_sid_mode(swe.SIDM_LAHIRI, 0.0, 0.0)
