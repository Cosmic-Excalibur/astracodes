# modified from https://github.com/apogiatzis/powsolver

import hashlib
import logging
import string
import pathos.multiprocessing as mp

from functools import partial
from itertools import product
from parse import parse, with_pattern
from re import finditer

from logger.astra_logger import debug, gray_, blue_

default_powfmt_1 = "{alg:^w}({inner:^_parse_inner}){:^_eqs}{target:^}"
default_powfmt_re_1 = r"[a-zA-Z0-9]+[ ]*\([a-zA-Z0-9\+ ]+\)[ ]*=+[ ]*[a-zA-Z0-9]+"

@with_pattern(r"=+")
def _eqs(text):
    return text

@with_pattern(r"[ ]*")
def _spaces(text):
    return text

@with_pattern(r"([a-zA-Z0-9]+[ ]*\+)?[ ]*[a-zA-Z0-9]+[ ]*(\+[ ]*[a-zA-Z0-9]+)?")
def _parse_inner(text):
    def are_unknowns(x):
        return len(set(x.lower())) == 1
    res = [x.strip() for x in text.split('+')]
    if len(res) == 3:
        return {'prefix': res[0], 'len': len(res[1]), 'suffix': res[2]}
    elif len(res) == 2:
        if are_unknowns(res[0]):
            return {'len': len(res[0]), 'suffix': res[1]}
        else:
            return {'prefix': res[0], 'len': len(res[1])}
    elif len(res) == 1:
        return {'len': len(res[0])}

class PoWSolver:
    def __init__(self, prog_tracker=None, parallel=False, charset=string.ascii_letters + string.digits, processes=8):
        self.charset = charset
        self.parallel = parallel
        self.processes = processes
        self.progress = prog_tracker is not None
        self.prog_tracker = (lambda x: x) if prog_tracker is None else prog_tracker

    def parse(self, pow_str, fmt = default_powfmt_1, regex = default_powfmt_re_1):
        """
        Uses a string format to parse parameters of the PoW puzzle
        """
        if regex is not None:
            pow_str = next(finditer(regex, pow_str)).group()
            debug("Regex match:", '"%s"' % gray_(pow_str))
        parsed = parse(fmt, pow_str, {'_parse_inner': _parse_inner, '_spaces': _spaces, '_eqs': _eqs})

        self.alg = getattr(hashlib, parsed["alg"])
        self.target = parsed["target"]
        self.len = parsed["inner"].get("len", 4)
        self.slice = slice(
            parsed["inner"].get("start", None),
            parsed["inner"].get("end", None),
            parsed["inner"].get("step", None),
        )
        self.prefix = parsed["inner"].get("prefix", "")
        self.suffix = parsed["inner"].get("suffix", "")
        debug("Parsed:", *(f"{x} = {blue_(repr(getattr(self, x)))}" for x in 'alg,target,len,slice,prefix,suffix,charset,parallel,processes'.split(',')))
        return self

    def solve(self):
        """
        Solves the given proof of work puzzle
        """
        return self.solve_parallel() if self.parallel else self.solve_sequential()
        

    def solve_sequential(self):
        """
        Solves the given proof of work puzzle in a sequential manner
        """
        gen = product(self.charset, repeat=self.len)
        if self.progress:
            gen = self.prog_tracker(gen, total=len(self.charset)**self.len)
        for proof in gen:
            proof = self.prefix.encode() + "".join(proof).encode() + self.suffix.encode()
            if self.valid_proof(proof):
                return proof[len(self.prefix):len(proof)-len(self.suffix)]
        return None

    def solve_parallel(self):
        """
        Solves the given proof of work puzzle in a parallel manner
        """
        pool = mp.Pool(self.processes)

        def test(x):
            return (x, self.valid_proof(x))

        gen = map(lambda s: self.prefix.encode() + ''.join(s).encode() + self.suffix.encode(), product(self.charset, repeat=self.len))
        if self.progress:
            gen = self.prog_tracker(gen, total=len(self.charset)**self.len)
        proofs = pool.imap_unordered(test, gen, chunksize=10000)
        pool.close()
        for proof, valid in proofs:
            if valid:
                pool.terminate()
                break
        pool.join()
        return proof[len(self.prefix):len(proof)-len(self.suffix)] if valid else None

    def valid_proof(self, proof):
        """Verifies that the proof matches the target"""
        h = self.alg(proof).hexdigest()[self.slice]
        return h == self.target
