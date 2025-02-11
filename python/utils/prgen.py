from sage.all import PolynomialRing
import sys

def prgen(base_ring, names = 'x', i = 0):
    PR = PolynomialRing(base_ring, names = names)
    x = PR.gen(i)
    sys._getframe(1).f_globals.update({str(x): x})
    return PR, x

def prgens(base_ring, names = 'x'):
    PR = PolynomialRing(base_ring, names = names)
    xs = PR.gens()
    frame = sys._getframe(1)
    for x in xs:
        frame.f_globals.update({str(x): x})
    return PR, xs
