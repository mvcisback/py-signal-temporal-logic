import operator as op
import re
from functools import reduce
from dataclasses import dataclass
from uuid import uuid1

import mtl
import sympy
from mtl.evaluator import to_signal


# Match substrings surrounded by currly braces.
# For example: {foo} {bar} -> [foo, bar].
SIGNAL_RE = re.compile("\{([^\}\{]+)\}")

# Used to split signal predicates on the comparison.
# For example: x > y  -> [x, >, y].
EXPR_RE = re.compile("([^<>]+)([<>])([^<>]+)")


@dataclass(frozen=True)
class STL:
    mtl: mtl.ast.Node
    exprs: dict[str, sympy.core.expr.Expr]
 
    def __call__(self, data, *args, **kwargs):
        # Preprocess to discrete signals.
        signal = to_signal(data)

        # Add signals derived from STL expressions.
        for sig, expr in self.exprs.items():
            # Note: Need to copy dictionary since evalf edits it...
            signal |= signal.map(expr, tag=sig) 
        return self.mtl(signal, *args, **kwargs)


def parse_expr(expr_txt:str):
    subexprs = EXPR_RE.split(expr_txt)
    if len(subexprs) != 5:
        raise ValueError(f"Failed to seperate lhs and rhs in {expr_txt}.")
    _, lhs, op, rhs, _ = subexprs

    # Rewrite to canonical form: f(x) > 0.
    if op == '<':
        lhs, rhs = rhs, lhs

    expr_txt = f"({lhs}) - ({rhs})"
    expr = sympy.parse_expr(expr_txt)
    return lambda subs: expr.evalf(subs=dict(subs))


def parse(stl_txt:str):
    # 1. Replace STL Signals with MTL Signals.
    template, nexprs = SIGNAL_RE.subn('{}', stl_txt)
    fresh_names = [f"x{uuid1()}" for _ in range(nexprs)]
    mtl_txt = template.format(*fresh_names)
    mtl_spec = mtl.parse(mtl_txt)
    
    # 2. Create parser for each expression.
    exprs = SIGNAL_RE.findall(stl_txt)
    exprs = {n: parse_expr(e) for n, e in zip(fresh_names, exprs)}

    return STL(mtl=mtl_spec, exprs=exprs)
