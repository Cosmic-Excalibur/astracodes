from sage.all import prod, Factorization
from astrautils.filter import proj0

def fac_prod(facs):
    return prod(pp**ee for pp, ee in facs)

facprod = factor_product = fac_prod

def gi_fac_mul(facs: Factorization, p, e = 1):
    GI = facs.universe(); I = GI.gen()
    *ps, = map(proj0, facs)
    for i in (1, -1, I, -I):
        p_i = p*i
        if p_i in ps:
            facs *= Factorization([(p_i, e)], unit = i**-1)
            break
    else:
        raise ValueError("Bad p.")
    return facs

gifacmul = gi_fac_mul
