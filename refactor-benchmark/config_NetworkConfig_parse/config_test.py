
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_parse(self):
        fname = Path(__file__).parent / "config.py"
        method = "parse"
        method_children = 299

        class_name = "NetworkConfig"
        class_children = 1480

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
