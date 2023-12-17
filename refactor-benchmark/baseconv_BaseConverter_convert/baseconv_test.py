
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_convert(self):
        fname = Path(__file__).parent / "baseconv.py"
        method = "convert"
        method_children = 144

        class_name = "BaseConverter"
        class_children = 298

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
