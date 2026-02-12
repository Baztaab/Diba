from diba.core.angles import normalize360, split_rasi

EPS = 1e-12


def test_sign_boundaries():
    for k in range(12):
        base = 30.0 * k
        for x in (base, base + EPS, base - EPS):
            lon = normalize360(x)
            rasi, deg = split_rasi(lon)
            assert 0 <= rasi <= 11
            assert 0 <= deg < 30.0

    lon = normalize360(360.0)
    rasi, deg = split_rasi(lon)
    assert lon == 0.0
    assert (rasi, deg) == (0, 0.0)

