
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_get_and_delete_all_sms(self):
        fname = Path(__file__).parent / "gateway.py"
        method = "get_and_delete_all_sms"
        method_children = 294

        class_name = "Gateway"
        class_children = 938

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
