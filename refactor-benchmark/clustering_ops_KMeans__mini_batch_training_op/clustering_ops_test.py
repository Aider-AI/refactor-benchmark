
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__mini_batch_training_op(self):
        fname = Path(__file__).parent / "clustering_ops.py"
        method = "_mini_batch_training_op"
        method_children = 334

        class_name = "KMeans"
        class_children = 1886

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
