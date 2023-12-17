
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_add_item_elements(self):
        fname = Path(__file__).parent / "feedgenerator.py"
        method = "add_item_elements"
        method_children = 301

        class_name = "Atom1Feed"
        class_children = 706

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
