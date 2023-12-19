
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__make_source_table(self):
        fname = Path(__file__).parent / "analyzer_cli.py"
        method = "_make_source_table"
        method_children = 466

        class_name = "DebugAnalyzer"
        class_children = 6016

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
