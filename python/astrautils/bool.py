from astrautils.commonstrings import *
import collections

def is_asciiprintable(s):
    if isinstance(s, str):
        return all(32 <= ord(x) <= 126 for x in s)
    else:
        return all(32 <= x <= 126 for x in s)


is_none        = lambda x: x is None
is_digits      = lambda x: all(y in digits      for y in x) if isinstance(x, str) else all(y in digits_b      for y in x)
is_uppercase   = lambda x: all(y in uppercase   for y in x) if isinstance(x, str) else all(y in uppercase_b   for y in x)
is_lowercase   = lambda x: all(y in lowercase   for y in x) if isinstance(x, str) else all(y in lowercase_b   for y in x)
is_letters     = lambda x: all(y in letters     for y in x) if isinstance(x, str) else all(y in letters_b     for y in x)
is_hexlower    = lambda x: all(y in hexlower    for y in x) if isinstance(x, str) else all(y in hexlower_b    for y in x)
is_hexupper    = lambda x: all(y in hexupper    for y in x) if isinstance(x, str) else all(y in hexupper_b    for y in x)
is_hexdigits   = lambda x: all(y in hexdigits   for y in x) if isinstance(x, str) else all(y in hexdigits_b   for y in x)
is_punctuation = lambda x: all(y in punctuation for y in x) if isinstance(x, str) else all(y in punctuation_b for y in x)

is_not_none        = lambda x: x is not None
is_not_digits      = lambda x: any(y not in digits      for y in x) if isinstance(x, str) else any(y not in digits_b      for y in x)
is_not_uppercase   = lambda x: any(y not in uppercase   for y in x) if isinstance(x, str) else any(y not in uppercase_b   for y in x)
is_not_lowercase   = lambda x: any(y not in lowercase   for y in x) if isinstance(x, str) else any(y not in lowercase_b   for y in x)
is_not_letters     = lambda x: any(y not in letters     for y in x) if isinstance(x, str) else any(y not in letters_b     for y in x)
is_not_hexlower    = lambda x: any(y not in hexlower    for y in x) if isinstance(x, str) else any(y not in hexlower_b    for y in x)
is_not_hexupper    = lambda x: any(y not in hexupper    for y in x) if isinstance(x, str) else any(y not in hexupper_b    for y in x)
is_not_hexdigits   = lambda x: any(y not in hexdigits   for y in x) if isinstance(x, str) else any(y not in hexdigits_b   for y in x)
is_not_punctuation = lambda x: any(y not in punctuation for y in x) if isinstance(x, str) else any(y not in punctuation_b for y in x)


def is_permutation_of(src, tgt):
    freq = collections.defaultdict(int)
    for i in tgt:
        freq[i] += 1
    for i in src:
        freq[i] -= 1
    return not any(freq.values())
            

