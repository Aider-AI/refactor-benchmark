
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__unscale_grads_(self):
        fname = Path(__file__).parent / "grad_scaler.py"
        method = "_unscale_grads_"
        method_children = 275

        class_name = "GradScaler"
        class_children = 2468

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
