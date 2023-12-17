# Refactor Command.output_hash

Refactor the `output_hash` method in the `Command` class to be a stand alone, top level function.
Name the new function `output_hash`, exactly the same name as the existing method.
Update any existing `self.output_hash` calls to work with the new `output_hash` function.
