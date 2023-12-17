
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__set_csrf_cookie(self):
        fname = Path(__file__).parent / "csrf.py"
        method = "_set_csrf_cookie"
        method_children = 101

        class_name = "CsrfViewMiddleware"
        class_children = 1120

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
