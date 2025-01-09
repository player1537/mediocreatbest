"""
run: Run a function with its dependencies
"""

from __future__ import annotations
from ._auto import auto


__all__ = [
    'run',
]


try:
    g
except NameError:
    g = {}

try:
    f
except NameError:
    f = {}

def run(func=None, /, name=None, cond=True, splat=False, after=None, scope=None, once=False):
    def wrapper(func, /, *, name=name, cond=cond):
        import inspect

        if callable(cond):
            cond = cond()

        if not cond:
            return None

        if name is None:
            name = func.__name__


        f[name] = func

        args = []
        for key, parameter in inspect.signature(func).parameters.items():
            if parameter.kind == inspect.Parameter.POSITIONAL_ONLY:
                keys = [key]
                if scope is not None:
                    keys.insert(0, f'{scope}__{key}')

                for key in keys:
                    try:
                        value = g[key]
                    except KeyError:
                        continue
                    else:
                        args.append(value)
                        break
                else:
                    raise KeyError(f'None of {keys=!r} found in g')


        if once:
            if scope is not None:
                if f'{scope}__{name}' in g:
                    return

            else:
                if name in g:
                    return

        ret = func(*args)

        if callable(after):
            after(ret)

        if splat:
            it = ret.items()
        else:
            it = [(name, ret)]

        for name, ret in it:
            if scope is not None:
                name = f'{scope}__{name}'

            g[name] = ret

        return None

    if func is not None:
        return wrapper(func)
    else:
        return wrapper
run.f = f
run.g = g
