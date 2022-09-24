import stl


def test_smoke():
    spec = stl.parse("F{x**2 > 3}")
    assert spec({'x': [(0, 10), (4, 4)]}) == 97

