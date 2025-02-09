from sage.all import PolynomialRing

def prgen(base_ring, names = 'x', i = 0):
    PR = PolynomialRing(base_ring, names = names)
    return PR, PR.gen(i)

def prgens(base_ring, names = 'x'):
    PR = PolynomialRing(base_ring, names = names)
    return PR, PR.gens()
