
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_replace_split(self):
        fname = Path(__file__).parent / "split_cat.py"
        method = "replace_split"
        method_children = 327

        class_name = "SplitCatSimplifier"
        class_children = 2326

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
