
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__parse_transit_response(self):
        fname = Path(__file__).parent / "coordinator.py"
        method = "_parse_transit_response"
        method_children = 288

        class_name = "HERETransitDataUpdateCoordinator"
        class_children = 599

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
