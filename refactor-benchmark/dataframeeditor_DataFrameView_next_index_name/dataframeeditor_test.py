
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_next_index_name(self):
        fname = Path(__file__).parent / "dataframeeditor.py"
        method = "next_index_name"
        method_children = 626

        class_name = "DataFrameView"
        class_children = 4394

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
