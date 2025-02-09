import sys

def printname(*args, **kwargs):
    frame = sys._getframe(1)
    print(*(f"{arg} = {repr(eval(arg, frame.f_globals, frame.f_locals))}" for arg in args), **kwargs)
