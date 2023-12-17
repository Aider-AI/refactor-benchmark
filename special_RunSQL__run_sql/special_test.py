
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__run_sql(self):
        fname = Path(__file__).parent / "special.py"
        method = "_run_sql"
        method_children = 119

        class_name = "RunSQL"
        class_children = 384

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
