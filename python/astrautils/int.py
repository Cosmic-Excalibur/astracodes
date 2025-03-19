def int_decode_strip(s, base = 10, encoding = 'utf-8', errors = 'strict', chars = None):
    return int(s.decode(encoding = encoding, errors = errors).strip(chars = chars), base = base)

intsd = intds = int_strip_decode = int_decode_strip

def int0_decode_strip(s, encoding = 'utf-8', errors = 'strict', chars = None):
    return int(s.decode(encoding = encoding, errors = errors).strip(chars = chars), base = 0)

int0sd = int0ds = int0_strip_decode = int0_decode_strip

def nbits(n):
    return n.bit_length()

def bit_count(n):
    return n.bit_count()

bitcount = bit_count
