# Refactor Command.get_meta

Refactor the `get_meta` method in the `Command` class to be a stand alone, top level function.
Name the new function `get_meta`, exactly the same name as the existing method.
Update any existing `self.get_meta` calls to work with the new `get_meta` function.
