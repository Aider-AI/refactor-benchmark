
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_get_paths(self):
        fname = Path(__file__).parent / "i18n.py"
        method = "get_paths"
        method_children = 105

        class_name = "JavaScriptCatalog"
        class_children = 662

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
