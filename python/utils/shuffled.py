from random import shuffle
from typing import Sequence

def shuffled(x):
    tmp = list(x)
    shuffle(tmp)
    typ = type(x)
    return tmp if typ == range or issubclass(typ, Sequence) else typ(tmp)

def random_table(dom):
    ret = dict()
    dom_ = list(dom)
    for i, j in zip(dom_, shuffled(dom_)):
        ret[i] = j
    return ret
