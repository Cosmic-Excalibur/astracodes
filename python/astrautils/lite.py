from astrautils.bitstruct_lite import *
from astrautils.bool import *
from astrautils.counter import *
from astrautils.filter import *
from astrautils.gg import GG, set_hp, get_hp
gg = goodgame = GG
from astrautils.path import *
from astrautils.peek import peek, peek_print
peekprint = peek_print
from astrautils.printname import *
from astrautils.shuffled import *
from astrautils import slicing
from astrautils.slicing import do_slice, set_fast_cutter_threshold, get_fast_cutter_threshold, cutter, long_range
set_fast_cutter_thres = sfct = set_fast_cutter_threshold
get_fast_cutter_thres = gfct = get_fast_cutter_threshold
from astrautils.timeit import *
stlf = set_ticktock_log_func
from astrautils.wrapper import *

from logger import astra_logger as alg
