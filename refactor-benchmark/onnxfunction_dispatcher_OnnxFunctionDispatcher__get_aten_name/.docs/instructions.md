# Refactor OnnxFunctionDispatcher._get_aten_name

Refactor the `_get_aten_name` method in the `OnnxFunctionDispatcher` class to be a stand alone, top level function.
Name the new function `_get_aten_name`, exactly the same name as the existing method.
Update any existing `self._get_aten_name` calls to work with the new `_get_aten_name` function.
