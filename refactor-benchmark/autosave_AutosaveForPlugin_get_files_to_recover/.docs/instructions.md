# Refactor AutosaveForPlugin.get_files_to_recover

Refactor the `get_files_to_recover` method in the `AutosaveForPlugin` class to be a stand alone, top level function.
Name the new function `get_files_to_recover`, exactly the same name as the existing method.
Update any existing `self.get_files_to_recover` calls to work with the new `get_files_to_recover` function.
