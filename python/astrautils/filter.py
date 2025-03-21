from astrautils.commonstrings import *
from itertools import zip_longest


def maps(maps_, *args):
    '''
    Generate a workflow of functions chaining **the first argument**.
    
    Example:
    
    >>> list(maps([lstrip, rstrip], [' bbbastraccc   ', '!*@@&@#UD*'], [['b ', '!*']], [[' c', '*D']]))
    ['astra', '@@&@#U']
    
    >>> list(maps([(lstrip, ['b ', '!*']), (rstrip, [' c', '*D'])], [' bbbastraccc   ', '!*@@&@#UD*']))
    ['astra', '@@&@#U']
    
    which is equivalent to
    
    >>> a = map(lstrip, [' bbbastraccc   ', '!*@@&@#UD*'], ['b ', '!*'])
    >>> b = map(rstrip, a, [' c', '*D'])
    >>> list(b)
    ['astra', '@@&@#U']
    
    Should not be used for filter objects below in this file, but instead use sth like
    
    >>> ''.join(filter_uppercase(filter_letters('aaSSSa  12lpedplleplLPLPELPSOdedwo!@*@d')))
    'SSSLPLPELPSO'
    
    Should not be used for map objects below in this file, for example,
    
    >>> list(map_lstrip(map_rstrip(['  lwqsqwslpwsp ', ' ookedwlll  '], 'l '), 'o '))
    ['lwqsqwslpwsp', 'kedw']
    
    `map_lstrip`, `map_rstrip` have fixed stripping characters.
    '''
    argiter = iter(args)
    res = next(argiter, ())
    for map_, arg in zip_longest(maps_, argiter, fillvalue = ()):
        if map_ == (): break
        if hasattr(map_, '__iter__'):
            if arg != ():
                raise ValueError("Ambiguous extra arguments.")
            map_, *arg = map_
        res = map(map_, res, *arg)
    return res

dict_map = lambda x, y: map(lambda z: x[z], y)
dict_map_get = lambda x, y, default = None: map(lambda z: x.get(z, default), y)

strip  = lambda x, *args, **kwargs: x.strip(*args, **kwargs)
lstrip = lambda x, *args, **kwargs: x.lstrip(*args, **kwargs)
rstrip = lambda x, *args, **kwargs: x.rstrip(*args, **kwargs)

map_strip  = lambda x, *args, **kwargs: map(lambda y: y.strip(*args, **kwargs), x)
map_lstrip = lambda x, *args, **kwargs: map(lambda y: y.lstrip(*args, **kwargs), x)
map_rstrip = lambda x, *args, **kwargs: map(lambda y: y.rstrip(*args, **kwargs), x)
map_relu   = lambda x: map(lambda y: y if y >= 0 else 0, x)

def wordify(text, lstrip_chars = None, rstrip_chars = None):
    if lstrip_chars is not None: text = text.lstrip(lstrip_chars)
    if rstrip_chars is not None: text = text.rstrip(rstrip_chars)
    return filter_bool(text.split())

filter_strip      = lambda x, *args, **kwargs: filter(lambda y: y.strip(*args, **kwargs), x)
filter_lstrip     = lambda x, *args, **kwargs: filter(lambda y: y.lstrip(*args, **kwargs), x)
filter_rstrip     = lambda x, *args, **kwargs: filter(lambda y: y.rstrip(*args, **kwargs), x)
filter_map_strip  = lambda x, *args, **kwargs: map_strip(filter(lambda y: y.strip(*args, **kwargs), x), *args, **kwargs)
filter_map_lstrip = lambda x, *args, **kwargs: map_lstrip(filter(lambda y: y.lstrip(*args, **kwargs), x), *args, **kwargs)
filter_map_rstrip = lambda x, *args, **kwargs: map_rstrip(filter(lambda y: y.rstrip(*args, **kwargs), x), *args, **kwargs)
filter_odd        = lambda x: filter(lambda y: int(y) % 2, x)
filter_even       = lambda x: filter(lambda y: not int(y) % 2, x)

filter_none        = lambda x: filter(lambda y: y is None, x)
filter_bool        = lambda x: filter(lambda y: bool(y), x)
filter_digits      = lambda x: filter(lambda y: y in digits      if isinstance(y, str) else y in digits_b, x)
filter_uppercase   = lambda x: filter(lambda y: y in uppercase   if isinstance(y, str) else y in uppercase_b, x)
filter_lowercase   = lambda x: filter(lambda y: y in lowercase   if isinstance(y, str) else y in lowercase_b, x)
filter_letters     = lambda x: filter(lambda y: y in letters     if isinstance(y, str) else y in letters_b, x)
filter_hexlower    = lambda x: filter(lambda y: y in hexlower    if isinstance(y, str) else y in hexlower_b, x)
filter_hexupper    = lambda x: filter(lambda y: y in hexupper    if isinstance(y, str) else y in hexupper_b, x)
filter_hexdigits   = lambda x: filter(lambda y: y in hexdigits   if isinstance(y, str) else y in hexdigits_b, x)
filter_punctuation = lambda x: filter(lambda y: y in punctuation if isinstance(y, str) else y in punctuation_b, x)
filter_printable   = lambda x: filter(lambda y: y in printable   if isinstance(y, str) else y in printable_b, x)

filter_contains = lambda x, y: filter(lambda z: x in z, y)
filter_in       = lambda x, y: filter(lambda z: z in x, y)

unfilter_none        = lambda x: filter(lambda y: y is not None, x)
unfilter_bool        = lambda x: filter(lambda y: not bool(y), x)
unfilter_digits      = lambda x: filter(lambda y: y not in digits      if isinstance(y, str) else y not in digits_b, x)
unfilter_uppercase   = lambda x: filter(lambda y: y not in uppercase   if isinstance(y, str) else y not in uppercase_b, x)
unfilter_lowercase   = lambda x: filter(lambda y: y not in lowercase   if isinstance(y, str) else y not in lowercase_b, x)
unfilter_letters     = lambda x: filter(lambda y: y not in letters     if isinstance(y, str) else y not in letters_b, x)
unfilter_hexlower    = lambda x: filter(lambda y: y not in hexlower    if isinstance(y, str) else y not in hexlower_b, x)
unfilter_hexupper    = lambda x: filter(lambda y: y not in hexupper    if isinstance(y, str) else y not in hexupper_b, x)
unfilter_hexdigits   = lambda x: filter(lambda y: y not in hexdigits   if isinstance(y, str) else y not in hexdigits_b, x)
unfilter_punctuation = lambda x: filter(lambda y: y not in punctuation if isinstance(y, str) else y not in punctuation_b, x)
unfilter_printable   = lambda x: filter(lambda y: y not in printable   if isinstance(y, str) else y not in printable_b, x)

unfilter_contains = lambda x, y: filter(lambda z: x not in z, y)
unfilter_in       = lambda x, y: filter(lambda z: z not in x, y)

filter_true = filter_bool
filter_false = unfilter_bool
filter_notin = filter_not_in = unfilter_in
filter_ni = filter_contains
filter_notni = filter_not_ni = filter_notcontains = filter_not_contains = unfilter_contains

proj = lambda i: lambda arr: arr[i]

proj0 = proj_0 = lambda arr: arr[0]
proj1 = proj_1 = lambda arr: arr[1]
proj2 = proj_2 = lambda arr: arr[2]
proj3 = proj_3 = lambda arr: arr[3]
proj4 = proj_4 = lambda arr: arr[4]
proj5 = proj_5 = lambda arr: arr[5]
