"""
wrap: Create Pre- and Postfix Functions
"""

from __future__ import annotations
from ._auto import auto

__all__ = [
    'wrap',
]


@auto.dataclasses.dataclass(frozen=True)
class Wrap:
    func: typing.Callable
    args: list = auto.dataclasses.field(default_factory=list)
    kwargs: dict = auto.dataclasses.field(default_factory=dict)

    def __call__(self, *args, **kwargs) -> auto.typing.Callable:
        return self.func(*self.args, *args, **self.kwargs, **kwargs)

    def __matmul__(self, other: auto.typing.Any) -> auto.typing.Any:
        return self(other)

    def __rmatmul__ (self, other: auto.typing.Any) -> auto.typing.Any:
        return self(other)

    def __or__(self, other: auto.typing.Any) -> auto.typing.Any:
        return self(other)

    def __ror__(self, other: auto.typing.Any) -> auto.typing.Any:
        return self(other)

def wrap(func: auto.typing.Callable, /, *args, **kwargs) -> Wrap:
    return Wrap(func, args, kwargs)

assert (wrap(lambda x: x + 1) @ 1) == 2
assert (1 @ wrap(lambda x: x + 1)) == 2

wrap = wrap(wrap)  # :)
