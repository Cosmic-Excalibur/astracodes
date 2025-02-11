from lazycrypto.lattice.lll_cvp import reduction
from utils.prgen import prgen
from sage.all import ZZ, ceil, matrix
import logger.astra_logger as alg

def hl_bits_leakage(N, pbar, epsilon, beta):
    d = 1
    h = ceil(beta**2/epsilon/d)
    k = ceil(d*h/beta)
    X = ceil((N**(beta**2/d-epsilon)))
    P, x = prgen(ZZ)
    f = pbar + x
    L = matrix(ZZ, k + 1 , k + 1 )
    alg.debug(f'{alg.blue_("β = ")}{beta}', f'{alg.blue_("ε = ")}{epsilon}', f'{alg.blue_("Bound of x (%s bits): " % X.bit_length())}{X}')
    for i in range(h*d):
        for j, l in enumerate(f ** i):
            L[i, j] = N ** (h - i) * l * X ** j
    for i in range(k - h*d + 1 ):
        for j, l in enumerate(x ** i * f ** h):
            L[i + h*d, j] = l * X ** j
    L_ = reduction(L)
    g = sum(j * x ** i / X ** i for i, j in enumerate(L_[0]))
    roots = g.roots()
    p = 1
    if roots:
        p = roots[0][0] + pbar
    if p in (0, 1, N) or N % p:
        return None, None
    return int(p), int(N//p)

