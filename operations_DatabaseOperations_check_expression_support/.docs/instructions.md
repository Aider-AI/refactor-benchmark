# Refactor DatabaseOperations.check_expression_support

Refactor the `check_expression_support` method in the `DatabaseOperations` class to be a stand alone, top level function.
Name the new function `check_expression_support`, exactly the same name as the existing method.
Update any existing `self.check_expression_support` calls to work with the new `check_expression_support` function.
