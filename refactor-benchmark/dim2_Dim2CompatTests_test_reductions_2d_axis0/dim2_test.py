
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_test_reductions_2d_axis0(self):
        fname = Path(__file__).parent / "dim2.py"
        method = "test_reductions_2d_axis0"
        method_children = 380

        class_name = "Dim2CompatTests"
        class_children = 1919

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
