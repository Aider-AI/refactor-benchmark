
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_quote_value(self):
        fname = Path(__file__).parent / "schema.py"
        method = "quote_value"
        method_children = 130

        class_name = "DatabaseSchemaEditor"
        class_children = 2395

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
