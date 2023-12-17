# Refactor ModelAdminChecks._check_action_permission_methods

Refactor the `_check_action_permission_methods` method in the `ModelAdminChecks` class to be a stand alone, top level function.
Name the new function `_check_action_permission_methods`, exactly the same name as the existing method.
Update any existing `self._check_action_permission_methods` calls to work with the new `_check_action_permission_methods` function.
