
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_check_expression_support(self):
        fname = Path(__file__).parent / "operations.py"
        method = "check_expression_support"
        method_children = 118

        class_name = "DatabaseOperations"
        class_children = 1942

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
