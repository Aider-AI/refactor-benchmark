# Refactor BaseReshapingTests.test_concat_mixed_dtypes

Refactor the `test_concat_mixed_dtypes` method in the `BaseReshapingTests` class to be a stand alone, top level function.
Name the new function `test_concat_mixed_dtypes`, exactly the same name as the existing method.
Update any existing `self.test_concat_mixed_dtypes` calls to work with the new `test_concat_mixed_dtypes` function.
