
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__add_partition(self):
        fname = Path(__file__).parent / "sharding_policies.py"
        method = "_add_partition"
        method_children = 382

        class_name = "MaxShardSizePolicy"
        class_children = 1235

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
