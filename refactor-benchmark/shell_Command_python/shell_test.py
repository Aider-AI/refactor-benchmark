
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_python(self):
        fname = Path(__file__).parent / "shell.py"
        method = "python"
        method_children = 166

        class_name = "Command"
        class_children = 378

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
