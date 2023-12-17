
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_adapt_method_mode(self):
        fname = Path(__file__).parent / "base.py"
        method = "adapt_method_mode"
        method_children = 104

        class_name = "BaseHandler"
        class_children = 1369

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
