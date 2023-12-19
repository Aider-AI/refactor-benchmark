# Refactor Dim2CompatTests.test_reductions_2d_axis0

Refactor the `test_reductions_2d_axis0` method in the `Dim2CompatTests` class to be a stand alone, top level function.
Name the new function `test_reductions_2d_axis0`, exactly the same name as the existing method.
Update any existing `self.test_reductions_2d_axis0` calls to work with the new `test_reductions_2d_axis0` function.
