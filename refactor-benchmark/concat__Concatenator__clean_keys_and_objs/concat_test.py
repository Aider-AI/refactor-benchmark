
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__clean_keys_and_objs(self):
        fname = Path(__file__).parent / "concat.py"
        method = "_clean_keys_and_objs"
        method_children = 305

        class_name = "_Concatenator"
        class_children = 2038

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
