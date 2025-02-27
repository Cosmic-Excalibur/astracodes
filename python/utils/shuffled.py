from random import shuffle

def shuffled(x):
    tmp = list(x)
    shuffle(tmp)
    return type(x)(tmp)

def random_table(dom):
    ret = dict()
    dom_ = list(dom)
    for i, j in zip(dom_, shuffled(dom_)):
        ret[i] = j
    return ret
