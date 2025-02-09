from utils.bitstruct import int_to_bits, int_to_bitstr, int_to_poly

def gray_code_int(n):
    for i in range(1 << n):
        yield i ^ (i >> 1)

def gray_code_bitstr(n, *args, **kwargs):
    for i in range(1 << n):
        yield int_to_bitstr(i ^ (i >> 1), n, *args, **kwargs)

def gray_code_bits(n, *args, **kwargs):
    for i in range(1 << n):
        yield int_to_bits(i ^ (i >> 1), n, *args, **kwargs)

def gray_code_poly(n, *args, **kwargs):
    for i in range(1 << n):
        yield int_to_poly(i ^ (i >> 1), 2, *args, **kwargs)

def gray_code(n, zero = 0, one = 1):
    fmt = '{0:0%db}' % n
    mapping = lambda x: one if x == '1' else zero
    for i in range(1 << n):
        yield list(map(mapping, fmt.format(i ^ (i >> 1))))

def gray_code_str(n, zero: str = '0', one: str = '1'):
    fmt = '{0:0%db}' % n
    for i in range(1 << n):
        yield fmt.format(i ^ (i >> 1)).replace('0', zero).replace('1', one)
