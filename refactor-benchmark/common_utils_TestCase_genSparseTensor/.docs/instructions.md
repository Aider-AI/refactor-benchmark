# Refactor TestCase.genSparseTensor

Refactor the `genSparseTensor` method in the `TestCase` class to be a stand alone, top level function.
Name the new function `genSparseTensor`, exactly the same name as the existing method.
Update any existing `self.genSparseTensor` calls to work with the new `genSparseTensor` function.
