from sage.all import ZZ, QQ, polygens, Sequence, Polynomial, prod, vector
from lazycrypto.lattice.lll_cvp import reduction
import itertools

def small_roots(f, bounds, m=1, d=None):
    if not d:
        d = f.degree()

    if isinstance(f, Polynomial):
        x, = polygens(f.base_ring(), f.variable_name(), 1)
        f = f(x)

    R = f.base_ring()
    N = R.cardinality()
    
    f /= f.coefficients().pop(0)
    f = f.change_ring(ZZ)

    G = Sequence([], f.parent())
    for i in range(m+1):
        base = N**(m-i) * f**i
        for shifts in itertools.product(range(d), repeat=f.nvariables()):
            g = base * prod(map(pow, f.variables(), shifts))
            G.append(g)

    B, monomials = G.coefficient_matrix()
    monomials = vector(monomials)

    factors = [monomial(*bounds) for monomial in monomials]
    for i, factor in enumerate(factors):
        B.rescale_col(i, factor)

    B = reduction(B.dense_matrix())

    B = B.change_ring(QQ)
    for i, factor in enumerate(factors):
        B.rescale_col(i, QQ(1)/factor)

    H = Sequence([], f.parent().change_ring(QQ))
    for h in filter(None, B*monomials):
        H.append(h)
        I = H.ideal()
        if I.dimension() == -1:
            H.pop()
        elif I.dimension() == 0:
            roots = []
            for root in I.variety(ring=ZZ):
                root = tuple(R(root[var]) for var in f.variables())
                roots.append(root)
            return roots

    return []