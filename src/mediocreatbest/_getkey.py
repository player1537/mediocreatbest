"""

"""

from __future__ import annotations
from ._auto import auto


def getkey(
    name: str,
    *,
    cache: dict | auto.typing.Literal[...] | None = ...,
) -> str:
    if cache is ...:
        global __getkey_cache
        try: __getkey_cache
        except NameError: __getkey_cache = {}
        cache = __getkey_cache

    ckey = name
    if cache is None or ckey not in cache:
        key = None

        if key is None and 'google' in auto.sys.modules:
            global __00e7dbf0
            try: __00e7dbf0
            except NameError: __00e7dbf0 = auto.functools.cache(auto.google.colab.userdata.get)
            try:
                key = __00e7dbf0(name)
            except auto.google.colab.userdata.NotebookAccessError:
                pass

        if key is None and name in auto.os.environ:
            key = auto.os.environ[name]

        if key is None:
            global __a2a21f38
            try: __a2a21f38
            except NameError: __a2a21f38 = auto.functools.cache(auto.getpass.getpass)
            key = __a2a21f38(f'Enter {name}: ')

        cache[ckey] = key

    else:
        key = cache[ckey]

    return key
