"""
Automatic namedtuple generation

It can be helpful to quickly have a class/namedtuple when declaring data
structures, but it is annoying to have to switch back and forth to write code,
write a class, then back to writing code that uses the class.

Instead, this helper class lets you write code like the following:

>>> mediocreatbest.stuple.name.position('hello', mediocreatbest.namedtuple.x.y.z(0.0, 1.0, 2.0))
np(name='hello', position=xyz(x=0., y=1., z=2.))

(Aside: I don't think this is all that helpful any more. I intentionally named
it "stuple" so that it could stand for "simple tuple" or equally "stupid
tuple".)
"""

from __future__ import annotations
from ._auto import auto

__all__ = [
    'stuple',
]


class STuple:
    def __init__(self, names=None):
        if names is None:
            names = []

        self.__names = names
        self.__class = None

    def __getattr__(self, name):
        attr = NamedTuple(self.__names + [name])
        setattr(self, name, attr)
        return attr

    def __call__(self, *args, **kwargs):
        if self.__class is None:
            typename = ''.join(name[0] for name in self.__names)
            fields = self.__names
            self.__class = auto.collections.namedtuple(typename, fields)

        return self.__class(*args, **kwargs)


stuple = STuple()
