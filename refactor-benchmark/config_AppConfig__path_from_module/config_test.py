
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__path_from_module(self):
        fname = Path(__file__).parent / "config.py"
        method = "_path_from_module"
        method_children = 112

        class_name = "AppConfig"
        class_children = 934

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
