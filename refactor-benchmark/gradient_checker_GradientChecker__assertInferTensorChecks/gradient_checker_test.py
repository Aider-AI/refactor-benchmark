
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__assertInferTensorChecks(self):
        fname = Path(__file__).parent / "gradient_checker.py"
        method = "_assertInferTensorChecks"
        method_children = 297

        class_name = "GradientChecker"
        class_children = 1237

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
