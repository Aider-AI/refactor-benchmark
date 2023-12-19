
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_colorbar(self):
        fname = Path(__file__).parent / "figure.py"
        method = "colorbar"
        method_children = 261

        class_name = "FigureBase"
        class_children = 5312

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
