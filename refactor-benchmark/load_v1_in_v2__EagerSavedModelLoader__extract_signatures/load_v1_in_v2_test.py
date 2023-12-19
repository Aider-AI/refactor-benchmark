
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__extract_signatures(self):
        fname = Path(__file__).parent / "load_v1_in_v2.py"
        method = "_extract_signatures"
        method_children = 424

        class_name = "_EagerSavedModelLoader"
        class_children = 1203

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
