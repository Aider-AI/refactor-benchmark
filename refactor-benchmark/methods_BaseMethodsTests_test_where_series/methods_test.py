
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_test_where_series(self):
        fname = Path(__file__).parent / "methods.py"
        method = "test_where_series"
        method_children = 370

        class_name = "BaseMethodsTests"
        class_children = 5272

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
