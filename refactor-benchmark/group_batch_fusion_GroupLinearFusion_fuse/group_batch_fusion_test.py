
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_fuse(self):
        fname = Path(__file__).parent / "group_batch_fusion.py"
        method = "fuse"
        method_children = 279

        class_name = "GroupLinearFusion"
        class_children = 635

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
