from logger.astra_logger import *

def wordle(tgt: str, guesses: str, do_print = True):
    TGT = tgt.upper()
    res = []
    for guess in guesses:
        assert len(guess) == len(TGT)
        tmp = []
        GUESS = guess.upper()
        for T, L in zip(TGT, GUESS):
            if L == T:
                if do_print: print(green_(L), end = '')
                tmp.append(2)
            elif L in TGT:
                if do_print: print(yellow_(L), end = '')
                tmp.append(1)
            else:
                if do_print: print(gray_(L), end = '')
                tmp.append(0)
        if do_print: print()
        res.append(tmp)
    return res
