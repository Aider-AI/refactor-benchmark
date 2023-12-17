# Refactor JavaScriptCatalog.get_paths

Refactor the `get_paths` method in the `JavaScriptCatalog` class to be a stand alone, top level function.
Name the new function `get_paths`, exactly the same name as the existing method.
Update any existing `self.get_paths` calls to work with the new `get_paths` function.
