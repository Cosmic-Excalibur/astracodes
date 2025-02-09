# ASTRACODES

Integrated code hub for commonly used stuff.
by **@Astrageldon**


## `/wsl`
Scripts intended for use in a WSL.

### `/wsl/.astra_scripts`<span id=".astra_scripts"/>
A collection of utilities.
Automatically loaded during the startup of a bash.
Copy this file to `~/`, or create a soft link in `~/` pointing to this file, then append `source ~/.astra_scripts` to `~/.bashrc`.

* `sourceme`: Apply updates of this file.
* `vimme`: Edit this file using vim.
* `astrahelp`: Learn more about each utility.
* ...: Call `astrahelp` for a list of utilities.


## `/python`

Python code hub. In order to use any python script in this folder at any time, call commands `astrapython`, `astraipython`... (as in [`/wsl/.astra_scripts`](#.astra_scripts)).

A SageMath 10.4 environment is recommended. Call `sage104` to activate it.

Run `from utils.lazy import *` to pre-import some frequently used modules.