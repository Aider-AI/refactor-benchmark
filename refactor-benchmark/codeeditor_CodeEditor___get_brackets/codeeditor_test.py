
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test___get_brackets(self):
        fname = Path(__file__).parent / "codeeditor.py"
        method = "__get_brackets"
        method_children = 271

        class_name = "CodeEditor"
        class_children = 22095

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
