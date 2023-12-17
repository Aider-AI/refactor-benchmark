
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__check_action_permission_methods(self):
        fname = Path(__file__).parent / "checks.py"
        method = "_check_action_permission_methods"
        method_children = 103

        class_name = "ModelAdminChecks"
        class_children = 1746

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
