# Refactor MigrationAutodetector.check_dependency

Refactor the `check_dependency` method in the `MigrationAutodetector` class to be a stand alone, top level function.
Name the new function `check_dependency`, exactly the same name as the existing method.
Update any existing `self.check_dependency` calls to work with the new `check_dependency` function.
