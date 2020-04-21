import unittest
from sectional.models import Configuration, AirportCondition, Color

class ConfigTest(unittest.TestCase):
    def test_loading(self):
        config = Configuration(config_path='test-config.yaml')
        color = Color('red', True)
        config.set_color_for_condition(AirportCondition.IFR, color)
        self.assertEquals(config.get_color_for_condition(AirportCondition.IFR),color) 

        
if __name__ == '__main__':
    unittest.main()
