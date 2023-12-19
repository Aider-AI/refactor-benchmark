# Refactor ConfigCLI._get_settings_vars

Refactor the `_get_settings_vars` method in the `ConfigCLI` class to be a stand alone, top level function.
Name the new function `_get_settings_vars`, exactly the same name as the existing method.
Update any existing `self._get_settings_vars` calls to work with the new `_get_settings_vars` function.
