
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__sample_rightmost_arg(self):
        fname = Path(__file__).parent / "common_methods_invocations.py"
        method = "_sample_rightmost_arg"
        method_children = 297

        class_name = "foreach_inputs_sample_func"
        class_children = 1626

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
