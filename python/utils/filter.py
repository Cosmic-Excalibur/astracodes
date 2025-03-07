from utils.commonstrings import *


dict_map = lambda x, y: map(lambda z: x[z], y)
dict_map_get = lambda x, y, default = None: map(lambda z: x.get(z, default), y)

map_strip = lambda x, *args, **kwargs: map(lambda y: y.strip(*args, **kwargs), x)
map_relu  = lambda x: map(lambda y: y if y >= 0 else 0, x)

filter_strip     = lambda x, *args, **kwargs: filter(lambda y: y.strip(*args, **kwargs), x)
filter_map_strip = lambda x, *args, **kwargs: map_strip(filter(lambda y: y.strip(*args, **kwargs), x), *args, **kwargs)
filter_odd       = lambda x: filter(lambda y: int(y) % 2, x)
filter_even      = lambda x: filter(lambda y: not int(y) % 2, x)

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

unfilter_contains = lambda x, y: filter(lambda z: x not in z, y)
unfilter_in       = lambda x, y: filter(lambda z: z not in x, y)

filter_true = filter_bool
filter_false = unfilter_bool
filter_notin = filter_not_in = unfilter_in
filter_ni = filter_contains
filter_notni = filter_not_ni = filter_notcontains = filter_not_contains = unfilter_contains
