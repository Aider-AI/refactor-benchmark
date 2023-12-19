
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__can_fuse_epilogue_impl(self):
        fname = Path(__file__).parent / "cuda_cpp_scheduling.py"
        method = "_can_fuse_epilogue_impl"
        method_children = 296

        class_name = "CUDACPPScheduling"
        class_children = 992

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
