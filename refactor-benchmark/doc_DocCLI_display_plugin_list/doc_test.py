
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_display_plugin_list(self):
        fname = Path(__file__).parent / "doc.py"
        method = "display_plugin_list"
        method_children = 389

        class_name = "DocCLI"
        class_children = 7038

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
