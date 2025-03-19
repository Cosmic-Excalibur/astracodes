# ASTRACODES

Codes, codes, and codes...
by **@Astrageldon**

Latest update: Wed Mar 19 20:05:31 CST 2025


## `/wsl`
Scripts intended for use in a WSL.

### `/wsl/.astra_scripts`<span id=".astra_scripts"/>
A collection of utilities.

Automatically loaded at the startup of a bash.

Copy `/wsl/.astra_scripts` to `~/`, or create a soft link in `~/` pointing to it, then append a line `source ~/.astra_scripts` to `~/.bashrc`. Restart your bash to make this file take effect.

* `sourceme`: Apply this file.
* `vimme`: Vim this file.
* `astrahelp`: Learn more about the commands.

Call `astrahelp` for a comprehensive list of available commands.


## `/python`

Python code hub. Source [`/wsl/.astra_scripts`](#.astra_scripts) to get import paths right.

A [SageMath 10.4 environment](https://doc.sagemath.org/html/en/installation/index.html#windows) named `sage104` in conda is required.

A list of required external modules can be found in `/python/requirements.txt`.

Run `from astrautils.lazy import *` (slow!) to pre-import some frequently used modules.

You will notice that most of these are some condesenation of python codes, for example, you may rewrite
```python
import string
printable = string.printable[:-6].encode('utf-8')
*blocks, = [printable[i:i+4] for i in range(0,len(printable),4)]
print(*(x.hex() for x in blocks), sep = '\n')
```
as
```python
from astrautils.lite import *
*blocks, = cutter(printable_b[:-6])[::4]
alg.printlines(map(b2h, blocks))
```
I write these mainly because I'm such a couch-potato coder (CTFer?) and I'm done with typing stuff like
```python
from Crypto.Util.number import *
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256, md5
import base64
# ...
pt = long_to_bytes(int(base64.b64decode(b'MzE2OTg0OTQ5Njg3NTU3NTY5NjE1MTI3NTk2Nzc=').decode()))
```
or stuff like
```python
from pwn import *
r = process("./pwn")
gdb.attach(r)
pause()
r.sendlineafter(b'name: ', b'a'*(0x40+8) + p64(backdoor))
r.interactive()
```
over & over again :\(
