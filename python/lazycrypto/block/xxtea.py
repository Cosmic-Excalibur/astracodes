from .block_cipher import (
    ECB_factory, CBC_factory, Modes,
    u32, p32, is_int
)


class XXTEA:

    @staticmethod
    def new(key, mode=Modes.ECB, *args, **kwargs):
        if not isinstance(key, (bytes, bytearray)):
            raise TypeError("`key` must be of type `bytes` or `bytearray`.")
        if len(key) != 16:
            raise TypeError(f"Incorrect XXTEA key length ({len(key)} bytes), expected 16 bytes.")
        key = bytes(key)
        if mode == Modes.ECB:
            return _XXTEA_block(key, *args, **kwargs)
        else:
            raise NotImplementedError(f"This mode for XXTEA cipher is not currently supported.")


class _XXTEA_block:

    def __init__(self, key, delta=0x9E3779B9, rounds_func=lambda n:6+52//n):
        self.key = key
        self.block_size = 4
        if not is_int(delta):
            raise TypeError(f"`delta` (of type {type(delta)}) must be an integer.")
        self.delta = int(delta)
        self.rounds_func = rounds_func
    
    def _shift(self, z, y, x, k, p, e):
        return ((((z >> 5) ^ (y << 2)) + ((y >> 3) ^ (z << 4))) ^ ((x ^ y) + (k[(p & 3) ^ e] ^ z)))
    
    def encrypt(self, plain_text):
        if not isinstance(plain_text, (bytes, bytearray)):
            raise TypeError("`plain_text` must be of type `bytes` or `bytearray`.")
        if len(plain_text) % self.block_size != 0:
            raise ValueError(f"`plain_text` must be aligned to block boundary ({self.block_size} byte(s)) in ECB mode.")
        v = [u32(plain_text[i:i+4]) for i in range(0, len(plain_text), 4)]
        if not v: return b''
        n = len(v)
        rounds = self.rounds_func(n)
        k = [u32(self.key[i:i+4]) for i in range(0, 16, 4)] 
        x = 0
        z = v[n - 1]
        for _ in range(rounds):
            x = (x + self.delta) & 0xFFFFFFFF
            e = (x >> 2) & 3
            for p in range(n - 1):
                y = v[p + 1]
                v[p] = (v[p] + self._shift(z, y, x, k, p, e)) & 0xFFFFFFFF
                z = v[p]
            p += 1
            y = v[0]
            v[n - 1] = (v[n - 1] + self._shift(z, y, x, k, p, e)) & 0xFFFFFFFF
            z = v[n - 1]
        return b''.join(map(p32, v))
    
    def decrypt(self, cipher_text):
        if not isinstance(cipher_text, (bytes, bytearray)):
            raise TypeError("`cipher_text` must be of type `bytes` or `bytearray`.")
        if len(cipher_text) % self.block_size != 0:
            raise ValueError(f"`cipher_text` must be aligned to block boundary ({self.block_size} byte(s)) in ECB mode.")
        v = [u32(cipher_text[i:i+4]) for i in range(0, len(cipher_text), 4)]
        if not v: return b''
        n = len(v)
        rounds = self.rounds_func(n)
        k = [u32(self.key[i:i+4]) for i in range(0, 16, 4)] 
        x = (rounds * self.delta) & 0xFFFFFFFF
        y = v[0]
        for _ in range(rounds):
            e = (x >> 2) & 3
            for p in range(n - 1, 0, -1):
                z = v[p - 1]
                v[p] = (v[p] - self._shift(z, y, x, k, p, e)) & 0xFFFFFFFF
                y = v[p]
            p -= 1
            z = v[n - 1]
            v[0] = (v[0] - self._shift(z, y, x, k, p, e)) & 0xFFFFFFFF
            y = v[0]
            x = (x - self.delta) & 0xFFFFFFFF
        return b''.join(map(p32, v))
