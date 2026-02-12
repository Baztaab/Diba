import pytest

from diba.core.indexing import rasi0_to_rasi1, rasi1_to_rasi0


def test_rasi_roundtrip():
    for index0 in range(12):
        assert rasi1_to_rasi0(rasi0_to_rasi1(index0)) == index0


@pytest.mark.parametrize("bad", [-1, 12, 999])
def test_rasi0_invalid(bad):
    with pytest.raises(ValueError):
        rasi0_to_rasi1(bad)


@pytest.mark.parametrize("bad", [0, 13, -5])
def test_rasi1_invalid(bad):
    with pytest.raises(ValueError):
        rasi1_to_rasi0(bad)

