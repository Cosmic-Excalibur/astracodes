import sys
import logger.astra_logger as alg

def printname(*args, log_func = print, **kwargs):
    frame = sys._getframe(1)
    log_func(*(f"{arg} = {repr(eval(arg, frame.f_globals, frame.f_locals))}" for arg in args), **kwargs)

def debugname(*args, **kwargs):
    frame = sys._getframe(1)
    alg.debug(*(f"{arg} = {repr(eval(arg, frame.f_globals, frame.f_locals))}" for arg in args), **kwargs)

def goodname(*args, **kwargs):
    frame = sys._getframe(1)
    alg.good(*(f"{arg} = {repr(eval(arg, frame.f_globals, frame.f_locals))}" for arg in args), **kwargs)

def badname(*args, **kwargs):
    frame = sys._getframe(1)
    alg.bad(*(f"{arg} = {repr(eval(arg, frame.f_globals, frame.f_locals))}" for arg in args), **kwargs)

def warnname(*args, **kwargs):
    frame = sys._getframe(1)
    alg.warn(*(f"{arg} = {repr(eval(arg, frame.f_globals, frame.f_locals))}" for arg in args), **kwargs)

def infoname(*args, **kwargs):
    frame = sys._getframe(1)
    alg.info(*(f"{arg} = {repr(eval(arg, frame.f_globals, frame.f_locals))}" for arg in args), **kwargs)
