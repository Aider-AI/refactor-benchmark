
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__get_column_collations(self):
        fname = Path(__file__).parent / "introspection.py"
        method = "_get_column_collations"
        method_children = 145

        class_name = "DatabaseIntrospection"
        class_children = 1779

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
