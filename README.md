# py-signal-temporal-logic
Wrapper on
[metric-temporal-logic](https://github.com/mvcisback/py-metric-temporal-logic)
to implement signal temporal logic.

# Installation

If you just need to use `py-signal-temporal-logic`, you can just run:

`$ pip install py-signal-temporal-logic`

For developers, note that this project uses the
[poetry](https://poetry.eustace.io/) python package/dependency
management tool. Please familarize yourself with it and then
run:

`$ poetry install`

# Usage

The `py-signal-temporal-logic` api is centered around the `parse` function. 

**Example Usage:**
```python
import stl

spec = stl.parse("(F{x**2 > 3} & G{2*y + x < 2})")
data = {
  'x': [(0, 10), (2, 4)],
  'y': [(0, 2), (2, 0)],
}
assert spec(data) == -12
```

This works by interpreting anything between curly braces { } as a
[sympy](https://www.sympy.org/en/index.html) expression.
