
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__get_aten_name(self):
        fname = Path(__file__).parent / "onnxfunction_dispatcher.py"
        method = "_get_aten_name"
        method_children = 355

        class_name = "OnnxFunctionDispatcher"
        class_children = 1323

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
