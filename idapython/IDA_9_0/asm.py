from idautils import *

import idc
import ida_auto

def disassemble_from(ea):
    idc.del_items(ea)
    idc.create_insn(ea)
    ida_auto.auto_wait()

def get_disasm_text(ea):
    return idc.GetDisasm(ea)

def disassemble_range(start_ea, end_ea=None):
    current = start_ea
    instructions = []
    if end_ea is None:
        end_ea = idc.get_func_attr(start_ea, idc.FUNCATTR_END)
    while current < end_ea and current != idc.BADADDR:
        if not idc.is_code(idc.get_full_flags(current)):
            idc.create_insn(current)
        disasm = idc.GetDisasm(current)
        length = idc.get_item_size(current)
        instructions.append({
            "address": current,
            "text": disasm,
            "length": length
        })
        current = idc.next_head(current, end_ea)
    return instructions

def disassemble_n(start_ea, count, window=0x20):
    current = start_ea
    instructions = []
    while count > 0 and current != idc.BADADDR:
        if not idc.is_code(idc.get_full_flags(current)):
            idc.create_insn(current)
        disasm = idc.GetDisasm(current)
        length = idc.get_item_size(current)
        instructions.append({
            "address": current,
            "text": disasm,
            "length": length
        })
        current = idc.next_head(current, current + window)
        count -= 1
    return instructions
