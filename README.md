# ASTRACODES

Codes, codes, and codes...
by **@Astrageldon**

Latest update: Wed Mar 19 20:05:31 CST 2025


# `/wsl`
Scripts intended for use in a WSL.

## `/wsl/.astra_scripts`<span id=".astra_scripts"/>
A collection of utilities.

Automatically loaded at the startup of a bash.

Copy `/wsl/.astra_scripts` to `~/`, or create a soft link in `~/` pointing to it, then append a line `source ~/.astra_scripts` to `~/.bashrc`. Restart your bash to make this file take effect.

* `sourceme`: Apply this file.
* `vimme`: Vim this file.
* `astrahelp`: Learn more about the commands.

Call `astrahelp` for a comprehensive list of available commands.


# `/python`

A collection of Python scripts. Source [`/wsl/.astra_scripts`](#.astra_scripts) to incorporate this folder for imports.

A [SageMath 10.4](https://doc.sagemath.org/html/en/installation/index.html#windows) environment named `sage104` in conda is required.

A list of required external modules can be found in `/python/requirements.txt`.

Run `from astrautils.lazy import *` (slow!) to pre-import some frequently used modules.

You will notice that some of these are condensations or abbreviations of Python scripts, for example, you may rewrite
```python
import string
printable = string.printable[:-6].encode('utf-8')
*blocks, = [printable[i:i+4] for i in range(0,28,4)] + [printable[i:i+3] for i in range(28,len(printable),3)]
print(*(x.hex() for x in blocks), sep = '\n')
# print('\n'.join(x.hex() for x in blocks))
```
as
```python
from astrautils.lite import *
*blocks, = cutter(printable_b[:-6])[:28:4, 28::3]
alg.printlines(map(b2h, blocks))
```
And some are for specialized usage, e.g.
```python
from lazycrypto.lattice.primal_attack import *
(A, b), (x, e) = random_lwe_uniform(10, 4, 65537, 16, 16, 2)
e_ = next(primal_attack(65537, A, b, 2))
assert err_oracle(e_, 2) and e == e_
```

## `astrautils`

| Module | Description |
| ------ | ----------- |
| all    | Everything in `astrautils`. |
| bitstruct | Interconversions among integers, bytes, hex strings, bit strings, bit lists, polynomials and n-adic integers. |
| bitstruct_lite | Interconversions among integers, bytes, hex strings, bit strings, bit lists, and n-adic integers. |
| bool | Dichotomous judgers. |
| commonstrings | Commonly used strings. |
| counter | Lightweight counters. |
| factorization | Utilities for SageMath `Factorization` object. |
| filter | `filter`, `map` objects and their pipelining. |
| gg | Short for Good Game :\) Force your program to exit and say goodgame! |
| int | Python `int` utilities. |
| lazy | (Maybe) frequently used stuff in Python and even Sage, so quite a lot :\) |
| lite | Lightweight version of `astrautils.all`. |
| path | OS path handling. |
| peek | Find a needle in a haystack :\) |
| prgen | Short for Polynomial Ring GENerators. |
| printname | Printing both variable names and values. One shot for all. |
| shuffled | -ed version of `random.shuffle` just like `sorted` and `sort`. |
| slicing | Automatic cake knives :\) |
| str | Python `str` utilities. |
| timeit | Time it! |
| varfactory | Variable factory objects. |
| wrapper | Object (`str`, `bytes`, ...) decorators. |


