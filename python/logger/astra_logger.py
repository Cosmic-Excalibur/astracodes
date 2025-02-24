from math import ceil
from pwn import hexdump

_output = print
_input = input

DEBUGGING = True

def set_debugging(b):
    global DEBUGGING
    DEBUGGING = bool(b)

green_ = lambda s: '\033[32;1m%s\033[0m' % s
red_ = lambda s: '\033[31;1m%s\033[0m' % s
yellow_ = lambda s: '\033[33;1m%s\033[0m' % s
blue_ = lambda s: '\033[34;1m%s\033[0m' % s
cyan_ = lambda s: '\033[36;1m%s\033[0m' % s
gray_ = lambda s: '\033[90;1m%s\033[0m' % s
underline_ = lambda s: '\033[4m%s\033[0m' % s
to_printable = lambda b: ''.join(yellow_(chr(x)) if x in range(32,127) else red_('·') for x in b)

good = lambda *args, end = "\n", sep = "\n    ": _output(f'[{green_("+")}] ' + sep.join(str(arg) for arg in args) + end, end = "")
bad = lambda *args, end = "\n", sep = "\n    ": _output(f'[{red_("-")}] ' + sep.join(str(arg) for arg in args) + end, end = "")
info = lambda *args, end = "\n", sep = "\n    ": _output(f'[{blue_("*")}] ' + sep.join(str(arg) for arg in args) + end, end = "")
warn = lambda *args, end = "\n", sep = "\n    ": _output(f'[{yellow_("!")}] ' + sep.join(str(arg) for arg in args) + end, end = "")
debug = lambda *args, end = "\n", sep = "\n        ": _output(f'[{gray_("DEBUG")}] ' + sep.join(str(arg) for arg in args) + end, end = "") if DEBUGGING else None
def gets(*args, header = True, end = "", sep = "\n    "):
    _output((f'[{gray_("·")}] ' if header else '') + sep.join(str(arg) for arg in args) + end, end = "")
    return _input()

RGB_black    = (   0,   0,   0)
RGB_blue     = (   0,   0, 255)
RGB_green    = (   0, 255,   0)
RGB_cyan     = (   0, 255, 255)
RGB_red      = ( 255,   0,   0)
RGB_magenta  = ( 255,   0, 255)
RGB_yellow   = ( 255, 255,   0)
RGB_white    = ( 255, 255, 255)

def colorify(text, start = RGB_red, end = RGB_yellow):
    linear_interpolation = lambda i, l: tuple(int(s + (e - s) * i / l) for s, e in zip(start, end))
    l = max(len(t) for t in text.splitlines())
    ret = []
    for line in text.splitlines():
        t = ''.join("\x1b[38;2;%s;%s;%s;1m%s"%(linear_interpolation(i, l) + (a,)) for i, a in enumerate(line))
        ret.append(t + '\x1b[0m')
    return '\n'.join(ret)