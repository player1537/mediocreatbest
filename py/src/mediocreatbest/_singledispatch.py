"""
Better singledispatch implementation

functools.singledispatch *only* supports positional arguments. If you want the
base function to be called with keyword arguments, but still allow the
dispatching on any positional argument, then you need to work around that
problem.
"""

from __future__ import annotations
from ._auto import auto

__all__ = [
    'dispatch',
]


def dispatch(func, /):
    dispatch = auto.functools.singledispatch(func)

    @auto.functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not args:
            return func(**kwargs)

        return dispatch(*args, **kwargs)

    wrapper.register = dispatch.register
    wrapper.dispatch = dispatch.dispatch
    wrapper.registry = dispatch.registry
    wrapper._clear_cache = dispatch._clear_cache
    return wrapper
