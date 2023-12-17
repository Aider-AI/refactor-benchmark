
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_get_field_type(self):
        fname = Path(__file__).parent / "inspectdb.py"
        method = "get_field_type"
        method_children = 194

        class_name = "Command"
        class_children = 1753

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
