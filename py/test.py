"""
Tests for the mediocreatbest package
"""

import unittest
from mediocreatbest import auto

class TestAutoModule(unittest.TestCase):
    def test_auto_self(self):
        """Test that auto.self points to the mediocreatbest module"""
        self.assertEqual(auto.self, auto.sys.modules['mediocreatbest'])
        
    def test_auto_lib(self):
        """Test that auto.lib points to the mediocreatbest module"""
        self.assertEqual(auto.self.lib, auto.sys.modules['mediocreatbest'])
        
    def test_auto_config(self):
        """Test that auto.self.config exists"""
        self.assertTrue(hasattr(auto.self, 'config') and auto.self.config is not None)

def test_random():
    x = int(auto.mediocreatbest.Random(1337))
    assert x == 8884109403313611730
    
    x = int(auto.mediocreatbest.Random(1337, 0))
    assert x == 2248471843543096417
    
    x = int(auto.mediocreatbest.Random(1337, 1))
    assert x == 11470864056151350042

def main():
    unittest.main()

if __name__ == '__main__':
    main()
