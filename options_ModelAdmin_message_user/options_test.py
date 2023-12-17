
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_message_user(self):
        fname = Path(__file__).parent / "options.py"
        method = "message_user"
        method_children = 106

        class_name = "ModelAdmin"
        class_children = 7705

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
