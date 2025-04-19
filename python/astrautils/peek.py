from logger.astra_logger import *

def peek(needle, haystack, vision = 10, atom_needle = False):
    i = -1
    l = len(needle) if hasattr(needle, '__len__') else 1
    while True:
        try:
            i = haystack.index(needle, i+(l if atom_needle else 1))
            yield haystack[max(i-vision,0):i+l+vision]
        except ValueError:
            return

def peek_print(needle: str, haystack: str, vision = 10, atom_needle = False, pos = True, printer = print, color = True, bound = True, ret = False):
    g = _peek_print(needle, haystack, vision = vision, atom_needle = atom_needle, pos = pos, printer = printer, color = color, bound = bound)
    if ret:
        return g
    else:
        for _ in g: pass

def _peek_print(needle: str, haystack: str, vision = 10, atom_needle = False, pos = True, printer = print, color = True, bound = True):
    assert vision >= 0
    i = -len(haystack)-1
    l = len(needle)
    L = len(haystack)
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
        i = haystack.find(needle, i+(l if atom_needle else 1))
        if i == -1:
            return
        res = ''
        if pos:
            res += head % i
        if i > vision:
            left = haystack[i-vision:i]
            if bound: res += ell
        else:
            left = haystack[:i]
            if bound: res += endleft
        if i+l+vision < L:
            right = haystack[i+l:i+l+vision]
            if bound: right += ell
        else:
            right = haystack[i+l:]
            if bound: right += endright
        res += left
        res += colored_needle
        res += right
        printer(res)
        yield i, haystack[max(0,i-vision):i+l+vision]
