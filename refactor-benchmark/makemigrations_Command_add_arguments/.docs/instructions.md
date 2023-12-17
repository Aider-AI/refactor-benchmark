# Refactor Command.add_arguments

Refactor the `add_arguments` method in the `Command` class to be a stand alone, top level function.
Name the new function `add_arguments`, exactly the same name as the existing method.
Update any existing `self.add_arguments` calls to work with the new `add_arguments` function.
