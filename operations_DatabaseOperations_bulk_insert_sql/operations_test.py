
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_bulk_insert_sql(self):
        fname = Path(__file__).parent / "operations.py"
        method = "bulk_insert_sql"
        method_children = 128

        class_name = "DatabaseOperations"
        class_children = 3107

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
