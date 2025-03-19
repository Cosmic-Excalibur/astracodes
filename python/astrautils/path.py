import os

_wsl_prefix = '/mnt/'

def set_wsl_abspath_prefix(s: str = '/mnt/'):
    global _wsl_prefix
    _wsl_prefix = s

def get_wsl_abspath_prefix():
    return _wsl_prefix

def toggle_win_wsl_abspath(abspath: str):
    abspath = abspath.strip()
    former, delim, latter = abspath.partition(':')
    if delim == ':' and '/' not in former and '\\' not in former:
        disk = former.lower()
        path = latter.replace("\\", "/")
        if disk:
            return f'{_wsl_prefix}{disk}{path}'
    elif abspath.startswith(_wsl_prefix):
        path = abspath[len(_wsl_prefix):]
        former, delim, latter = path.partition('/')
        path = (delim + latter).replace("/", "\\")
        if former:
            return f'{former.upper()}:{path}'
    raise ValueError(f'Invalid absolute path "{abspath}".')

twwa = toggle_wsl_win_abspath = toggle_win_wsl_abspath

def is_wsl_abspath(abspath):
    abspath = abspath.strip()
    if abspath.startswith(_wsl_prefix):
        path = abspath[len(_wsl_prefix):]
        former, delim, latter = path.partition('/')
        path = (delim + latter).replace("/", "\\")
        if former:
            return True
    return False

def is_win_abspath(abspath):
    abspath = abspath.strip()
    former, delim, latter = abspath.partition(':')
    if delim == ':' and '/' not in former and '\\' not in former:
        disk = former.lower()
        path = latter.replace("\\", "/")
        if disk:
            return True
    return False
