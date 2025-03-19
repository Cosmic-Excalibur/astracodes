from sage.all import matrix, vector, Zmod, ZZ, block_matrix, diagonal_matrix
from lazycrypto.lattice.lll_cvp import reduction
from logger.astra_logger import *
from astrautils.timeit import timeit

def random_lwe_uniform(nrows, ncols, p, Abits, xbits, ebits):
    Zp = Zmod(p)
    A = matrix(Zp, nrows, ncols, [randrange(2**Abits) for _ in range(nrows * ncols)])
    x = vector(randrange(2**xbits) for _ in range(ncols)).change_ring(Zp)
    e = vector(randrange(2**ebits) for _ in range(nrows)).change_ring(Zp)
    return (A, A * x + e), (x, e)

def err_oracle(v, ebits):
    return max([min(ZZ(x).nbits(), ZZ(-x).nbits()) for x in v]) <= ebits

def primal_attack(p, A, b, ebits):
    nrows, ncols = A.dimensions()
    L = block_matrix([
        [matrix(Zmod(p), A).T.echelon_form().change_ring(ZZ), 0],
        [matrix.zero(nrows - ncols, ncols).augment(matrix.identity(nrows - ncols) * p), 0],
        [matrix(ZZ, b), 1],
    ])
    bounds = [2**ebits] * nrows + [1]
    K = p**2
    P = diagonal_matrix([K // x for x in bounds])
    L *= P
    with timeit("lattice reduction"):
        L_ = reduction(L)
    L_ /= P
    g = (v[-1] * v for v in L_ if abs(v[-1]) == 1)
    flag = 1
    while True:
        try:
            e = vector(Zmod(p), next(g)[:-1])
            flag = 0
            yield e
        except StopIteration:
            if flag:
                debug("Failed to solve LWE :(")
            return
