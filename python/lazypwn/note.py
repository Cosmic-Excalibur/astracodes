from astrautils.int import is_int
from sortedcontainers.sortedset import SortedSet


class Indexing:

    def __init__(self,
        start=None,
        stop=None,
        lb=None,
        ub=None,
        gap=1,
        base_index=None,
        index=None
    ):
        if not (
            (is_int(start) or start is None) and \
            (is_int(stop) or stop is None) and \
            is_int(gap) and \
            (is_int(ub) or ub is None) and \
            (is_int(lb) or lb is None) and \
            (is_int(base_index) or base_index is None) and \
            (is_int(index) or index is None)
        ):
            raise TypeError("Invalid indexing parameters.")
        self.gap = abs(int(gap))
        if self.gap == 0:
            raise ValueError("`gap` must not be zero.")
        if lb is not None:
            if start is None:
                self.start = int(lb)
            else:
                raise ValueError("Ambiguous lower bound.")
        elif start is None:
            self.start = None
        else:
            self.start = int(start)
        if ub is not None:
            if stop is None:
                if self.start is not None and (int(ub) - self.start) % self.gap:
                    raise ValueError("Improper upper bound.")
                self.stop = int(ub) + self.gap
            else:
                raise ValueError("Ambiguous upper bound.")
        elif stop is None:
            self.stop = None
        else:
            self.stop = int(stop)
        self.base_index = None
        if self.start is not None or self.stop is not None:
            if base_index is not None:
                raise ValueError("`base_index` is meaningful for doubly boundless ranges only.")
        elif base_index is None:
            raise ValueError("`base_index` should be specified for doubly boundless ranges.")
        else:
            self.base_index = int(base_index)
        if self.start is not None and self.stop is not None and \
            ((self.stop - self.start) % self.gap or self.start >= self.stop):
            raise ValueError("Invalid bounds.")
        if index is None:
            self.index = None
        else:
            self.index = int(index)
            if not self.is_sane_index(self.index):
                raise ValueError("Invalid index.")
    
    def is_sane_index(self, index):
        if not is_int(index):
            return False
        if self.start is None:
            if self.stop is None:
                return (self.base_index - index) % self.gap == 0
            else:
                return self.stop > index and (self.stop - index) % self.gap == 0
        else:
            if self.stop is None:
                return self.start <= index and (index - self.start) % self.gap == 0
            else:
                return self.start <= index < self.stop and \
                    (index - self.start) % self.gap == 0
    

class LeastFirstIndexing(Indexing):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.taken = SortedSet()
    
    def take(self, index=None):
        if index is None:
            index = self.next()
        if not self.is_sane_index(index):
            raise IndexError("Invalid index / Empty.")
        idx = self.taken.bisect_right(index)
        if idx & 1:
            raise IndexError(f"Index #{index} has already been taken.")
        else:
            if len(self.taken) >= idx > 0 and self.taken[idx-1] == index:
                del self.taken[idx-1]
            else:
                self.taken.add(index)
            if index + self.gap in self.taken:
                self.taken.remove(index + self.gap)
            else:
                self.taken.add(index + self.gap)
    
    def next(self, index=None):
        if index is None:
            index = self.start
        if not self.is_sane_index(index):
            return None
        idx = self.taken.bisect_right(index)
        if idx & 1:
            cand = self.taken[idx]
            if self.stop is not None and cand >= self.stop:
                return None
            else:
                return cand
        else:
            return index
    
    def put(self, index):
        if not self.is_sane_index(index):
            raise IndexError("Invalid index.")
        idx = self.taken.bisect_right(index)
        if idx & 1:
            if len(self.taken) >= idx > 0 and self.taken[idx-1] == index:
                del self.taken[idx-1]
            else:
                self.taken.add(index)
            if index + self.gap in self.taken:
                self.taken.remove(index + self.gap)
            else:
                self.taken.add(index + self.gap)
    
    def is_taken(self, index):
        if not self.is_sane_index(index):
            raise IndexError("Invalid index.")
        return self.next(index) == index
    

class GreatestFirstIndexing(Indexing):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.taken = SortedSet(key=lambda x: -x)
    
    def take(self, index=None):
        if index is None:
            index = self.next()
        if not self.is_sane_index(index):
            raise IndexError("Invalid index / Empty.")
        idx = self.taken.bisect_right(index)
        if idx & 1:
            raise IndexError(f"Index #{index} has already been taken.")
        else:
            if len(self.taken) >= idx > 0 and self.taken[idx-1] == index:
                del self.taken[idx-1]
            else:
                self.taken.add(index)
            if index - self.gap in self.taken:
                self.taken.remove(index - self.gap)
            else:
                self.taken.add(index - self.gap)
    
    def next(self, index=None):
        if index is None:
            index = self.stop - self.gap
        if not self.is_sane_index(index):
            return None
        idx = self.taken.bisect_right(index)
        if idx & 1:
            cand = self.taken[idx]
            if self.start is not None and cand < self.start:
                return None
            else:
                return cand
        else:
            return index
    
    def put(self, index):
        if not self.is_sane_index(index):
            raise IndexError("Invalid index.")
        idx = self.taken.bisect_right(index)
        if idx & 1:
            if len(self.taken) >= idx > 0 and self.taken[idx-1] == index:
                del self.taken[idx-1]
            else:
                self.taken.add(index)
            if index - self.gap in self.taken:
                self.taken.remove(index - self.gap)
            else:
                self.taken.add(index - self.gap)
    
    def is_taken(self, index):
        if not self.is_sane_index(index):
            raise IndexError("Invalid index.")
        return self.next(index) == index


class AscendingLIFOIndexing(Indexing):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.base_index is not None and self.index is None:
            self.index = self.base_index
        if self.index is None:
            if self.start is None:
                raise ValueError("`index` must specified for bottomless ranges.")
            self.index = self.start
    
    def take(self):
        if self.stop is not None and self.index >= self.stop:
            raise IndexError("Empty.")
        self.index += self.gap
    
    def put(self):
        if self.start is not None and self.index - self.gap < self.start:
            raise IndexError("Full.")
        self.index -= self.gap
    
    def next(self, index=None):
        if self.stop is not None and index >= self.stop and index is None:
            return None
        elif not self.is_sane_index(index):
            return None
        return max(index, self.index)
    
    def is_taken(self, index):
        if not self.is_sane_index(index):
            raise IndexError("Invalid index.")
        return index < self.index


class DescendingLIFOIndexing(Indexing):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.base_index is not None and self.index is None:
            self.index = self.base_index
        if self.index is None:
            if self.stop is None:
                raise ValueError("`index` must specified for topless ranges.")
            self.index = self.stop - self.gap
    
    def take(self):
        if self.start is not None and self.index < self.start:
            raise IndexError("Empty.")
        self.index -= self.gap
    
    def put(self):
        if self.stop is not None and self.index + self.gap >= self.stop:
            raise IndexError("Full.")
        self.index += self.gap
    
    def next(self, index=None):
        if self.start is not None and self.index < self.start and index is None:
            return None
        elif not self.is_sane_index(index):
            return None
        return min(index, self.index)
    
    def is_taken(self, index):
        if not self.is_sane_index(index):
            raise IndexError("Invalid index.")
        return index > self.index


class AscendingYOLOIndexing(Indexing):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.base_index is not None and self.index is None:
            self.index = self.base_index
        if self.index is None:
            if self.start is None:
                raise ValueError("`index` must specified for bottomless ranges.")
            self.index = self.start
    
    def take(self):
        if self.stop is not None and self.index >= self.stop:
            raise IndexError("Empty.")
        self.index += self.gap
    
    def put(self):
        raise AttributeError("You Only Look Once :)")
    
    def next(self, index=None):
        if self.stop is not None and self.index >= self.stop and index is None:
            return None
        elif not self.is_sane_index(index):
            return None
        return max(index, self.index)
    
    def is_taken(self, index):
        if not self.is_sane_index(index):
            raise IndexError("Invalid index.")
        return index < self.index


class DescendingYOLOIndexing(Indexing):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.base_index is not None and self.index is None:
            self.index = self.base_index
        if self.index is None:
            if self.stop is None:
                raise ValueError("`index` must specified for topless ranges.")
            self.index = self.stop - self.gap
    
    def take(self):
        if self.start is not None and self.index < self.start:
            raise IndexError("Empty.")
        self.index -= self.gap
    
    def put(self):
        raise AttributeError("You Only Look Once :)")
    
    def next(self, index=None):
        if self.start is not None and self.index < self.start and index is None:
            return None
        elif not self.is_sane_index(index):
            return None
        return min(index, self.index)
    
    def is_taken(self, index):
        if not self.is_sane_index(index):
            raise IndexError("Invalid index.")
        return index > self.index


SupportedReadingPatterns = {
    'faithful': lambda x, *args, **kwargs: (x, len(x)),
    'linefeed_truncated_to_null': lambda x, *args, **kwargs: (x + b'\n', len(x) + 1) if b'\n' not in x else (x[:x.index(b'\n') + 1], x.index(b'\n') + 1),
    'linefeed_truncated': lambda x, *args, **kwargs: (x + b'\n', len(x)) if b'\n' not in x else (x[:x.index(b'\n') + 1], x.index(b'\n')),
    'null_truncated_to_null': lambda x, *args, **kwargs: (x, len(x) + 1) if b'\0' not in x else (x[:x.index(b'\0')], x.index(b'\0') + 1),
    'null_truncated': lambda x: (x, len(x)) if b'\0' not in x else (x[:x.index(b'\0')], x.index(b'\0')),
    'linefeed_truncated_or_stuffed': lambda x, reach, *args, **kwargs: (x[:reach], reach) if b'\n' not in x[:reach] else (x[:x.index(b'\n')], x.index(b'\n')),
    'linefeed_truncated_to_null_or_stuffed': None,
    'null_truncated_or_stuffed': None,
    'null_truncated_to_null_or_stuffed': None,
    'stuffed': None
}


SupportedPrintingPatterns = (
    'faithful': None,
    'ending_linefeed': None,
    'null_truncated': None,
    'null_truncated_ending_linefeed': None,
    'linefeed_truncated': None,
    'linefeed_truncated_ending_linefeed': None
)


class Note_factory:

    def __init__(self, heap='ptmalloc2', version=('GLIBC', (2, 35))):
        self.config = {
            'add': {
                'oracle': None,
                'indexing': None,
                'index_needed': None,
                'reach': None,
                'size_range': None,
                'content_constraint': None,
                'reading_pattern': None
            }, 
            'delete': {
                'oracle': None,
                'allowing_mapping': None,
                'uaf': None,
                'max_trials': None
            },
            'show': {
                'oracle': None,
                'allowing_mapping': None,
                'reach': None,
                'printing_pattern': None
            },
            'edit': {
                'oracle': None,
                'allowing_mapping': None,
                'reach': None,
                'content_constraint': None,
                'reading_pattern': None
            }
        }
        self.heap = heap
        self.version = version
        self.notes = dict()
    
    def config_add(self,
        oracle,
        indexing=None,
        index_needed=True,
        reach=None,
        size_range=None,
        content_constraint=None,
        reading_pattern='faithful'
    ):
        if not hasattr(oracle, '__call__'):
            raise TypeError("Invalid oracle.")
        self.config['add']['oracle'] = oracle
        if indexing is None:
            indexing = LeastFirstIndexing(start=0)
        if not isinstance(indexing, Indexing):
            raise TypeError("Invalid indexing.")
        if reach is not None and (not is_int(reach) or int(reach) < 0):
            raise TypeError("Reach must be either unspecified or a non-negative integer.")
        if size_range is not None and not (hasattr(size_range, '__iter__') and hasattr(size_range, '__contains__')):
            raise TypeError("Invalid size range.")
        if content_constraint is not None not hasattr(content_constraint, '__call__'):
            raise TypeError("Invalid content constraint.")
        if reading_pattern not in SupportedReadingPatterns:
             raise AttributeError("Reading pattern must be one of %s." % ", ".join('"%s"' % pattern in SupportedReadingPatterns.keys()))
        self.config['add']['indexing'] = indexing
        self.config['add']['index_needed'] = bool(index_needed)
        self.config['add']['reach'] = None if reach is None else int(reach)
        self.config['add']['size_range'] = size_range
        self.config['add']['content_constraint'] = content_constraint
        self.config['add']['reading_pattern'] = reading_pattern
    
    def config_create(self, *args, **kwargs): self.config_add(*args, **kwargs)
    
    def config_write(self, *args, **kwargs): self.config_add(*args, **kwargs)
    
    def config_creat(self, *args, **kwargs): self.config_add(*args, **kwargs)
    
    def config_new(self, *args, **kwargs): self.config_add(*args, **kwargs)
    
    def config_alloc(self, *args, **kwargs): self.config_add(*args, **kwargs)
    
    def config_malloc(self, *args, **kwargs): self.config_add(*args, **kwargs)

    def config_delete(self,
        oracle,
        uaf=False,
        allowing_mapping=None,
        max_trials=0
    ):
        if not hasattr(oracle, '__call__'):
            raise TypeError("Invalid oracle.")
        self.config['delete']['oracle'] = oracle
        self.config['delete']['uaf'] = bool(uaf)
        if not hasattr(allowing_mapping, '__call__'):
            raise TypeError("Allowing mapping must be a function, mapping an `Indexing` object to an iterable of indices.")
        self.config['delete']['allowing_mapping'] = allowing_mapping
        if not is_int(max_trials):
            raise TypeError("`max_trials` must be an integer.")
        self.config['delete']['max_trials'] = int(max_trials)
    
    def config_remove(self, *args, **kwargs): self.config_delete(*args, **kwargs)
    
    def config_del(self, *args, **kwargs): self.config_delete(*args, **kwargs)
    
    def config_dele(self, *args, **kwargs): self.config_delete(*args, **kwargs)
    
    def config_delet(self, *args, **kwargs): self.config_delete(*args, **kwargs)
    
    def config_free(self, *args, **kwargs): self.config_delete(*args, **kwargs)
    
    def config_purge(self, *args, **kwargs): self.config_delete(*args, **kwargs)
    
    def config_rm(self, *args, **kwargs): self.config_delete(*args, **kwargs)
    
    def config_show(self,
        oracle,
        allowing_mapping=None,
        reach=None,
        printing_pattern='faithful'
    ):
        if not hasattr(oracle, '__call__'):
            raise TypeError("Invalid oracle.")
        self.config['show']['oracle'] = oracle
        if not hasattr(allowing_mapping, '__call__'):
            raise TypeError("Allowing mapping must be a function, mapping an `Indexing` object to an iterable of indices.")
        self.config['show']['allowing_mapping'] = allowing_mapping
        if reach is not None and (not is_int(reach) or int(reach) < 0):
            raise TypeError("Reach must be either unspecified or a non-negative integer.")
        self.config['show']['reach'] = None if reach is None else int(reach)
        if printing_pattern not in SupportedPrintingPatterns:
             raise AttributeError("Printing pattern must be one of %s." % ", ".join('"%s"' % pattern in SupportedPrintingPatterns.keys()))
        self.config['show']['printing_pattern'] = printing_pattern
    
    def config_print(self, *args, **kwargs): self.config_show(*args, **kwargs)
    
    def config_read(self, *args, **kwargs): self.config_show(*args, **kwargs)
    
    def config_edit(self,
        oracle=None,
        allowing_mapping=None,
        reach=None,
        content_constraint=None,
        reading_pattern=SupportedReadingPatterns[0]
    ):
        if not hasattr(oracle, '__call__'):
            raise TypeError("Invalid oracle.")
        self.config['show']['oracle'] = oracle
        if not hasattr(allowing_mapping, '__call__'):
            raise TypeError("Allowing mapping must be a function, mapping an `Indexing` object to an iterable of indices.")
        if reach is not None and (not is_int(reach) or int(reach) < 0):
            raise TypeError("Reach must be either unspecified or a non-negative integer.")
        if content_constraint is not None not hasattr(content_constraint, '__call__'):
            raise TypeError("Invalid content constraint.")
        if reading_pattern not in SupportedReadingPatterns:
             raise AttributeError("Reading pattern must be one of %s." % ", ".join('"%s"' % pattern in SupportedReadingPatterns))
        self.config['edit']['allowing_mapping'] = allowing_mapping
        self.config['edit']['reach'] = None if reach is None else int(reach)
        self.config['edit']['content_constraint'] = content_constraint
        self.config['edit']['reading_pattern'] = reading_pattern
    
    def config_modify(self, *args, **kwargs): self.config_edit(*args, **kwargs)
    
    def config_change(self, *args, **kwargs): self.config_edit(*args, **kwargs)
    
    @staticmethod
    def content_modifier(content, reading_pattern):
        pass

    def add(self, size, content):
        if size not in self.config['add']['size_range'] or not self.config['add']['content_constraint'](content):
            return None
        content_ = self.content_modifier(content, self.config['add']['reading_pattern'])
        if self.config['add']['reach'] is not None:
            ret = min(len(content), self.config['add']['reach'])
        else:
            ret = len(content)
        g = iter(self.config['add']['size_range'])
        next(g)
        self.config['add']['oracle'](*([index]*(self.config['add']['index_needed']) + [size]*(next(g, None) is not None) + [content]*(ret)))
        