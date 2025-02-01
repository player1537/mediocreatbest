"""
Tests for the mediocreatbest package
"""

from mediocreatbest import auto

def test_auto_module():
    """Test that auto.self points to the mediocreatbest module"""
    assert auto.self == auto.sys.modules['mediocreatbest']
    
def test_auto_lib():
    """Test that auto.lib points to the mediocreatbest module"""
    assert auto.self.lib == auto.sys.modules['mediocreatbest']
    
def test_auto_config():
    """Test that auto.self.config exists"""
    assert hasattr(auto.self, 'config') and auto.self.config is not None

def test_random():
    x = int(auto.mediocreatbest.Random(1337))
    assert x == 8884109403313611730
    
    x = int(auto.mediocreatbest.Random(1337, 0))
    assert x == 2248471843543096417
    
    x = int(auto.mediocreatbest.Random(1337, 1))
    assert x == 11470864056151350042
