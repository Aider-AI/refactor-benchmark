# Refactor GroupLinearFusion.fuse

Refactor the `fuse` method in the `GroupLinearFusion` class to be a stand alone, top level function.
Name the new function `fuse`, exactly the same name as the existing method.
Update any existing `self.fuse` calls to work with the new `fuse` function.
