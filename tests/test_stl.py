import stl


def test_smoke():
    spec = stl.parse("F{x**2 > 3}")
    assert spec({'x': [(0, 10), (4, 4)]}) == 97
 
    spec = stl.parse("(F{x**2 > 3} & G{2*y + x < 2})")
    data = {
        'x': [(0, 10), (2, 4)],
        'y': [(0, 2), (2, 0)],
    }
    assert spec(data) == -12

