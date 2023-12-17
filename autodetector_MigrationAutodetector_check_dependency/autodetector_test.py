
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_check_dependency(self):
        fname = Path(__file__).parent / "autodetector.py"
        method = "check_dependency"
        method_children = 452

        class_name = "MigrationAutodetector"
        class_children = 8548

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
