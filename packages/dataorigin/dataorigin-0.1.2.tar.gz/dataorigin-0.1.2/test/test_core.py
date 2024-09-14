import unittest
from dataorigin.core import greet

class TestGreet(unittest.TestCase):
    def test_greet(self):
        self.assertEqual(greet(), "¡Bienvenido a DataOrigin!")

if __name__ == '__main__':
    unittest.main()
