
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_get_files_to_recover(self):
        fname = Path(__file__).parent / "autosave.py"
        method = "get_files_to_recover"
        method_children = 289

        class_name = "AutosaveForPlugin"
        class_children = 659

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
