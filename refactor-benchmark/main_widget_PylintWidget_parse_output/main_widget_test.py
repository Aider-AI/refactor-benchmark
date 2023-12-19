
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_parse_output(self):
        fname = Path(__file__).parent / "main_widget.py"
        method = "parse_output"
        method_children = 376

        class_name = "PylintWidget"
        class_children = 3564

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
