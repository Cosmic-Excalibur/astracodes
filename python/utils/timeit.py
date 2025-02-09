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

def set_ticktock_log_func(log_func, wrapper = 'Ticktock: %.4fs'):
    global _log_func
    if log_func == None: _log_func = None
    elif wrapper != None: _log_func = lambda x: log_func(wrapper % x)
    else: _log_func = log_func
