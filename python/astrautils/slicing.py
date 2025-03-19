from sortedcontainers import SortedDict, SortedList
from functools import reduce
from typing import Sequence

def do_slice(slice_, func, n = None, ret_type = list):    # slow
    if n == 0: return ret_type([])
    start = slice_.start
    stop = slice_.stop
    if slice_.step == 0: raise ValueError("Step must not be zero.")
    step = slice_.step or 1
    if n != None:
        if start == None: start = n-1 if step < 0 else 0
        else:
            start = start if start >= 0 else n + start
            if start >= n and step < 0: start = n-1
        if stop == None: stop = n if step > 0 else -1
        else:
            stop = stop if stop >= 0 else n + stop
            if stop > n and step > 0: stop = n
    else:
        if start == None: start = 0
        if stop == None: raise OverflowError("Specify an upper bound.")
    if stop < 0 and step < 0: stop = -1
    if start < 0 and step > 0: start = 0
    res = []
    i = start
    if step > 0:
        while i < stop:
            res.append(func(i))
            i += step
    else:
        while i > stop:
            res.append(func(i))
            i += step
    return ret_type(res)

def slice_interval(slice_, n):
    start, stop, step = slice_.indices(n)
    if step < 0:
        step = -step
        if start > stop:
            start, stop = start - ((start - stop) - 1) // step * step, min(start + step, n)
        else:
            stop = -1
    if start >= stop: stop = -1
    return start, stop, step

def _floordiv(a, b):
    return a // b

def _ceildiv(a, b):
    return (a + b - 1) // b

_FAST_CUTTER_THRESHOLD = 1000000

def set_fast_cutter_threshold(n):
    global _FAST_CUTTER_THRESHOLD
    _FAST_CUTTER_THRESHOLD = n

def get_fast_cutter_threshold():
    return _FAST_CUTTER_THRESHOLD

class cutter:
    def __init__(self, *seq, lstrip = True, rstrip = True):
        if len(seq) == 0:
            raise ValueError
        typ = type(seq[0])
        if len(seq) == 1:
            self.seq = seq[0] if issubclass(typ, Sequence) else list(seq[0])
        else:
            if not issubclass(typ, Sequence): typ = list
            self.seq = typ()
            for s in seq: self.seq += typ(s)
        self._scratches = SortedDict()
        self.do_lstrip = lstrip
        self.do_rstrip = rstrip
    def split(self, indices = None):
        self.refresh()
        if indices is not None:
            return self[indices]
        return iter([self.seq])
    def _scratch(self, range_):
        start1, stop1, step1 = range_
        if start1 >= stop1 or start1 > self.seq.__len__(): return
        tmp = SortedList(self._scratches.get(start1, []))
        tmp0 = list(tmp)
        less = []
        moreflag = True
        for i, (step, stop) in enumerate(tmp):
            if step % step1 == 0:
                end = start1 + (_ceildiv(stop - start1, step) - 1) * step + 1
                end1 = start1 + (_ceildiv(stop1 - start1, step1) - 1) * step1 + 1
                if end > end1:
                    end_ = start1 + (_ceildiv(end1 - start1, step) - 1) * step + 1
                    start_ = end_ + step - 1
                    self._scratch((start_, end, step))
                less.append(i)
            elif step1 % step == 0:
                end = start1 + (_ceildiv(stop - start1, step) - 1) * step + 1
                end1 = start1 + (_ceildiv(stop1 - start1, step1) - 1) * step1 + 1
                step_ = step1
                if end1 > end:
                    end1_ = start1 + (_ceildiv(end - start1, step1) - 1) * step1 + 1
                    start1_ = end1_ + step1 - 1
                    self._scratch((start1_, end1, step1))
                moreflag = False
        for i, j in enumerate(less):
            del tmp[j-i]
        if moreflag:
            tmp.add((step1, stop1))
        self._scratches[start1] = tmp
    def crazydiamond(self):
        self.refresh()
    def refresh(self):
        self._scratches = SortedDict()
    def __getitem__(self, indices):
        self.refresh()
        n = self.seq.__len__() + 1
        if hasattr(indices, '__iter__'):
            if n < _FAST_CUTTER_THRESHOLD:
                return self._fast_split(indices)
            for index in indices:
                if isinstance(index, slice):
                    self._scratch(slice_interval(index, n))
                else:
                    if index < 0: index += n
                    if index >= 0 and index < n: self._scratch((index, index+1, 1))
        else:
            if n < _FAST_CUTTER_THRESHOLD:
                return self._fast_split([indices])
            if isinstance(indices, slice):
                self._scratch(slice_interval(indices, n))
            else:
                if indices < 0: indices += n
                if indices >= 0 and indices < n: self._scratch((indices, indices+1, 1))
        return self._split()
    def _fast_split(self, indices):
        n = self.seq.__len__() + 1
        ptr = 0
        dummy = list(range(n))
        for next_ in sorted(reduce(lambda a, b: a | b, (set(dummy[idx]) if isinstance(idx, slice) else set([dummy[idx]]) for idx in indices), set())):
            if not self.do_lstrip or next_ > 0:
                yield self.seq[ptr:next_]
            ptr = next_
        if not self.do_rstrip or ptr != n-1:
            yield self.seq[ptr:]
    def _split(self):
        state = SortedList()
        keys = list(self._scratches.keys())
        ptr = 0
        n = self.seq.__len__() + 1
        while len(state) or len(keys):
            if not len(state) or (len(keys) and state[0][0] >= keys[0]):
                new_start = keys.pop(0)
                data = self._scratches[new_start]
                state += [[new_start, step, stop] for step, stop in data]
            victim_start, victim_step, victim_stop = state.pop(0)
            if not self.do_lstrip or victim_start != 0:
                yield self.seq[ptr:victim_start]
            ptr = victim_start
            while len(state) and state[0][0] == victim_start:
                tmp_start, tmp_step, tmp_stop = state.pop(0)
                tmp_start_ = tmp_start + tmp_step
                if tmp_start_ < tmp_stop:
                    state.add([tmp_start_, tmp_step, tmp_stop])
            end = victim_stop
            if len(keys): end = min(end, keys[0])
            if len(state): end = min(end, state[0][0])
            end -= victim_step
            if ptr < end:
                for ptr in range(ptr, end, victim_step):
                    yield self.seq[ptr:ptr+victim_step]
                ptr += victim_step
            if ptr + victim_step < victim_stop:
                state.add([ptr + victim_step, victim_step, victim_stop])
        if (not self.do_rstrip or ptr != n-1) and ptr < n:
            yield self.seq[ptr:]
    def __str__(self):
        return f'cutter({self.seq})'
    def __repr__(self):
        return self.__str__()

class long_range:
    def __init__(self, *args, **kwargs):
        self._range = range(*args, **kwargs)
        self.start, self.step, self.stop = self._range.start, self._range.step, self._range.stop
    def __len__(self):
        return max(_ceildiv(self.stop - self.start, self.step), 0)
    def count(self, *args, **kwargs):
        return self._range.count(*args, **kwargs)
    def index(self, *args, **kwargs):
        return self._range.index(*args, **kwargs)
    def __bool__(self, *args, **kwargs):
        return self._range.__bool__(*args, **kwargs)
    def __contains__(self, *args, **kwargs):
        return self._range.__contains__(*args, **kwargs)
    def __delattr__(self, *args, **kwargs):
        return self._range.__delattr__(*args, **kwargs)
    def __dir__(self, *args, **kwargs):
        return self._range.__dir__(*args, **kwargs)
    def __doc__(self, *args, **kwargs):
        return self._range.__doc__(*args, **kwargs)
    def __eq__(self, *args, **kwargs):
        return self._range.__eq__(*args, **kwargs)
    def __format__(self, *args, **kwargs):
        return self._range.__format__(*args, **kwargs)
    def __ge__(self, *args, **kwargs):
        return self._range.__ge__(*args, **kwargs)
    def __getitem__(self, *args, **kwargs):
        return self._range.__getitem__(*args, **kwargs)
    def __getstate__(self, *args, **kwargs):
        return self._range.__getstate__(*args, **kwargs)
    def __gt__(self, *args, **kwargs):
        return self._range.__gt__(*args, **kwargs)
    def __hash__(self, *args, **kwargs):
        return self._range.__hash__(*args, **kwargs)
    def __iter__(self, *args, **kwargs):
        return self._range.__iter__(*args, **kwargs)
    def __le__(self, *args, **kwargs):
        return self._range.__le__(*args, **kwargs)
    def __lt__(self, *args, **kwargs):
        return self._range.__lt__(*args, **kwargs)
    def __ne__(self, *args, **kwargs):
        return self._range.__ne__(*args, **kwargs)
    def __reduce__(self, *args, **kwargs):
        return self._range.__reduce__(*args, **kwargs)
    def __reduce_ex__(self, *args, **kwargs):
        return self._range.__reduce_ex__(*args, **kwargs)
    def __repr__(self):
        return f'long_range({self.start}, {self.stop}, {self.step})'
    def __reversed__(self, *args, **kwargs):
        return self._range.__reversed__(*args, **kwargs)
    def __sizeof__(self, *args, **kwargs):
        return self._range.__sizeof__(*args, **kwargs)
    def __str__(self):
        return f'long_range({self.start}, {self.stop}, {self.step})'
    def __subclasshook__(self, *args, **kwargs):
        return self._range.__subclasshook__(*args, **kwargs)

if __name__ == '__main__':
    from rich.progress import track
    import random
    from itertools import zip_longest
    from astrautils.timeit import ticktock
    from astrautils.gg import GG as gg
    n = 100
    P = lambda p = 1/4: random.random() <= p
    def random_slice(n, p = 1/4):
        start, stop, step = [None if P() else random.randint(-n*2,n*2) for _ in '123']
        while step == 0:
            step = None if P() else random.randint(-n*2,n*2)
        slice_ = slice(start, stop, step)
        return slice_
    '''
    for i in track(range(100000)):
        start, stop, step = [None if P() else random.randint(-n*2,n*2) for _ in '123']
        while step == 0:
            step = None if P() else random.randint(-n*2,n*2)
        slice_ = slice(start, stop, step)
        assert set(range(*slice_interval(slice_, n))) == set(range(*slice_.indices(n))), ("slice_interval", i, slice_)
    '''
    set_fast_cutter_threshold(0)
    c = cutter([0,1,2,3,4,5], [6,7,8,9,10], lstrip=0, rstrip=0)
    c._scratch((2,3,1))
    print(c.seq)
    print(c._scratches, end = '\n\n')
    print(*c[2], sep = '\n', end = '\n\n')
    c = cutter(list(range(20)), lstrip=0, rstrip=0)
    for i in c[5:7,11:15]:
        print(i)
    print()
    
    for i in c[1:15:3]:
        print(i)
    print()
    
    c.refresh()
    c._scratch((0,21,2))
    c._scratch((0,21,4))
    print(c._scratches)
    for i in c._split():
        print(i)
    print()
    
    c.refresh()
    c._scratch((0,21,4))
    c._scratch((0,21,2))
    print(c._scratches)
    for i in c._split():
        print(i)
    print()
    
    c = cutter(list(range(40)), lstrip=0, rstrip=0)
    c._scratch((0,20,3))
    c._scratch((0,20,2))
    print(c._scratches)
    for i, _ in zip(c._split(), (0 if i else gg() for i in reversed(range(30)))):
        print(i)
    print(sorted(set(range(0,20,3)) | set(range(0,20,2))))
    print()
    
    for i, _ in zip(c[:20:3, :20:2, 7:30:4], (0 if i else gg() for i in reversed(range(50)))):
        print(i)
    print(sorted(set(range(0,20,3)) | set(range(0,20,2)) | set(range(7,30,4))))
    print()
    
    N = 0
    #N = 100000
    n = 1000
    nb = (1, 2)
    c = cutter(list(range(n)), lstrip=0, rstrip=0)
    dummy = list(range(n+1))
    for i in track(range(N)):
        slices = [random.randint(0,n) if P() else random_slice(n) for _ in range(random.randint(*nb))]
        a = list(c[*slices])
        b = sorted(reduce(lambda a, b: a | b, ((set(dummy[s]) if isinstance(s, slice) else set([s])) for s in slices), set()))
        if len(a) == 1:
            assert b == []
        else:
            tb = ''
            for aa, bb in zip_longest(a[1:], b):
                tb += '%s %s\n' % (aa, bb)
                assert (aa == [] and bb == n) or aa[0] == bb, ((i, slices, a, b), print(tb))[0]
    N = 0
    #N = 10000
    n = 10000
    nb = (1, 10)
    c = cutter(list(range(n)), lstrip=0, rstrip=0)
    dummy = list(range(n+1))
    for i in track(range(N)):
        slices = [random.randint(0,n) if P() else random_slice(n) for _ in range(random.randint(*nb))]
        a = list(c[*slices])
        b = sorted(reduce(lambda a, b: a | b, ((set(dummy[s]) if isinstance(s, slice) else set([s])) for s in slices), set()))
        if len(a) == 1:
            assert b == []
        else:
            tb = ''
            for aa, bb in zip_longest(a[1:], b):
                tb += '%s %s\n' % (aa, bb)
                assert (aa == [] and bb == n) or aa[0] == bb, ((i, slices, a, b), print(tb))[0]
    N = 0
    #N = 100000
    n = 20000
    nb = (1, 200)
    c = cutter(list(range(n)), lstrip=0, rstrip=0)
    dummy = list(range(n+1))
    a_better = 0
    for i in track(range(N)):
        slices = [random.randint(0,n) if P() else random_slice(n) for _ in range(random.randint(*nb))]
        ticktock()
        a = list(c[*slices])
        res1 = ticktock()
        b = sorted(reduce(lambda a, b: a | b, ((set(dummy[s]) if isinstance(s, slice) else set([s])) for s in slices), set()))
        res2 = ticktock()
        if len(a) == 1:
            assert b == []
        else:
            tb = ''
            for aa, bb in zip_longest(a[1:], b):
                tb += '%s %s\n' % (aa, bb)
                assert (aa == [] and bb == n) or aa[0] == bb, ((i, slices, a, b), print(tb))[0]
        #print(res1, res2)
        if res1 < res2: a_better += 1
    if N > 0: print(a_better / N)
    
    set_fast_cutter_threshold(1000000)
    
    N = 0
    N = 100000
    n = 200000
    nb = (1, 200)
    c = cutter(list(range(n)), lstrip=0, rstrip=0)
    dummy = list(range(n+1))
    a_better = 0
    for i in track(range(N)):
        slices = [random.randint(0,n) if P() else random_slice(n) for _ in range(random.randint(*nb))]
        ticktock()
        a = list(c[*slices])
        res1 = ticktock()
        b = sorted(reduce(lambda a, b: a | b, ((set(dummy[s]) if isinstance(s, slice) else set([s])) for s in slices), set()))
        res2 = ticktock()
        if len(a) == 1:
            assert b == []
        else:
            tb = ''
            for aa, bb in zip_longest(a[1:], b):
                tb += '%s %s\n' % (aa, bb)
                assert (aa == [] and bb == n) or aa[0] == bb, ((i, slices, a, b), print(tb))[0]
        print(res1, res2)
        if res1 < res2: a_better += 1
    if N > 0: print(a_better / N)
