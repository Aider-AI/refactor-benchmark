
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_last_executed_query(self):
        fname = Path(__file__).parent / "operations.py"
        method = "last_executed_query"
        method_children = 122

        class_name = "DatabaseOperations"
        class_children = 3107

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
