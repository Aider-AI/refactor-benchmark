# Refactor AppConfig._path_from_module

Refactor the `_path_from_module` method in the `AppConfig` class to be a stand alone, top level function.
Name the new function `_path_from_module`, exactly the same name as the existing method.
Update any existing `self._path_from_module` calls to work with the new `_path_from_module` function.
