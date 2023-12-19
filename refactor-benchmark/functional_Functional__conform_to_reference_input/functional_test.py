
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__conform_to_reference_input(self):
        fname = Path(__file__).parent / "functional.py"
        method = "_conform_to_reference_input"
        method_children = 267

        class_name = "Functional"
        class_children = 3817

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
