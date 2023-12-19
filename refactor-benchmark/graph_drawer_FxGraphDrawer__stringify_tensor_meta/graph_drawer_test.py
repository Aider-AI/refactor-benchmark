
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__stringify_tensor_meta(self):
        fname = Path(__file__).parent / "graph_drawer.py"
        method = "_stringify_tensor_meta"
        method_children = 354

        class_name = "FxGraphDrawer"
        class_children = 2078

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
