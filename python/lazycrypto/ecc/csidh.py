from sage.all import primes, prod, GF, EllipticCurve, pari, factor
from Crypto.Util.number import isPrime

ells_200_269 = [*primes(3, 200), 269]
p_200_269 = 4*prod(ells_200_269) - 1

ells_128_163 = [*primes(3, 128), 163]
p_128_163 = 4*prod(ells_128_163) - 1

class CSIDH:
    def __init__(self, p, sanity_check = True):
        if hasattr(p, '__int__'):
            p = int(p)
            self.p = p
            self.ells = []
            if sanity_check:
                if p < 0 or (p + 1) % 4 or not isPrime(p):
                    raise ValueError("Malformed p for CSIDH.")
            for pp, ee in factor((p + 1) // 4):
                if ee > 1:
                    raise ValueError("Factor %s has exponent %s > 1" % (pp, ee))
                self.ells.append(pp)
        else:
            self.ells = list(p)
            self.p = 4*prod(self.ells) - 1
            if sanity_check:
                if any(not isPrime(l) for l in self.ells) or not isPrime(self.p):
                    raise ValueError("Malformed p for CSIDH.")
        self.F = GF(self.p)
    def __str__(self):
        return f"CSIDH protocol over {self.F} with primes {', '.join(map(str, self.ells))}."
    def __repr__(self):
        return self.__str__()
    def encrypt(self, A, key):
        E = EllipticCurve(self.F, [0, A, 0, 1, 0])
        for sgn in (1, -1):
            for e, ell in zip(key, self.ells):
                for i in range(sgn * e):
                    while not (P := (self.p + 1) // ell * E.random_element()) or P.order() != ell:
                        pass
                    E = E.isogeny_codomain(P)
            E = E.quadratic_twist()
        return E.montgomery_model().a2()
    def decrypt(self, A, key):
        E = EllipticCurve(self.F, [0, A, 0, 1, 0])
        for sgn in (-1, 1):
            for e, ell in zip(key, self.ells):
                for i in range(sgn * e):
                    while not (P := (self.p + 1) // ell * E.random_element()) or P.order() != ell:
                        pass
                    E = E.isogeny_codomain(P)
            E = E.quadratic_twist()
        return E.montgomery_model().a2()
    def qfb(self, ell):
        return pari.Qfb(ell, 2, (self.p + 1) // ell)

# CSIDH_200_269 = CSIDH(ells_200_269)
# CSIDH_128_163 = CSIDH(ells_128_163)
