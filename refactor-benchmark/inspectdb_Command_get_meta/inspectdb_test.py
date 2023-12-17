
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_get_meta(self):
        fname = Path(__file__).parent / "inspectdb.py"
        method = "get_meta"
        method_children = 191

        class_name = "Command"
        class_children = 1753

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
