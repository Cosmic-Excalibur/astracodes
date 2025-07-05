def int_decode_strip(s, base = 10, encoding = 'utf-8', errors = 'strict', chars = None):
    return int(s.decode(encoding = encoding, errors = errors).strip(chars), base = base)

intsd = intds = int_strip_decode = int_decode_strip

def int0_decode_strip(s, encoding = 'utf-8', errors = 'strict', chars = None):
    return int(s.decode(encoding = encoding, errors = errors).strip(chars), base = 0)

int0sd = int0ds = int0_strip_decode = int0_decode_strip

def nbits(n):
    b, m = is_int_int(n)
    assert b
    return m.bit_length()

def bit_count(n):
    b, m = is_int_int(n)
    assert b
    return m.bit_count()

bitcount = bit_count
bit_length = bitlength = nbits

def is_int(n):
    return hasattr(n, '__int__') and int(n) == n

def is_int_int(n):
    if not hasattr(n, '__int__'):
        return False, None
    else:
        m = int(n)
        return n == m, m
