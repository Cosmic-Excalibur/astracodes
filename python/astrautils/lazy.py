from astrautils.timeit import ticktock, set_ticktock_log_func
from logger import astra_logger
alg = astra_logger

alg.set_debugging(True)
set_ticktock_log_func(None)

print(alg.colorify("ASTRAPYTHON -- Good luck coding LALLAALLLALLALALAALLLALLLALALLAAA :3"))
ticktock()

from rich.progress import Progress

import sys

_import_cnt = 0

with Progress() as _progress:
    _startup_task = _progress.add_task("Preparing...", total = 1756)
    class _Watcher:
        @classmethod
        def find_module(cls, name, path, target = None):
            global _import_cnt
            _import_cnt += 1
            _progress.update(_startup_task, advance = 1)
            return None
    sys.meta_path.insert(0, _Watcher)
    
    from sage.all import *
    from sage.rings.factorint import factor_trial_division
    from sage.schemes.elliptic_curves.mod_poly import classical_modular_polynomial
    from sage.rings.number_field.order_ideal import NumberFieldOrderIdeal
    var('x')

    from sage.all import load

    from Crypto.Util.number import *
    from Crypto.Cipher import AES, DES, DES3, ARC4
    from Crypto.Util.Padding import pad, unpad
    import hashlib
    from hashlib import sha256, md5, sha1
    import functools
    from functools import partial
    import itertools
    from itertools import permutations, combinations, product, chain
    import tqdm
    from rich.progress import track as track
    richtrack = track
    from rich import print as richprint
    import gf2bv
    import parse
    import string
    import random
    from random import choice, choices, randint, randrange, getrandbits, randbytes, shuffle
    import sys
    import os
    import struct
    from os import urandom
    import re
    from re import findall, match, finditer
    from ast import literal_eval
    import base64
    from base64 import b64encode, b64decode
    from gf2bv import LinearSystem
    gf2linsys = LinearSystem
    from gf2bv.crypto.mt import MT19937
    from urllib.parse import quote, unquote
    import difflib


    
    from astrapython_buoy import *
    
    import itertools_ex
    
    from lazycrypto.ecc.csidh import *
    csidh = CSIDH
    from lazycrypto.lattice.coppersmith import *
    from lazycrypto.lattice.lll_cvp import *
    from lazycrypto.lattice.primal_attack import primal_attack
    from lazycrypto.lattice.small_roots import small_roots
    
    from lazymath import babydiop
    from lazymath.graycode import *
    from lazymath.linsys import LinearizedSystem
    linsys = Linsys = LinSys = LinearizedSystem
    
    from lazypwn import *
    restore('log')
    
    from pow.powsolver import PoWSolver
    powsolver = Powsolver = PoWSolver
    
    from astrautils.all import *
    
    
    
    sys.meta_path.pop(0)









def astrapython_banner():
    print(alg.colorify(r"""
 ██████\   ██████\ ████████\ ███████\   ██████\              
██  __██\ ██  __██\\__██  __|██  __██\ ██  __██\             
██ /  ██ |██ /  \__|  ██ |   ██ |  ██ |██ /  ██ |            
████████ |\██████\    ██ |   ███████  |████████ |            
██  __██ | \____██\   ██ |   ██  __██< ██  __██ |            
██ |  ██ |██\   ██ |  ██ |   ██ |  ██ |██ |  ██ |            
██ |  ██ |\██████  |  ██ |   ██ |  ██ |██ |  ██ |            
\__|  \__| \______/   \__|   \__|  \__|\__|  \__|            
                                                             
                                                             
                                                             
███████\ ██\     ██\ ████████\ ██\   ██\  ██████\  ██\   ██\ 
██  __██\\██\   ██  |\__██  __|██ |  ██ |██  __██\ ███\  ██ |
██ |  ██ |\██\ ██  /    ██ |   ██ |  ██ |██ /  ██ |████\ ██ |
███████  | \████  /     ██ |   ████████ |██ |  ██ |██ ██\██ |
██  ____/   \██  /      ██ |   ██  __██ |██ |  ██ |██ \████ |
██ |         ██ |       ██ |   ██ |  ██ |██ |  ██ |██ |\███ |
██ |         ██ |       ██ |   ██ |  ██ | ██████  |██ | \██ |
\__|         \__|       \__|   \__|  \__| \______/ \__|  \__|



Astrageldon's personal python :3


"""))


alg.debug("Startup took %.4f second(s) with %d import attempt(s)." % (ticktock(), _import_cnt))
print()

set_ticktock_log_func(print)
