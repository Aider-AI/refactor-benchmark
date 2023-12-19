
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_define_kernel(self):
        fname = Path(__file__).parent / "triton.py"
        method = "define_kernel"
        method_children = 267

        class_name = "TritonScheduling"
        class_children = 4346

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
