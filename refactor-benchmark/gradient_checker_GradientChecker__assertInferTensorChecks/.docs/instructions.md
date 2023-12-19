# Refactor GradientChecker._assertInferTensorChecks

Refactor the `_assertInferTensorChecks` method in the `GradientChecker` class to be a stand alone, top level function.
Name the new function `_assertInferTensorChecks`, exactly the same name as the existing method.
Update any existing `self._assertInferTensorChecks` calls to work with the new `_assertInferTensorChecks` function.
