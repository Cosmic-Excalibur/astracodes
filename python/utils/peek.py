from logger.astra_logger import *

def peek(needle, mess, stride = 10):
    i = -1
    l = len(needle) if hasattr(needle, '__len__') else 1
    while True:
        try:
            i = mess.index(needle, i+1)
            yield mess[max(i-stride,0):i+l+stride]
        except ValueError:
            return

def peek_print(needle: str, mess: str, stride = 10, pos = True, printer = print, color = True, bound = True, ret = False):
    g = _peek_print(needle, mess, stride = stride, pos = pos, printer = printer, color = color, bound = bound)
    if ret:
        return g
    else:
        for _ in g: pass

def _peek_print(needle: str, mess: str, stride = 10, pos = True, printer = print, color = True, bound = True):
    assert stride >= 0
    i = -len(mess)-1
    l = len(needle)
    L = len(mess)
    ell = '…'
    if color: ell = gray_(ell)
    endleft = '“'
    if color: endleft = gray_(endleft)
    endright = '”'
    if color: endright = gray_(endright)
    colored_needle = red_(needle) if color else needle
    head = f'%{len(str(L))}d: '
    if color: head = yellow_(head)
    while True:
        i = mess.find(needle, i+1)
        if i == -1:
            return
        res = ''
        if pos:
            res += head % i
        if i > stride:
            left = mess[i-stride:i]
            if bound: res += ell
        else:
            left = mess[:i]
            if bound: res += endleft
        if i+l+stride < L:
            right = mess[i+l:i+l+stride]
            if bound: right += endright
        else:
            right = mess[i+l:]
        res += left
        res += colored_needle
        res += right
        printer(res)
        yield i, mess[max(0,i-stride):i+l+stride]
