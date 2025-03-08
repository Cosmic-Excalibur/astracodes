from pwn import remote, process, context, gdb, pause
import sys

context(os = 'linux', arch = 'amd64', log_level = 'debug')

class IOCTX:
    def __init__(self):
        self._state = {
            'name': 'r',
            'io': None,
            'debugging': True,
            'pausing': True,
            'first_debug': True,
            'debug_if_remote': False
        }
    def __call__(self, **kwargs):
        for k, v in kwargs.items():
            self[k] = v
    def __setitem__(self, a, b):
        if a not in self._state:
            raise AttributeError(f"'IOCTX' object has no attribute '{a}'.")
        self._state[a] = b
    def __getitem__(self, a):
        if a not in self._state:
            raise AttributeError(f"'IOCTX' object has no attribute '{a}'.")
        return self._state[a]
    def __setattr__(self, a, b):
        if a == '_state':
            super(IOCTX, self).__setattr__(a, b)
            return
        if a not in self._state:
            raise AttributeError(f"'IOCTX' object has no attribute '{a}'.")
        self._state[a] = b
    def __getattr__(self, a):
        if a == '_state':
            super(IOCTX, self).__getattr__(a)
            return
        if a not in self._state:
            raise AttributeError(f"'IOCTX' object has no attribute '{a}'.")
        return self._state[a]
    def __str__(self):
        return f'IOCTX({", ".join("%s = %s" % (x, repr(y)) for x, y in sorted(self._state.items(), key = lambda k: k[0]))})'
    def __repr__(self):
        return self.__str__()

ioctx = IOCTX()

def loglevel(l):
    context(log_level = l)

def logleveldebug():
    loglevel('debug')

def loglevelinfo():
    loglevel('info')

def getio(conn_creator, *args, **kwargs):
    frame = sys._getframe(1)
    def _assign(x):
        frame.f_globals[ioctx.name] = ioctx.io = x
        return ioctx.io
    if conn_creator is remote:
        if not ioctx.debug_if_remote:
            ioctx.debugging = False
        if len(args) == 1 and isinstance(args[0], str) and ':' in args[0]:
            host, port = args[0].split(':')
            return _assign(conn_creator(host, int(port), **kwargs))
    return _assign(conn_creator(*args, **kwargs))

send                = lambda *args, **kwargs: ioctx.io.send(*args, **kwargs)
recv                = lambda *args, **kwargs: ioctx.io.recv(*args, **kwargs)
interact            = lambda *args, **kwargs: ioctx.io.interactive(*args, **kwargs)
sendline      = sl  = lambda *args, **kwargs: ioctx.io.sendline(*args, **kwargs)
sendlineafter = sla = lambda *args, **kwargs: ioctx.io.sendlineafter(*args, **kwargs)
sendafter     = sa  = lambda *args, **kwargs: ioctx.io.sendafter(*args, **kwargs)
recvuntil     = ru  = lambda *args, **kwargs: ioctx.io.recvuntil(*args, **kwargs)
recvline      = rl  = lambda *args, **kwargs: ioctx.io.recvline(*args, **kwargs)
recvafter     = ra  = lambda delims, *args, **kwargs: (ioctx.io.recvuntil(delims), ioctx.io.recv(*args, **kwargs))[1]
recvlineafter = rla = lambda delims, *args, **kwargs: (ioctx.io.recvuntil(delims), ioctx.io.recvline(*args, **kwargs))[1]

def dbg(*args, pausing = False, **kwargs):
    if not ioctx.debugging: return
    if ioctx.first_debug:
        gdb.attach(ioctx.io, *args, **kwargs)
        ioctx.first_debug = False
    if pausing or ioctx.pausing:
        pause()

def die():
    if ioctx.io is not None:
        ioctx.io.close()
        ioctx.io = None

suicide = jisatsu = die
