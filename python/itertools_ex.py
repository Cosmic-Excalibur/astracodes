from collections.abc import Iterable, Sequence
from typing import Callable, List, Union
from itertools import *

def chunks(iterable: Iterable, size: int, proc: Callable = None):
    """
    Split an iterable into chunks of "smaller" iterables,
    works as generator.
    
    Parameters
    ----------
    iterable : Iterable
        The target iterable, can be `list`, `generator`,
        `bytes`, `iterator` and so on.
    size : int
        The maximum of each chunk.
    proc : Callable
        Before outputting, chunks are passed to this
        processor function / class unless it's set to `None`.
        Similar to `map`.
    
    Examples
    --------
    
    >>> for chunk in chunks(range(10), 3):
    ...     print(*chunk)
    0 1 2
    3 4 5
    6 7 8
    9
    
    >>> for chunk in chunks(range(10), 3):
    ...     print(chunk)
    <itertools.chain object at 0x000001D87EDB76D0>
    <itertools.chain object at 0x000001D87EF2AF70>
    <itertools.chain object at 0x000001D87EDB7D30>
    <itertools.chain object at 0x000001D87EF2A520>
    
    >>> for chunk in chunks(range(10), 3, bytes):
    ... # also for chunk in map(bytes, chunks(range(10), 3)):
    ...     print(chunk)
    b'\x00\x01\x02'
    b'\x03\x04\x05'
    b'\x06\x07\x08'
    b'\t'
    
    """
    i = iter(iterable)
    flag = proc == None
    for first in i:
        rest = islice(i, size - 1)
        yield chain([first], rest) if flag else proc(chain([first], rest))
        next(islice(rest, size - 1, None), None)