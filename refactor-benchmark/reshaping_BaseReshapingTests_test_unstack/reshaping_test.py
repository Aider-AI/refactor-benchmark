
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_test_unstack(self):
        fname = Path(__file__).parent / "reshaping.py"
        method = "test_unstack"
        method_children = 376

        class_name = "BaseReshapingTests"
        class_children = 3099

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
