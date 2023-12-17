
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__parse_column_or_constraint_definition(self):
        fname = Path(__file__).parent / "introspection.py"
        method = "_parse_column_or_constraint_definition"
        method_children = 578

        class_name = "DatabaseIntrospection"
        class_children = 1779

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
