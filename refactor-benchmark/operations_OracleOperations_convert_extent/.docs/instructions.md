# Refactor OracleOperations.convert_extent

Refactor the `convert_extent` method in the `OracleOperations` class to be a stand alone, top level function.
Name the new function `convert_extent`, exactly the same name as the existing method.
Update any existing `self.convert_extent` calls to work with the new `convert_extent` function.
