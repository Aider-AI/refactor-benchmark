
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_check(self):
        fname = Path(__file__).parent / "finders.py"
        method = "check"
        method_children = 166

        class_name = "FileSystemFinder"
        class_children = 509

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
