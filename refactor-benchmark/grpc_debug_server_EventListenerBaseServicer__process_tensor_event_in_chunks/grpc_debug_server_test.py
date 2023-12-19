
import unittest
from benchmark.refactor_tools import verify_refactor
from pathlib import Path

class TheTest(unittest.TestCase):
    def test__process_tensor_event_in_chunks(self):
        fname = Path(__file__).parent / "grpc_debug_server.py"
        method = "_process_tensor_event_in_chunks"
        method_children = 279

        class_name = "EventListenerBaseServicer"
        class_children = 1416

        verify_refactor(fname, method, method_children, class_name, class_children)

if __name__ == "__main__":
    unittest.main()
