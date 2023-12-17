# Refactor FileSystemFinder.check

Refactor the `check` method in the `FileSystemFinder` class to be a stand alone, top level function.
Name the new function `check`, exactly the same name as the existing method.
Update any existing `self.check` calls to work with the new `check` function.
