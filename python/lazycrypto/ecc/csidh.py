from sage.all import primes, prod, GF, EllipticCurve, pari, factor, ZZ, matrix, pari, sage, discrete_log
from Crypto.Util.number import isPrime
from lazymath.graycode import gray_code_int
from astrautils.filter import filter_digits, map_relu
from collections import namedtuple
from logger import astra_logger as alg
from astrautils.int import is_int_int
from lazycrypto.lattice.lll_cvp import reduction
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

def to_montgomery(E):
    F = E.base_ring().base_ring()
    return E.change_ring(F).montgomery_model().a2()

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
        self.F2 = GF(self.p**2)
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
    def encrypt2(self, A, key, use_curve = None):
        _use_curve = self._use_curve if use_curve is None else use_curve
        E = A if _use_curve else EllipticCurve(self.F, [0, A, 0, 1, 0])
        E = E.change_ring(self.F2)
        keys = list(e for l, e in zip(self.ells, key))
        keys = [list(map_relu(e*(1-2*r) for e in keys)) for r in range(2)]
        for r in range(2):
            key_ = keys[r]
            while any(key_):
                k = prod((l for l, e in zip(self.ells, key_) if e > 0))
                while True:
                    P = E.lift_x(self.F.random_element())
                    if r != (P.y() in self.F):
                        break
                P *= (self.p + 1) // k
                for i, (l, e) in enumerate(zip(self.ells, key_)):
                    if e == 0:
                        continue
                    Q = k // l * P
                    if not Q:
                        continue
                    Q._order = l
                    phi = E.isogeny(Q)
                    E, P = phi.codomain(), phi(P)
                    key_[i] -= 1
                    k //= l
        return E.change_ring(self.F).montgomery_model() if _use_curve else int(to_montgomery(E))
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
    def decrypt2(self, A, key, use_curve = None):
        _use_curve = self._use_curve if use_curve is None else use_curve
        E = A if _use_curve else EllipticCurve(self.F, [0, A, 0, 1, 0])
        E = E.change_ring(self.F2)
        keys = list(e for l, e in zip(self.ells, key))
        keys = [list(map_relu(e*(2*r-1) for e in keys)) for r in range(2)]
        for r in range(2):
            key_ = keys[r]
            while any(key_):
                k = prod((l for l, e in zip(self.ells, key_) if e > 0))
                while True:
                    P = E.lift_x(self.F.random_element())
                    if r != (P.y() in self.F):
                        break
                P *= (self.p + 1) // k
                for i, (l, e) in enumerate(zip(self.ells, key_)):
                    if e == 0:
                        continue
                    Q = k // l * P
                    if not Q:
                        continue
                    Q._order = l
                    phi = E.isogeny(Q)
                    E, P = phi.codomain(), phi(P)
                    key_[i] -= 1
                    k //= l
        return E.change_ring(self.F).montgomery_model() if _use_curve else int(to_montgomery(E))
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
    def qfb(self, ell, conductor = 2):
        return pari.Qfb(ell, conductor, ZZ(self.p + 1) * conductor**2 / ell / 4)

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

def calc_csidh_data(csidh: CSIDH, conductor = 2, flag = 0, tech = None, precision = 0, elkies_first = True, kannan_embedding = None, show_rank = True):
    b, f = is_int_int(conductor)
    assert b and f > 0
    d = -f**2 * csidh.p
    alg.info(f"Computing class group of a quadratic order of discriminant {d}.")
    no, cyc, gen, reg = pari.quadclassunit(d, flag = flag, tech = tech, precision = precision)
    no = ZZ(no)
    if reg != 1 or len(cyc) != 1 or len(gen) != 1:
        alg.bad("Malformed class group.", f"{no = }", f"{cyc = }", f"{gen = }", f"{reg = }")
        raise ValueError(f"Malformed class group. {no = }, {cyc = }, {gen = }, {reg = }")
    alg.info("Found class group.", f"{no = }", f"{cyc = }", f"{gen = }", f"{reg = }")
    g = gen[0]
    facs = factor(no)
    alg.info(f"{no} = {facs}")
    if elkies_first and gen[0][0] not in csidh.ells:
        q0 = gen[0]**0
        for ell in csidh.ells:
            q = csidh.qfb(ell, conductor = f)
            for fac, e in facs:
                if q**(no//fac) == q0:
                    break
            else:
                g = q
                break
        alg.info(f"Using generator {g = }.")
    dlogs = []
    alg.info("Computing discrete logs.")
    for ell in csidh.ells:
        q = csidh.qfb(ell, conductor = f)
        default_n_factor_to_list = sage.rings.integer.n_factor_to_list
        sage.rings.integer.n_factor_to_list = lambda x, y: default_n_factor_to_list(x, y) if x != no else list(facs)
        try:
            dlog = discrete_log(q, g, no, operation = None, identity = g**0, inverse = lambda x: x**-1, op = lambda a, b: a*b)
        except Exception as e:
            sage.rings.integer.n_factor_to_list = default_n_factor_to_list
            raise e
        sage.rings.integer.n_factor_to_list = default_n_factor_to_list
        dlogs.append(dlog)
        alg.info(f"{q} == {g}^{dlog}")
    L = matrix(len(csidh.ells) + 1)
    embedding = kannan_embedding if kannan_embedding is not None else no
    L[0,0] = no
    for i, (ell, dlog) in enumerate(zip(csidh.ells, dlogs)):
        L[i+1,0] = dlog
        L[i+1,i+1] = 1
    L[:,0] *= embedding
    L_ = reduction(L)
    relation_lattice = []
    for row in L_:
        if row[0] == 0:
            relation_lattice.append(tuple(row[1:]))
    if show_rank:
        alg.info(f"Rank of the relation lattice: {matrix(relation_lattice).rank()}")
    save_csidh_data(csidh.p, csidh.ells, no, f, dlogs, g[0], relation_lattice)
