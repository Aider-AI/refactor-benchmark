
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__get_settings_vars(self):
        fname = Path(__file__).parent / "config.py"
        method = "_get_settings_vars"
        method_children = 386

        class_name = "ConfigCLI"
        class_children = 3084

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
