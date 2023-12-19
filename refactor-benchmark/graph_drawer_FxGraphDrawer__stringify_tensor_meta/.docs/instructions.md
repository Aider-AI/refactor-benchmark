# Refactor FxGraphDrawer._stringify_tensor_meta

Refactor the `_stringify_tensor_meta` method in the `FxGraphDrawer` class to be a stand alone, top level function.
Name the new function `_stringify_tensor_meta`, exactly the same name as the existing method.
Update any existing `self._stringify_tensor_meta` calls to work with the new `_stringify_tensor_meta` function.
