
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_add_arguments(self):
        fname = Path(__file__).parent / "ogrinspect.py"
        method = "add_arguments"
        method_children = 144

        class_name = "Command"
        class_children = 413

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
