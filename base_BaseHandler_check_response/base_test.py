
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_check_response(self):
        fname = Path(__file__).parent / "base.py"
        method = "check_response"
        method_children = 108

        class_name = "BaseHandler"
        class_children = 1369

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
