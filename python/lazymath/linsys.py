from logger.astra_logger import *
from functools import reduce
from sage.all import SR, vector, matrix, log, RR

class LinearizedSystem:
    def __init__(self, F, var_list, ignore_uncaught = False, sol_debug = True, sol_thres = 10000, sol_strict_thres = False):
        self.F = F
        self.PR = self.F[*reduce(lambda a, b: a | set(SR(b).variables()), var_list, set())]
        self.vars = self.PR.gens()
        self.var_list = [self.PR(x) for x in var_list]
        self.n = len(self.var_list)
        self._system = []
        self._target = []
        self._ignore_uncaught = ignore_uncaught
        self._sol_debug = sol_debug
        self._sol_thres = sol_thres
        self._sol_strict_thres = sol_strict_thres
    def varindex(self, varname):
        return self.var_list.index(self.PR(varname))
    def append(self, pol, target):
        pol = self.PR(pol)
        if not self._ignore_uncaught:
            _left = set(pol.monomials()) - {1}
            _right = set(self.var_list)
            assert _left <= _right, f"Uncaught vars {_left - _right}."
        coeffs = dict((y, x) for x, y in pol)
        tmp = [coeffs.pop(x, 0) for x in self.var_list]
        self._target.append(self.F(target) - self.F(pol.constant_coefficient()))
        self._system.append(vector(self.F, tmp))
    def clear(self):
        self._system = []
        self._target = []
    def pop(self, row):
        return self._system.pop(row), self._target.pop(row)
    def solutions(self):
        A = matrix(self.F, self._system)
        if self._sol_debug:
            rnk = A.rank()
            dim = A.dimensions()
            ord_ = self.F.order()
            debug(f'Rank = {rnk}', f'Dims = {dim}', f'Base Order = {ord_}')
            if self._sol_thres is not None and dim[1] > rnk and RR(dim[1] - rnk) > log(self._sol_thres) / log(ord_):
                if self._sol_strict_thres or gets(f"Too many possible solutions (>{self._sol_thres}), continue? [y/N] ").strip().lower() != 'y':
                    debug("LinearizedSystem solutions aborted.")
                    return
        try:
            ksi = A.solve_right(vector(self.F, self._target))
        except ValueError:
            debug("LinearizedSystem no solution.")
            return
        yield ksi
        for v in A.right_kernel():
            if not v: continue
            yield v + ksi
    def __str__(self):
        return f"System of {len(self._system)} equation(s) in {self.n} linearized var(s)."
    def __repr__(self):
        return self.__str__()
