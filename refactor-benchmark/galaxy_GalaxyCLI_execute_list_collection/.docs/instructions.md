# Refactor GalaxyCLI.execute_list_collection

Refactor the `execute_list_collection` method in the `GalaxyCLI` class to be a stand alone, top level function.
Name the new function `execute_list_collection`, exactly the same name as the existing method.
Update any existing `self.execute_list_collection` calls to work with the new `execute_list_collection` function.
