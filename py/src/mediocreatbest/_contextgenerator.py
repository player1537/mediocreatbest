"""
Combination Context Manager + Generator/Coroutine

Example: A coroutine/generator for reading from a file.

@contextgenerator
def foo():
    with open(__file__, 'rt') as f:
        text = None
        while True:
            size_to_read = yield text
            text = f.read(size_to_read)

with foo() as foo:
    foo.send(64)
    foo.send(64)
"""

from __future__ import annotations
from ._auto import auto

__all__ = [
    'contextgenerator',
]


def contextgenerator(func=None, /, *, call=lambda generator: generator):
    if func is None:
        return auto.functools.partial(contextgenerator, call=call)

    @auto.contextlib.contextmanager
    @auto.functools.wraps(func)
    def wrapper(*args, **kwargs):
        generator = None
        try:
            generator = func(*args, **kwargs)

            next(generator)
            yield call(generator)

        finally:
            if generator is not None:
                generator.close()

    return wrapper
