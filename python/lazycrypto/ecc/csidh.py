from sage.all import primes, prod, GF, EllipticCurve, pari, factor
from Crypto.Util.number import isPrime
from lazymath.graycode import gray_code_int
from utils.filter import filter_digits
from collections import namedtuple
import os, pickle

ells_374_587 = [*primes(3, 374), 587]
p_374_587    = 4*prod(ells_374_587) - 1

ells_200_269 = [*primes(3, 200), 269]
p_200_269    = 4*prod(ells_200_269) - 1

ells_128_163 = [*primes(3, 128), 163]
p_128_163    = 4*prod(ells_128_163) - 1

ells_110_113 = [*primes(3, 110), 113]
p_110_113    = 4*prod(ells_110_113) - 1

ells_102_149 = [*primes(3, 102), 149]
p_102_149    = 4*prod(ells_102_149) - 1

ells_80_97   = [*primes(3,  80),  97]
p_80_97      = 4*prod(ells_80_97)   - 1

ells_42_61   = [*primes(3,  42),  61]
p_42_61      = 4*prod(ells_42_61)   - 1

ells_20_97   = [*primes(3,  20),  97]
p_20_97      = 4*prod(ells_20_97)   - 1

ells_14_17   = [*primes(3,  14),  17]
p_14_17      = 4*prod(ells_14_17)   - 1

ells_4_5     = [*primes(3,   4),   5]
p_4_5        = 4*prod(ells_4_5)     - 1

class CSIDH:
    def __init__(self, p, sanity_check = True, use_curve = False):
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
            self.ells = tuple(self.ells)
        else:
            self.ells = tuple(p)
            self.p = 4*prod(self.ells) - 1
            if sanity_check:
                if any(not isPrime(l) for l in self.ells) or not isPrime(self.p):
                    raise ValueError("Malformed p for CSIDH.")
        self.F = GF(self.p)
        self._use_curve = use_curve
        self.base = EllipticCurve(self.F, [0, 0, 0, 1, 0])
    def __str__(self):
        return f"CSIDH protocol over {self.F} with primes {', '.join(map(str, self.ells))}."
    def __repr__(self):
        return self.__str__()
    def encrypt(self, A, key, use_curve = None):
        _use_curve = self._use_curve if use_curve is None else use_curve
        E = A if _use_curve else EllipticCurve(self.F, [0, A, 0, 1, 0])
        for sgn in (1, -1):
            for e, ell in zip(key, self.ells):
                for i in range(sgn * e):
                    while not (P := (self.p + 1) // ell * E.random_element()) or P.order() != ell:
                        pass
                    E = E.isogeny_codomain(P)
            E = E.quadratic_twist()
        return E.montgomery_model() if _use_curve else int(E.montgomery_model().a2())
    def decrypt(self, A, key, use_curve = None):
        _use_curve = self._use_curve if use_curve is None else use_curve
        E = A if _use_curve else EllipticCurve(self.F, [0, A, 0, 1, 0])
        for sgn in (-1, 1):
            for e, ell in zip(key, self.ells):
                for i in range(sgn * e):
                    while not (P := (self.p + 1) // ell * E.random_element()) or P.order() != ell:
                        pass
                    E = E.isogeny_codomain(P)
            E = E.quadratic_twist()
        return E.montgomery_model() if _use_curve else int(E.montgomery_model().a2())
    def walk_one(self, A, elkies, stride, use_curve = None):
        _use_curve = self._use_curve if use_curve is None else use_curve
        E = A if _use_curve else EllipticCurve(self.F, [0, A, 0, 1, 0])
        if stride < 0:
            E = E.quadratic_twist()
        for i in range(abs(stride)):
            while not (P := (self.p + 1) // elkies * E.random_element()) or P.order() != elkies:
                pass
            E = E.isogeny_codomain(P)
        if stride < 0:
            E = E.quadratic_twist()
        return E.montgomery_model() if _use_curve else int(E.montgomery_model().a2())
    def binwalk(self, A, walk1 = 0, walk2 = 1, exclude_indices = None, exclude_ells = None, collector = None, use_curve = None, prog_tracker = None, compress_tuple = True):
        if exclude_indices is None and exclude_ells is None:
            exclude = ()
        elif exclude_indices is not None and exclude_ells is None:
            exclude = tuple(exclude_indices)
        elif exclude_indices is None and exclude_ells is not None:
            exclude = tuple(self.ells.index(ell) for ell in exclude_ells)
        else:
            raise ValueError("Ambiguous exclusion.")
        n = len(self.ells)
        victims = tuple(i for i in range(n) if i not in exclude)
        l = len(victims)
        table = {}
        def _default_collector(k, v):
            table[int(k)] = v
        if (collector_is_none := collector is None): collector = _default_collector
        if abs(walk1) < abs(walk2):
            first = walk1
            second = walk2 - walk1
        else:
            first = walk2
            second = walk1 - walk2
        key0 = tuple(first if i in victims else 0 for i in range(n))
        if not second:
            Anew = self.encrypt(A, key0)
            collector(Anew, 0 if compress_tuple else key0)
            return table if collector_is_none else None
        _use_curve = self._use_curve if use_curve is None else use_curve
        E = A if _use_curve else EllipticCurve(self.F, [0, A, 0, 1, 0])
        E = self.encrypt(E, key0, use_curve = True)
        if not compress_tuple:
            keynow = list(key0)
        last = None
        if prog_tracker is None:
            prog_tracker = lambda x, *args, **kwargs: x
        for i in prog_tracker(gray_code_int(l), total = 2**l):
            if last is None:
                assert not i
                last = 0
                collector(E.a2(), 0 if compress_tuple else tuple(keynow))
            else:
                delta = last ^ i
                sign = (last & delta == 0) * 2 - 1
                last = i
                victim = victims[delta.bit_length() - 1]
                E = self.walk_one(E, self.ells[victim], second * sign, use_curve = True)
                if not compress_tuple:
                    keynow[victim] = walk1 if keynow[victim] == walk2 else walk2
                collector(E.a2(), i if compress_tuple else tuple(keynow))
        return table if collector_is_none else None
    def qfb(self, ell):
        return pari.Qfb(ell, 2, (self.p + 1) // ell)

_database_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'csidh_database')

def _to_filename(p):
    res = str(p)
    res = ''.join(filter_digits(res))
    res = res if len(res) <= 30 else res[:30] + '_'
    return f'csidh_{res}.pickle'

def load_csidh_data(p):
    path = os.path.join(_database_path, _to_filename(p))
    if not os.path.exists(path):
        return None
    data = pickle.load(open(path, "rb"))
    return namedtuple('CsidhData', data.keys())(*data.values())

def save_csidh_data(p, ells, class_number, conductor, dlogs, gen_ell, loops):
    # loops: non trivial $(e_1, ..., e_t)$ such that $\prod\limits_i l_i^{e_i} = (1)$.
    path = os.path.join(_database_path, _to_filename(p))
    data = {
        'p': int(p),
        'ells': tuple(ells),
        'class_number': int(class_number),
        'conductor': int(conductor),
        'dlogs': tuple(dlogs),
        'gen_ell': int(gen_ell),
        'loops': tuple(loops)
    }
    pickle.dump(data, open(path, "wb"))
