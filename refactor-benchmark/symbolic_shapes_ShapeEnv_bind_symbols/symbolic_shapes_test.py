
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_bind_symbols(self):
        fname = Path(__file__).parent / "symbolic_shapes.py"
        method = "bind_symbols"
        method_children = 277

        class_name = "ShapeEnv"
        class_children = 11290

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
