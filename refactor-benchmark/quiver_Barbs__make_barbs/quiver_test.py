
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__make_barbs(self):
        fname = Path(__file__).parent / "quiver.py"
        method = "_make_barbs"
        method_children = 530

        class_name = "Barbs"
        class_children = 1408

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
