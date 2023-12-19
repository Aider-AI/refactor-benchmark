
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_execute_list_collection(self):
        fname = Path(__file__).parent / "galaxy.py"
        method = "execute_list_collection"
        method_children = 454

        class_name = "GalaxyCLI"
        class_children = 9670

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
