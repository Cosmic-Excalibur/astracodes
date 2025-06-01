import os, sys, re
os.environ['TERM'] = 'xterm'

from pwn import *
from time import sleep
from lazypow.powsolver import PoWSolver
powsolver = Powsolver = PoWSolver
from astrautils.lite import *

context(os = 'linux', arch = 'amd64', log_level = 'debug')

class IOCTX:
    def __init__(self):
        self._state = {
            'io_name': 'r',
            'io': None,
            'argv': None,
            'elf_name': 'elf',
            'elf': None,
            'libc_name': 'libc',
            'libc': None,
            'libc_path': None,
            'debugging': True,
            'pausing': True,
            'first_debug': True,
            'debug_if_remote': False,
            'kernel_base': 0xffffffff81000000,
        }
    def __call__(self, target = None, libc_path = None, **kwargs):
        if target is not None:
            self.argv = list(target) if isinstance(target, (list, tuple)) else [target]
        if libc_path is not None:
            self.libc_path = libc_path
        for k, v in kwargs.items():
            self[k] = v
        return self
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

def loglevelwarn():
    loglevel('warn')

def loglevelwarning():
    loglevel('warning')

def loglevelcritical():
    loglevel('critical')

def loglevelnotset():
    loglevel('notset')

def loglevelerror():
    loglevel('error')

def get_io(conn_creator, *args, **kwargs):
    frame = sys._getframe(1)
    ioctx.first_debug = True
    def _assign(x):
        frame.f_globals[ioctx.io_name] = ioctx.io = x
        return x
    if conn_creator is remote:
        if not ioctx.debug_if_remote:
            ioctx.debugging = False
        if len(args) >= 1 and isinstance(args[0], (str, bytes, bytearray)) and ':' in args[0]:
            host, port = args[0].split(':')
            return _assign(conn_creator(host, int(port), **kwargs))
    elif conn_creator is process:
        if 'argv' not in kwargs and len(args) == 0:
            if ioctx.argv is not None:
                return _assign(conn_creator(ioctx.argv))
        else:
            ioctx.argv = [args[0]] if len(args) >= 1 and isinstance(args[0], (str, bytes, bytearray)) else args[0]
    return _assign(conn_creator(*args, **kwargs))

getio = get_io

def get_elf(elf_path = None, libc_path = None, elf_checksec = False, libc_checksec = False):
    frame = sys._getframe(1)
    elf_path = elf_path if elf_path is not None else (ioctx.argv[0] if ioctx.argv else None)
    if elf_path is None:
        warn("get_elf: ELF path not specified.")
    else:
        frame.f_globals[ioctx.elf_name] = ioctx.elf = ELF(path = elf_path, checksec = elf_checksec)
    libc_path = libc_path if libc_path is not None else ioctx.libc_path
    if libc_path is None:
        warn("get_elf: Libc path not specified.")
    else:
        frame.f_globals[ioctx.libc_name] = ioctx.libc = ELF(path = libc_path, checksec = libc_checksec)
    return ioctx.elf, ioctx.libc

getelf = get_elf

send                  = lambda *args, **kwargs: ioctx.io.send(*args, **kwargs)
recv                  = lambda *args, **kwargs: ioctx.io.recv(*args, **kwargs)
interact      = inter = lambda *args, **kwargs: ioctx.io.interactive(*args, **kwargs)
sendline      = sl    = lambda *args, **kwargs: ioctx.io.sendline(*args, **kwargs)
sendlineafter = sla   = lambda *args, **kwargs: ioctx.io.sendlineafter(*args, **kwargs)
sendafter     = sa    = lambda *args, **kwargs: ioctx.io.sendafter(*args, **kwargs)
recvuntil     = ru    = lambda *args, **kwargs: ioctx.io.recvuntil(*args, **kwargs)
recvline      = rl    = lambda *args, **kwargs: ioctx.io.recvline(*args, **kwargs)
interact      = itr   = lambda *args, **kwargs: ioctx.io.interactive(*args, **kwargs)
recvafter     = ra    = lambda delims, *args, **kwargs: (ioctx.io.recvuntil(delims), ioctx.io.recv(*args, **kwargs))[1]
recvlineafter = rla   = lambda delims, *args, **kwargs: (ioctx.io.recvuntil(delims), ioctx.io.recvline(*args, **kwargs))[1]

uu8  = u8lsb  = lambda b, *args, **kwargs: u8(b.ljust(1, b'\0'))
uu16 = u16lsb = lambda b, *args, **kwargs: u16(b.ljust(2, b'\0'))
uu32 = u32lsb = lambda b, *args, **kwargs: u32(b.ljust(4, b'\0'))
uu64 = u64lsb = lambda b, *args, **kwargs: u64(b.ljust(8, b'\0'))

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

def protect_ptr(ptr, addr = None):
    if addr is None: addr = ptr
    return ptr ^ (addr >> 12)

def hack_ptr(ptr, delta = 0):
    assert delta >= 0
    ptr ^= delta >> 12
    ptr ^= ptr   >> 12
    ptr ^= ptr   >> 24
    ptr ^= ptr   >> 48
    return ptr

def kernel_rebase(addr, base = None, old_base = 0xffffffff81000000):
    if base is None: base = ioctx.kernel_base
    return addr - old_base + base

def kernel_rebase_static(addr, base = None, static_base = 0xffffffff81000000):
    if base is None: base = ioctx.kernel_rebase
    return addr - base + static_base
