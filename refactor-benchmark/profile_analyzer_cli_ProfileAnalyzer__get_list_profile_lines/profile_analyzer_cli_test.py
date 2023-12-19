
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__get_list_profile_lines(self):
        fname = Path(__file__).parent / "profile_analyzer_cli.py"
        method = "_get_list_profile_lines"
        method_children = 539

        class_name = "ProfileAnalyzer"
        class_children = 2723

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
