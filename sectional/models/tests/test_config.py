import unittest
from sectional.models import Configuration

class ConfigTest(unittest.TestCase):
    def test_loading(self):
        config = Configuration()
        
if __name__ == '__main__':
    unittest.main()
