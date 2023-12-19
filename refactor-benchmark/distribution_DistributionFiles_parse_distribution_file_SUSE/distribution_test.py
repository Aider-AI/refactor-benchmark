
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_parse_distribution_file_SUSE(self):
        fname = Path(__file__).parent / "distribution.py"
        method = "parse_distribution_file_SUSE"
        method_children = 440

        class_name = "DistributionFiles"
        class_children = 2766

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
