# Refactor Command.get_field_type

Refactor the `get_field_type` method in the `Command` class to be a stand alone, top level function.
Name the new function `get_field_type`, exactly the same name as the existing method.
Update any existing `self.get_field_type` calls to work with the new `get_field_type` function.
