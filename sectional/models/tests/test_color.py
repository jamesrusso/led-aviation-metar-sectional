import unittest
from sectional.models import Color


class ColorTest(unittest.TestCase):
    def test_name(self):
        x = Color("red")
        self.assertEqual((255, 0, 0), x.rgb)

    def test_hex(self):
        x = Color("#fff")
        self.assertEqual((255, 255, 255), x.rgb)

    def test_tuple(self):
        x = Color("#141400")
        self.assertEqual((20, 20, 0), x.rgb)

if __name__ == '__main__':
    unittest.main()
