
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_call_setattr(self):
        fname = Path(__file__).parent / "builtin.py"
        method = "call_setattr"
        method_children = 534

        class_name = "BuiltinVariable"
        class_children = 8457

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
