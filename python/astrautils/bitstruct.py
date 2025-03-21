from sage.all import oo, Zmod, sign, ZZ
from Crypto.Util.number import long_to_bytes, bytes_to_long
import itertools

l2b = long_to_bytes
b2l = bytes_to_long

_HEX_2_BITSTR_TABLE = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'a': '1010',
    'b': '1011',
    'c': '1100',
    'd': '1101',
    'e': '1110',
    'f': '1111'
}

_DEFAULT_BYTE_ENDIAN = 'msb'
_DEFAULT_BIT_ENDIAN  = 'msb'
_DEFAULT_POLY_ENDIAN = 'msb'
_DEFAULT_ADIC_ENDIAN = 'lsb'

def _check_endian(endian):
    if endian not in ('big', 'little', 'lsb', 'msb'):
        raise ValueError(f"Unknown endian '{endian}'.")

def set_default_endians(byte_endian = 'msb', bit_endian = 'msb', poly_endian = 'msb', adic_endian = 'lsb'):
    global _DEFAULT_BYTE_ENDIAN, _DEFAULT_BIT_ENDIAN, _DEFAULT_POLY_ENDIAN, _DEFAULT_ADIC_ENDIAN
    _check_endian(byte_endian)
    _check_endian(bit_endian)
    _check_endian(poly_endian)
    _check_endian(adic_endian)
    _DEFAULT_BYTE_ENDIAN = byte_endian
    _DEFAULT_BIT_ENDIAN  = bit_endian
    _DEFAULT_POLY_ENDIAN = poly_endian
    _DEFAULT_ADIC_ENDIAN = adic_endian

sde = set_default_endians

def get_default_endians():
    return {
        'byte': _DEFAULT_BYTE_ENDIAN,
        'bit':  _DEFAULT_BIT_ENDIAN,
        'poly': _DEFAULT_POLY_ENDIAN,
        'adic': _DEFAULT_ADIC_ENDIAN
    }

gde = get_default_endians

def get_default_byte_endian():
    return _DEFAULT_BYTE_ENDIAN

def get_default_bit_endian():
    return _DEFAULT_BIT_ENDIAN

def get_default_poly_endian():
    return _DEFAULT_POLY_ENDIAN

def get_default_adic_endian():
    return _DEFAULT_ADIC_ENDIAN

def int_to_bytes(int_, blocksize = 0, byte_endian = None, **kwargs):
    if byte_endian is None: byte_endian = _DEFAULT_BYTE_ENDIAN
    else: _check_endian(byte_endian)
    res = long_to_bytes(int_, blocksize = blocksize)
    return res if byte_endian in ('big', 'msb') else res[::-1]

i2b = int_to_bytes

def bytes_to_int(bytes_, byte_endian = None, **kwargs):
    if byte_endian is None: byte_endian = _DEFAULT_BYTE_ENDIAN
    else: _check_endian(byte_endian)
    return bytes_to_long(bytes_) if byte_endian in ('big', 'msb') else b2l(bytes_[::-1])

b2i = bytes_to_int

def bytes_to_bitstr(bytes_, byte_endian = None, bit_endian = None, **kwargs):
    if byte_endian is None: byte_endian = _DEFAULT_BYTE_ENDIAN
    else: _check_endian(byte_endian)
    if bit_endian is None: bit_endian = _DEFAULT_BIT_ENDIAN
    else: _check_endian(bit_endian)
    res = ''.join(f'{b:08b}' for b in (bytes_ if byte_endian in ('big', 'msb') else reversed(bytes_)))
    return res if bit_endian in ('big', 'msb') else res[::-1]

b2bis = bytes_to_bitstr

def bytes_to_bits(bytes_, byte_endian = None, bit_endian = None, **kwargs):
    if byte_endian is None: byte_endian = _DEFAULT_BYTE_ENDIAN
    else: _check_endian(byte_endian)
    if bit_endian is None: bit_endian = _DEFAULT_BIT_ENDIAN
    else: _check_endian(bit_endian)
    return list(map(int, bytes_to_bitstr(bytes_, byte_endian = byte_endian, bit_endian = bit_endian)))

b2bi = bytes_to_bits

def bitstr_to_bytes(bitstr, byte_endian = None, bit_endian = None, **kwargs):
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

def int_to_bitstr(int_, pad = None, bit_endian = None, **kwargs):
    if bit_endian is None: bit_endian = _DEFAULT_BIT_ENDIAN
    else: _check_endian(bit_endian)
    res = f'{int_:b}'
    if pad is not None: res = res.zfill(pad)
    return res if bit_endian in ('big', 'msb') else res[::-1]

i2bis = int_to_bitstr

def int_to_bits(int_, pad = None, bit_endian = None, **kwargs):
    return list(map(int, int_to_bitstr(int_, pad = pad, bit_endian = bit_endian)))

i2bi = int_to_bits

def bitstr_to_int(bitstr, bit_endian = None, **kwargs):
    if bit_endian is None: bit_endian = _DEFAULT_BIT_ENDIAN
    else: _check_endian(bit_endian)
    return int(bitstr, 2) if bit_endian in ('big', 'msb') else int(bitstr[::-1], 2)

bis2i = bitstr_to_int

def bits_to_int(bits, bit_endian = None, **kwargs):
    return bitstr_to_int(''.join(map(str, bits)), bit_endian = bit_endian)

bi2i = bits_to_int

def bytes_to_hex(bytes_, byte_endian = None, **kwargs):
    if byte_endian is None: byte_endian = _DEFAULT_BYTE_ENDIAN
    else: _check_endian(byte_endian)
    return bytes_.hex() if byte_endian in ('big', 'msb') else bytes_[::-1].hex()

b2h = bytes_to_hex

def hex_to_bytes(hex_, byte_endian = None, **kwargs):
    if byte_endian is None: byte_endian = _DEFAULT_BYTE_ENDIAN
    else: _check_endian(byte_endian)
    if len(hex_) & 1:
        return bytes.fromhex('0'+hex_) if byte_endian in ('big', 'msb') else bytes.fromhex('0'+hex_)[::-1]
    else:
        return bytes.fromhex(hex_) if byte_endian in ('big', 'msb') else bytes.fromhex(hex_)[::-1]

h2b = hex_to_bytes

def hex_to_int(hex_, **kwargs):
    return int(hex_, 16)

h2i = hex_to_int

def int_to_hex(int_, **kwargs):
    res = f'{int_:x}'
    return '0' + res if len(res) & 1 else res

i2h = int_to_hex

def hex_to_bitstr(hex_, bit_endian = None, **kwargs):
    if bit_endian is None: bit_endian = _DEFAULT_BIT_ENDIAN
    else: _check_endian(bit_endian)
    res = ''.join(_HEX_2_BITSTR_TABLE[i] for i in hex_)
    return res if bit_endian in ('big', 'msb') else res[::-1]

h2bis = hex_to_bitstr

def hex_to_bits(hex_, bit_endian = None, **kwargs):
    if bit_endian is None: bit_endian = _DEFAULT_BIT_ENDIAN
    else: _check_endian(bit_endian)
    res = ''.join(_HEX_2_BITSTR_TABLE[i] for i in hex_)
    return list(map(int, res)) if bit_endian in ('big', 'msb') else list(map(int, res[::-1]))

h2bi = hex_to_bits

def int_to_poly(int_, order = 2, poly_endian = None, ring = None, **kwargs):
    if poly_endian is None: poly_endian = _DEFAULT_POLY_ENDIAN
    else: _check_endian(poly_endian)
    if ring is None and order is not None:
        ring = Zmod(order)['x']
    elif ring is not None and order is None:
        order = ring.base_ring().order()
    elif ring is None and order is None:
        raise ValueError("Specify the order.")
    if order == 2:
        return ring(list(reversed(f'{abs(int_):b}'))) if poly_endian in ('big', 'msb') else ring(list(f'{abs(int_):b}'))
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
    return ring(res) if poly_endian in ('big', 'msb') else ring(res[::-1])

i2p = int_to_poly

def bitstr_to_poly(bitstr, order = 2, bit_endian = None, poly_endian = None, ring = None, **kwargs):
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

def bits_to_poly(bits, order = 2, bit_endian = None, poly_endian = None, ring = None, **kwargs):
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

def poly_to_int(poly, order = None, poly_endian = None, **kwargs):
    if poly_endian is None: poly_endian = _DEFAULT_POLY_ENDIAN
    else: _check_endian(poly_endian)
    R = poly.base_ring()
    if order is None:
        order = R.order()
    if order is oo:
        raise ValueError("Infinite order.")
    elif order <= 1:
        raise ValueError("Order must be > 1.")
    if poly_endian in ('little', 'lsb'):
        poly = R['x'](poly.list()[::-1])
    return poly.change_ring(ZZ)(order)

p2i = poly_to_int

def int_to_adic(n, base = 2, pad = None, adic_endian = None, **kwargs):
    if adic_endian is None: adic_endian = _DEFAULT_ADIC_ENDIAN
    else: _check_endian(adic_endian)
    n = int(n)
    if n < 0:
        raise ValueError("Integer cannot be negative.")
    elif base <= 1:
        raise ValueError("Base must be > 1.")
    res = []
    if pad is None: pad = 0
    while n:
        if adic_endian in ('little', 'lsb'):
            res.append(n % base)
        else:
            res.insert(0, n % base)
        n //= base
        pad -= 1
    if pad > 0:
        if adic_endian in ('little', 'lsb'):
            res += [0] * pad
        else:
            res = [0] * pad + res
    return res

i2a = int_to_adic

def adic_to_int(arr, base = 2, adic_endian = None, **kwargs):
    if adic_endian is None: adic_endian = _DEFAULT_ADIC_ENDIAN
    else: _check_endian(adic_endian)
    if base <= 1:
        raise ValueError("Base must be > 1.")
    res = 0
    k = 1
    for i in arr if adic_endian in ('little', 'lsb') else reversed(arr):
        i = int(i)
        if i >= base or i < 0:
            raise ValueError(f'Invalid component "{i}".')
        res += k*i
        k *= base
    return res

a2i = adic_to_int

def _factory(a2i, i2b):
    return lambda x, *args, **kwargs: i2b(a2i(x, *args, **kwargs), *args, **kwargs)

_abbr_table = {
    'int':    'i',
    'bits':   'bi',
    'bitstr': 'bis',
    'bytes':  'b',
    'poly':   'p',
    'hex':    'h',
    'adic':   'a'
}

for (_a, _abbr_a), (_b, _abbr_b) in itertools.permutations(_abbr_table.items(), 2):
    _name = f'{_a}_to_{_b}'
    _abbr_name = f'{_abbr_a}2{_abbr_b}'
    if _abbr_name not in globals():
        assert _abbr_a != 'i' and _abbr_b != 'i'
        _a2i = globals()[f'{_abbr_a}2i']
        _i2b = globals()[f'i2{_abbr_b}']
        _func = _factory(_a2i, _i2b)
        globals()[_name] = globals()[_abbr_name] = _func

if __name__ == '__main__':
    from astrautils.timeit import ticktock, timeit
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
