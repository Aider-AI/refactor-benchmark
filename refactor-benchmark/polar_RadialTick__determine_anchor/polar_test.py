
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__determine_anchor(self):
        fname = Path(__file__).parent / "polar.py"
        method = "_determine_anchor"
        method_children = 252

        class_name = "RadialTick"
        class_children = 945

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
