import pwnlib.asm
from pwnlib.asm import asm as pwnlib_asm
from pwnlib.asm import disasm as pwnlib_disasm
from pwnlib.asm import LocalContext, context
import json, os, base64

PWNLIB_ASM_CACHE_PATH = os.path.join(os.path.dirname(__file__), 'astracodes_pwnlib_asm_cache_file.json')

pwnlib_assembler = pwnlib.asm._assembler
pwnlib_linker = pwnlib.asm._linker
pwnlib_objcopy = pwnlib.asm._objcopy
pwnlib_objdump = pwnlib.asm._objdump
pwnlib_which_binutils = pwnlib.asm.which_binutils

class CachedPwnlibAsmContext:
    def __init__(self, use_file = True, cached_which = True):
        self.use_file = use_file
        if cached_which:
            pwnlib.asm._assembler = self.cached_pwnlib_assembler
            pwnlib.asm._linker = self.cached_pwnlib_linker
            pwnlib.asm._objcopy = self.cached_pwnlib_objcopy
            pwnlib.asm._objdump = self.cached_pwnlib_objdump
            pwnlib.asm.which_binutils = self.cached_pwnlib_which_binutils
        self.reload()
        
    def update(self):
        if self.use_file:
            with open(PWNLIB_ASM_CACHE_PATH, 'w', encoding = 'utf-8') as f:
                json.dump({'asm': self.assembler, 'disasm': self.disassembler, 'which': self.which, 'headers': self.headers}, f)
    
    def reload(self):
        if self.use_file and os.path.exists(PWNLIB_ASM_CACHE_PATH):
            with open(PWNLIB_ASM_CACHE_PATH, 'r', encoding = 'utf-8') as f:
                data = json.load(f)
            self.assembler = data.get('asm', {})
            self.disassembler = data.get('disasm', {})
            self.which = data.get('which', {})
            self.headers = data.get('headers', [])
        else:
            self.assembler = dict()
            self.disassembler = dict()
            self.which = dict()
            self.headers = []
    
    def _serialize(self, data, extra = ()):
        header = ''
        for thing in map(str, (context.arch, context.bits, context.os, context.endian) + extra):
            header += str(len(thing)) + '$' + thing
        if header in self.headers:
            index = self.headers.index(header)
        else:
            index = len(self.headers)
            self.headers.append(header)
        res = str(index) + '#' + data
        return res
    
    def cached_pwnlib_util(self, name, pwnlib_func, *args, **kwargs):
        key = self._serialize(name, args + tuple(f'{k}:{v}' for k, v in kwargs.items()))
        hit = self.which.get(key, None)
        if hit is None:
            hit = pwnlib_func(*args, **kwargs)
            self.which[key] = hit
        return hit
    
    def cached_pwnlib_assembler(self, *args, **kwargs):
        return self.cached_pwnlib_util('_assembler', pwnlib_assembler, *args, **kwargs)
    
    def cached_pwnlib_linker(self, *args, **kwargs):
        return self.cached_pwnlib_util('_linker', pwnlib_linker, *args, **kwargs)
    
    def cached_pwnlib_objcopy(self, *args, **kwargs):
        return self.cached_pwnlib_util('_objcopy', pwnlib_objcopy, *args, **kwargs)
    
    def cached_pwnlib_objdump(self, *args, **kwargs):
        return self.cached_pwnlib_util('_objdump', pwnlib_objdump, *args, **kwargs)
    
    def cached_pwnlib_which_binutils(self, *args, **kwargs):
        return self.cached_pwnlib_util('which_binutils', pwnlib_which_binutils, *args, **kwargs)
    
    @LocalContext
    def asm(self, asmcodes, cached_data, reload):
        if reload: self.reload()
        asmcodes_ = asmcodes
        key = self._serialize(asmcodes_)
        if cached_data:
            res = self.assembler.get(key, None)
        else:
            res = None
        if res is None:
            mcodes = pwnlib_asm(asmcodes_)
            mcodes_ = base64.b64encode(mcodes).decode()
            self.assembler.update({key: mcodes_})
            self.disassembler.update({self._serialize(mcodes_): asmcodes_})
            self.update()
            return mcodes
        else:
            return base64.b64decode(res.encode())
    
    @LocalContext
    def disasm(self, mcodes, cached_data, reload):
        if reload: self.reload()
        mcodes_ = base64.b64encode(mcodes).decode()
        key = self._serialize(mcodes_)
        if cached_data:
            res = self.disassembler.get(key, None)
        else:
            res = None
        if res is None:
            asmcodes = pwnlib_disasm(mcodes)
            asmcodes_ = asmcodes
            mkey = self._serialize(asmcodes_)
            self.assembler.update({mkey: mcodes_})
            self.disassembler.update({key: asmcodes_})
            self.update()
            return asmcodes
        else:
            return res
    
    def clear(self):
        self.assembler = dict()
        self.disassembler = dict()
        self.which = dict()
        if os.path.exists(PWNLIB_ASM_CACHE_PATH):
            os.remove(PWNLIB_ASM_CACHE_PATH)

cached_pwnlib_asm_context = CachedPwnlibAsmContext()

@LocalContext
def asm(shellcode, *args, cached_data = True, reload = False, **kwargs):
    if args or kwargs:
        return pwnlib_asm(shellcode, *args, **kwargs)
    else:
        return cached_pwnlib_asm_context.asm(shellcode, cached_data = cached_data, reload = reload)

@LocalContext
def disasm(data, *args, cached_data = True, reload = False, **kwargs):
    if args or kwargs:
        return pwnlib_disasm(data, *args, **kwargs)
    else:
        return cached_pwnlib_asm_context.disasm(data, cached_data = cached_data, reload = reload)
