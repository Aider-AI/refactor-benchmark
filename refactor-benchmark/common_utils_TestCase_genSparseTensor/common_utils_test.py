
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_genSparseTensor(self):
        fname = Path(__file__).parent / "common_utils.py"
        method = "genSparseTensor"
        method_children = 261

        class_name = "TestCase"
        class_children = 8203

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
