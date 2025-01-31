"""

"""

from __future__ import annotations
from mediocreatbest import auto


def test_random():
    x = int(auto.mediocreatbest.Random(1337))
    assert x == 8884109403313611730
    
    x = int(auto.mediocreatbest.Random(1337, 0))
    assert x == 2248471843543096417
    
    x = int(auto.mediocreatbest.Random(1337, 1))
    assert x == 11470864056151350042
