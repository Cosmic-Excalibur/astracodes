from sage.all import GaussianIntegers, factor, ZZ
from astrautils.factorization import *
from itertools import product

'''
use ```python
from sympy.solvers.diophantine import diophantine
from sympy import symbols
x, y = symbols("x, y", integer=True)
diophantine(x**2 + y**2 - n0, syms=(x, y))
``` instead, unless the complicated factorization of `n` is known.
'''
def two_squares(n, cached_factorization = None):
    GI = GaussianIntegers(); I = GI.gen(1)
    facs = factor(GI(n)) if cached_factorization is None else cached_factorization
    assert facs.value() == n
    cands = {}
    while len(facs):
        p = facs[0][0]
        p_ = p.conjugate()
        facs = gifacmul(facs,  p, -1)
        facs = gifacmul(facs, p_, -1)
        cands[p] = cands.get(p, 0) + 1
    for es in product(*(range(x+1) for x in cands.values())):
        yield tuple(map(ZZ, prod(p**i * p.conjugate()**(e-i) for p, i, e in zip(cands.keys(), es, cands.values()))))
        
    