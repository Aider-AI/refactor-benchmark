
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_test_get(self):
        fname = Path(__file__).parent / "getitem.py"
        method = "test_get"
        method_children = 339

        class_name = "BaseGetitemTests"
        class_children = 3543

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
