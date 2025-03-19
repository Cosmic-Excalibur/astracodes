from sage.all import var
from astrautils.slicing import do_slice
import sys, itertools

class V:
    def __init__(self, bn: str, upper_bound: [int, None] = None, pad: [int, None] = None):
        self.bn = bn
        self.upper_bound = upper_bound
        if self.upper_bound != None and self.upper_bound <= 0:
            raise ValueError("Non-positive upper bound.")
        self.pad = pad if pad != None else (0 if self.upper_bound == None else len(str(upper_bound)))
        name = 'v%s' % bn
        self._frame = sys._getframe(1)
        self._store_global(name, self)
    def _store_global(self, name, thing):
        self._frame.f_globals.update({name: thing})
        return thing
    def __getitem__(self, i):
        def func(idx):
            if self.upper_bound != None and (idx < 0 or idx >= self.upper_bound):
                raise IndexError(f'Out of range ({self.bn}%0{self.pad}d~{self.bn}%0{self.pad}d).' % (0, self.upper_bound - 1))
            return self._i(idx)
        do = lambda idx: do_slice(idx, func, self.upper_bound) if isinstance(idx, slice) else [func(idx if self.upper_bound == None else (self.upper_bound + idx if idx < 0 else idx))]
        return sum(map(do, i), []) if hasattr(i, '__iter__') else (do(i) if isinstance(i, slice) else do(i)[0])
    def _i(self, i):
        name = f'{self.bn}%0{self.pad}d' % i
        return self._store_global(name, var(name))
    def __iter__(self):
        return (self._i(idx) for idx in itertools.count()) if self.upper_bound == None else (self._i(idx) for idx in range(self.upper_bound))
    def __str__(self):
        return 'Var factory "v%s"' % self.bn + ('' if self.upper_bound == None else ' with at most %s elements' % self.upper_bound)
    def __repr__(self):
        return self.__str__()

if __name__ == '__main__':
    from rich.progress import track
    import random
    n = 100
    P = lambda p = 1/4: random.random() <= p
    V('a', upper_bound = n)
    dummy = [f'a%0{len(str(n))}d' % i for i in range(n)]
    for i in track(range(100000), description = 'Sanity check 1...'):
        start, stop, step = [None if P() else random.randint(-n*2,n*2) for _ in '123']
        while step == 0:
            step = None if P() else random.randint(-n*2,n*2)
        try:
            assert all(str(x) == y for x, y in zip(va[start:stop:step, 23, :n//2, -10], dummy[start:stop:step] + [dummy[23]] + dummy[:n//2] + [dummy[-10]])), (1, i, (start, stop, step))
        except IndexError:
            assert 0, (1, i, (start, stop, step))
    n = 100
    V('a')
    dummy = ['a%d' % i for i in range(n)]
    for i in track(range(100000), description = 'Sanity check 2...'):
        start, step = [None if P() else random.randrange(-n*2,n-1) for _ in '12']
        stop = random.randrange(-n*2,n-1)
        while step == 0:
            step = None if P() else random.randint(-n*2,n*2)
        try:
            assert all(str(x) == y for x, y in zip(va[start:stop:step, 23, :n//2], dummy[0 if start == None else (-n-1 if start < 0 else start):0 if stop == None else (-n-1 if stop < 0 else stop):step] + [dummy[23]] + dummy[:n//2])), (2, i, (start, stop, step))
        except IndexError:
            assert 0, (2, i, (start, stop, step))
