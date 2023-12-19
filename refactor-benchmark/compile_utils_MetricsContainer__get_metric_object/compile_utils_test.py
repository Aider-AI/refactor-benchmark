
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__get_metric_object(self):
        fname = Path(__file__).parent / "compile_utils.py"
        method = "_get_metric_object"
        method_children = 280

        class_name = "MetricsContainer"
        class_children = 1423

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
