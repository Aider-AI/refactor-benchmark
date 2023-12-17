
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_with_perm(self):
        fname = Path(__file__).parent / "backends.py"
        method = "with_perm"
        method_children = 178

        class_name = "ModelBackend"
        class_children = 665

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
