# Refactor DataLoader._is_role

Refactor the `_is_role` method in the `DataLoader` class to be a stand alone, top level function.
Name the new function `_is_role`, exactly the same name as the existing method.
Update any existing `self._is_role` calls to work with the new `_is_role` function.
