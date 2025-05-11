# weil pairing implemented for fun
# refer to EllipticCurvePoint.weil_pairing, EllipticCurvePoint._miller_, EllipticCurvePoint._line_ for SageMath impls.

from sage.all import *

def _g_PQ(P, Q, X, Y):
    a1, a2, a3, a4, a6 = P.curve().a_invariants()
    if not P and not Q:
        return X.parent()(1)
    elif not P:
        return X + (-Q.x())
    elif not Q:
        return X + (-P.x())
    if Q == -P:
        x, y, _ = P
        return X + (-x)
    elif P == Q:
        x, y, _ = P
        if y == 0:
            return X + (-x)
        lam = (3*x**2 + 2*a2*x + a4 - a1*y) / (2*y + a1*x + a3)
        return -lam*X + Y + (-y + lam*x)
    else:
        x1, y1, _ = P
        x2, y2, _ = Q
        lam = (y2-y1) / (x2-x1)
        return -lam*X + Y + (-y1 + lam*x1)

def g_PQ(P, Q, DR):
    X, Y = P.base_ring()['X,Y'].fraction_field().gens()
    pol = _g_PQ(P, Q, X, Y)
    return prod(pol(R.xy())**e for e, R in DR)

def toy_miller_algorithm(P, R, DQ, l):
    V = P
    f1 = g_PQ(P+R, -(P+R), DQ) / g_PQ(P, R, DQ)
    f = f1
    bins = bin(l)[3:]
    for i, b in enumerate(map(int, bins)):
        f = f**2 * g_PQ(V, V, DQ) / g_PQ(2*V, -2*V, DQ)
        V = 2*V
        if b:
            f = f * f1 * g_PQ(V, P, DQ) / g_PQ(V+P, -(V+P), DQ)
            V = V + P
    return f

def toy_pairing(P, Q, l):
    E = P.curve()
    if not P or not Q:
        return P.base_ring().one()
    while 1:
        S = E.random_element()
        T = E.random_element()
        A, B, C, D = S+Q, S, T+P, T
        if len(set([A, B, C, D, E(0)])) == 5:
            break
    return (-1)**l * toy_miller_algorithm(P, T, ((1, B), (-1, A)), l) * toy_miller_algorithm(Q, S, ((1, C), (-1, D)), l)    # should be 1 if ZeroDivisionError
