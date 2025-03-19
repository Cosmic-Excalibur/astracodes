# count = lambda iterable, func = None: functools.reduce(lambda a, b: a+1, iterable) if func is None else functools.reduce(lambda a, b: a+1 if func(b) else a, iterable)
def count(iterable, func = None):
    res = 0
    if func is None:
        for i in iterable:
            res += 1
    else:
        for i in iterable:
            if func(i):
                res += 1
    return res
