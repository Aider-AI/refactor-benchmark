
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_get_fault_text(self):
        fname = Path(__file__).parent / "kernel.py"
        method = "get_fault_text"
        method_children = 265

        class_name = "SpyderKernel"
        class_children = 3684

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
