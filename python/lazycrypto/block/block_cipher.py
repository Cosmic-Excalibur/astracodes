from astrautils.int import is_int
from pwn import u8, p8, u16, p16, u32, p32, u64, p64, xor, context
from os import urandom
from typing import Sequence


def rol(n, k, word_size = None):
    word_size = word_size or context.word_size

    if not is_int(word_size) or word_size <= 0:
        raise ValueError("rol(): 'word_size' must be a strictly positive integer")

    if not is_int(k):
        raise ValueError("rol(): 'k' must be an integer")

    if isinstance(n, (bytes, bytearray, list, tuple)):
        return n[k % len(n):] + n[:k % len(n)]
    elif is_int(n):
        mask = (1 << word_size) - 1
        k %= word_size
        n &= mask
        n = (n << k) | (n >> (word_size - k))
        n &= mask
        return n
    else:
        raise ValueError("rol(): 'n' must be an integer, string, list or tuple")

def ror(n, k, word_size = None):
    word_size = word_size or context.word_size

    if not is_int(word_size) or word_size <= 0:
        raise ValueError("ror(): 'word_size' must be a strictly positive integer")

    if not is_int(k):
        raise ValueError("ror(): 'k' must be an integer")

    k = -k
    if isinstance(n, (bytes, bytearray, list, tuple)):
        return n[k % len(n):] + n[:k % len(n)]
    elif is_int(n):
        mask = (1 << word_size) - 1
        k %= word_size
        n &= mask
        n = (n << k) | (n >> (word_size - k))
        n &= mask
        return n
    else:
        raise ValueError("ror(): 'n' must be an integer, string, list or tuple")


class Modes:
    
    ECB = 1
    CBC = 2
    CFB = 3
    OFB = 4
    CTR = 5


def random_initialization_vector(block_size):
    return urandom(block_size)


class BlockCipher:
    
    def __init__(self):
        pass


class ECB_factory(BlockCipher):
    
    def __init__(self, factory, key, *args, **kwargs):
        super().__init__()
        self.block = factory(key, *args, **kwargs)
    
    def encrypt(self, plain_text):
        if not isinstance(plain_text, (bytes, bytearray)):
            raise TypeError("`plain_text` must be of type `bytes` or `bytearray`.")
        if len(plain_text) % self.block.block_size != 0:
            raise ValueError(f"`plain_text` must be aligned to block boundary ({self.block.block_size} byte(s)) in ECB mode.")
        cipher_text = b''
        for i in range(0, len(plain_text), self.block.block_size):
            cipher_text += self.block.encrypt_block(plain_text[i:i+self.block.block_size])
        plain_text = cipher_text
        return cipher_text
    
    def decrypt(self, cipher_text):
        if not isinstance(cipher_text, (bytes, bytearray)):
            raise TypeError("`cipher_text` must be of type `bytes` or `bytearray`.")
        if len(cipher_text) % self.block.block_size != 0:
            raise ValueError(f"`cipher_text` must be aligned to block boundary ({self.block.block_size} byte(s)) in ECB mode.")
        plain_text = b''
        for i in range(0, len(cipher_text), self.block.block_size):
            plain_text += self.block.decrypt_block(cipher_text[i:i+self.block.block_size])
        cipher_text = plain_text
        return plain_text


class CBC_factory(BlockCipher):
    
    def __init__(self, factory, key, *args, **kwargs):
        super().__init__()
        self.IV = None
        self._role = None
        if "IV" in kwargs:
            self.IV = kwargs["IV"]
            if not isinstance(self.IV, (bytes, bytearray)):
                raise TypeError("`IV` must be of type `bytes` or `bytearray`.")
            kwargs.pop("IV")
        self.block = factory(key, *args, **kwargs)
        if self.IV is None:
            self.IV = random_initialization_vector(self.block.block_size)
        if len(self.IV) != self.block.block_size:
            raise TypeError(f"Incorrect IV length ({len(self.IV)} bytes), expected {self.block.block_size} bytes.")
    
    def encrypt(self, plain_text):
        if self._role == 'decrypt':
            raise TypeError("encrypt() cannot be called after decrypt()")
        self._role = 'encrypt'
        if not isinstance(plain_text, (bytes, bytearray)):
            raise TypeError("`plain_text` must be of type `bytes` or `bytearray`.")
        if len(plain_text) % self.block.block_size != 0:
            raise ValueError(f"`plain_text` must be aligned to block boundary ({self.block.block_size} byte(s)) in ECB mode.")
        cipher_text = b''
        for i in range(0, len(plain_text), self.block.block_size):
            output = self.block.encrypt_block(xor(plain_text[i:i+self.block.block_size], self.IV))
            self.IV = output
            cipher_text += output
        plain_text = cipher_text
        return cipher_text
    
    def decrypt(self, cipher_text):
        if self._role == 'encrypt':
            raise TypeError("decrypt() cannot be called after encrypt()")
        self._role = 'decrypt'
        if not isinstance(cipher_text, (bytes, bytearray)):
            raise TypeError("`cipher_text` must be of type `bytes` or `bytearray`.")
        if len(cipher_text) % self.block.block_size != 0:
            raise ValueError(f"`cipher_text` must be aligned to block boundary ({self.block.block_size} byte(s)) in ECB mode.")
        plain_text = b''
        for i in range(0, len(cipher_text), self.block.block_size):
            input = cipher_text[i:i+self.block.block_size]
            plain_text += xor(self.block.decrypt_block(input), self.IV)
            self.IV = input
        cipher_text = plain_text
        return plain_text
