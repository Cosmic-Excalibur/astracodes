from .block_cipher import (
    ECB_factory, CBC_factory, Modes,
    u16, p16, u32, p32, u64, p64, is_int, rol, ror
)


class RC5:

    @staticmethod
    def new(key, mode=Modes.ECB, *args, **kwargs):
        if not isinstance(key, (bytes, bytearray)):
            raise TypeError("`key` must be of type `bytes` or `bytearray`.")
        key = bytes(key)
        if mode == Modes.ECB:
            return ECB_factory(_RC5_block, key, *args, **kwargs)
        elif mode == Modes.CBC:
            return CBC_factory(_RC5_block, key, *args, **kwargs)
        else:
            raise NotImplementedError(f"This mode for RC5 cipher is not currently supported.")


class _RC5_block:

    def __init__(self, key, word_size=32, rounds=12, Pw=None, Qw=None):
        self.key = key
        if not is_int(word_size) or word_size & 7:
            raise ValueError(f"Invalid word bits.")
        self.w = int(word_size)
        if self.w not in {16, 32, 64}:
            raise ValueError(f"{self.w} bits for RC5 is not currently supported.")
        Pw_table = {
            16: 0xB7E1,
            32: 0xB7E15163,
            64: 0xB7E151628AED2A6B
        }
        Qw_table = {
            16: 0x9E37,
            32: 0x9E3779B9,
            64: 0x9E3779B97F4A7C15
        }
        self.u = self.w >> 3
        self.mask = (1 << self.w) - 1
        self.block_size = self.u * 2
        self.uxx = {16: u16, 32: u32, 64: u64}[self.w]
        self.pxx = {16: p16, 32: p32, 64: p64}[self.w]
        self.b = len(key)
        if self.b == 0:
            raise ValueError(f"Invalid RC5 key.")
        elif self.b % self.u:
            raise ValueError(f"Misaligned key ({self.b} bytes).")
        self.c = self.b // self.u
        if not is_int(rounds):
            raise TypeError(f"`rounds` must be an integer.")
        self.rounds = int(rounds)
        if self.rounds <= 0:
            raise TypeError(f"`rounds` must be a positive integer.")
        if Pw is None:
            self.Pw = Pw_table[self.w]
        else:
            if is_int(Pw):
                self.Pw = int(Pw)
                if self.Pw < 0 or self.Pw.bit_length() > self.w:
                    raise ValueError(f"Oversized `Pw`.")
            else:
                raise ValueError(f"Invalid `Pw`.")
        if Qw is None:
            self.Qw = Qw_table[word_size]
        else:
            if is_int(Qw):
                self.Qw = int(Qw)
                if self.Qw < 0 or self.Qw.bit_length() > self.w:
                    raise ValueError(f"Oversized `Qw`.")
            else:
                raise ValueError(f"Invalid `Qw`.")

        self.S = [None] * (2*(self.rounds+1))
        self.t = 2*(self.rounds+1)
        self.key_schedule()
    
    def key_schedule(self):
        L = [None] * self.c
        L[self.c-1] = 0
        for i in reversed(range(0, self.b, self.u)):
            L[i//self.u] = int.from_bytes(self.key[i:i+self.u], 'little')
        
        self.S[0] = self.Pw
        for i in range(1, self.t):
            self.S[i] = self.S[i-1] + self.Qw
        
        A = B = 0
        i = j = 0
        for k in range(3*self.t):
            i = k % self.t
            j = k % self.c
            A = self.S[i] = rol(self.S[i] + (A + B), 3, self.w)
            B = L[j] = rol(L[j] + (A + B), A + B, self.w)
    
    def encrypt_block(self, plain_text):
        A = self.uxx(plain_text[:self.u]) + self.S[0]
        B = self.uxx(plain_text[self.u:]) + self.S[1]
        for i in range(1, self.rounds + 1):
            A = rol(A ^ B, B, self.w) + self.S[2*i]
            B = rol(B ^ A, A, self.w) + self.S[2*i + 1]
        return self.pxx(A & self.mask) + self.pxx(B & self.mask)
    
    def decrypt_block(self, cipher_text):
        A = self.uxx(cipher_text[:self.u])
        B = self.uxx(cipher_text[self.u:])
        for i in range(self.rounds, 0, -1):
            B = ror(B - self.S[2*i + 1], A, self.w) ^ A
            A = ror(A - self.S[2*i], B, self.w) ^ B
        B -= self.S[1]
        A -= self.S[0]
        return self.pxx(A & self.mask) + self.pxx(B & self.mask)
