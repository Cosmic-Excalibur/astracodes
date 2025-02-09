from sage.all import oo, Zmod, sign, ZZ
from Crypto.Util.number import long_to_bytes, bytes_to_long

l2b = long_to_bytes
b2l = bytes_to_long

_DEFAULT_BYTE_ENDIAN = 'msb'
_DEFAULT_BIT_ENDIAN = 'msb'
_DEFAULT_POLY_ENDIAN = 'msb'

def _check_endian(endian):
    if endian not in ('big', 'little', 'lsb', 'msb'):
        raise ValueError(f"Unknown endian '{endian}'.")

def set_default_endians(byte_endian = 'msb', bit_endian = 'msb', poly_endian = 'msb'):
    global _DEFAULT_BYTE_ENDIAN, _DEFAULT_BIT_ENDIAN, _DEFAULT_POLY_ENDIAN
    _check_endian(byte_endian)
    _check_endian(bit_endian)
    _check_endian(poly_endian)
    _DEFAULT_BYTE_ENDIAN = byte_endian
    _DEFAULT_BIT_ENDIAN = bit_endian
    _DEFAULT_POLY_ENDIAN = poly_endian

def get_default_endians():
    return {'byte': _DEFAULT_BYTE_ENDIAN, 'bit': _DEFAULT_BIT_ENDIAN, 'poly': _DEFAULT_POLY_ENDIAN}

def get_default_byte_endian():
    return _DEFAULT_BYTE_ENDIAN

def get_default_bit_endian():
    return _DEFAULT_BIT_ENDIAN

def get_default_poly_endian():
    return _DEFAULT_POLY_ENDIAN

def int_to_bytes(int_, blocksize = 0, endian = None):
    if endian is None: endian = _DEFAULT_BYTE_ENDIAN
    else: _check_endian(endian)
    res = long_to_bytes(int_, blocksize = blocksize)
    return res if endian in ('big', 'msb') else res[::-1]

i2b = int_to_bytes

def bytes_to_int(bytes_, endian = None):
    if endian is None: endian = _DEFAULT_BYTE_ENDIAN
    else: _check_endian(endian)
    return bytes_to_long(bytes_) if endian in ('big', 'msb') else b2l(bytes_[::-1])

b2i = bytes_to_int

def bytes_to_bitstr(bytes_, byte_endian = None, bit_endian = None):
    if byte_endian is None: byte_endian = _DEFAULT_BYTE_ENDIAN
    else: _check_endian(byte_endian)
    if bit_endian is None: bit_endian = _DEFAULT_BIT_ENDIAN
    else: _check_endian(bit_endian)
    res = ''.join(f'{b:08b}' for b in (bytes_ if byte_endian in ('big', 'msb') else reversed(bytes_)))
    return res if bit_endian in ('big', 'msb') else res[::-1]

b2bis = bytes_to_bitstr

def bytes_to_bits(bytes_, byte_endian = None, bit_endian = None):
    if byte_endian is None: byte_endian = _DEFAULT_BYTE_ENDIAN
    else: _check_endian(byte_endian)
    if bit_endian is None: bit_endian = _DEFAULT_BIT_ENDIAN
    else: _check_endian(bit_endian)
    return list(map(int, bytes_to_bitstr(bytes_, byte_endian = byte_endian, bit_endian = bit_endian)))

b2bi = bytes_to_bits

def bitstr_to_bytes(bitstr, byte_endian = None, bit_endian = None):
    if byte_endian is None: byte_endian = _DEFAULT_BYTE_ENDIAN
    else: _check_endian(byte_endian)
    if bit_endian is None: bit_endian = _DEFAULT_BIT_ENDIAN
    else: _check_endian(bit_endian)
    l = len(bitstr)
    rem = l % 8
    if bit_endian in ('little', 'lsb'):
        bitstr = bitstr[::-1]
    if byte_endian in ('big', 'msb'):
        if rem:
            return bytes([int(bitstr[:rem], 2)]) + bytes(int(bitstr[i:i+8], 2) for i in range(rem, l, 8))
        else:
            return bytes(int(bitstr[i:i+8], 2) for i in range(0, l, 8))
    else:
        if rem:
            return bytes([int(bitstr[-rem:], 2)]) + bytes(int(bitstr[i:i+8], 2) for i in reversed(range(0, l-rem, 8)))
        else:
            return bytes(int(bitstr[i:i+8], 2) for i in reversed(range(0, l, 8)))

bis2b = bitstr_to_bytes

def int_to_bitstr(int_, pad = None, endian = None):
    if endian is None: endian = _DEFAULT_BIT_ENDIAN
    else: _check_endian(endian)
    res = f'{int_:b}'
    if pad is not None: res = res.zfill(pad)
    return res if endian in ('big', 'msb') else res[::-1]

i2bis = int_to_bitstr

def int_to_bits(int_, pad = None, endian = None):
    return list(map(int, int_to_bitstr(int_, pad = pad, endian = endian)))

i2bi = int_to_bits

def bitstr_to_int(bitstr, endian = None):
    if endian is None: endian = _DEFAULT_BIT_ENDIAN
    else: _check_endian(endian)
    return int(bitstr, 2) if endian in ('big', 'msb') else int(bitstr[::-1], 2)

bis2i = bitstr_to_int

def bits_to_int(bits, endian = None):
    return bitstr_to_int(''.join(map(str, bits)), endian = endian)

bi2i = bits_to_int

def int_to_poly(int_, order = 2, endian = None, ring = None):
    if endian is None: endian = _DEFAULT_POLY_ENDIAN
    else: _check_endian(endian)
    if ring is None and order is not None:
        ring = Zmod(order)['x']
    elif ring is not None and order is None:
        order = ring.base_ring().order()
    elif ring is None and order is None:
        raise ValueError("Specify the order.")
    if order == 2:
        return ring(list(reversed(f'{abs(int_):b}'))) if endian in ('big', 'msb') else ring(list(f'{abs(int_):b}'))
    elif order is oo:
        raise ValueError("Infinite order.")
    elif order <= 1:
        raise ValueError("Order must be > 1.")
    res = []
    s = sign(int_)
    int_ *= s
    while int_:
        int_, rem = divmod(int_, order)
        res.append(rem * s)
    return ring(res) if endian in ('big', 'msb') else ring(res[::-1])

i2p = int_to_poly

def bitstr_to_poly(bitstr, order = 2, bit_endian = None, poly_endian = None, ring = None):
    if bit_endian is None: bit_endian = _DEFAULT_BIT_ENDIAN
    else: _check_endian(bit_endian)
    if poly_endian is None: poly_endian = _DEFAULT_POLY_ENDIAN
    else: _check_endian(poly_endian)
    if ring is None and order is not None:
        ring = Zmod(order)['x']
    elif ring is not None and order is None:
        order = ring.base_ring().order()
    elif ring is None and order is None:
        raise ValueError("Specify the order.")
    if order == 2:
        return ring(list(bitstr)) if (bit_endian in ('big', 'msb')) ^ (poly_endian in ('big', 'msb')) else ring(list(reversed(bitstr)))
    elif order is oo:
        raise ValueError("Infinite order.")
    elif order <= 1:
        raise ValueError("Order must be > 1.")
    int_ = int(bitstr, 2)
    res = []
    s = sign(int_)
    int_ *= s
    while int_:
        int_, rem = divmod(int_, order)
        res.append(rem * s)
    return ring(res) if poly_endian in ('big', 'msb') else ring(res[::-1])

bis2p = bitstr_to_poly

def bits_to_poly(bits, order = 2, bit_endian = None, poly_endian = None, ring = None):
    if bit_endian is None: bit_endian = _DEFAULT_BIT_ENDIAN
    else: _check_endian(bit_endian)
    if poly_endian is None: poly_endian = _DEFAULT_POLY_ENDIAN
    else: _check_endian(poly_endian)
    if ring is None and order is not None:
        ring = Zmod(order)['x']
    elif ring is not None and order is None:
        order = ring.base_ring().order()
    elif ring is None and order is None:
        raise ValueError("Specify the order.")
    if order == 2:
        return ring(bits) if (bit_endian in ('big', 'msb')) ^ (poly_endian in ('big', 'msb')) else ring(bits[::-1])
    elif order is oo:
        raise ValueError("Infinite order.")
    elif order <= 1:
        raise ValueError("Order must be > 1.")
    int_ = int(''.join(map(str, bits)), 2)
    res = []
    s = sign(int_)
    int_ *= s
    while int_:
        int_, rem = divmod(int_, order)
        res.append(rem * s)
    return ring(res) if poly_endian in ('big', 'msb') else ring(res[::-1])

bi2p = bits_to_poly

def poly_to_int(poly, order = None, endian = None):
    if endian is None: endian = _DEFAULT_POLY_ENDIAN
    else: _check_endian(endian)
    R = poly.base_ring()
    if order is None:
        order = R.order()
    if order is oo:
        raise ValueError("Infinite order.")
    elif order <= 1:
        raise ValueError("Order must be > 1.")
    if endian in ('little', 'lsb'):
        poly = R['x'](poly.list()[::-1])
    return poly.change_ring(ZZ)(order)

p2i = poly_to_int

if __name__ == '__main__':
    from utils.timeit import ticktock, timeit
    from rich.progress import track
    from pwn import bits_str
    from Crypto.Util.number import long_to_bytes as l2b
    from functools import reduce
    from logger.astra_logger import yellow_, blue_
    import os, random, itertools
    for cand in itertools.product(['lsb', 'msb'], repeat = 3):
        set_default_endians(*cand)
        print(blue_(get_default_endians()))
        with timeit():
            print('start = ', end = '') or print(yellow_(repr(reduce(lambda a, b: print(f'{yellow_(repr(a))}\n{b.__name__}({yellow_(repr(a))}) == ', end = '') or b(a), [b2i, i2bi, bi2p, p2i, i2bis, bis2b, b2bi, bi2p, p2i, i2b, b2bis, bis2i, i2b], b'\x81bitstruct.py is awesome!!\x81'))))
        print()
    N = 0
    n = 1000
    #N = 1000
    test = lambda bytes_: sum((list(map(int, bin(b)[2:].zfill(8))) for b in bytes_), [])
    a_better = 0
    for _ in track(range(N), description = '1'):
        c = os.urandom(n)
        ticktock()
        a = test(c)
        res1 = ticktock()
        b = bytes_to_bits(c)
        res2 = ticktock()
        assert a == b
        if res1 < res2: a_better += 1
    if N: print(a_better / N)
    N = 0
    # 0.0
    n = 2000
    #N = 10000
    a_better = 0
    for _ in track(range(N), description = '2'):
        c = os.urandom(n)
        ticktock()
        a = bits_str(c)
        res1 = ticktock()
        b = bytes_to_bitstr(c)
        res2 = ticktock()
        assert a == b
        if res1 < res2: a_better += 1
    if N: print(a_better / N)
    N = 0
    # 0.0034
    # The implementation from pwntools is slower :)
    n = 160005
    blocks = (n + 7) // 8
    #N = 10000
    test = lambda bitstr: l2b(int(c, 2), blocks)
    a_better = 0
    for _ in track(range(N), description = '3'):
        c = ''.join(random.choices('01', k = n))
        ticktock()
        a = test(c)
        res1 = ticktock()
        b = bitstr_to_bytes(c)
        res2 = ticktock()
        assert a == b
        if res1 < res2: a_better += 1
    if N: print(a_better / N)
    N = 0
    # 0.007
