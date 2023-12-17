# Refactor DatabaseIntrospection._parse_column_or_constraint_definition

Refactor the `_parse_column_or_constraint_definition` method in the `DatabaseIntrospection` class to be a stand alone, top level function.
Name the new function `_parse_column_or_constraint_definition`, exactly the same name as the existing method.
Update any existing `self._parse_column_or_constraint_definition` calls to work with the new `_parse_column_or_constraint_definition` function.
