# Refactor BaseReshapingTests.test_unstack

Refactor the `test_unstack` method in the `BaseReshapingTests` class to be a stand alone, top level function.
Name the new function `test_unstack`, exactly the same name as the existing method.
Update any existing `self.test_unstack` calls to work with the new `test_unstack` function.
