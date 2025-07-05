from .block_cipher import (
    ECB_factory, CBC_factory, Modes,
    u32, p32, is_int
)


class TEA:

    @staticmethod
    def new(key, mode=Modes.ECB, *args, **kwargs):
        if not isinstance(key, (bytes, bytearray)):
            raise TypeError("`key` must be of type `bytes` or `bytearray`.")
        if len(key) != 16:
            raise TypeError(f"Incorrect TEA key length ({len(key)} bytes), expected 16 bytes.")
        key = bytes(key)
        if mode == Modes.ECB:
            return ECB_factory(_TEA_block, key, *args, **kwargs)
        elif mode == Modes.CBC:
            return CBC_factory(_TEA_block, key, *args, **kwargs)
        else:
            raise NotImplementedError(f"This mode for TEA cipher is not currently supported.")


class _TEA_block:

    def __init__(self, key, delta=0x9E3779B9, rounds=32):
        self.key = key
        self.block_size = 8
        if not is_int(delta):
            raise TypeError(f"`delta` (of type {type(delta)}) must be an integer.")
        self.delta = int(delta)
        if not is_int(rounds):
            raise TypeError(f"`rounds` (of type {type(rounds)}) must be an integer.")
        self.rounds = int(rounds)
        if self.rounds <= 0:
            raise TypeError(f"`rounds` must be a positive integer.")
    
    def encrypt_block(self, plain_text):
        v0 = u32(plain_text[:4])
        v1 = u32(plain_text[4:])
        x = 0
        k0 = u32(self.key[ 0: 4])
        k1 = u32(self.key[ 4: 8])
        k2 = u32(self.key[ 8:12])
        k3 = u32(self.key[12:16])
        for _ in range(self.rounds):
            x += self.delta
            x &= 0xFFFFFFFF
            v0 += ((v1 << 4) + k0) ^ (v1 + x) ^ ((v1 >> 5) + k1)
            v0 &= 0xFFFFFFFF
            v1 += ((v0 << 4) + k2) ^ (v0 + x) ^ ((v0 >> 5) + k3)
            v1 &= 0xFFFFFFFF
        return p32(v0) + p32(v1)
    
    def decrypt_block(self, cipher_text):
        v0 = u32(cipher_text[:4])
        v1 = u32(cipher_text[4:])
        x = self.rounds * self.delta & 0xFFFFFFFF
        k0 = u32(self.key[ 0: 4])
        k1 = u32(self.key[ 4: 8])
        k2 = u32(self.key[ 8:12])
        k3 = u32(self.key[12:16])
        for _ in range(self.rounds):
            v1 -= ((v0 << 4) + k2) ^ (v0 + x) ^ ((v0 >> 5) + k3)
            v1 &= 0xFFFFFFFF
            v0 -= ((v1 << 4) + k0) ^ (v1 + x) ^ ((v1 >> 5) + k1)
            v0 &= 0xFFFFFFFF
            x -= self.delta
            x &= 0xFFFFFFFF
        return p32(v0) + p32(v1)
