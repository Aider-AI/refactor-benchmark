
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__is_role(self):
        fname = Path(__file__).parent / "dataloader.py"
        method = "_is_role"
        method_children = 261

        class_name = "DataLoader"
        class_children = 2512

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
