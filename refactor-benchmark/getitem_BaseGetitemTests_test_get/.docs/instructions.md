# Refactor BaseGetitemTests.test_get

Refactor the `test_get` method in the `BaseGetitemTests` class to be a stand alone, top level function.
Name the new function `test_get`, exactly the same name as the existing method.
Update any existing `self.test_get` calls to work with the new `test_get` function.
