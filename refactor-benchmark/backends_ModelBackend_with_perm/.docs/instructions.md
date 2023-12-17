# Refactor ModelBackend.with_perm

Refactor the `with_perm` method in the `ModelBackend` class to be a stand alone, top level function.
Name the new function `with_perm`, exactly the same name as the existing method.
Update any existing `self.with_perm` calls to work with the new `with_perm` function.
