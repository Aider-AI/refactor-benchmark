# Refactor MigrationAutodetector._trim_to_apps

Refactor the `_trim_to_apps` method in the `MigrationAutodetector` class to be a stand alone, top level function.
Name the new function `_trim_to_apps`, exactly the same name as the existing method.
Update any existing `self._trim_to_apps` calls to work with the new `_trim_to_apps` function.
