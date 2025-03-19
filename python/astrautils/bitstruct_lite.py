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

sde = set_default_endians

def get_default_endians():
    return {'byte': _DEFAULT_BYTE_ENDIAN, 'bit': _DEFAULT_BIT_ENDIAN, 'poly': _DEFAULT_POLY_ENDIAN}

gde = get_default_endians

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

def bytes_to_hex(bytes_, endian = None):
    if endian is None: endian = _DEFAULT_BYTE_ENDIAN
    else: _check_endian(endian)
    return bytes_.hex() if endian in ('big', 'msb') else bytes_[::-1].hex()

b2h = bytes_to_hex

def hex_to_bytes(hex_, endian = None):
    if endian is None: endian = _DEFAULT_BYTE_ENDIAN
    else: _check_endian(endian)
    if len(hex_) & 1:
        return bytes.fromhex('0'+hex_) if endian in ('big', 'msb') else bytes.fromhex('0'+hex_)[::-1]
    else:
        return bytes.fromhex(hex_) if endian in ('big', 'msb') else bytes.fromhex(hex_)[::-1]

h2b = hex_to_bytes

def hex_to_int(hex_):
    return int(hex_, 16)

h2i = hex_to_int

def int_to_hex(int_):
    res = f'{int_:x}'
    return '0' + res if len(res) & 1 else res

i2h = int_to_hex

def hex_to_bitstr(hex_, endian = None):
    if endian is None: endian = _DEFAULT_BIT_ENDIAN
    else: _check_endian(endian)
    res = ''.join(_HEX_2_BITSTR_TABLE[i] for i in hex_)
    return res if endian in ('big', 'msb') else res[::-1]

h2bis = hex_to_bitstr

def hex_to_bits(hex_, endian = None):
    if endian is None: endian = _DEFAULT_BIT_ENDIAN
    else: _check_endian(endian)
    res = ''.join(_HEX_2_BITSTR_TABLE[i] for i in hex_)
    return list(map(int, res)) if endian in ('big', 'msb') else list(map(int, res[::-1]))

h2bi = hex_to_bits

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

def _factory(a2i, i2b):
    return lambda x: i2b(a2i(x))

_abbr_table = {
    'int':    'i',
    'bits':   'bi',
    'bitstr': 'bis',
    'bytes':  'b',
    'hex':    'h'
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
