
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__check_autocomplete_fields_item(self):
        fname = Path(__file__).parent / "checks.py"
        method = "_check_autocomplete_fields_item"
        method_children = 176

        class_name = "BaseModelAdminChecks"
        class_children = 2479

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
