import string

_digits = string.digits
_uppercase = string.ascii_uppercase
_lowercase = string.ascii_lowercase
_letters = string.ascii_letters
_hexlower = '0123456789abcdef'
_hexupper = '0123456789ABCDEF'
_hexdigits = string.hexdigits
_punctuation = string.punctuation

_digits_b = _digits.encode('utf-8')
_uppercase_b = _uppercase.encode('utf-8')
_lowercase_b = _lowercase.encode('utf-8')
_letters_b = _letters.encode('utf-8')
_hexlower_b = _hexlower.encode('utf-8')
_hexupper_b = _hexupper.encode('utf-8')
_hexdigits_b = _hexdigits.encode('utf-8')
_punctuation_b = _punctuation.encode('utf-8')


map_strip = lambda x, *args, **kwargs: map(lambda y: y.strip(*args, **kwargs), x)

filter_strip     = lambda x, *args, **kwargs: filter(lambda y: y.strip(*args, **kwargs), x)
filter_map_strip = lambda x, *args, **kwargs: map_strip(filter(lambda y: y.strip(*args, **kwargs), x), *args, **kwargs)
filter_odd       = lambda x: filter(lambda y: int(y) % 2, x)
filter_even      = lambda x: filter(lambda y: not int(y) % 2, x)

filter_none        = lambda x: filter(lambda y: y is None, x)
filter_bool        = lambda x: filter(lambda y: bool(y), x)
filter_digits      = lambda x: filter(lambda y: y in _digits      if isinstance(y, str) else y in _digits_b, x)
filter_uppercase   = lambda x: filter(lambda y: y in _uppercase   if isinstance(y, str) else y in _uppercase_b, x)
filter_lowercase   = lambda x: filter(lambda y: y in _lowercase   if isinstance(y, str) else y in _lowercase_b, x)
filter_letters     = lambda x: filter(lambda y: y in _letters     if isinstance(y, str) else y in _letters_b, x)
filter_hexlower    = lambda x: filter(lambda y: y in _hexlower    if isinstance(y, str) else y in _hexlower_b, x)
filter_hexupper    = lambda x: filter(lambda y: y in _hexupper    if isinstance(y, str) else y in _hexupper_b, x)
filter_hexdigits   = lambda x: filter(lambda y: y in _hexdigits   if isinstance(y, str) else y in _hexdigits_b, x)
filter_punctuation = lambda x: filter(lambda y: y in _punctuation if isinstance(y, str) else y in _punctuation_b, x)

unfilter_none        = lambda x: filter(lambda y: y is not None, x)
unfilter_bool        = lambda x: filter(lambda y: not bool(y), x)
unfilter_digits      = lambda x: filter(lambda y: y not in _digits      if isinstance(y, str) else y not in _digits_b, x)
unfilter_uppercase   = lambda x: filter(lambda y: y not in _uppercase   if isinstance(y, str) else y not in _uppercase_b, x)
unfilter_lowercase   = lambda x: filter(lambda y: y not in _lowercase   if isinstance(y, str) else y not in _lowercase_b, x)
unfilter_letters     = lambda x: filter(lambda y: y not in _letters     if isinstance(y, str) else y not in _letters_b, x)
unfilter_hexlower    = lambda x: filter(lambda y: y not in _hexlower    if isinstance(y, str) else y not in _hexlower_b, x)
unfilter_hexupper    = lambda x: filter(lambda y: y not in _hexupper    if isinstance(y, str) else y not in _hexupper_b, x)
unfilter_hexdigits   = lambda x: filter(lambda y: y not in _hexdigits   if isinstance(y, str) else y not in _hexdigits_b, x)
unfilter_punctuation = lambda x: filter(lambda y: y not in _punctuation if isinstance(y, str) else y not in _punctuation_b, x)

filter_true = filter_bool
filter_false = unfilter_bool
