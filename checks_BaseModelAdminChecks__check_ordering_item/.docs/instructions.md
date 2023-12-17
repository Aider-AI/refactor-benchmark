# Refactor BaseModelAdminChecks._check_ordering_item

Refactor the `_check_ordering_item` method in the `BaseModelAdminChecks` class to be a stand alone, top level function.
Name the new function `_check_ordering_item`, exactly the same name as the existing method.
Update any existing `self._check_ordering_item` calls to work with the new `_check_ordering_item` function.
