# Refactor DatabaseOperations.last_executed_query

Refactor the `last_executed_query` method in the `DatabaseOperations` class to be a stand alone, top level function.
Name the new function `last_executed_query`, exactly the same name as the existing method.
Update any existing `self.last_executed_query` calls to work with the new `last_executed_query` function.
