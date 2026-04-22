"""
Random number generation utility
"""

from __future__ import annotations
from ._auto import auto

__all__ = [
    'RANDOM',
]


# RANDOM = (
#     *,
#     seed: int,
# ) -> Random
# 
# Random = (
#     n: int,
# ) -> random.Random
# 
# int(Random(n: int)) = int


class __Random(auto.random.Random):
    def __int__(self):
        return int.from_bytes(self.randbytes(4), 'little')


def RANDOM(*, seed: int):
    def Random(n: int, /):
        random = auto.random.Random(seed)
        # random.randbytes(n)  # XXX(th): This call doesn't work!
        for _ in range(n):
            random.randbytes(1)
        n = random.randbytes(4)
        m = int.from_bytes(n, 'little')
        random = auto.random.Random(n)
        random.np = auto.np.random.default_rng(m)
        random.__class__ = __Random
        return random
    return Random


def scope():
    display(RANDOM(seed=1337)(0).sample(list(range(100)), 10))
    display(RANDOM(seed=1337)(1).sample(list(range(100)), 10))
    display(RANDOM(seed=1337)(2).sample(list(range(100)), 10))
    display(RANDOM(seed=1337)(2).sample(list(range(100)), 10))

    display(RANDOM(seed=1337)(0).np.integers(0, 100, 10))
    display(RANDOM(seed=1337)(1).np.integers(0, 100, 10))
    display(RANDOM(seed=1337)(2).np.integers(0, 100, 10))
    display(RANDOM(seed=1337)(2).np.integers(0, 100, 10))

    Random = RANDOM(seed=1337)
    print(f'{int(Random(0)):08x}')
    print(f'{int(Random(1)):08x}')
    print(f'{int(Random(2)):08x}')
    print(f'{int(Random(2)):08x}')

    Random = RANDOM(seed=1337)
    print(f'{int(Random(0)):08x}')
    print(f'{int(Random(1)):08x}')
    print(f'{int(Random(2)):08x}')
    print(f'{int(Random(2)):08x}')

# /scope
