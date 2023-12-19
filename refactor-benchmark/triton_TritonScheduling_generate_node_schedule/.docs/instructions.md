# Refactor TritonScheduling.generate_node_schedule

Refactor the `generate_node_schedule` method in the `TritonScheduling` class to be a stand alone, top level function.
Name the new function `generate_node_schedule`, exactly the same name as the existing method.
Update any existing `self.generate_node_schedule` calls to work with the new `generate_node_schedule` function.
