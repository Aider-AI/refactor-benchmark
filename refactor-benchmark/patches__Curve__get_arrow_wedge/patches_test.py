
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__get_arrow_wedge(self):
        fname = Path(__file__).parent / "patches.py"
        method = "_get_arrow_wedge"
        method_children = 287

        class_name = "_Curve"
        class_children = 1467

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
