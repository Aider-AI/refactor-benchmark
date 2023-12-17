
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test_iterative_dfs(self):
        fname = Path(__file__).parent / "graph.py"
        method = "iterative_dfs"
        method_children = 114

        class_name = "MigrationGraph"
        class_children = 1324

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
