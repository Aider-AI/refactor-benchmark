
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_get_role_man_text(self):
        fname = Path(__file__).parent / "doc.py"
        method = "get_role_man_text"
        method_children = 428

        class_name = "DocCLI"
        class_children = 7038

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
