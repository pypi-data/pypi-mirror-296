import sys
import os
import unittest


SCRIPT_DIR: str = os.path.dirname(p=os.path.abspath(path=__file__))
sys.path.append(os.path.dirname(p=SCRIPT_DIR))

from src.double import Double

class TestDouble(unittest.TestCase):
    def test_addition(self):
        a = Double(1.5)
        b = Double(2.5)
        result = a + b
        self.assertEqual(str(result), "4.00000000000000000000000000000000000000000000000000")



if __name__ == "__main__":
    unittest.main()
