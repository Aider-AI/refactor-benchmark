# Refactor ModelAdminChecks._check_list_editable_item

Refactor the `_check_list_editable_item` method in the `ModelAdminChecks` class to be a stand alone, top level function.
Name the new function `_check_list_editable_item`, exactly the same name as the existing method.
Update any existing `self._check_list_editable_item` calls to work with the new `_check_list_editable_item` function.
