# Refactor BaseMethodsTests.test_where_series

Refactor the `test_where_series` method in the `BaseMethodsTests` class to be a stand alone, top level function.
Name the new function `test_where_series`, exactly the same name as the existing method.
Update any existing `self.test_where_series` calls to work with the new `test_where_series` function.
