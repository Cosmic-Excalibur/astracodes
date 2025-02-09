from utils.timeit import ticktock, set_ticktock_log_func
from logger import astra_logger
alg = astra_logger

alg.set_debugging(True)
set_ticktock_log_func(None)

print(alg.colorify("ASTRAPYTHON -- LALLAALLLALLALALAALLLALLLALLALLALLALLLALLAAA :3"))
ticktock()

from sage.all import *
from sage.rings.factorint import factor_trial_division
var('x')

from pwn import *

from Crypto.Util.number import *
from Crypto.Cipher import AES, DES, DES3, ARC4
from Crypto.Util.Padding import pad, unpad
import hashlib
from hashlib import sha256, md5
import functools
import itertools
import tqdm
from rich.progress import track as track
richtrack = track
from rich import print as richprint
import gf2bv
import parse
import string
import random
from random import choice, choices, randint, randrange, getrandbits, randbytes
import sys
import os
from os import urandom
import re
from re import findall, match, finditer
from ast import literal_eval
import base64
from base64 import b64encode, b64decode


from utils.timeit import timeit, ticktock, set_ticktock_log_func
stlf = set_ticktock_log_func
from utils.gg import GG, set_hp, get_hp
gg = goodgame = GG
from utils import slicing
from utils.slicing import do_slice, set_fast_cutter_threshold, get_fast_cutter_threshold, cutter
set_fast_cutter_thres = sfct = set_fast_cutter_threshold
get_fast_cutter_thres = gfct = get_fast_cutter_threshold
from utils import varfactory
from utils.varfactory import V
import itertools_ex
from lazypwn import *
from lazymath.linsys import LinearizedSystem
linsys = Linsys = LinSys = LinearizedSystem
from lazycrypto.lattice.small_roots import small_roots
from lazycrypto.lattice.lll_cvp import *
from lazycrypto.lattice.primal_attack import primal_attack
from pow.powsolver import PoWSolver
powsolver = Powsolver = PoWSolver
from utils.peek import peek, peek_print
peekprint = peek_print
from utils.printname import printname
from utils.prgen import prgen, prgens
from utils.bitstruct import *
from lazycrypto.ecc.csidh import *
csidh = CSIDH
from lazymath.graycode import gray_code, gray_code_int, gray_code_poly, gray_code_bits, gray_code_bitstr, gray_code_str









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


alg.debug("Startup took %.4f second(s)." % ticktock())
print()

set_ticktock_log_func(print)
