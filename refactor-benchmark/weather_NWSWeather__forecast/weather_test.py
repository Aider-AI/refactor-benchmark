
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__forecast(self):
        fname = Path(__file__).parent / "weather.py"
        method = "_forecast"
        method_children = 327

        class_name = "NWSWeather"
        class_children = 1235

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
