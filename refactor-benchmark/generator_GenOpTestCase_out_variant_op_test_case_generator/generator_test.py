
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_out_variant_op_test_case_generator(self):
        fname = Path(__file__).parent / "generator.py"
        method = "out_variant_op_test_case_generator"
        method_children = 269

        class_name = "GenOpTestCase"
        class_children = 645

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
