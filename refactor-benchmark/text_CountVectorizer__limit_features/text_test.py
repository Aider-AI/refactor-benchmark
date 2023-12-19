
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__limit_features(self):
        fname = Path(__file__).parent / "text.py"
        method = "_limit_features"
        method_children = 300

        class_name = "CountVectorizer"
        class_children = 1601

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
