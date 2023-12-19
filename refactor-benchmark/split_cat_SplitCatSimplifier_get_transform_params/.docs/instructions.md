# Refactor SplitCatSimplifier.get_transform_params

Refactor the `get_transform_params` method in the `SplitCatSimplifier` class to be a stand alone, top level function.
Name the new function `get_transform_params`, exactly the same name as the existing method.
Update any existing `self.get_transform_params` calls to work with the new `get_transform_params` function.
