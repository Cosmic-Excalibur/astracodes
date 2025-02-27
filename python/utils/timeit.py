from time import perf_counter
from contextlib import contextmanager

@contextmanager
def timeit(task_name = 'timeit'):
    start = perf_counter()
    try:
        yield
    finally:
        end = perf_counter()
        print(f"{task_name} took {end - start:.4f} second(s).")

_ticktock_time = None
_log_func = None
def ticktock():
    global _ticktock_time
    t = perf_counter()
    if _ticktock_time == None:
        res = 0.0
    else:
        res = t - _ticktock_time
    _ticktock_time = t
    if _log_func != None: _log_func(res)
    return res

_PARITY = 0
def set_global_parity(new = 0):
    global _PARITY
    _PARITY = int(new)

def global_odd(func):
    def _wrapper(*args, **kwargs):
        global _PARITY
        _PARITY ^= 1
        return func(*args, **kwargs) if _PARITY else None
    return _wrapper

def global_even(func):
    def _wrapper(*args, **kwargs):
        global _PARITY
        _PARITY ^= 1
        return None if _PARITY else func(*args, **kwargs)
    return _wrapper

def odd(func):
    _INNER_PARITY = 0
    def _wrapper(*args, **kwargs):
        nonlocal _INNER_PARITY
        _INNER_PARITY ^= 1
        return func(*args, **kwargs) if _INNER_PARITY else None
    return _wrapper

def even(func):
    _INNER_PARITY = 0
    def _wrapper(*args, **kwargs):
        nonlocal _INNER_PARITY
        _INNER_PARITY ^= 1
        return None if _INNER_PARITY else func(*args, **kwargs)
    return _wrapper

_COUNTER = -1
def set_global_counter(new = -1):
    global _COUNTER
    _COUNTER = int(new)

def global_hill(range_ = None):
    def _decorator(func):
        def _wrapper(*args, **kwargs):
            global _COUNTER
            _COUNTER += 1
            return func(*args, **kwargs) if (range_ is None or _COUNTER in range_) else None
        return _wrapper
    return _decorator

def global_valley(range_ = None):
    def _decorator(func):
        def _wrapper(*args, **kwargs):
            global _COUNTER
            _COUNTER += 1
            return None if (range_ is None or _COUNTER in range_) else func(*args, **kwargs)
        return _wrapper
    return _decorator

def hill(range_ = None):
    def _decorator(func):
        _INNER_COUNTER = -1
        def _wrapper(*args, **kwargs):
            nonlocal _INNER_COUNTER
            _INNER_COUNTER += 1
            return func(*args, **kwargs) if (range_ is None or _INNER_COUNTER in range_) else None
        return _wrapper
    return _decorator

def valley(range_ = None):
    def _decorator(func):
        _INNER_COUNTER = -1
        def _wrapper(*args, **kwargs):
            nonlocal _INNER_COUNTER
            _INNER_COUNTER += 1
            return None if (range_ is None or _INNER_COUNTER in range_) else func(*args, **kwargs)
        return _wrapper
    return _decorator

@global_odd
def global_odd_print(*args, **kwargs):
    print(*args, **kwargs)

@global_even
def global_even_print(*args, **kwargs):
    print(*args, **kwargs)

def odd_print_factory(print_func = print):
    @odd
    def odd_print(*args, **kwargs):
        print_func(*args, **kwargs)
    return odd_print

def even_print_factory(print_func = print):
    @even
    def even_print(*args, **kwargs):
        print_func(*args, **kwargs)
    return even_print

odd_print = odd_print_factory()
even_print = even_print_factory()

def set_ticktock_log_func(log_func, wrapper = 'Ticktock: %.4fs'):
    global _log_func
    if log_func == None: _log_func = None
    elif wrapper != None: _log_func = lambda x: log_func(wrapper % x)
    else: _log_func = log_func
