
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_parse_inet_line(self):
        fname = Path(__file__).parent / "generic_bsd.py"
        method = "parse_inet_line"
        method_children = 390

        class_name = "GenericBsdIfconfigNetwork"
        class_children = 1918

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
