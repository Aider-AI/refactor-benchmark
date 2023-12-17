
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_output_hash(self):
        fname = Path(__file__).parent / "diffsettings.py"
        method = "output_hash"
        method_children = 107

        class_name = "Command"
        class_children = 399

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
