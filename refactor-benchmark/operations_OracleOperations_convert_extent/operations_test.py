
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_convert_extent(self):
        fname = Path(__file__).parent / "operations.py"
        method = "convert_extent"
        method_children = 133

        class_name = "OracleOperations"
        class_children = 635

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
