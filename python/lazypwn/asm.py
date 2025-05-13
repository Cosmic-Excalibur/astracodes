from pwnlib.asm import asm as pwnlib_asm
from pwnlib.asm import disasm as pwnlib_disasm
import json, os

PWNLIB_ASM_CACHE_PATH = os.path.join(os.path.dirname(__file__), 'pwnlib_asm_cache.json')

class PwnlibAsmCache:
    def __init__(self, use_file = True):
        self.use_file = use_file
        self.reload()
        
    def update(self):
        if self.use_file:
            with open(PWNLIB_ASM_CACHE_PATH, 'w', encoding = 'utf-8') as f:
                json.dump(self.assembler, f)
    
    def reload(self):
        if self.use_file and os.path.exists(PWNLIB_ASM_CACHE_PATH):
            with open(PWNLIB_ASM_CACHE_PATH, 'r', encoding = 'utf-8') as f:
                data = json.load(f)
            self.assembler = data
            self.disassembler = dict((v, k) for k, v in data.items())
        else:
            self.assembler = dict()
            self.disassembler = dict()
    
    def asm(self, asmcodes, reload = True):
        res = self.assembler.get(asmcodes.strip(), None)
        if reload: self.reload()
        if res is None:
            mcodes = pwnlib_asm(asmcodes.strip())
            self.assembler.update({asmcodes.strip(): mcodes.hex()})
            self.disassembler.update({mcodes.hex(): asmcodes.strip()})
            self.update()
            return mcodes
        else:
            return bytes.fromhex(res)
    
    def disasm(self, mcodes, reload = True):
        res = self.disassembler.get(mcodes.hex(), None)
        if reload: self.reload()
        if res is None:
            asmcodes = pwnlib_disasm(mcodes)
            self.assembler.update({asmcodes.strip(): mcodes.hex()})
            self.disassembler.update({mcodes.hex(): asmcodes.strip()})
            self.update()
            return asmcodes
        else:
            return res
    
    def clear(self):
        self.assembler = dict()
        self.disassembler = dict()
        os.remove(PWNLIB_ASM_CACHE_PATH)

pwnlib_asm_cache = PwnlibAsmCache()

def asm(shellcode, *args, reload = True, **kwargs):
    if args or kwargs:
        return pwnlib_asm(shellcode, *args, **kwargs)
    else:
        return pwnlib_asm_cache.asm(shellcode, reload = reload)

def disasm(data, *args, reload = True, **kwargs):
    if args or kwargs:
        return pwnlib_disasm(data, *args, **kwargs)
    else:
        return pwnlib_asm_cache.disasm(data, reload = reload)
