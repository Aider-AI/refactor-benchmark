# Refactor DatabaseIntrospection._get_column_collations

Refactor the `_get_column_collations` method in the `DatabaseIntrospection` class to be a stand alone, top level function.
Name the new function `_get_column_collations`, exactly the same name as the existing method.
Update any existing `self._get_column_collations` calls to work with the new `_get_column_collations` function.
